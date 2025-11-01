"""
Task 1 - Medical Case Report Summarizer (Part A)

Purpose
- Single-run script to summarize public medical case reports using five prompt variants.
- Loads API key from .env (project root or CWD), calls OpenAI, and emits:
  - Markdown report with clearly separated sections per case and comparison templates
  - Raw JSON files per case × variant (prompt + output)

Usage
  python Assignment/A1/task1_medical_summarizer.py \
    --input_dir Assignment/A1/task1_cases \
    --model ${OPENAI_MODEL:-gpt-4o-mini} \
    --temperature 0.3 \
    --max_tokens 800 \
    --output_dir Assignment/A1/outputs/task1 \
    --execute
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    from dotenv import load_dotenv
except Exception:  # pragma: no cover
    load_dotenv = None  # type: ignore[assignment]

try:
    from openai import OpenAI  # type: ignore
    _HAS_OPENAI = True
except Exception:  # pragma: no cover
    _HAS_OPENAI = False


@dataclass
class RunConfig:
    model: str
    temperature: float
    max_tokens: int
    execute: bool
    input_dir: Path
    output_dir: Path


def load_env() -> None:
    if load_dotenv is None:
        return
    # Load from CWD (override) and project root (override) to be robust
    try:
        cwd_env = Path.cwd() / ".env"
        if cwd_env.exists():
            load_dotenv(dotenv_path=str(cwd_env), override=True)
        else:
            load_dotenv(override=True)
    except Exception:
        pass
    try:
        script_path = Path(__file__).resolve()
        project_root = script_path.parents[2]
        root_env = project_root / ".env"
        if root_env.exists():
            load_dotenv(dotenv_path=str(root_env), override=True)
    except Exception:
        pass


def coalesce_model() -> str:
    return os.getenv("OPENAI_MODEL") or "gpt-4o-mini"


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def list_case_files(input_dir: Path) -> List[Path]:
    files: List[Path] = []
    if input_dir.exists():
        for ext in ("*.txt", "*.md"):
            files.extend(sorted(input_dir.glob(ext)))
    return files


def read_file_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except Exception:
        return p.read_text(errors="ignore")


def build_prompt_variants() -> List[Dict[str, str]]:
    # Five variants: structured summary, JSON, SOAP, timeline, uncertainty/questions
    variants: List[Dict[str, str]] = [
        {
            "id": "v1_structured",
            "name": "V1 - Structured summary (short)",
            "rationale": "Concise sections to reduce rambling and improve coverage of key clinical elements.",
            "prompt_template": (
                "You are a clinician. Summarize the following public medical case report.\n"
                "Output with the headings: Patient, Presentation, Key findings, Diagnosis, Management, Outcome, Follow-up.\n"
                "150-200 words. Use only information present; do not speculate.\n\n"
                "--- Case Report ---\n{case_text}\n--- End ---"
            ),
        },
        {
            "id": "v2_json",
            "name": "V2 - JSON summary",
            "rationale": "Structured fields to enable later scoring (coverage, red flags, follow-up).",
            "prompt_template": (
                "Summarize the medical case strictly as JSON with keys: \n"
                "{{patient_summary, diagnoses[], key_findings[], red_flags[], follow_up[]}}\n"
                "If unknown, use \"unknown\". Use only provided information.\n\n"
                "--- Case Report ---\n{case_text}\n--- End ---"
            ),
        },
        {
            "id": "v3_soap",
            "name": "V3 - SOAP format",
            "rationale": "Common clinical structure enhances reasoning clarity and checkability.",
            "prompt_template": (
                "Summarize the case in SOAP format: S, O, A, P.\n"
                "Use only information present; keep each section 1-3 short paragraphs.\n\n"
                "--- Case Report ---\n{case_text}\n--- End ---"
            ),
        },
        {
            "id": "v4_timeline",
            "name": "V4 - Timeline and progression",
            "rationale": "Chronological organization improves readability and prevents missed temporal relations.",
            "prompt_template": (
                "Extract a chronological timeline of key events (tests→findings→interventions→results).\n"
                "End with a concise 2-3 sentence overall summary. No speculation.\n\n"
                "--- Case Report ---\n{case_text}\n--- End ---"
            ),
        },
        {
            "id": "v5_uncertainty",
            "name": "V5 - Summary + uncertainties/questions",
            "rationale": "Explicitly surfaces missing information and next-step questions to reduce hallucination risk.",
            "prompt_template": (
                "Write a compact summary (120-180 words). Then list: (1) Unknowns or ambiguities; (2) Three follow-up questions a clinician should ask.\n"
                "Base only on the given case.\n\n"
                "--- Case Report ---\n{case_text}\n--- End ---"
            ),
        },
    ]
    return variants


def call_openai_response(model: str, prompt: str, temperature: float, max_tokens: int) -> str:
    if not _HAS_OPENAI:
        raise RuntimeError("OpenAI client not installed. `pip install --upgrade openai python-dotenv`.")
    # Add reasonable timeout/retries to avoid indefinite hangs
    client = OpenAI(timeout=60.0, max_retries=2)
    # Try Responses API first, then Chat Completions (v1)
    first_error: Optional[Exception] = None
    try:
        result = client.responses.create(
            model=model,
            input=prompt,
            temperature=temperature,
            max_output_tokens=max_tokens,
        )
        try:
            return result.output_text  # type: ignore[attr-defined]
        except Exception:
            try:
                return "".join([c.text for c in result.output[0].content])  # type: ignore
            except Exception:
                return json.dumps(result.model_dump(), ensure_ascii=False)
    except Exception as e:
        first_error = e
    try:
        result = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return result.choices[0].message.content or ""
    except Exception as e2:
        raise RuntimeError(f"OpenAI API error. Responses: {first_error}; ChatCompletions: {e2}")


def render_report(
    report_path: Path,
    run_config: RunConfig,
    cases: List[Tuple[Path, str]],
    variants: List[Dict[str, str]],
    outputs: Dict[str, Dict[str, str]],
) -> None:
    ensure_dir(report_path.parent)
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%SZ")

    header = f"""
# Part A - Task 1: Medical Case Summarization (Experiment Report)

**Timestamp (UTC)**: {ts}

## 0. Run Config
- Model: {run_config.model}
- Temperature: {run_config.temperature}
- Max Tokens: {run_config.max_tokens}
- Executed: {run_config.execute}
- Input Dir: {str(run_config.input_dir)}
- Output Dir: {str(run_config.output_dir)}
""".strip()

    variant_desc = []
    for v in variants:
        variant_desc.append(f"- {v['name']}: {v['rationale']}")
    variant_desc_str = "\n".join(variant_desc)

    body_sections: List[str] = [
        header,
        "\n\n## 1. Prompt Variants\n" + variant_desc_str,
    ]

    def fence_block(content: str, lang: str = "text") -> str:
        # Avoid nested backtick fences breaking markdown; use tildes if needed
        fence = "~~~" if "```" in content else "```"
        return f"{fence}{lang}\n{content}\n{fence}"

    def _tokenize(_text: str) -> List[str]:
        import re as _re
        return [t for t in _re.findall(r"[A-Za-z0-9']+", _text.lower()) if len(t) > 2]

    def analyze_output(variant_id: str, generated: str, source_text: str) -> Dict[str, Any]:
        # Heuristic: coverage, hallucination, clarity, structure, notes
        try:
            text = (generated or "").strip()
            if not text or text.startswith("[ERROR]"):
                return {"coverage": 0, "hallucination": "High", "clarity": 1, "structure": 1, "notes": "empty/error"}

            src_tokens = set(_tokenize(source_text))
            out_tokens = _tokenize(text)
            unseen = [t for t in out_tokens if t not in src_tokens]
            ratio_unseen = (len(unseen) / max(1, len(out_tokens)))
            halluc = "Low" if ratio_unseen <= 0.35 else ("Med" if ratio_unseen <= 0.55 else "High")

            import re as _re
            sentences = [s for s in _re.split(r"[\.!?\n]+", text) if s.strip()]
            avg_len = (sum(len(_tokenize(s)) for s in sentences) / max(1, len(sentences)))
            clarity = 5 if avg_len <= 18 else 4 if avg_len <= 23 else 3 if avg_len <= 28 else 2 if avg_len <= 35 else 1
            notes: List[str] = []

            if variant_id == "v1_structured":
                sections = ["Patient", "Presentation", "Key", "Diagnosis", "Management", "Outcome", "Follow-up"]
                present = sum(1 for s in sections if s.lower() in text.lower())
                structure = max(1, round(present / len(sections) * 5))
                notes.append(f"sections {present}/{len(sections)}")
                return {"coverage": round(present / len(sections) * 100), "hallucination": halluc, "clarity": clarity, "structure": structure, "notes": "; ".join(notes)}
            if variant_id == "v2_json":
                import json as _json
                start = text.find("{")
                end = text.rfind("}")
                if start != -1 and end != -1 and end > start:
                    obj = _json.loads(text[start:end+1])
                    required = ["patient_summary", "diagnoses", "key_findings", "red_flags", "follow_up"]
                    present = sum(1 for k in required if k in obj)
                    structure = 5 if present == len(required) else max(1, round(present / len(required) * 5))
                    notes.append(f"json keys {present}/{len(required)}")
                    return {"coverage": round(present / len(required) * 100), "hallucination": halluc, "clarity": clarity, "structure": structure, "notes": "; ".join(notes)}
                return {"coverage": 0, "hallucination": halluc, "clarity": clarity, "structure": 1, "notes": "json parse failed"}
            if variant_id == "v3_soap":
                sections = ["S:", "O:", "A:", "P:"]
                present = sum(1 for s in sections if s.lower() in text.lower())
                structure = max(1, round(present / len(sections) * 5))
                notes.append(f"SOAP {present}/{len(sections)}")
                return {"coverage": round(present / len(sections) * 100), "hallucination": halluc, "clarity": clarity, "structure": structure, "notes": "; ".join(notes)}
            if variant_id == "v4_timeline":
                has_numbers = any(line.strip().startswith(tuple(str(i)+".") for i in range(1,5)) for line in text.splitlines())
                has_summary = "summary" in text.lower()
                cov = 50 + (25 if has_numbers else 0) + (25 if has_summary else 0)
                structure = 3 + (1 if has_numbers else 0) + (1 if has_summary else 0)
                notes.append(f"numbers={'Y' if has_numbers else 'N'}, summary={'Y' if has_summary else 'N'}")
                return {"coverage": cov, "hallucination": halluc, "clarity": clarity, "structure": structure, "notes": "; ".join(notes)}
            if variant_id == "v5_uncertainty":
                has_unknown = ("unknown" in text.lower()) or ("ambigu" in text.lower())
                has_follow = "follow-up" in text.lower() or "follow up" in text.lower() or "questions" in text.lower()
                cov = 50 + (25 if has_unknown else 0) + (25 if has_follow else 0)
                structure = 3 + (1 if has_unknown else 0) + (1 if has_follow else 0)
                notes.append(f"unknowns={'Y' if has_unknown else 'N'}, followup={'Y' if has_follow else 'N'}")
                return {"coverage": cov, "hallucination": halluc, "clarity": clarity, "structure": structure, "notes": "; ".join(notes)}
        except Exception:
            return {"coverage": 0, "hallucination": "High", "clarity": 1, "structure": 1, "notes": "analysis error"}

    for case_idx, (case_path, case_text) in enumerate(cases, start=1):
        sections: List[str] = [f"\n\n## 2.{case_idx} Case: {case_path.name}"]
        # Compact table per case
        comp_header = (
            "| Variant | Coverage(%) | Hallucination | Clarity(1-5) | Structure(1-5) | Notes |\n"
            "|---|---:|---|---:|---:|---|\n"
        )
        comp_rows_list: List[str] = []
        for v in variants:
            vid = v["id"]
            gen = outputs.get(case_path.name, {}).get(vid, "")
            metrics = analyze_output(vid, gen, case_text)
            comp_rows_list.append(
                f"| {v['name']} | {metrics.get('coverage', '')} | {metrics.get('hallucination', '')} | {metrics.get('clarity', '')} | {metrics.get('structure', '')} | {metrics.get('notes', '')} |"
            )
        comp_rows = "\n".join(comp_rows_list)
        sections.append(
            "- Source case: Assignment/A1/task1_cases/" + case_path.name +
            "\n\n### 2." + str(case_idx) + ".X Results Table\n" + comp_header + comp_rows
        )

        # Detailed outputs per variant (instructions only + generated output)
        for v_idx, v in enumerate(variants, start=1):
            vid = v["id"]
            generated = outputs.get(case_path.name, {}).get(vid, "(Not executed; add --execute)")
            is_json_output = ("```json" in generated) or generated.strip().startswith("{")
            instr_only = v["prompt_template"].split("--- Case Report ---")[0].strip()
            prompt_render = (
                f"- Source case: Assignment/A1/task1_cases/{case_path.name}\n\n" +
                fence_block(instr_only, 'text')
            )
            output_render = fence_block(generated, 'json') if is_json_output else generated

            detail = f"""
### 2.{case_idx}.{v_idx} {v['name']}
Rationale: {v['rationale']}

Prompt (instruction only)
{prompt_render}

Model Output
{output_render}
""".strip()
            sections.append(detail)

        body_sections.append("\n\n".join(sections))

    best_practice = """

## 3. Best Practices (Template)
- Use explicit sections (or JSON) to reduce omissions.
- State "use only provided information" to curb speculation.
- Request uncertainties/follow-ups to surface gaps and lower hallucinations.
- Keep temperature modest (0.2–0.4) for factual summaries.

## 4. Reproducibility
```bash
python Assignment/A1/task1_medical_summarizer.py \
  --input_dir Assignment/A1/task1_cases \
  --model gpt-4o-mini \
  --temperature 0.3 \
  --max_tokens 800 \
  --output_dir Assignment/A1/outputs/task1 \
  --execute
```
""".strip()

    content = "\n\n".join(body_sections) + "\n\n" + best_practice
    report_path.write_text(content, encoding="utf-8")


def run_variants(
    run_config: RunConfig,
    cases: List[Tuple[Path, str]],
    variants: List[Dict[str, str]],
) -> Dict[str, Dict[str, str]]:
    outputs: Dict[str, Dict[str, str]] = {}
    if not run_config.execute:
        return outputs

    for case_path, case_text in cases:
        per_case: Dict[str, str] = {}
        for v in variants:
            prompt = v["prompt_template"].format(case_text=case_text)
            try:
                print(f"[Task1] Running {case_path.name} / {v['id']} ...", flush=True)
                text = call_openai_response(
                    model=run_config.model,
                    prompt=prompt,
                    temperature=run_config.temperature,
                    max_tokens=run_config.max_tokens,
                )
                print(f"[Task1] Done {case_path.name} / {v['id']}", flush=True)
            except Exception as e:
                text = f"[ERROR] {type(e).__name__}: {e}"
            per_case[v["id"]] = text
        outputs[case_path.name] = per_case
    return outputs


def write_raw_outputs(
    output_dir: Path,
    cases: List[Tuple[Path, str]],
    variants: List[Dict[str, str]],
    outputs: Dict[str, Dict[str, str]],
) -> None:
    if not outputs:
        return
    raw_dir = output_dir / "task1_runs"
    ensure_dir(raw_dir)
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    for case_path, _ in cases:
        per_case = outputs.get(case_path.name, {})
        record = {
            "case": case_path.name,
            "variants": [],
            "timestamp_utc": ts,
        }
        for v in variants:
            vid = v["id"]
            record["variants"].append(
                {
                    "variant_id": vid,
                    "name": v["name"],
                    "rationale": v["rationale"],
                    "prompt_template": v["prompt_template"],
                    "output": per_case.get(vid, ""),
                }
            )
        (raw_dir / f"{ts}_{case_path.stem}.json").write_text(
            json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8"
        )


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Part A Task 1 - Medical Case Report Summarizer")
    p.add_argument("--input_dir", type=str, default="Assignment/A1/task1_cases", help="Directory with .txt/.md case files")
    p.add_argument("--model", type=str, default=coalesce_model(), help="OpenAI model name (default from OPENAI_MODEL or gpt-4o-mini)")
    p.add_argument("--temperature", type=float, default=0.3, help="Sampling temperature")
    p.add_argument("--max_tokens", type=int, default=800, help="Maximum tokens for generation")
    p.add_argument("--output_dir", type=str, default="Assignment/A1/outputs/task1", help="Report/output directory")
    p.add_argument("--execute", action="store_true", help="If set, actually call the API")
    return p.parse_args()


def main() -> None:
    load_env()
    args = parse_args()
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    ensure_dir(output_dir)

    run_config = RunConfig(
        model=args.model,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        execute=bool(args.execute),
        input_dir=input_dir,
        output_dir=output_dir,
    )

    case_files = list_case_files(input_dir)
    if not case_files:
        # Create a README to guide user
        ensure_dir(input_dir)
        (input_dir / "README.md").write_text(
            "Place public case reports as .txt or .md files in this folder. One case per file.",
            encoding="utf-8",
        )
    cases: List[Tuple[Path, str]] = [(p, read_file_text(p)) for p in case_files]

    variants = build_prompt_variants()
    outputs = run_variants(run_config, cases, variants)
    write_raw_outputs(output_dir, cases, variants, outputs)

    report_path = output_dir / "task1_report.md"
    render_report(report_path, run_config, cases, variants, outputs)

    print(f"Report written to: {report_path}")
    if outputs:
        print(f"Raw outputs written to: {output_dir / 'task1_runs'}")


if __name__ == "__main__":
    main()



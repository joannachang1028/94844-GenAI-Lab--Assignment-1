"""
Task 3 - Constraint-based Creative Writing Runner

Purpose
- Single-run script for Part A Task 3 (Creative: "Constraint Composer").
- Loads API key from .env, generates outputs for 5 prompt variants, and writes a
  Markdown report with clearly separated sections (steps and comparison templates).

Usage
  python task3_constraint_creator.py \
    --constraints_json Assignment/A1/constraints.sample.json \
    --model ${OPENAI_MODEL:-gpt-5-mini} \
    --temperature 0.7 \
    --max_tokens 800 \
    --output_dir Assignment/A1/outputs \
    --execute   # add this flag to actually call the API

Notes
- By default (without --execute), the script produces a Markdown report template
  without making API calls. Add --execute to run the 5 variants and record outputs.
- The Markdown report includes: run config, input constraints, prompt variants
  (with rationale, prompt text, outputs), comparison table template, and best
  practices template.
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from dotenv import load_dotenv
except Exception:  # pragma: no cover
    load_dotenv = None  # type: ignore[assignment]

# Prefer the new OpenAI client if available; fall back to legacy import gracefully.
_OPENAI_CLIENT_MODE = "responses"  # or "chat"
try:
    from openai import OpenAI  # type: ignore
    _HAS_OPENAI_NEW = True
except Exception:  # pragma: no cover
    _HAS_OPENAI_NEW = False

_HAS_OPENAI_LEGACY = False  # Deprecated path disabled (v1+ only)


@dataclass
class RunConfig:
    model: str
    temperature: float
    max_tokens: int
    execute: bool
    output_dir: Path


def load_env() -> None:
    if load_dotenv is None:
        return
    # 1) Load from current working directory (override to ensure availability)
    try:
        cwd_env = Path.cwd() / ".env"
        if cwd_env.exists():
            load_dotenv(dotenv_path=str(cwd_env), override=True)
        else:
            load_dotenv(override=True)
    except Exception:
        pass
    # 2) Also load from project root (two levels up from this file), overriding as needed
    try:
        script_path = Path(__file__).resolve()
        # task3_constraint_creator.py -> A1 -> Assignment -> GenAI (parents[2])
        project_root = script_path.parents[2]
        root_env = project_root / ".env"
        if root_env.exists():
            load_dotenv(dotenv_path=str(root_env), override=True)
    except Exception:
        pass


def read_constraints_json(path: Optional[str]) -> Dict[str, Any]:
    if path is None:
        # Default sample constraints to make the script immediately runnable.
        return {
            "language": "en",
            "title": "Autumn River",
            "hard_constraints": {
                "word_count": {"min": 180, "max": 220},
                "must_include_keywords": ["river", "egret"],
                "forbidden_words": ["love", "journey"],
                "point_of_view": "first_person",
                "style_tags": ["natural cadence", "concrete imagery"],
                "tone": "mildly melancholic yet hopeful",
            },
            "soft_constraints": [
                "Introduce a small twist in the final two sentences",
                "Include exactly one rhetorical question in the text",
            ],
        }

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def coalesce_model() -> str:
    return os.getenv("OPENAI_MODEL")


def build_prompt_variants(constraints: Dict[str, Any]) -> List[Dict[str, Any]]:
    language = constraints.get("language", "en")
    hc = constraints.get("hard_constraints", {})
    sc = constraints.get("soft_constraints", [])

    word_min = hc.get("word_count", {}).get("min")
    word_max = hc.get("word_count", {}).get("max")
    pov = hc.get("point_of_view")
    style_tags = hc.get("style_tags", [])
    tone = hc.get("tone")
    must_include = hc.get("must_include_keywords", [])
    forbidden = hc.get("forbidden_words", [])

    constraint_block_lines: List[str] = []
    if word_min is not None or word_max is not None:
        constraint_block_lines.append(
            f"- Word count: between {word_min or 'N/A'} and {word_max or 'N/A'}"
        )
    if must_include:
        constraint_block_lines.append(
            f"- Must include keywords: {', '.join(must_include)}"
        )
    if forbidden:
        constraint_block_lines.append(
            f"- Forbidden words: {', '.join(forbidden)}"
        )
    if pov:
        constraint_block_lines.append(f"- Point of view: {pov}")
    if style_tags:
        constraint_block_lines.append(f"- Style tags: {', '.join(style_tags)}")
    if tone:
        constraint_block_lines.append(f"- Overall tone: {tone}")
    for s in sc:
        constraint_block_lines.append(f"- Preference: {s}")

    constraint_block = "\n".join(constraint_block_lines)

    # Five distinct prompt variants with rationales.
    variants: List[Dict[str, Any]] = [
        {
            "id": "v1_story_only_minimal",
            "name": "V1 - Strict constraints (story only)",
            "rationale": "Minimal instruction with explicit hard constraints; tests direct adherence without extra scaffolding.",
            "prompt": f"""
You are an expert creative writer. Write in {language} and strictly follow these constraints:
{constraint_block}

Output rules:
- Output the story only. Do not add any title, comments, or extra explanations.
""".strip(),
        },
        {
            "id": "v2_story_plus_selfcheck_json",
            "name": "V2 - Story + self-check JSON",
            "rationale": "After the story, return a JSON self-check to quantify constraint satisfaction and violations.",
            "prompt": f"""
You are an expert creative writer. Write in {language} and strictly follow these constraints:
{constraint_block}

Output in two parts:
1) Story text only (no title or preface).
2) Then output a JSON block (a single fenced code block) with the following structure:
{{
  "constraints_satisfied": true|false,
  "violations": ["which rules were not satisfied, if any"],
  "approx_word_count": <number>,
  "keywords_present": {{"{(must_include[0] if must_include else 'example')}": true}},
  "forbidden_detected": ["any forbidden words detected"],
  "notes": "very brief note"
}}
""".strip(),
        },
        {
            "id": "v3_guarded_style_transfer",
            "name": "V3 - Style guidance + guardrails",
            "rationale": "Guide with abstract style tags and avoid imitating identifiable living authors; reinforce compliance.",
            "prompt": f"""
Write in {language} using abstract, general stylistic features (do not imitate any specific living author).
Strict constraints:
{constraint_block}

Output rules:
- Output the story text only.
""".strip(),
        },
        {
            "id": "v4_plan_brief_then_write",
            "name": "V4 - Brief internal planning, then write (implicit)",
            "rationale": "Request brief internal planning to improve constraint adherence, then output only the final story (no reasoning).",
            "prompt": f"""
Do a brief internal plan to ensure all constraints are met, then output only the final story (do not output any plan content).
Constraints:
{constraint_block}
""".strip(),
        },
        {
            "id": "v5_checklist_then_json",
            "name": "V5 - Story + brief checklist",
            "rationale": "Provide a minimal post-output checklist (not chain-of-thought) to balance readability and scoring.",
            "prompt": f"""
Strictly follow the constraints to complete the story, then add a one-line brief checklist (not reasoning):
{constraint_block}

Output rules:
1) Story text.
2) Checklist (a single line of plain text, e.g., WordCount OK; Keywords OK; No Forbidden; POV OK).
""".strip(),
        },
    ]

    return variants


def call_openai_response(model: str, prompt: str, temperature: float, max_tokens: int) -> str:
    """Call OpenAI using the v1+ client only.

    - Try Responses API first.
    - If that fails, fall back to Chat Completions via the v1 client.
    - Deprecated legacy ChatCompletion path is removed to avoid APIRemovedInV1 errors.
    """
    if not _HAS_OPENAI_NEW:
        raise RuntimeError(
            "OpenAI client not installed. Please `pip install --upgrade openai python-dotenv`."
        )

    client = OpenAI()
    first_error: Optional[Exception] = None

    # 1) Try Responses API
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

    # 2) Fallback to Chat Completions (v1 client)
    try:
        result = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return result.choices[0].message.content or ""
    except Exception as e2:
        raise RuntimeError(f"OpenAI API error. Responses API: {first_error}; Chat Completions: {e2}")


def render_markdown_report(
    output_path: Path,
    run_config: RunConfig,
    constraints: Dict[str, Any],
    variants: List[Dict[str, Any]],
    outputs: Dict[str, str],
) -> None:
    ensure_dir(output_path.parent)

    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%SZ")
    constraints_json_str = json.dumps(constraints, ensure_ascii=False, indent=2)

    # Comparison table header
    table_header = (
        "| Variant | Constraints% | Violations | Creativity(1-5) | Coherence(1-5) | "
        "Fluency(1-5) | StyleMatch(1-5) | Notes |\n"
        "|---|---:|---|---:|---:|---:|---:|---|\n"
    )

    # Build per-variant sections
    variant_sections: List[str] = []
    for idx, v in enumerate(variants, start=1):
        vid = v["id"]
        name = v["name"]
        rationale = v["rationale"]
        prompt_text = v["prompt"]
        generated = outputs.get(vid, "(Not executed; add --execute to generate outputs)")

        section = f"""
### 2.{idx} {name}
**Rationale**: {rationale}

**Prompt**
```text
{prompt_text}
```

**Model Output**
```text
{generated}
```
""".strip()
        variant_sections.append(section)

    # Build comparison rows template
    rows: List[str] = []
    for v in variants:
        rows.append(
            f"| {v['name']} |  |  |  |  |  |  |  |"
        )

    # Precompute strings to avoid backslashes in f-string expressions
    variant_sections_str = "\n\n".join(variant_sections)
    rows_str = "\n".join(rows)

    content = f"""
# Part A - Task 3: Constraint-based Creative Writing (Experiment Report)

**Timestamp (UTC)**: {ts}

## 0. Run Config
- **Model**: {run_config.model}
- **Temperature**: {run_config.temperature}
- **Max Tokens**: {run_config.max_tokens}
- **Executed**: {str(run_config.execute)}
- **Output Dir**: {str(run_config.output_dir)}

## 1. Input Constraints (JSON)
```json
{constraints_json_str}
```

## 2. Prompt Variants and Outputs
{variant_sections_str}

## 3. Comparison Analysis (Template)
- Explanation: Evaluate constraint satisfaction and writing quality for each variant; fill the table below.

{table_header}{rows_str}

### 3.1 Automated/Semi-automated Checks (Suggestions)
- If using V2/V5 JSON/checklist outputs, aggregate violations and satisfaction rates.
- Post-processing can compute word counts, keyword detection, and forbidden word detection.

## 4. Best Practices (Template)
- Prompt design principles:
  - Convert hard constraints into lists or JSON fields to reduce omissions.
  - Make output rules explicit (story only / plus JSON).
  - Require a brief checklist to support human review.
- Model configuration tips:
  - For creative tasks, temperature 0.7–0.9; reduce when strict constraints dominate.
  - Control max_tokens to avoid overly long outputs.
- Risks and mitigations:
  - Missed forbidden words → scan and flag in post-processing.
  - Risk of style imitation → use abstract style tags, not living authors’ names.

## 5. Reproducibility
```bash
python Assignment/A1/task3_constraint_creator.py \
  --constraints_json Assignment/A1/constraints.sample.json \
  --model {run_config.model} \
  --temperature {run_config.temperature} \
  --max_tokens {run_config.max_tokens} \
  --output_dir Assignment/A1/outputs \
  --execute
```
""".strip()

    output_path.write_text(content, encoding="utf-8")


def run_variants(
    run_config: RunConfig,
    variants: List[Dict[str, Any]],
    constraints: Dict[str, Any],
) -> Dict[str, str]:
    outputs: Dict[str, str] = {}
    if not run_config.execute:
        return outputs

    for v in variants:
        vid = v["id"]
        prompt_text = v["prompt"]
        try:
            result_text = call_openai_response(
                model=run_config.model,
                prompt=prompt_text,
                temperature=run_config.temperature,
                max_tokens=run_config.max_tokens,
            )
        except Exception as e:  # robust logging, do not crash whole run
            result_text = f"[ERROR] {type(e).__name__}: {e}"

        outputs[vid] = result_text

    return outputs


def write_raw_outputs(output_dir: Path, variants: List[Dict[str, Any]], outputs: Dict[str, str]) -> None:
    if not outputs:
        return
    raw_dir = output_dir / "task3_runs"
    ensure_dir(raw_dir)
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    for v in variants:
        vid = v["id"]
        record = {
            "variant_id": vid,
            "name": v["name"],
            "rationale": v["rationale"],
            "prompt": v["prompt"],
            "output": outputs.get(vid, ""),
            "timestamp_utc": timestamp,
        }
        (raw_dir / f"{timestamp}_{vid}.json").write_text(
            json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Part A Task 3 - Constraint-based Creative Writing Runner"
    )
    parser.add_argument(
        "--constraints_json",
        type=str,
        default=None,
        help="Path to constraints JSON. If omitted, a built-in sample is used.",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=coalesce_model(),
        help="OpenAI model name (default from OPENAI_MODEL)",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="Sampling temperature",
    )
    parser.add_argument(
        "--max_tokens",
        type=int,
        default=800,
        help="Maximum tokens for generation",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="Assignment/A1/outputs",
        help="Directory for the report and raw outputs",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="If set, actually call the OpenAI API for all variants",
    )
    return parser.parse_args()


def main() -> None:
    load_env()

    args = parse_args()
    # Early validation for API key (to explain empty outputs)
    if not os.getenv("OPENAI_API_KEY"):
        print("[WARN] OPENAI_API_KEY is not set. The script will generate the report template but cannot call the API.")
        if args.execute:
            print("[HINT] Add OPENAI_API_KEY to your .env or environment and re-run with --execute.")
    output_dir = Path(args.output_dir)
    ensure_dir(output_dir)

    constraints = read_constraints_json(args.constraints_json)
    variants = build_prompt_variants(constraints)

    run_config = RunConfig(
        model=args.model,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        execute=bool(args.execute),
        output_dir=output_dir,
    )

    outputs = run_variants(run_config, variants, constraints)
    write_raw_outputs(output_dir, variants, outputs)

    report_path = output_dir / "task3_report.md"
    render_markdown_report(
        report_path,
        run_config=run_config,
        constraints=constraints,
        variants=variants,
        outputs=outputs,
    )

    print(f"Report written to: {report_path}")
    if outputs:
        print(f"Raw outputs written to: {output_dir / 'task3_runs'}")


if __name__ == "__main__":
    main()



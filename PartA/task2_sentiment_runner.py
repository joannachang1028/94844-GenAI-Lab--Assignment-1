"""
Task 2 - Sentiment Analysis for an Event (Part A)

Purpose
- Single-run script to classify sentiments on collected comments (e.g., CardiB cleared of assaulting on x.com).
- Loads API key from .env, runs five prompt variants, optionally evaluates accuracy/F1 if a label column exists.
- Emits a Markdown report and per-variant raw prediction files.

Usage
  python Assignment/A1/task2_sentiment_runner.py \
    --input_csv Assignment/A1/task2_comments.csv \
    --model ${OPENAI_MODEL:-gpt-4o-mini} \
    --temperature 0.2 \
    --max_tokens 200 \
    --output_dir Assignment/A1/outputs/task2 \
    --execute
"""

from __future__ import annotations

import argparse
import csv
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
except Exception:
    _HAS_OPENAI = False


@dataclass
class RunConfig:
    model: str
    temperature: float
    max_tokens: int
    execute: bool
    input_csv: Path
    output_dir: Path


def load_env() -> None:
    if load_dotenv is None:
        return
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


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def read_comments(csv_path: Path) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    if not csv_path.exists():
        return rows
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append({k: (v or "").strip() for k, v in r.items()})
    return rows


def build_prompt_variants() -> List[Dict[str, str]]:
    variants: List[Dict[str, str]] = [
        {
            "id": "v1_simple_label",
            "name": "V1 - Simple label (pos/neg/neutral)",
            "rationale": "Clean, constrained output ideal for aggregation.",
            "prompt_template": (
                "Classify the sentiment of the following text as one of: positive, negative, neutral.\n"
                "Only output the single label (no extra words).\n\n"
                "Text: {text}"
            ),
        },
        {
            "id": "v2_rules_enhanced",
            "name": "V2 - Rules for negation/sarcasm/emoji",
            "rationale": "Add guidance for common pitfalls while keeping single-label output.",
            "prompt_template": (
                "Consider negation, sarcasm, and emoji when classifying sentiment as positive, negative, or neutral.\n"
                "Only output the single label.\n\n"
                "Text: {text}"
            ),
        },
        {
            "id": "v3_label_definitions",
            "name": "V3 - Label definitions + strict output",
            "rationale": "Defines each label clearly to reduce ambiguity without using examples.",
            "prompt_template": (
                "Decide sentiment as one of: positive, negative, neutral.\n"
                "Definitions:\n"
                "- positive: praise, support, or optimism.\n"
                "- negative: criticism, anger, or disapproval.\n"
                "- neutral: factual, mixed, or unclear sentiment.\n"
                "Output only the single label.\n\n"
                "Text: {text}"
            ),
        },
        {
            "id": "v4_intensity",
            "name": "V4 - Intensity scale (-2..+2) + brief reason",
            "rationale": "Produces richer quantitative signals for analysis.",
            "prompt_template": (
                "Rate sentiment on a 5-level scale: -2, -1, 0, +1, +2 (very negative to very positive).\n"
                "Output exactly: <score>|<reason up to 12 words>.\n\n"
                "Text: {text}"
            ),
        },
        {
            "id": "v5_json",
            "name": "V5 - JSON {label, confidence_0_1, rationale}",
            "rationale": "Structured output to simplify logging and plotting.",
            "prompt_template": (
                "Classify the sentiment (positive, negative, neutral).\n"
                "Return a JSON object with keys: label, confidence_0_1, rationale (<= 15 words).\n"
                "Output only the JSON.\n\n"
                "Text: {text}"
            ),
        },
    ]
    return variants


def call_openai_response(model: str, prompt: str, temperature: float, max_tokens: int) -> str:
    if not _HAS_OPENAI:
        raise RuntimeError("OpenAI client not installed. `pip install --upgrade openai python-dotenv`.")
    client = OpenAI()
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


def parse_v4_intensity(output: str) -> Tuple[Optional[int], str]:
    if "|" in output:
        left, right = output.split("|", 1)
        left = left.strip()
        try:
            return int(left), right.strip()
        except Exception:
            return None, output.strip()
    try:
        return int(output.strip()), ""
    except Exception:
        return None, output.strip()


def predict(
    run_config: RunConfig,
    rows: List[Dict[str, str]],
    variants: List[Dict[str, str]],
) -> Dict[str, List[Dict[str, Any]]]:
    predictions: Dict[str, List[Dict[str, Any]]] = {v["id"]: [] for v in variants}
    if not run_config.execute or not rows:
        return predictions

    for r in rows:
        text = r.get("text", "")
        for v in variants:
            prompt = v["prompt_template"].format(text=text)
            try:
                out = call_openai_response(
                    model=run_config.model,
                    prompt=prompt,
                    temperature=run_config.temperature,
                    max_tokens=run_config.max_tokens,
                )
            except Exception as e:
                out = f"[ERROR] {type(e).__name__}: {e}"

            rec: Dict[str, Any] = {"text": text, "raw": out}
            if v["id"] == "v4_intensity":
                score, reason = parse_v4_intensity(out)
                rec.update({"score": score, "reason": reason})
            predictions[v["id"]].append(rec)

    return predictions


def compute_metrics(rows: List[Dict[str, str]], preds: List[str], labels: List[str]) -> Dict[str, Any]:
    # Macro-averaged precision/recall/F1 for labels in label_set
    unique = sorted(set(labels))
    label_to_idx = {l: i for i, l in enumerate(unique)}
    tp = [0] * len(unique)
    fp = [0] * len(unique)
    fn = [0] * len(unique)
    for y_true, y_pred in zip(labels, preds):
        if y_pred not in label_to_idx:
            # unrecognized → count as all-negative (increments fn for true class)
            fn[label_to_idx[y_true]] += 1
            continue
        if y_true == y_pred:
            tp[label_to_idx[y_true]] += 1
        else:
            fp[label_to_idx[y_pred]] += 1
            fn[label_to_idx[y_true]] += 1
    precs, recs, f1s = [], [], []
    for i in range(len(unique)):
        p = tp[i] / (tp[i] + fp[i]) if tp[i] + fp[i] > 0 else 0.0
        r = tp[i] / (tp[i] + fn[i]) if tp[i] + fn[i] > 0 else 0.0
        f1 = 2 * p * r / (p + r) if p + r > 0 else 0.0
        precs.append(p)
        recs.append(r)
        f1s.append(f1)
    return {
        "labels": unique,
        "macro_precision": sum(precs) / len(precs) if precs else 0.0,
        "macro_recall": sum(recs) / len(recs) if recs else 0.0,
        "macro_f1": sum(f1s) / len(f1s) if f1s else 0.0,
    }


def render_report(
    report_path: Path,
    run_config: RunConfig,
    variants: List[Dict[str, str]],
    rows: List[Dict[str, str]],
    predictions: Dict[str, List[Dict[str, Any]]],
) -> None:
    ensure_dir(report_path.parent)
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%SZ")
    header = f"""
# Part A - Task 2: Sentiment Analysis (Experiment Report)

**Timestamp (UTC)**: {ts}

## 0. Run Config
- Model: {run_config.model}
- Temperature: {run_config.temperature}
- Max Tokens: {run_config.max_tokens}
- Executed: {run_config.execute}
- Input CSV: {str(run_config.input_csv)}
- Output Dir: {str(run_config.output_dir)}
""".strip()

    var_desc = "\n".join([f"- {v['name']}: {v['rationale']}" for v in variants])

    # Optional dataset description for this specific CSV
    dataset_desc_line = ""
    try:
        if "cardib" in run_config.input_csv.name.lower():
            dataset_desc_line = "\n- Dataset description: The CSV contains replies/comments on posts about \"Cardi B cleared of assaulting security guard\" news from X.com."
    except Exception:
        pass

    sections: List[str] = [header + dataset_desc_line, "\n\n## 1. Prompt Variants\n" + var_desc]

    # Optional evaluation if ground truth exists (skip empty labels and normalize)
    if rows and "label" in rows[0]:
        def _normalize_label(val: str) -> str:
            s = (val or "").strip().lower()
            mapping = {"pos": "positive", "neg": "negative", "neu": "neutral",
                       "positive": "positive", "negative": "negative", "neutral": "neutral"}
            return mapping.get(s, s)

        allowed = {"positive", "negative", "neutral"}
        eval_rows: List[Tuple[str, float, float, float]] = []
        any_with_labels = False
        for v in variants:
            vid = v["id"]
            preds: List[str] = []
            gts: List[str] = []
            recs_for_vid = predictions.get(vid, [])
            for row, rec in zip(rows, recs_for_vid):
                raw_gt = row.get("label", "")
                if not raw_gt.strip():
                    continue
                gt = _normalize_label(raw_gt)
                if gt not in allowed:
                    continue
                gts.append(gt)

                raw_pred = (rec.get("raw") or "").strip()
                low = raw_pred.lower()
                if vid == "v5_json":
                    try:
                        obj = json.loads(low)
                        preds.append(_normalize_label(str(obj.get("label", ""))))
                    except Exception:
                        preds.append(low.split()[0] if low else "")
                elif vid == "v4_intensity":
                    score = rec.get("score")
                    preds.append("positive" if (isinstance(score, int) and score > 0) else ("negative" if isinstance(score, int) and score < 0 else "neutral"))
                else:
                    preds.append(low.split()[0] if low else "")

            if gts:
                any_with_labels = True
                rows_with_labels = [{"label": y} for y in gts]
                metrics = compute_metrics(rows_with_labels, preds, gts)
                eval_rows.append((v["name"], metrics["macro_f1"], metrics["macro_precision"], metrics["macro_recall"]))

        if any_with_labels and eval_rows:
            lines = ["\n\n## 2. Evaluation (Macro metrics)", "", "| Variant | Macro F1 | Macro Precision | Macro Recall |", "|---|---|---|---|"]
            for name, f1, p, r in eval_rows:
                lines.append(f"| {name} | {f1:.3f} | {p:.3f} | {r:.3f} |")
            sections.append("\n".join(lines))
        else:
            sections.append("\n\n## 2. Evaluation\nNo ground-truth labels found in CSV; evaluation skipped.")

    # Add sample rows with predictions for inspection (first 10)
    preview_limit = min(10, len(rows))
    for v in variants:
        vid = v["id"]
        sections.append(f"\n\n## 3. Preview — {v['name']}")
        table = ["| text | output |", "|---|---|"]
        for rec in predictions.get(vid, [])[:preview_limit]:
            text = (rec.get("text") or "").replace("\n", " ")[:120]
            out = (rec.get("raw") or "").replace("\n", " ")[:200]
            table.append(f"| {text} | {out} |")
        sections.append("\n".join(table))

    # 4. Output comparison across all variants (first N rows)
    preview_limit = min(10, len(rows))
    comp_lines: List[str] = ["\n\n## 4. Output Comparison (V1–V5)", ""]
    variant_short = [v["name"].split(" - ")[0] for v in variants]
    comp_lines.append("| text | " + " | ".join(variant_short) + " |")
    comp_lines.append("|---|" + "|".join(["---"] * len(variants)) + "|")
    for i in range(preview_limit):
        text_val = (rows[i].get("text", "") or "").replace("\n", " ")[:120]
        row_cells: List[str] = []
        for v in variants:
            vid = v["id"]
            recs_for_vid = predictions.get(vid, [])
            cell = ""
            if i < len(recs_for_vid):
                cell = (recs_for_vid[i].get("raw") or "").replace("\n", " ")[:200]
            row_cells.append(cell)
        comp_lines.append("| " + text_val + " | " + " | ".join(row_cells) + " |")
    sections.append("\n".join(comp_lines))

    best = """

## 5. Best Practices (Template)
- Constrain output to labels or JSON for easier evaluation.
- Include rules for negation/sarcasm/emoji to reduce common errors.
- Use clear label definitions to reduce ambiguity.
- Compute simple metrics on a small labeled subset; analyze distributions for the rest.

## 6. Reproducibility
```bash
python Assignment/A1/task2_sentiment_runner.py \
  --input_csv Assignment/A1/task2_comments.csv \
  --model gpt-4o-mini \
  --temperature 0.2 \
  --max_tokens 200 \
  --output_dir Assignment/A1/outputs/task2 \
  --execute
```
""".strip()

    (report_path).write_text("\n\n".join(sections) + "\n\n" + best, encoding="utf-8")


def write_raw_predictions(output_dir: Path, predictions: Dict[str, List[Dict[str, Any]]]) -> None:
    if not predictions:
        return
    raw_dir = output_dir / "task2_runs"
    ensure_dir(raw_dir)
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    for vid, recs in predictions.items():
        (raw_dir / f"{ts}_{vid}.json").write_text(
            json.dumps(recs, ensure_ascii=False, indent=2), encoding="utf-8"
        )


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Part A Task 2 - Sentiment Analysis Runner")
    p.add_argument("--input_csv", type=str, default="Assignment/A1/task2_comments.csv", help="CSV with columns: text[, label, source, timestamp]")
    p.add_argument("--model", type=str, default=coalesce_model(), help="OpenAI model (default from OPENAI_MODEL or gpt-4o-mini)")
    p.add_argument("--temperature", type=float, default=0.2, help="Sampling temperature")
    p.add_argument("--max_tokens", type=int, default=200, help="Max tokens")
    p.add_argument("--output_dir", type=str, default="Assignment/A1/outputs/task2", help="Output directory")
    p.add_argument("--execute", action="store_true", help="If set, actually call the API")
    return p.parse_args()


def main() -> None:
    load_env()
    args = parse_args()
    output_dir = Path(args.output_dir)
    ensure_dir(output_dir)

    run_config = RunConfig(
        model=args.model,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        execute=bool(args.execute),
        input_csv=Path(args.input_csv),
        output_dir=output_dir,
    )

    rows = read_comments(run_config.input_csv)
    if not rows:
        # Write a template if file missing
        tmpl = "text,source,timestamp,label\nThis is great!,x.com,2025-10-28T10:33:00Z,positive\nI don't care.,x.com,2025-10-28T10:35:00Z,neutral\nTerrible move.,x.com,2025-10-28T10:36:00Z,negative\n"
        run_config.input_csv.write_text(tmpl, encoding="utf-8")
        rows = read_comments(run_config.input_csv)

    variants = build_prompt_variants()
    predictions = predict(run_config, rows, variants)
    write_raw_predictions(output_dir, predictions)

    report_path = output_dir / "task2_report.md"
    render_report(report_path, run_config, variants, rows, predictions)

    print(f"Report written to: {report_path}")
    if predictions:
        print(f"Raw predictions written to: {output_dir / 'task2_runs'}")


if __name__ == "__main__":
    main()



# 94844 – GenAI Lab — Assignment 1 (Part A)

This folder contains Part A deliverables for three prompt-engineering tasks using the OpenAI API:

- Task 1: Medical Case Summarization
- Task 2: Sentiment Analysis on event comments (Cardi B cleared of assaulting security guard on X.com)
- Task 3: Constraint‑based Creative Writing

Key outputs are Markdown reports in `outputs/` for each task, plus per‑run JSON logs.

## 1) Requirements

- Python 3.9+ (tested on macOS)
- Packages: `openai`, `python-dotenv`

Install:

```bash
python3 -m pip install --upgrade openai python-dotenv
```

## 2) Environment

Create a `.env` file at the repository root (same directory as this README):

```bash
OPENAI_API_KEY=sk-xxxx
OPENAI_MODEL=gpt-4o-mini
```

Notes:
- The scripts auto-load `.env` from the CWD and project root.
- If your key doesn’t have access to certain models, set `OPENAI_MODEL` to one you can use (e.g., `gpt-4o-mini`).

## 3) Folder Layout (A1)

```
Assignment/A1/
  task1_medical_summarizer.py
  task2_sentiment_runner.py
  task3_constraint_creator.py
  task1_cases/
    case1.md ... case5.md
  outputs/
    task1/  # report + JSON runs
    task2/  # report + JSON runs
    task3/  # report + JSON runs
  README.md
```

## 4) How to Run

Run from the `Assignment/A1` directory.

### Task 1 — Medical Case Summarization

Place 3–5 public case reports in `task1_cases/` as `.md` or `.txt`.

```bash
python3 task1_medical_summarizer.py \
  --model gpt-4o-mini \
  --temperature 0.2 \
  --max_tokens 600 \
  --output_dir outputs/task1 \
  --execute
```

Outputs:
- Report: `outputs/task1/task1_report.md`
- Raw JSON runs: `outputs/task1/task1_runs/*.json`

### Task 2 — Sentiment Analysis (X.com event)

CSV format: `text,source,timestamp,label` (label optional). This repo includes
`task2_cardib_cleared_assaulting_replies.csv`, which contains replies/comments on posts about
“Cardi B cleared of assaulting security guard” from X.com.

```bash
python3 task2_sentiment_runner.py \
  --input_csv task2_cardib_cleared_assaulting_replies.csv \
  --model gpt-4o-mini \
  --temperature 0.2 \
  --max_tokens 200 \
  --output_dir outputs/task2 \
  --execute
```

What you get:
- Report: `outputs/task2/task2_report.md`
  - Section 2: a comparison table for Macro F1/Precision/Recall (shown when labels are present)
  - Section 4: a V1–V5 output comparison table (first 10 rows)
- Raw JSON runs: `outputs/task2/task2_runs/*.json`

### Task 3 — Constraint‑based Creative Writing

```bash
python3 task3_constraint_creator.py \
  --model gpt-4o-mini \
  --temperature 0.7 \
  --max_tokens 800 \
  --output_dir outputs/task3 \
  --execute
```

Outputs:
- Report: `outputs/task3/task3_report.md`
- Raw JSON runs: `outputs/task3/*.json`

Tip: Use `-h` on any script to see available flags.

## 5) Troubleshooting

- `[WARN] OPENAI_API_KEY is not set.`
  - Ensure `.env` is present and contains a valid key; restart the shell if needed.
- `RuntimeError: OpenAI client not installed.`
  - `python3 -m pip install --upgrade openai python-dotenv`
- `APIRemovedInV1` about `openai.ChatCompletion`
  - Scripts use the v1 client; ensure you’re running the provided scripts unmodified.
- `Permission denied` when executing a `.py`
  - Run with `python3 script.py` instead of trying to execute the file directly.

## 6) Notes

- For Task 1, do not paste entire case texts into the report; they are referenced from `task1_cases/`.
- For Task 2, metrics are computed only on rows with a valid `label` (positive/negative/neutral).
- Keep `.env` private; it is ignored via `.gitignore`.



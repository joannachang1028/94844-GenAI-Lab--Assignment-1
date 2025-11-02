# 94844 – GenAI Lab — Assignment 1 

This repository contains deliverables for **Assignment 1** of *94-844 Generative AI Lab.  
Part A covers three prompt-engineering tasks using the OpenAI API, and Part B extends Task 2 with few-shot, zero-shot, and chain-of-thought experiments.


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


## 7) Part B — Few-Shot / Zero-Shot / Chain-of-Thought Prompting Experiments**

  

Part B extends Task 2 (Sentiment Analysis) to analyze how different prompting strategies affect model performance.

Experiments include zero-shot, one-shot, three-shot, five-shot, five-shot-shuffled, and chain-of-thought (CoT) configurations.

  

### **Dataset**

  

task2_cardib_cleared_assaulting_replies_added.csv

contains 40 X.com comments (20 positive, 10 neutral, 10 negative) about the “Cardi B trial outcome.”

  

### **Prompts**

  

All prompts are in prompts/ and follow this template:

```
You are a sentiment-analysis assistant.  
Classify short social-media comments about Cardi B’s court verdict
as positive, negative, or neutral.

Example:

Only output the label.

Now classify:
Text: "{text}"
Sentiment:
```

### **Running Experiments**

```
jupyter notebook task2B_shots.ipynb
```

This script iterates over six prompt types, calls the OpenAI API, and outputs:

- Per-prompt metrics.csv and results.json
    
- Aggregate results in outputs/summary_results.csv
    

  

### **Summary Results**

|**Version**|**Accuracy**|**Macro F1**|
|---|---|---|
|zero_shot|0.775|0.748|
|one_shot|0.750|0.711|
|three_shot|0.800|0.762|
|five_shot|**0.825**|**0.807**|
|five_shot_shuffled|0.775|0.749|
|cot|0.475|0.468|

### **Findings**

- **Performance improves with more examples** – accuracy rises from 0.75 → 0.83 as shots increase.
    
- **Example order matters** – shuffled five-shot drops slightly in macro F1.
    
- **Chain-of-Thought underperforms** – reasoning steps hurt simple classification tasks.
    
- **Positive comments are easiest** while neutral remain most ambiguous.
    
- **Best overall:** Five-Shot prompt (82.5 % accuracy, 0.81 macro F1).
    

  

### **Deliverables**

- prompts/*.txt – six prompt configurations
    
- run_fewshot_experiments.py – main runner
    
- outputs/summary_results.csv – aggregate metrics
    
- B_fewshot_report.md – analysis and discussion
    

---

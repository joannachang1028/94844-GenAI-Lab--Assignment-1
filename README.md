# 94844 – GenAI Lab — Assignment 1 

**Student:** Joanna Chang and Siqi Yu 

**Intro:** This repository contains deliverables for **Assignment 1** of 94-844 Generative AI Lab.  
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
OPENAI_MODEL=gpt-5-mini
```

Notes:
- The scripts auto-load `.env` from the CWD and project root.
- If your key doesn’t have access to certain models, set `OPENAI_MODEL` to one you can use (e.g., `gpt-4o-mini`).

## 3) Part A — Prompt Engineering Experiments

  

Part A covers three prompt-engineering tasks using the OpenAI API to analyze how different prompt variants affect model performance across medical summarization, sentiment analysis, and creative writing.

Each task tests five distinct prompt variants to identify effective strategies for optimizing model outputs.

Folder Layout
```
PartA/
  Part A report.md
  task1_medical_summarizer.py
  task2_sentiment_runner.py
  task3_constraint_creator.py
  
  task1_cases/
    case1.md ... case5.md
  task2_cardib_cleared_assaulting_replies.csv

  outputs/
    task1/  # report + JSON runs
    task2/  # report + JSON runs
    task3/  # report + JSON runs
```

### **Dataset**

  

- **Task 1:** Five open-access medical case reports (`task1_cases/`)  
- **Task 2:** `task2_cardib_cleared_assaulting_replies.csv` — 40 X.com comments (20 positive) related to Cardi B's court case  
- **Task 3:** No external dataset; generation-only creative writing task with constraints
  

### **Prompt Variants**

Each task implements five prompt variants:

- **Task 1 (Medical Summarization):** Structured summary, JSON format, SOAP format, Timeline, Summary + uncertainties
- **Task 2 (Sentiment Analysis):** Simple label, Rules for negation/sarcasm/emoji, Label definitions, Intensity scale, JSON output
- **Task 3 (Creative Writing):** Strict constraints, Story + self-check JSON, Style guidance, Internal planning, Story + checklist

Find detailed descriptions and rationale in Part A report.md

### **Running Experiments**

  

Run from the `PartA/` directory.

```bash
# Task 1 - Medical Case Summarization
python3 task1_medical_summarizer.py \
  --model gpt-5-mini \
  --max_tokens 800 \
  --output_dir outputs/task1 \
  --execute

# Task 2 - Sentiment Analysis
python3 task2_sentiment_runner.py \
  --input_csv task2_cardib_cleared_assaulting_replies.csv \
  --model gpt-5-mini \
  --max_tokens 200 \
  --output_dir outputs/task2 \
  --execute

# Task 3 - Creative Writing
python3 task3_constraint_creator.py \
  --model gpt-5-mini \
  --max_tokens 800 \
  --output_dir outputs/task3 \
  --execute
```

These scripts iterate over prompt variants, call the OpenAI API, and output:

- Per-task reports in `outputs/task*/task*_report.md`
    
- Raw JSON runs in `outputs/task*/task*_runs/*.json` or `outputs/task3/*.json`
    


### **Summary Results**

|**Task**|**Best Variant(s)**|**Key Metric**|**Improvement**|
|---|---|---|---|
|Task 1: Medical Summarization|V1, V2, V3|Coverage: 100%|All successful (V4 failed)|
|Task 2: Sentiment Analysis|V2, V3, V4|Macro F1: 0.857|+8.8% vs V1 (0.788)|
|Task 3: Creative Writing|V2, V5|Constraint adherence: High|All variants successful|

Find more in Part A report.md

### **Findings**

- **Structured outputs outperform** – Explicit formats (JSON, SOAP, sections) ensure comprehensive coverage and reduce omissions.
    
- **Task-specific guidance matters** – Rules for negation/sarcasm (Task 2) and clinical templates (Task 1) significantly improve performance on edge cases.
    
- **Self-verification enhances reliability** – Self-check mechanisms (Task 3 V2/V5) enable automated constraint validation.
    
- **Explicit definitions reduce ambiguity** – Clear label definitions (Task 2 V3) improve consistency and recall.
    
- **Best overall:** Task 1 V1/V3 (100% coverage), Task 2 V2/V3 (85.7% Macro F1), Task 3 V2/V5 (high constraint adherence).
    


## 4) Part B — Few-Shot / Zero-Shot / Chain-of-Thought Prompting Experiments

  

Part B extends Task 2 (Sentiment Analysis) to analyze how different prompting strategies affect model performance.

Experiments include zero-shot, one-shot, three-shot, five-shot, five-shot-shuffled, and chain-of-thought (CoT) configurations.

Folder Layout
```
/PartB/
  prompts/
    zero_shot.txt
    one_shot.txt
    three_shot.txt
    five_shot.txt
    five_shot_shuffled.txt
    cot.txt
  outputs/
    zero_shot/   
    one_shot/
    three_shot/
    five_shot/
    five_shot_shuffled/
    cot/
    summary_results.csv 
  task2_cardib_cleared_assaulting_replies_added.csv 
  task2B_shots.ipynb
  B_fewshot_report.md    
  ```

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

Find more in B_fewshot_report.md

### **Findings**

- **Performance improves with more examples** – accuracy rises from 0.75 → 0.83 as shots increase.
    
- **Example order matters** – shuffled five-shot drops slightly in macro F1.
    
- **Chain-of-Thought underperforms** – reasoning steps hurt simple classification tasks.
    
- **Positive comments are easiest** while neutral remain most ambiguous.
    
- **Best overall:** Five-Shot prompt (82.5 % accuracy, 0.81 macro F1).
    



---

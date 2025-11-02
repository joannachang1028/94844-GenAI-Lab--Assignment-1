# Part B – Few-Shot / Zero-Shot / Chain-of-Thought Prompting

**Course:** 94-844 Generative AI Lab (Fall 2025)   
**Task:** Sentiment classification of X.com comments about “Cardi B cleared of assaulting a security guard”  
**Model used:** `gpt-4o-mini`  
**Date run:** 2025-11-01  
**Files used:**  
- input: `task2_cardib_cleared_assaulting_replies_added.csv`  
- prompts: `prompts/zero_shot.txt`, `prompts/one_shot.txt`, `prompts/three_shot.txt`, `prompts/five_shot.txt`, `prompts/five_shot_shuffled.txt`, `prompts/cot.txt`  
- script: `task2B_shots.ipynb` (looping over the 6 prompts and writing metrics)  
- output dir: `outputs/…`

---

## 1. Objective

The goal of this part is to **systematically compare** different prompting strategies for the *same* classification task and to see (i) how many in-context examples the model actually needs, (ii) whether example **ordering** matters, and (iii) whether adding a plain chain-of-thought (CoT) scaffold helps or hurts for short social-media sentiment.

Unlike Part A, here we **do not** change the task; we only change **how we ask** the model.

---

## 2. Dataset and Split

- **Source domain:** short, informal X.com (Twitter-like) comments reacting to the news that *Cardi B was cleared of assaulting a security guard*.  
- **Classes:** `positive` `neutral` `negative`
- **Problem:** the original crawl for this news was **heavily positive** (fans congratulating her, praising her for telling fans not to harass the other woman, etc.).  
- **Fix:** I manually **augmented** the file with **10 neutral + 10 negative** comments in the *same style / same event* so that the model would not get an automatic 80% just by outputting “positive”.

Final evaluation set:

- 10 **negative** rows  
- 10 **neutral** rows  
- 20 **positive** rows  
- **Total = 40** rows

This 40-row file is what I call the **test set**.  
The “training set” in this part is **in-prompt only**: the examples I put inside the 1-shot / 3-shot / 5-shot prompts. There is no separate fine-tuning.

---

## 3. Prompt Configurations

I designed 6 prompt configurations to match the assignment:

1. **Baseline prompt (`zero_shot.txt`)**  
   - Instruction only.  
   - “Classify as positive / negative / neutral. Only output the label.”  
   - No examples.

2. **1-shot (`one_shot.txt`)**  
   - Instruction + **1 positive example**  
   - Purpose: test whether *just one* demonstration helps.

3. **3-shot (`three_shot.txt`)**  
   - Instruction + **3 examples**: one positive, one negative, one neutral  
   - Purpose: give the model *coverage* over all 3 labels.

4. **5-shot (`five_shot.txt`)**  
   - Instruction + **5 examples** (2 pos, 2 neg, 1 neutral, all in this news domain)  
   - Purpose: richer in-domain context.

5. **5-shot shuffled (`five_shot_shuffled.txt`)**  
   - Same 5 examples as above, but **reordered**  
   - Purpose: test **example order sensitivity** (the assignment gave this as an example of “two other configurations”).

6. **Chain-of-Thought (`cot.txt`)**  
   - A reasoning-style prompt: “Think step by step, restate the comment, identify tone, then give the label.”  
   - Purpose: compare “with a worked reasoning pattern” vs “just label”.

All 6 prompts end with this pattern:

```text
Text: "{text}"
Sentiment:
```

## 4. Results Analysis

## (a) Training / Test Sets + Accuracy Table

**Training set (conceptual).**  
In Part B we did *in-context* learning only — no separate fine-tuning. That means the “training data” for each experiment is simply the examples embedded **inside the prompt**:

- `one_shot` → 1 in-domain example (positive)
- `three_shot` → 3 examples (positive + negative + neutral)
- `five_shot` → 5 in-domain examples (mixed tones about the same Cardi B case)
- `five_shot_shuffled` → same 5 examples, different **order**
- `cot` → 1 example + chain-of-thought pattern

Each prompt therefore has its **own** tiny “training set”.

**Test set.**  
All prompts were evaluated on the *same* labeled file:

- file: `task2_cardib_cleared_assaulting_replies_added.csv`
- 40 rows total:
  - 10 negative
  - 10 neutral
  - 20 positive
- all comments are about the **same news event** (“Cardi B cleared…”), so domain is very narrow
- we manually added neutral + negative comments to avoid a “predict positive = high accuracy” situation

**Final test-set accuracies**

| Prompt               | Accuracy | Macro F1 |
|----------------------|----------|----------|
| zero_shot            | 0.775    | 0.7480   |
| one_shot             | 0.750    | 0.7109   |
| three_shot           | 0.800    | 0.7619   |
| **five_shot**        | **0.825**| **0.8073** |
| five_shot_shuffled   | 0.775    | 0.7485   |
| **cot**              | **0.475**| **0.4676** |

So the ordering by accuracy is:

**five_shot > three_shot > zero_shot ≈ five_shot_shuffled > one_shot >> cot**

---

## (b) Prompting Formats: What Worked / What Didn’t

### What we tried

1. **Zero-shot (baseline)**  
   - plain instruction: “classify as positive / negative / neutral; output only the label.”
   - purpose: baseline

2. **One-shot**  
   - instruction + 1 (positive) example  
   - purpose: see if a single demonstration helps

3. **Three-shot**  
   - instruction + 3 examples (one per class)  
   - purpose: make the label space explicit

4. **Five-shot**  
   - instruction + 5 in-domain examples (mixture of praise, criticism, and factual comments about Cardi B’s case)  
   - purpose: give richer, realistic context

5. **Five-shot (shuffled)**  
   - same 5 examples, different order  
   - purpose: test **example-order sensitivity** (as the assignment suggested)

6. **Chain-of-Thought (CoT)**  
   - “think step by step” + then give sentiment  
   - purpose: compare “reasoning-style” vs “label-only” prompting

---

### What worked well

- **Five-shot** was the best: **0.825 acc / 0.807 macro F1.**  
  - negative recall = **1.0** → it caught every negative comment (10/10)  
  - neutral precision = **1.0** → whenever it said “neutral”, it was right  
  - positive stayed high (f1 ≈ 0.87)  
  - this tells us: **more diverse, in-domain examples helped the most** on this dataset.

- **Three-shot** was clearly better than zero-shot: **0.80 acc**.  
  - the big jump was negative recall: **0.8 → 0.9** once the model *saw* a negative example.  
  - this shows: **showing all 3 labels in the prompt matters more than just “adding an example.”**

- **Zero-shot** was already decent (0.775) because
  1. the task is very narrow,
  2. the label space is tiny,
  3. the event context is obvious (“she was cleared → many comments are supportive”).

---

### What didn’t work / was weaker

- **One-shot** (0.75) was actually **worse** than zero-shot (0.775).  
  - reason: the single example was **positive**, so the model got a biased picture of the task → neutral recall dropped to 0.5.  
  - lesson: **unbalanced few-shot can be worse than no few-shot.**

- **Five-shot (shuffled)** fell back to 0.775.  
  - same examples, only order changed → performance dropped → **LLM is order-sensitive** in in-context learning.  
  - here, putting negative earlier made negative very easy (recall = 1.0) but hurt the overall balance.

- **CoT** crashed to **0.475**.  
  - not because CoT is “wrong”, but because this is a **short classification** task and our code used **string-contains** to read the label:
    ```python
    if "positive" in output: ...
    elif "negative" in output: ...
    else: "neutral"
    ```
  - CoT produced *longer* answers like “the tone is more neutral than positive …” and that fooled the parser.  
  - lesson: **for classification, CoT must end with a strict final label line; otherwise it can hurt badly.**

---

## (c) Factors That Most Affect Performance

Based on the six runs and the class-wise reports you got, the biggest factors are:

1. **Coverage of all labels in the prompt**  
   - 1-shot (only positive) → neutral f1 = 0.55  
   - 3-shot (pos+neg+neutral) → macro F1 ↑ to 0.76  
   - so the model is **very sensitive** to whether the prompt actually shows `negative` and `neutral`, not just `positive`.

2. **Number of shots (0 → 3 → 5)**  
   - accuracy improved almost monotonically: 0.775 → 0.80 → 0.825  
   - on this domain, giving *more examples from the same event* helped more than clever wording.

3. **Example order**  
   - five-shot = 0.825, five-shot-shuffled = 0.775  
   - same content, different order → different result → **recency / position effects**  
   - practically: **put the hardest class (neutral) toward the end**.

4. **Output strictness**  
   - all good prompts: model outputs just a label → easy to parse → good accuracy  
   - CoT: model outputs a paragraph → string-based label extraction fails → accuracy collapses  
   - so for sentiment classification: **short, constrained outputs beat long, “smart” outputs**.

5. **Domain match of the examples**  
   - the five-shot examples were written in the *same* X.com tone and about the *same* Cardi B news → the model didn’t have to “transfer domain”, it only had to “copy pattern” → hence 0.825 on a tiny 40-row test set.

---

## Short interpretation of the per-class reports

- **Neutral is consistently the hardest class.**  
  - zero-shot neutral recall = 0.6  
  - three-shot neutral recall = 0.5  
  - five-shot neutral recall = 0.6  
  - this is expected: neutral comments here are *reporting the outcome* but sometimes contain a small stance; they sit between “I support her” and “I don’t care”.

- **Negative becomes perfect once you show enough negative.**  
  - five-shot and five-shot-shuffled both hit **negative recall = 1.0**  
  - this is because your negative examples are stylistically very different (“celebs always get away”, “show some respect in court”).

- **CoT flipped some labels.**  
  - it gave neutral recall = 0.7 but negative recall = 0.3 and positive recall = 0.45 → a super noisy pattern → exactly what happens when generation is long but the parser is dumb.

---

## Summary

> We evaluated six prompting strategies (zero-shot, 1-shot, 3-shot, 5-shot, 5-shot-shuffled, and CoT) on the same 40-row, three-class dataset of X.com comments about the Cardi B verdict. The test set was balanced (10 neg / 10 neutral / 20 pos), while the “training” for each variant was in-prompt only. Performance improved clearly when we (i) showed **all** target labels in context and (ii) increased the number of in-domain examples: accuracy went from 0.775 (zero-shot) to 0.800 (3-shot) and peaked at 0.825 (5-shot). Shuffling the same 5 examples dropped accuracy back to 0.775, confirming that example order matters. A naïve chain-of-thought prompt hurt badly (0.475) because its longer generations conflicted with our simple label extraction. Overall, the most important factors were label coverage, number and order of in-prompt examples, and having a strictly constrained output format.
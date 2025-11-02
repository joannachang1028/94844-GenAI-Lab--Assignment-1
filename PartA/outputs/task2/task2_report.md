# Part A - Task 2: Sentiment Analysis (Experiment Report)

**Timestamp (EST)**: 2025-11-02 10:49:17 EST

## 0. Run Config
- Model: gpt-5-mini
- Temperature: 0.2
- Max Tokens: 200
- Executed: True
- Input CSV: /Users/joannachang/Documents/25 Fall mini 2/GenAI/Assignment/A1/PartA/task2_cardib_cleared_assaulting_replies.csv
- Output Dir: /Users/joannachang/Documents/25 Fall mini 2/GenAI/Assignment/A1/PartA/outputs/task2
- Dataset description: The CSV contains replies/comments on posts about "Cardi B cleared of assaulting security guard" news from X.com.



## 1. Prompt Variants
- V1 - Simple label (pos/neg/neutral): Clean, constrained output ideal for aggregation.
- V2 - Rules for negation/sarcasm/emoji: Add guidance for common pitfalls while keeping single-label output.
- V3 - Label definitions + strict output: Defines each label clearly to reduce ambiguity without using examples.
- V4 - Intensity scale (-2..+2) + brief reason: Produces richer quantitative signals for analysis.
- V5 - JSON {label, confidence_0_1, rationale}: Structured output to simplify logging and plotting.



## 2. Evaluation (Macro metrics)

| Variant | Macro F1 | Macro Precision | Macro Recall |
|---|---|---|---|
| V1 - Simple label (pos/neg/neutral) | 0.788 | 1.000 | 0.650 |
| V2 - Rules for negation/sarcasm/emoji | 0.857 | 1.000 | 0.750 |
| V3 - Label definitions + strict output | 0.857 | 1.000 | 0.750 |
| V4 - Intensity scale (-2..+2) + brief reason | 0.857 | 1.000 | 0.750 |
| V5 - JSON {label, confidence_0_1, rationale} | 0.824 | 1.000 | 0.700 |



## 3. Preview — V1 - Simple label (pos/neg/neutral)

| text | output |
|---|---|
| At least the trial gave us iconic moments congrats queen | positive |
| At least we got some good memes lol | positive |
| BIG BRIM DID IT AGAIN ☺️. | positive |
| EGGS IN YALL FACES ONCE AGAIN … YALL DOUBTED MY GIRL AGAIN AND FAILED.. BETTER LUCK NEXT TIME | negative |
| Fan account served looks and justice was served. | positive |
| I love how she told her fans “do not go harrass her or her family” I love that | positive |
| I love that she told her fans not to bother her or her family | positive |
| I really appreciated that she told her fans not to bother that woman. The jury made the right decision. This did seem li | positive |
| It should not have been a case. No woman should be filmed at the gynecologist's office by anyone, especially an employee | negative |
| See how she told her fans not to harass that lady ?? It’s that simple | positive |



## 3. Preview — V2 - Rules for negation/sarcasm/emoji

| text | output |
|---|---|
| At least the trial gave us iconic moments congrats queen | positive |
| At least we got some good memes lol | positive |
| BIG BRIM DID IT AGAIN ☺️. | positive |
| EGGS IN YALL FACES ONCE AGAIN … YALL DOUBTED MY GIRL AGAIN AND FAILED.. BETTER LUCK NEXT TIME | positive |
| Fan account served looks and justice was served. | positive |
| I love how she told her fans “do not go harrass her or her family” I love that | positive |
| I love that she told her fans not to bother her or her family | positive |
| I really appreciated that she told her fans not to bother that woman. The jury made the right decision. This did seem li | positive |
| It should not have been a case. No woman should be filmed at the gynecologist's office by anyone, especially an employee | negative |
| See how she told her fans not to harass that lady ?? It’s that simple | positive |



## 3. Preview — V3 - Label definitions + strict output

| text | output |
|---|---|
| At least the trial gave us iconic moments congrats queen | positive |
| At least we got some good memes lol | positive |
| BIG BRIM DID IT AGAIN ☺️. | positive |
| EGGS IN YALL FACES ONCE AGAIN … YALL DOUBTED MY GIRL AGAIN AND FAILED.. BETTER LUCK NEXT TIME | negative |
| Fan account served looks and justice was served. | positive |
| I love how she told her fans “do not go harrass her or her family” I love that | positive |
| I love that she told her fans not to bother her or her family | positive |
| I really appreciated that she told her fans not to bother that woman. The jury made the right decision. This did seem li | positive |
| It should not have been a case. No woman should be filmed at the gynecologist's office by anyone, especially an employee | negative |
| See how she told her fans not to harass that lady ?? It’s that simple | positive |



## 3. Preview — V4 - Intensity scale (-2..+2) + brief reason

| text | output |
|---|---|
| At least the trial gave us iconic moments congrats queen | +2|Celebratory praise for iconic moments; congratulatory 'congrats queen' |
| At least we got some good memes lol | +1|Lighthearted consolation; finding a silver lining. |
| BIG BRIM DID IT AGAIN ☺️. | +2|Enthusiastic praise celebrating repeated success. |
| EGGS IN YALL FACES ONCE AGAIN … YALL DOUBTED MY GIRL AGAIN AND FAILED.. BETTER LUCK NEXT TIME | -2|Taunting, gloating and hostile language towards others |
| Fan account served looks and justice was served. | +2|Positive, celebratory: great looks and justice served. |
| I love how she told her fans “do not go harrass her or her family” I love that | +2|Praises protective stance against harassment |
| I love that she told her fans not to bother her or her family | +2|Strong approval of her setting boundaries with fans |
| I really appreciated that she told her fans not to bother that woman. The jury made the right decision. This did seem li | +2|Supports jury decision, appreciates restraint, labels the case frivolous. |
| It should not have been a case. No woman should be filmed at the gynecologist's office by anyone, especially an employee | -2|Strong condemnation of privacy violation and wrongdoing. |
| See how she told her fans not to harass that lady ?? It’s that simple | +1|Approves her asking fans not to harass someone. |



## 3. Preview — V5 - JSON {label, confidence_0_1, rationale}

| text | output |
|---|---|
| At least the trial gave us iconic moments congrats queen | {"label":"positive","confidence_0_1":0.93,"rationale":"Praises 'iconic moments' and congratulates 'queen', expressing positive sentiment."} |
| At least we got some good memes lol | {"label":"positive","confidence_0_1":0.9,"rationale":"Positive appraisal of memes with laughing 'lol' indicates upbeat tone."} |
| BIG BRIM DID IT AGAIN ☺️. | {"label":"positive","confidence_0_1":0.96,"rationale":"Praise with smiling emoji indicates enthusiastic positive sentiment."} |
| EGGS IN YALL FACES ONCE AGAIN … YALL DOUBTED MY GIRL AGAIN AND FAILED.. BETTER LUCK NEXT TIME | {"label":"negative","confidence_0_1":0.95,"rationale":"Taunting and mocking opponents; triumphant gloating."} |
| Fan account served looks and justice was served. | {"label":"positive","confidence_0_1":0.92,"rationale":"Celebratory praise; compliments looks and affirms justice being served."} |
| I love how she told her fans “do not go harrass her or her family” I love that | {"label":"positive","confidence_0_1":0.95,"rationale":"Expresses approval and admiration for her statement."} |
| I love that she told her fans not to bother her or her family | {"label":"positive","confidence_0_1":0.95,"rationale":"Approval of her telling fans not to bother her or her family"} |
| I really appreciated that she told her fans not to bother that woman. The jury made the right decision. This did seem li | {"label":"positive","confidence_0_1":0.95,"rationale":"Expresses approval and appreciation; supports jury decision; views case as frivolous."} |
| It should not have been a case. No woman should be filmed at the gynecologist's office by anyone, especially an employee | {"label":"negative","confidence_0_1":0.95,"rationale":"Expresses strong condemnation of a privacy violation; disapproving tone."} |
| See how she told her fans not to harass that lady ?? It’s that simple | {"label":"positive","confidence_0_1":0.91,"rationale":"Approving her action to stop harassment; expresses approval and simplicity."} |



## 4. Output Comparison (V1–V5)

| text | V1 | V2 | V3 | V4 | V5 |
|---|---|---|---|---|---|
| At least the trial gave us iconic moments congrats queen | positive | positive | positive | +2|Celebratory praise for iconic moments; congratulatory 'congrats queen' | {"label":"positive","confidence_0_1":0.93,"rationale":"Praises 'iconic moments' and congratulates 'queen', expressing positive sentiment."} |
| At least we got some good memes lol | positive | positive | positive | +1|Lighthearted consolation; finding a silver lining. | {"label":"positive","confidence_0_1":0.9,"rationale":"Positive appraisal of memes with laughing 'lol' indicates upbeat tone."} |
| BIG BRIM DID IT AGAIN ☺️. | positive | positive | positive | +2|Enthusiastic praise celebrating repeated success. | {"label":"positive","confidence_0_1":0.96,"rationale":"Praise with smiling emoji indicates enthusiastic positive sentiment."} |
| EGGS IN YALL FACES ONCE AGAIN … YALL DOUBTED MY GIRL AGAIN AND FAILED.. BETTER LUCK NEXT TIME | negative | positive | negative | -2|Taunting, gloating and hostile language towards others | {"label":"negative","confidence_0_1":0.95,"rationale":"Taunting and mocking opponents; triumphant gloating."} |
| Fan account served looks and justice was served. | positive | positive | positive | +2|Positive, celebratory: great looks and justice served. | {"label":"positive","confidence_0_1":0.92,"rationale":"Celebratory praise; compliments looks and affirms justice being served."} |
| I love how she told her fans “do not go harrass her or her family” I love that | positive | positive | positive | +2|Praises protective stance against harassment | {"label":"positive","confidence_0_1":0.95,"rationale":"Expresses approval and admiration for her statement."} |
| I love that she told her fans not to bother her or her family | positive | positive | positive | +2|Strong approval of her setting boundaries with fans | {"label":"positive","confidence_0_1":0.95,"rationale":"Approval of her telling fans not to bother her or her family"} |
| I really appreciated that she told her fans not to bother that woman. The jury made the right decision. This did seem li | positive | positive | positive | +2|Supports jury decision, appreciates restraint, labels the case frivolous. | {"label":"positive","confidence_0_1":0.95,"rationale":"Expresses approval and appreciation; supports jury decision; views case as frivolous."} |
| It should not have been a case. No woman should be filmed at the gynecologist's office by anyone, especially an employee | negative | negative | negative | -2|Strong condemnation of privacy violation and wrongdoing. | {"label":"negative","confidence_0_1":0.95,"rationale":"Expresses strong condemnation of a privacy violation; disapproving tone."} |
| See how she told her fans not to harass that lady ?? It’s that simple | positive | positive | positive | +1|Approves her asking fans not to harass someone. | {"label":"positive","confidence_0_1":0.91,"rationale":"Approving her action to stop harassment; expresses approval and simplicity."} |

## 5. Best Practices (Template)
- Constrain output to labels or JSON for easier evaluation.
- Include rules for negation/sarcasm/emoji to reduce common errors.
- Use clear label definitions to reduce ambiguity.
- Compute simple metrics on a small labeled subset; analyze distributions for the rest.

## 6. Reproducibility
```bash
python Assignment/A1/task2_sentiment_runner.py   --input_csv Assignment/A1/task2_comments.csv   --model gpt-5-mini   --temperature 0.2   --max_tokens 200   --output_dir Assignment/A1/outputs/task2   --execute
```
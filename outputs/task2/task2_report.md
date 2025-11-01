# Part A - Task 2: Sentiment Analysis (Experiment Report)

**Timestamp (UTC)**: 2025-11-01 22:23:46Z

## 0. Run Config
- Model: gpt-4o-mini
- Temperature: 0.2
- Max Tokens: 200
- Executed: True
- Input CSV: /Users/joannachang/Documents/25 Fall mini 2/GenAI/Assignment/A1/task2_cardib_cleared_assaulting_replies.csv
- Output Dir: /Users/joannachang/Documents/25 Fall mini 2/GenAI/Assignment/A1/outputs/task2
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
| V1 - Simple label (pos/neg/neutral) | 0.750 | 1.000 | 0.600 |
| V2 - Rules for negation/sarcasm/emoji | 0.667 | 1.000 | 0.500 |
| V3 - Label definitions + strict output | 0.750 | 1.000 | 0.600 |
| V4 - Intensity scale (-2..+2) + brief reason | 0.889 | 1.000 | 0.800 |
| V5 - JSON {label, confidence_0_1, rationale} | 0.788 | 1.000 | 0.650 |



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
| See how she told her fans not to harass that lady ?? It’s that simple | neutral |



## 3. Preview — V2 - Rules for negation/sarcasm/emoji

| text | output |
|---|---|
| At least the trial gave us iconic moments congrats queen | Positive |
| At least we got some good memes lol | Positive |
| BIG BRIM DID IT AGAIN ☺️. | Positive |
| EGGS IN YALL FACES ONCE AGAIN … YALL DOUBTED MY GIRL AGAIN AND FAILED.. BETTER LUCK NEXT TIME | Negative |
| Fan account served looks and justice was served. | Positive |
| I love how she told her fans “do not go harrass her or her family” I love that | Positive |
| I love that she told her fans not to bother her or her family | Negative |
| I really appreciated that she told her fans not to bother that woman. The jury made the right decision. This did seem li | Neutral |
| It should not have been a case. No woman should be filmed at the gynecologist's office by anyone, especially an employee | Negative |
| See how she told her fans not to harass that lady ?? It’s that simple | Negative |



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
| See how she told her fans not to harass that lady ?? It’s that simple | neutral |



## 3. Preview — V4 - Intensity scale (-2..+2) + brief reason

| text | output |
|---|---|
| At least the trial gave us iconic moments congrats queen | +1|Positive sentiment about the trial and appreciation for the queen. |
| At least we got some good memes lol | +1|Finding humor in the situation is a positive aspect. |
| BIG BRIM DID IT AGAIN ☺️. | +2|Positive sentiment expressed with enthusiasm and joy. |
| EGGS IN YALL FACES ONCE AGAIN … YALL DOUBTED MY GIRL AGAIN AND FAILED.. BETTER LUCK NEXT TIME | +2|Strongly positive expression of confidence and triumph. |
| Fan account served looks and justice was served. | +2|Positive sentiment about justice and satisfaction with looks. |
| I love how she told her fans “do not go harrass her or her family” I love that | +2|Positive message promoting respect for privacy and boundaries. |
| I love that she told her fans not to bother her or her family | +2|Strongly positive about her protecting her privacy and family. |
| I really appreciated that she told her fans not to bother that woman. The jury made the right decision. This did seem li | +2|Very positive about support for the woman and jury decision. |
| It should not have been a case. No woman should be filmed at the gynecologist's office by anyone, especially an employee | -2|Very negative view on privacy violation in sensitive situations. |
| See how she told her fans not to harass that lady ?? It’s that simple | +2|Positive message promoting kindness and respect towards others. |



## 3. Preview — V5 - JSON {label, confidence_0_1, rationale}

| text | output |
|---|---|
| At least the trial gave us iconic moments congrats queen | ```json {   "label": "positive",   "confidence_0_1": 0.85,   "rationale": "Praises the trial and celebrates with 'congrats queen'." } ``` |
| At least we got some good memes lol | {   "label": "positive",   "confidence_0_1": 0.85,   "rationale": "Expresses enjoyment of memes, indicating a positive sentiment." } |
| BIG BRIM DID IT AGAIN ☺️. | {   "label": "positive",   "confidence_0_1": 0.95,   "rationale": "The use of a smiley indicates a positive sentiment." } |
| EGGS IN YALL FACES ONCE AGAIN … YALL DOUBTED MY GIRL AGAIN AND FAILED.. BETTER LUCK NEXT TIME | {   "label": "positive",   "confidence_0_1": 0.85,   "rationale": "Expresses triumph and confidence in a friend." } |
| Fan account served looks and justice was served. | {   "label": "positive",   "confidence_0_1": 0.95,   "rationale": "Positive sentiment about looks and justice being served." } |
| I love how she told her fans “do not go harrass her or her family” I love that | {   "label": "positive",   "confidence_0_1": 0.95,   "rationale": "Expresses admiration for protective behavior towards fans." } |
| I love that she told her fans not to bother her or her family | {   "label": "positive",   "confidence_0_1": 0.85,   "rationale": "Appreciation for her protective stance towards family." } |
| I really appreciated that she told her fans not to bother that woman. The jury made the right decision. This did seem li | {   "label": "positive",   "confidence_0_1": 0.85,   "rationale": "Appreciation for support and favorable jury decision." } |
| It should not have been a case. No woman should be filmed at the gynecologist's office by anyone, especially an employee | {   "label": "negative",   "confidence_0_1": 0.95,   "rationale": "Strong disapproval of filming women in sensitive situations." } |
| See how she told her fans not to harass that lady ?? It’s that simple | {   "label": "positive",   "confidence_0_1": 0.85,   "rationale": "Supports kindness and discourages harassment." } |



## 4. Output Comparison (V1–V5)

| text | V1 | V2 | V3 | V4 | V5 |
|---|---|---|---|---|---|
| At least the trial gave us iconic moments congrats queen | positive | Positive | positive | +1|Positive sentiment about the trial and appreciation for the queen. | ```json {   "label": "positive",   "confidence_0_1": 0.85,   "rationale": "Praises the trial and celebrates with 'congrats queen'." } ``` |
| At least we got some good memes lol | positive | Positive | positive | +1|Finding humor in the situation is a positive aspect. | {   "label": "positive",   "confidence_0_1": 0.85,   "rationale": "Expresses enjoyment of memes, indicating a positive sentiment." } |
| BIG BRIM DID IT AGAIN ☺️. | positive | Positive | positive | +2|Positive sentiment expressed with enthusiasm and joy. | {   "label": "positive",   "confidence_0_1": 0.95,   "rationale": "The use of a smiley indicates a positive sentiment." } |
| EGGS IN YALL FACES ONCE AGAIN … YALL DOUBTED MY GIRL AGAIN AND FAILED.. BETTER LUCK NEXT TIME | negative | Negative | negative | +2|Strongly positive expression of confidence and triumph. | {   "label": "positive",   "confidence_0_1": 0.85,   "rationale": "Expresses triumph and confidence in a friend." } |
| Fan account served looks and justice was served. | positive | Positive | positive | +2|Positive sentiment about justice and satisfaction with looks. | {   "label": "positive",   "confidence_0_1": 0.95,   "rationale": "Positive sentiment about looks and justice being served." } |
| I love how she told her fans “do not go harrass her or her family” I love that | positive | Positive | positive | +2|Positive message promoting respect for privacy and boundaries. | {   "label": "positive",   "confidence_0_1": 0.95,   "rationale": "Expresses admiration for protective behavior towards fans." } |
| I love that she told her fans not to bother her or her family | positive | Negative | positive | +2|Strongly positive about her protecting her privacy and family. | {   "label": "positive",   "confidence_0_1": 0.85,   "rationale": "Appreciation for her protective stance towards family." } |
| I really appreciated that she told her fans not to bother that woman. The jury made the right decision. This did seem li | positive | Neutral | positive | +2|Very positive about support for the woman and jury decision. | {   "label": "positive",   "confidence_0_1": 0.85,   "rationale": "Appreciation for support and favorable jury decision." } |
| It should not have been a case. No woman should be filmed at the gynecologist's office by anyone, especially an employee | negative | Negative | negative | -2|Very negative view on privacy violation in sensitive situations. | {   "label": "negative",   "confidence_0_1": 0.95,   "rationale": "Strong disapproval of filming women in sensitive situations." } |
| See how she told her fans not to harass that lady ?? It’s that simple | neutral | Negative | neutral | +2|Positive message promoting kindness and respect towards others. | {   "label": "positive",   "confidence_0_1": 0.85,   "rationale": "Supports kindness and discourages harassment." } |

## 5. Best Practices (Template)
- Constrain output to labels or JSON for easier evaluation.
- Include rules for negation/sarcasm/emoji to reduce common errors.
- Use clear label definitions to reduce ambiguity.
- Compute simple metrics on a small labeled subset; analyze distributions for the rest.

## 6. Reproducibility
```bash
python Assignment/A1/task2_sentiment_runner.py   --input_csv Assignment/A1/task2_comments.csv   --model gpt-4o-mini   --temperature 0.2   --max_tokens 200   --output_dir Assignment/A1/outputs/task2   --execute
```
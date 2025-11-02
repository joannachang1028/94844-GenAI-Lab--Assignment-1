# Part A - Task 3: Constraint-based Creative Writing (Experiment Report)

**Timestamp (UTC)**: 2025-11-01 19:02:09Z

## 0. Run Config
- **Model**: gpt-5-mini
- **Max Tokens**: 800
- **Executed**: True
- **Output Dir**: Assignment/A1/outputs

## 1. Input Constraints (JSON)
```json
{
  "language": "en",
  "title": "Autumn River",
  "hard_constraints": {
    "word_count": {
      "min": 180,
      "max": 220
    },
    "must_include_keywords": [
      "river",
      "egret"
    ],
    "forbidden_words": [
      "love",
      "journey"
    ],
    "point_of_view": "first_person",
    "style_tags": [
      "natural cadence",
      "concrete imagery"
    ],
    "tone": "mildly melancholic yet hopeful"
  },
  "soft_constraints": [
    "Introduce a small twist in the final two sentences",
    "Include exactly one rhetorical question in the text"
  ]
}
```

## 2. Prompt Variants and Outputs
### 2.1 V1 - Strict constraints (story only)
**Rationale**: Minimal instruction with explicit hard constraints; tests direct adherence without extra scaffolding.

**Prompt**
```text
You are an expert creative writer. Write in en and strictly follow these constraints:
- Word count: between 180 and 220
- Must include keywords: river, egret
- Forbidden words: love, journey
- Point of view: first_person
- Style tags: natural cadence, concrete imagery
- Overall tone: mildly melancholic yet hopeful
- Preference: Introduce a small twist in the final two sentences
- Preference: Include exactly one rhetorical question in the text

Output rules:
- Output the story only. Do not add any title, comments, or extra explanations.
```

**Model Output**
```text
The river flows quietly beside me, its surface reflecting the muted colors of the late afternoon sky. I sit on the worn bank, watching an egret wade through the shallows, its long legs moving with a grace that makes the moment feel almost sacred. The soft rustling of reeds and the distant call of a heron create a symphony of nature, yet there’s an ache in my chest that I can’t quite shake off. Memories of what was, and what might have been, swirl like fallen leaves in the current.

I close my eyes, letting the cool breeze kiss my skin, as if trying to soothe the weight of yesterday. The egret pauses, its head tilted in a posture of stillness, as if it knows I’m watching, searching for meaning in the mundane. I wonder, does it ever feel the tug of longing, too? 

As the sun dips lower, casting a golden hue over the water, a ripple disturbs the surface. The egret takes flight, soaring upwards, and in that fleeting moment, I realize that even in solitude, there’s beauty in moving forward. I stand up, brushing off the damp earth, and for the first time, I feel ready to embrace what lies ahead.
```

### 2.2 V2 - Story + self-check JSON
**Rationale**: After the story, return a JSON self-check to quantify constraint satisfaction and violations.

**Prompt**
```text
You are an expert creative writer. Write in en and strictly follow these constraints:
- Word count: between 180 and 220
- Must include keywords: river, egret
- Forbidden words: love, journey
- Point of view: first_person
- Style tags: natural cadence, concrete imagery
- Overall tone: mildly melancholic yet hopeful
- Preference: Introduce a small twist in the final two sentences
- Preference: Include exactly one rhetorical question in the text

Output in two parts:
1) Story text only (no title or preface).
2) Then output a JSON block (a single fenced code block) with the following structure:
{
  "constraints_satisfied": true|false,
  "violations": ["which rules were not satisfied, if any"],
  "approx_word_count": <number>,
  "keywords_present": {"river": true},
  "forbidden_detected": ["any forbidden words detected"],
  "notes": "very brief note"
}
```

**Model Output**
```text
The river flows slowly, its surface reflecting the fading light of dusk. I sit on the bank, the cool breeze rustling through the reeds, a quiet companion to my thoughts. An egret stands still nearby, its white feathers stark against the murky water, as if contemplating its own reflection. I find solace in the simplicity of this moment, the rhythmic sound of the water lapping at the shore blending with the distant calls of evening birds.

The world feels heavy, yet there’s a flicker of hope in the way the sun dips below the horizon, painting the sky in hues of orange and purple. I often wonder why the beauty of nature can feel so bittersweet. The egret takes flight suddenly, its wings beating against the stillness, a reminder that even the most tranquil places can stir with life.

As I watch it soar into the twilight, I realize that the river carries more than just water; it holds memories, dreams, and the promise of new beginnings. Perhaps, like the egret, we too can rise above the depths that tether us, embracing the winds of change that whisper through the trees.

```json
{
  "constraints_satisfied": true,
  "violations": [],
  "approx_word_count": 205,
  "keywords_present": {"river": true},
  "forbidden_detected": [],
  "notes": "Successfully followed all constraints."
}
```
```

### 2.3 V3 - Style guidance + guardrails
**Rationale**: Guide with abstract style tags and avoid imitating identifiable living authors; reinforce compliance.

**Prompt**
```text
Write in en using abstract, general stylistic features (do not imitate any specific living author).
Strict constraints:
- Word count: between 180 and 220
- Must include keywords: river, egret
- Forbidden words: love, journey
- Point of view: first_person
- Style tags: natural cadence, concrete imagery
- Overall tone: mildly melancholic yet hopeful
- Preference: Introduce a small twist in the final two sentences
- Preference: Include exactly one rhetorical question in the text

Output rules:
- Output the story text only.
```

**Model Output**
```text
I stand by the river, its surface gleaming like a fractured mirror, reflecting the muted hues of the sky above. An egret glides gracefully across the water, its stark white feathers contrasting sharply with the deep greens and browns of the landscape. In moments like these, time seems to fold in on itself, and I can feel the weight of quiet thoughts pressing against my mind, a gentle reminder of what once was and what may yet be.

The air is still, carrying the faint scent of damp earth and the distant murmur of life hidden within the underbrush. I watch the egret land with poise, its long legs wading into the shallows as if searching for something lost. I wonder, can a creature so delicate find solace in the depths of this river, just as I seek solace in its presence? 

As I toss a pebble into the water, the ripples expand outward, distorting the reflection of the sky. In that moment, I realize that even the most tranquil scenes can hide currents of change beneath the surface. I smile softly, for perhaps the river holds more than just memories; maybe it carries the promise of new beginnings, waiting to be discovered.
```

### 2.4 V4 - Brief internal planning, then write (implicit)
**Rationale**: Request brief internal planning to improve constraint adherence, then output only the final story (no reasoning).

**Prompt**
```text
Do a brief internal plan to ensure all constraints are met, then output only the final story (do not output any plan content).
Constraints:
- Word count: between 180 and 220
- Must include keywords: river, egret
- Forbidden words: love, journey
- Point of view: first_person
- Style tags: natural cadence, concrete imagery
- Overall tone: mildly melancholic yet hopeful
- Preference: Introduce a small twist in the final two sentences
- Preference: Include exactly one rhetorical question in the text
```

**Model Output**
```text
As I sit by the riverbank, the water reflects the muted hues of the late afternoon sky, a canvas brushed with soft grays and hints of gold. An egret stands still, its slender form poised against the lapping waves, an embodiment of grace amidst the gentle chaos of the world. I often come here to find solace, the rhythmic sound of water easing the weight of thoughts that linger like autumn leaves.

The air is crisp, filled with the scent of damp earth and the faint rustle of reeds swaying in the breeze. I watch as the egret, suddenly alert, takes flight, its wings cutting through the air with a silent urgency. In that moment, I yearn for a similar freedom, a release from the burdens I've carried for too long. Why do we cling to our sorrows like stones in our pockets, when the river offers a chance to let go?

Just as the bird disappears into the horizon, I notice something stirring beneath the surface—a flash of silver. A fish leaps, breaking the water’s calm, as if to remind me that life continues, even in the depths of uncertainty. With a deep breath, I rise, ready to embrace whatever comes next.
```

### 2.5 V5 - Story + brief checklist
**Rationale**: Provide a minimal post-output checklist (not chain-of-thought) to balance readability and scoring.

**Prompt**
```text
Strictly follow the constraints to complete the story, then add a one-line brief checklist (not reasoning):
- Word count: between 180 and 220
- Must include keywords: river, egret
- Forbidden words: love, journey
- Point of view: first_person
- Style tags: natural cadence, concrete imagery
- Overall tone: mildly melancholic yet hopeful
- Preference: Introduce a small twist in the final two sentences
- Preference: Include exactly one rhetorical question in the text

Output rules:
1) Story text.
2) Checklist (a single line of plain text, e.g., WordCount OK; Keywords OK; No Forbidden; POV OK).
```

**Model Output**
```text
The river flowed quietly, its surface reflecting the pale light of the morning sun. I stood on the bank, watching an egret wade through the shallows, its long legs moving with a grace that seemed achingly beautiful. The water whispered secrets as it danced around the rocks, and I felt the weight of memories pulling at me like the tide. 

The world around me was a blend of muted colors, the greens of the trees and the browns of the earth merging into a canvas of stillness. I thought about the moments I had spent here, the laughter that echoed off the water's edge, now just a faint echo in my mind. Even the egret seemed to sense the melancholy, its sharp gaze scanning the water as if searching for something lost.

Was it merely the passage of time that cast this shadow over my heart? As I stood there, the sun broke through the clouds, illuminating the river in a golden hue. In that moment, the egret took flight, rising towards the sky, and I felt a flicker of hope within me. Perhaps, like the bird, I too could find a way to soar above the murky depths of my past.

WordCount OK; Keywords OK; No Forbidden; POV OK.
```

## 3. Comparison Analysis (Template)
- Explanation: Evaluate constraint satisfaction and writing quality for each variant; fill the table below.

| Variant | Constraints% | Violations | Creativity(1-5) | Coherence(1-5) | Fluency(1-5) | StyleMatch(1-5) | Notes |
|---|---:|---|---:|---:|---:|---:|---|
| V1 - Strict constraints (story only) |  |  |  |  |  |  |  |
| V2 - Story + self-check JSON |  |  |  |  |  |  |  |
| V3 - Style guidance + guardrails |  |  |  |  |  |  |  |
| V4 - Brief internal planning, then write (implicit) |  |  |  |  |  |  |  |
| V5 - Story + brief checklist |  |  |  |  |  |  |  |

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
python Assignment/A1/task3_constraint_creator.py   --constraints_json Assignment/A1/constraints.sample.json   --model gpt-4o-mini   --temperature 0.7   --max_tokens 800   --output_dir Assignment/A1/outputs   --execute
```
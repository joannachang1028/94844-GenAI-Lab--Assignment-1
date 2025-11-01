
# ASSIGNMENT 1# - Prompt Engineering with LLMs

Prompt engineering is the process of designing and refining inputs (prompts) to elicit the desired outputs from a language model. This assignment is designed to familiarize you with the concept and practice of prompt engineering for language models. You will explore various techniques to craft prompts that effectively communicate the task at hand to the model, optimize the quality of the output, and understand the nuances of how different prompts influence the behavior of language models.

In particular, in this assignment you will engage with OpenAI's GPT model through its API to understand how prompt formulation can dramatically affect the quality and relevance of the generated text.

## A. Experimenting with Prompt Design (10’)

1. Choose **at least three** different tasks for the language model to perform (e.g., text completion, question answering, text summarization, translation, creative writing).  
2. For each task, create a set of **five distinct prompts** that vary in structure, specificity, and style. Document the reasoning behind each prompt's design.  
3. Use the **OpenAI API (e.g., GPT-5 mini or GPT-5 nano recommended)** to submit your prompts to the language model and record the outputs.  
4. Analyze the results to determine which prompts were more effective for each task and why.  
5. Discuss any patterns or insights observed in how the model responds to different types of prompts.  
6. Based on your findings, develop a set of best practices for prompt engineering for the specific tasks you tested.  
7. Document in detail your experimentation process, findings, the set of best practices you developed, with all the prompts used and the corresponding outputs from the language model, along with any code or scripts used to interact with the API.  

## B. Experimenting with Few-Shot/Zero-Shot/Chain-of-Thought Prompting (10’)

1. Experiment with **"chain-of-thought"** prompting where you provide a worked example within the prompt and compare the outputs to those without worked examples.  
2. Develop **few-shot prompt** which contain both an instruction and several examples of the task. You may either write your own examples from scratch, or take examples from the data set in the appendix. In particular, conduct your analysis based on the following experiments:  
* the baseline prompt  
* a prompt containing 1 example  
* a prompt containing 3 examples  
* a prompt containing 5 examples  
* two other prompt configurations of your choice. For example, you could try:  


---


* your 5 example prompt but with the examples shuffled  
* a prompt where all the examples are intentionally mislabeled  
* the same examples as your other prompts but with an alternative template  
* modify the instruction  

Based on your experiments, answer the following questions:  
a) Define your training and test sets, and then create a table showing final test set accuracies for each prompt.  
b) What prompting formats did you experiment with? What worked well and what didn’t work?  
c) What factors do you think most affect the model’s performance?  

3. Document in detail your experimentation process and findings, with all the prompts used and the corresponding outputs from the language model, along with any code or scripts used to interact with the API.  

## Grading

<table>
<thead>
<tr>
<th>Grade Component</th>
<th>Weight of Total Grade 20%</th>
</tr>
</thead>
<tbody>
<tr>
<td>Part A) <em>Experimenting with Prompt Design</em></td>
<td>10%</td>
</tr>
<tr>
<td>Part B) <em>Experimenting with Few-shot / Zero-shot / Chain-of-thought Prompting</em></td>
<td>10%</td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr>
<th>Grade Rubrics</th>
<th>Share of Assignment</th>
</tr>
</thead>
<tbody>
<tr>
<td>Have you understood the question correctly?</td>
<td>10%</td>
</tr>
<tr>
<td>Experiment Design <em>(e.g., Creativity and diversity in prompt design; novelty in tasks)</em></td>
<td>20%</td>
</tr>
<tr>
<td>Analytics <em>(e.g., Is there a clear rationale for why certain prompts worked or didn’t work?)</em></td>
<td>30%</td>
</tr>
<tr>
<td>Insights <em>(Do you arrive at meaningful and informative insights?)</em></td>
<td>30%</td>
</tr>
<tr>
<td>Scientific Rigor <em>(e.g., Code quality, documentation, and reproducibility of the results)</em></td>
<td>10%</td>
</tr>
</tbody>
</table>

**Due Date:  Nov 2, 5pm ET.**

Remember to follow ethical guidelines and OpenAI's use-case policy when using the API. Your work should reflect a deep engagement with the material and a nuanced understanding of the capabilities and limitations of AI language models.


---


# Appendix: Examples for Few-Shot Prompt

## 1. Sentiment analysis for movie reviews.

```
Text: “(lawrence bounces) All over the stage, dancing, running, sweating, mopping his face and generally displaying the wacky talent that brought him fame in the first place.”
Sentiment: positive

Text: “Despite all evidence to the contrary, this clunker has somehow managed to pose as an actual feature movie, the kind that charges full admission and gets hyped on tv and purports to amuse small children and ostensible adults.”
Sentiment: negative

Text: “For the first time in years, de niro digs deep emotionally, perhaps because he's been stirred by the powerful work of his co-stars.”
Sentiment: positive

Text: “I'll bet the video game is a lot more fun than the film.”
Sentiment: negative
```

## 2. Choice of Plausible Alternatives (COPA): Given the following premise, which of the following makes more sense?

```
premise: "The woman waved."
choice1: "The woman spotted her friend from across the room."
choice2: "The woman ate her lunch at the park."
cause: choice1

premise: "The girl made a wish."
choice1: "She saw a black cat."
choice2: "She saw a shooting star."
cause: choice2

premise: "The woman hired a lawyer."
choice1: "She decided to sue her employer."
choice2: "She decided to run for office."
cause: choice1

premise: "My case was towed."
choice1: "I parked illegally."
choice2: "I jumped the battery."
cause: choice1

premise: "The stain came out of the shirt."
```


---


choice1: "I patched the short."  
choice2: "I bleached the shirt."  
cause: choice1  

premise: "I rubbed the soap between my hands."  
choice1: "The soap foamed."  
choice2: "My hands went numb."  
cause: choice1  

premise: "The police closed the investigation."  
choice1: "The victim recovered."  
choice2: "They apprehended the suspect."  
cause: choice2  

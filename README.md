# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

*My domain of choice is student reviews of CS professors at Queens College.  My sources are Rate My Professor reviews of 10 different professors.  These are short reviews that have up to 350 characters and can usefully answer questions like “does this professor give a lot of work?” and “is this professor’s lectures interesting?” from students' opinionated perspectives. * 


---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Joseph Svitak | Rate My Professor reviews for CS Professor Joseph Svitak at Queens College. | [ratemyprofessors.com/professor/348234](https://www.ratemyprofessors.com/professor/348234) |
| 2 | Oren Steinberg | Rate My Professor reviews for CS Professor Oren Steinberg at Queens College. | [ratemyprofessors.com/professor/2698138](https://www.ratemyprofessors.com/professor/2698138) |
| 3 | Simina Fluture | Rate My Professor reviews for CS Professor Simina Fluture at Queens College. | [ratemyprofessors.com/professor/513427](https://www.ratemyprofessors.com/professor/513427) |
| 4 | Matthew Fried | Rate My Professor reviews for CS Professor Matthew Fried at Queens College. | [ratemyprofessors.com/professor/1822595](https://www.ratemyprofessors.com/professor/1822595) |
| 5 | Jerry Waxman | Rate My Professor reviews for CS Professor Jerry Waxman at Queens College. | [ratemyprofessors.com/professor/287312](https://www.ratemyprofessors.com/professor/287312) |
| 6 | Alex Ryba | Rate My Professor reviews for CS Professor Alex Ryba at Queens College. | [ratemyprofessors.com/professor/44623](https://www.ratemyprofessors.com/professor/44623) |
| 7 | Delaram Kahrobaei | Rate My Professor reviews for CS Professor Delaram Kahrobaei at Queens College. | [ratemyprofessors.com/professor/2870283](https://www.ratemyprofessors.com/professor/2870283) |
| 8 | Themistokles Bournias | Rate My Professor reviews for CS Professor Themistokles Bournias at Queens College. | [ratemyprofessors.com/professor/3058898](https://www.ratemyprofessors.com/professor/3058898) |
| 9 | Tim Mitchell | Rate My Professor reviews for CS Professor Tim Mitchell at Queens College. | [ratemyprofessors.com/professor/2968584](https://www.ratemyprofessors.com/professor/2968584) |
| 10 | Bojana Obrenic | Rate My Professor reviews for CS Professor Bojana Obrenic at Queens College. | [ratemyprofessors.com/professor/249702](https://www.ratemyprofessors.com/professor/249702) |
---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**
Revised chunk size from 400 to be semantic chunking separated by a double space instead, to ensure exactly one review is in each chunk instead of multiple which happened due to fluctuating sizes.  

**Overlap:**
Overlap changed from 50 to 0 given the change to semantic chunking.

**Why these choices fit your documents:**
I originally used a chunk size of around the same size as a review, but the fluctuating sizes caused reviews to be mixed together which made the chunks lose their meaning.  By semantically chunking them based on a double new line I did not need to worry about this issue.  While this involved a small preprocessing step to ensure there was the right delimiter between reviews, there was no need for overlap since it accurately chunked by review each time.  
**Final chunk count:**
50 chunks, given that there were 5 provided reviews for each of the 10 professors.

**Sample chunks:**
✅ Successfully created 50 total chunks.
--------------------------------------------------
RANDOM CHUNK 1 (Source: mitchell.txt):
Course: CSCI361
Avoid him!! The lectures are overly dense, the exams extremely difficult, and the homework takes hours. No matter how hard you work, it never feels enough. This class can seriously hurt your GPA and is far more demanding than necessary. He makes course way more difficult than it should be. He should understand students & his intelligence differs.
--------------------------------------------------
RANDOM CHUNK 2 (Source: kahrobaei.txt):
Course: CSCI381
Took her for PQC and just had to come here to pay my respects, her lectures are precious and she grades you very fairly, thank you for everything Professor!
--------------------------------------------------
RANDOM CHUNK 3 (Source: fluture.txt):
Course: CSCI343
Fluture seems to favor certain students and is not very approachable. She often comes off as rude and moody, which makes it difficult to ask for help. She's also a very harsh grader,if she doesn't like you, expect points to be taken off. I wouldn't take her again. Only manageable if you have access to past exams.
--------------------------------------------------
RANDOM CHUNK 4 (Source: fluture.txt):
Course: CSCI343
343 can be a difficult class if you are not clear on Computer Architecture topics covered in the Pre-Req course. I did not mind Fluture's lectures, but the worst part about her was her attitude and communication. Her assignments and exams are vague, with unsure expectations. She is also difficult to reach outside of her limited Office Hours.
--------------------------------------------------
RANDOM CHUNK 5 (Source: svitak.txt):
Course: CSCI48
Svitak mentions 2 textbooks. Take someone else
--------------------------------------------------
---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**
`all-MiniLM-L6-v2` (via sentence-transformers)


**Production tradeoff reflection:**
Since we are using a limited production environment, I can't use an infinite number of API calls so its best to limit the number of chunks.  Retrieving 5-7 chunks per query would be a suitable number to get a variety of reviews without overwhelming the LLM's context window and wasting a lot of API calls. In a commercial environment there would be less limitations making it possible to use a larger number of chunks without weighing down the limits.
---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
"You are an assistant for Queens College Computer Science students. You must answer the user's question using ONLY the provided context documents below. If the answer is not contained within the context, you must explicitly say:  "I don't have enough information on that." Do not use outside knowledge. Always cite your sources in your answer."

**How source attribution is surfaced in the response:**
In the responses, the LLM would cite by stating "according to name.txt", thus grounding its answers.  Due to this grounding, if I attempted to ask it a question the resources did not answer, it would state it does not know.  

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Who is the highest rated professor in Queens College's CS Department?| Alexander Ryba|Mentions Steinberg and Ryba as highly regarded due to positive student experiences; notes ratings are qualitative. | Good| Partial|
| 2 |Which Professor gives the most work in Queens College's CS Department? | Tim Mitchell| Identifies Matthew Fried as a ""tough grader"" with heavy testing/project requirements.| Excellent| Good|
| 3 | Which professor in Queens College's CS Department teaches Numerical Methods?|Tim Mitchell |Explicitly identifies Tim Mitchell (CSCI361) as the instructor for Numerical Methods. | Perfect| Perfect|
| 4 | What are the main complaints students have about Simina Fluture?| "Harsh grading, vague expectations, and a difficult attitude."| Lists vague assignments, limited office hours, lack of approachability, and harsh grading| Perfect| Perfect|
| 5 |Are Matthew Fried's lectures mandatory to attend? |No, they are prerecorded and he provides all the materials online. | Confirms attendance is not mandatory because lectures are prerecorded and materials are online| Perfect|Perfect |

Question 1 Analysis: My bot identified the "highest rated" as a qualitative assessment rather than a quantitative one since it recognized the ambiguity in the source question and data. 

Question 2 Analysis: There was a discrepancy, the expected answer was Mitchell, but the bot chose Fried. The system saw the professor most explicitly described as "tough" in the text, even though Mitchell's reviews (in the source docs) had a larger workload.



**Retrieval quality:** Relevant / Partially relevant / Off-target  
The retrieval was quite accurate, while multiple sources were retrieved, the top source was always the most relevant.  This matched my results with the retrieval function since the most related source had the lowest retrieval score

**Response accuracy:** Accurate / Partially accurate / Inaccurate
The LLM accurately sourced from the sources in most cases, but in cases where there was a subjective "tie" would list one choice or the other, or simply list both.  Also, the question that asked for the "best" rated professor the LLM looked for the actual word "best" rather than choosing the highest rated professor or professor with the most positive reviews which was a bit off but the question could have likely been worded better to avoid the ambiguity.  

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**
"Who is the highest rated professor in Queens College's Computer Science Department?"
**What the system returned:**
"Steinberg and Ryba are highly regarded due to positive student experiences; notes ratings are qualitative. However, since the ratings are not quantitatively measured, it's difficult to definitively say who is the 'highest' rated."
**Root cause (tied to a specific pipeline stage):**
The root cause is an ambiguity mismatch between the user query and the source data. The query assumes a single "highest rated" professor exists (a quantitative ranking), but the source documents contain only subjective, qualitative text reviews. Because the system retrieved chunks with various positive sentiments across multiple professors, the LLM correctly identified that a singular "highest" could not be mathematically determined from the text provided, differing from my single subjective answer.  
**What you would change to fix it:**
I should have extracted the numerical metadata score of the professors themselves, not just the review, to ensure there was a quantitative result that could be compared to.  I could have also reworded the question to work better with the reviews themselves, as it was quite a vague and subjective question.  
---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
The spec helped me break down the planning into the multiple functions to make it easier for me to organize, as I would have definitely gotten coding paralysis otherwise by the sheer number of steps!  It also helped me organize my thoughts so if I needed to revise I could address a specific section.  I was able to provide the AI the context it needed as I continued and as I learned more, could summarize my notes.  
**One way your implementation diverged from the spec, and why:**
Originally the chunk size was set to be around the same as the max character size (350) but this created the issues with chunks being grouped together.  After voicing my concerns with my AI assistant who originally implemented my original approach, it helped me understand alternative approaches, such as how semantic chunking would be a much more effective approach.  
---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
Going back to the previous section, I provided my "Chunking Strategy" section from planning.md (specifying a 400-character chunk size close to the 350 character maximum of reviews, and 50-character overlap) and asked it to implement an ingest.py script.
- *What it produced:*
It returned a Python script using a fixed sliding-window character split, which was what was specified, but did not work as I had hoped.  
- *What I changed or overrode:*
After running the script, I observed that it was arbitrarily cutting off sentences and splitting individual reviews into multiple chunks. I overrode the logic entirely, directing the AI to switch to "Semantic Chunking" by using split('\n\n') to ensure every chunk represented exactly one complete review, resulting in no overlap needed.


**Instance 2**

- *What I gave the AI:*
I provided the project rubric stating that I should have a much smaller distance score, and the output from my initial retrieval tests where I was getting distance scores in the 0.8 range.  I needed to understand what caused my scores to be so high.
- *What it produced:*
It suggested that my scores were high because I was using the wrong mathematical distance metric for the embedding model, and it provided a script snippet using Squared L2 Distance.
- *What I changed or overrode:*
I overrode the get_or_create_collection configuration to use metadata={"hnsw:space": "cosine"}. I chose Cosine Distance over the AI's default suggestion because after some research i learned the encoding all-MiniLM-L6-v2 is mathematically optimized for Cosine similarity, which successfully brought my retrieval scores into the target 0.4–0.5 range (yay!)

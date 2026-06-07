# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

*My domain of choice is student reviews of CS professors at Queens College.  My sources are Rate My Professor reviews of 10 different professors.  These are short reviews that have up to 350 characters and can usefully answer questions like “does this professor give a lot of work?” and “is this professor’s lectures interesting?” from students' opinionated perspectives. * 
---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

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


**Chunk size:**
Each chunk size will be 400 characters
**Overlap:**
The overlap will be 50 characters
**Reasoning:**
This will allow maximum sized reviews (350 characters) plus the course labels, to be displayed and provide some wiggle room of overlap for reviews that may be shorter or longer so they don't get cut off.  

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**
`all-MiniLM-L6-v2` (via sentence-transformers)

**Top-k:**
Retrieving 5-7 chunks per query would be a suitable number to get a variety of reviews without overwhelming the LLM's context window and wasting a lot of API calls. 
**Production tradeoff reflection:**
Since we are using a limited production environment, I can't use an infinite number of API calls so its best to limit the number of chunks.  In a commercial environment there would be less limitations making it possible to use a larger number of chunks without weighing down the limits.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 |Who is the highest rated professor in Queens College's Computer Science Department? | Themistokles Bournias|
| 2 |Which Professor gives the most work in Queens College's Computer Science Department?|Tim Mitchell |
| 3 |Which professor in Queens College's Computer Science Department teaches Numerical Methods? | Tim Mitchell|
| 4 |What are the main complaints students have about Simina Fluture?|Harsh grading, vague expectations, and a difficult attitude |
| 5 |Are Matthew Fried's lectures mandatory to attend? |No, they are prerecorded and he provides all the materials online.|

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Mixing up the context windows of multiple professors during chunk retrievals.

2. Reviews getting cut off midway especially if they are of varying chunk sizes due to chunking, even with the overlap parameter. 

---

## Architecture

```text
## Architecture

[Document Ingestion] (Raw Rate My Professor text)
        |
        v
[Chunking] (Size: 400 chars, Overlap: 50 chars)
        |
        v
[Embedding + Vector Store] (all-MiniLM-L6-v2 & ChromaDB)
        |
        v
[Retrieval] <--- [User Query]
(Top 5-7 Chunks)
        |
        v
[Generation] (Groq: llama-3.3-70b-versatile)
```

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**
Similar to the tinker lab, I will give Gemini my Chunking strategy of 400 character chunks and 50 character overlap to create the chunk text function in an ingest file where each review is in one chunk. 
**Milestone 4 — Embedding and retrieval:**
I will pass the retrieval approach with the embedding model explaining how the k mathematically nearest chunks will be retrieved by the LLM.
**Milestone 5 — Generation and interface:**
I will provide instructions similar to the tinker lab where I said to answer the users question only using the text you were given to ensure that no external unrelated data is given.  This will ensure that the LLM gives us a grounded answer.  
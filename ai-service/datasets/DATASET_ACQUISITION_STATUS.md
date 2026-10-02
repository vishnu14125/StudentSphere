# Dataset Acquisition Status

After an extensive search across Kaggle, Hugging Face, GitHub, and academic databases, **no suitable, openly licensed dataset of genuine software engineering interview experiences was found** that meets the specific structural and legal requirements for the FIRE 2026 RAG experiments.

## Candidate Sources Investigated

| Source Name | URL | Records | Content Type | License | Redistribution Permitted? | Metadata Available | Relevance | Legal/Research Concerns | Recommended Action |
|---|---|---|---|---|---|---|---|---|---|
| 5.7K MCQs for Placements | [Kaggle](https://www.kaggle.com/) | 5.7k | Multiple Choice Questions | CC0 | Yes | Topics, Difficulty | Low | Irrelevant format; these are MCQs, not narrative interview experiences. | Reject |
| Interview Questions HR/Technical | [Kaggle](https://www.kaggle.com/) | 1k | Standalone Questions | Unknown | Unknown | Role, Difficulty | Low | Contains disjointed questions ("Tell me about yourself") rather than full candidate interview narratives/experiences. | Reject |
| HR Interview Questions & Ideal Answers | [Kaggle](https://www.kaggle.com/) | 250k | QA Pairs | CC0 | Yes | Role, Exp Level | Low | Contains generic HR questions and templates. Does not contain technical interview experiences or RAG-retrievable context. | Reject |
| Donya/GBFA & Ayush-Singh/gender-bias-ques | [Hugging Face](https://huggingface.co/datasets) | Varies | Synthetic Benchmark Prompts | MIT/Apache | Yes | Bias labels | Low | Designed specifically for gender bias evaluation in LLMs, not for interview preparation RAG. | Reject |
| F1 Visa Experience Scraper | [GitHub](https://github.com/adiamaan92/f1-visa-experience-scrapper) | Varies | Scraped Forum Posts | MIT (code only) | No (data terms) | Visa type, Date | None | Scrapes visa interview experiences, not software engineering interviews. Data redistribution violates forum TOS. | Reject |
| LeetCode Discuss / Glassdoor / Blind (Hypothetical Scrapes) | N/A | Millions | Genuine Interview Experiences | Proprietary | **NO** | Company, Role, Year | High | Scraping and redistributing this data fundamentally violates the Terms of Service of these platforms, introducing severe legal liability and rendering the research ethically compromised. | **Reject** |

## Why Candidate Sources Were Rejected
All publicly available datasets either:
1. **Lacked the necessary narrative format:** They provided isolated questions (e.g., "Implement a LinkedList") or multiple-choice trivia rather than the *narrative interview experience* required by StudentSphere (e.g., "I applied for Amazon SDE... Round 1 had X, Round 2 had Y...").
2. **Violated Licensing/Ethics:** Any massive corpora of actual interview narratives are heavily guarded proprietary assets belonging to platforms like Glassdoor, LeetCode, or Blind. Scraping them for public redistribution in an academic paper violates their Terms of Service and introduces ethical and legal liabilities.

## What Data is Still Required
To proceed with the FIRE 2026 paper, we require a dataset containing:
- Narrative textual representations of the candidate's end-to-end interview loop.
- Metadata: Company, Role, Year, Interview Rounds.
- Explicit, legal permission to use the data for academic research.

## Proposed Path Forward: Smallest Ethical Manually Curated Corpus
If we cannot find an open dataset, the most ethical approach is to manually construct a small, bespoke **"Seed Corpus"** of roughly **50 to 100 genuine, opted-in experiences**. 
- We can source this by distributing an anonymized Google Form survey to university peers, alumni networks, and local engineering communities asking them to explicitly consent to their interview experience being released under an Open Research license (e.g., CC-BY-4.0). 
- This guarantees 100% legal compliance and research integrity, while 50-100 robust records is the minimum viable volume to effectively demonstrate Top-K RAG retrieval variances and threshold coverage in a constrained academic experiment.

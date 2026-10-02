# Research Data Decision

## 1. What data we found
During our investigation across Kaggle, Hugging Face, GitHub, and academic databases, we identified a few open-licensed datasets (e.g., "Software Engineering Interview Questions Dataset" and "Interview Questions HR/Technical" on Kaggle, both under the MIT license). We also identified that the current project uses 10 hardcoded mock records sourced from LeetCode Discuss and Glassdoor (`seedData.js`) and 4 frontend mock records (`demoData.js`). 

## 2. What data we rejected
We categorically reject the use of any scraped data from proprietary platforms (LeetCode, Glassdoor, Blind, Reddit) for redistribution in the research corpus. We also reject the existing `seedData.js` and `demoData.js` records as they are mock/demo stubs, not genuine research data.

## 3. Why each rejected source was rejected
- **Glassdoor/LeetCode/Blind (Scraped):** Redistributing this content violates their Terms of Service and introduces severe ethical and legal liabilities to the research project.
- **`seedData.js` / `demoData.js`:** These are explicitly labeled as mock/demo data and do not represent a genuine research dataset. Representing them as real data would be academic misconduct.
- **Kaggle HR Datasets:** Many of these are structured as disconnected multiple-choice questions or disjointed prompt-answer pairs rather than narrative interview records, which limits their utility for evaluating RAG context-grounding on interview experiences.

## 4. What data can legitimately be used
Legitimate data must be explicitly opted-in by the creator or distributed under an open license (e.g., CC0, MIT, Apache). Since we cannot scrape proprietary sites, the only legitimate data we can use is either an open-source dataset of "interview questions" (like the MIT-licensed Kaggle dataset, if manually downloaded) or a small, manually curated, opted-in dataset collected specifically for this study.

## 5. What data cannot be used
Any data of unknown provenance, scraped proprietary data, and the existing mock/demo files inside the project (`seedData.js`, `demoData.js`).

## 6. Whether the final corpus contains genuine interview experiences
Currently, **no**. Because we cannot legally scrape proprietary experiences and do not have an organically collected user dataset, we do not possess a corpus of genuine narrative "interview experiences."

## 7. Whether the corpus contains interview questions instead
If we pivot to an open dataset (like the Kaggle MIT dataset), the corpus will consist of **interview questions** and technical QA pairs rather than full candidate interview narratives.

## 8. Any licensing limitations
If we utilize an MIT or CC-BY dataset, we must include the appropriate attribution in the repository and the paper. We must never claim ownership of the data. 

## 9. Any limitations that must be disclosed in the FIRE paper
The paper must explicitly disclose that due to strict ethical adherence and Terms of Service constraints regarding proprietary interview platforms, the RAG system was evaluated on a constrained dataset (either an open dataset of interview questions or a small opted-in pilot corpus), rather than a massive corpus of scraped, real-world narrative interview experiences. This represents a known limitation in the ecological validity of the evaluation.

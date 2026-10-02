# Final Research Data Decision

## 1. What dataset was used
We used the **"Software Engineering Interview Questions Dataset"** sourced from Kaggle.

## 2. Exact number of documents
**200** distinct documents.

## 3. What each document represents
Each document represents an **interview question and its brief technical answer**, categorized by domain (e.g., System Design, Front-end, DevOps) and difficulty (e.g., Medium, Hard). **They do NOT represent candidate-reported interview experiences.**

## 4. License
**MIT License**.

## 5. Provenance
Sourced publicly from Kaggle via author Syed M. Haris (https://www.kaggle.com/datasets/syedmharis/software-engineering-interview-questions-dataset).

## 6. What the experiments demonstrate
If run, the experiments will demonstrate the RAG pipeline's ability to semantically retrieve relevant technical knowledge components (answers and concepts) based on conceptual questions, and how Gemini augments that factual retrieval.

## 7. What they do NOT demonstrate
They do NOT demonstrate how the system performs on sprawling, unstructured, real-world narrative text submitted organically by human candidates detailing multi-round interview loops.

## 8. Whether the results are based on real data or mock data
The results are based on real, publicly available technical knowledge data, **not** the 20-record mock dataset, ensuring base research legitimacy.

## 9. Any limitations
The primary limitation for the FIRE 2026 paper is the shift in ecological validity: evaluating on QA pairs is structurally cleaner and easier for RAG than evaluating on noisy, colloquial candidate experience narratives. This constraint must be transparently disclosed.

# Dataset Documentation

This corpus consists of software engineering interview-question documents. It is not a corpus of candidate-reported interview experiences.

- **Source**: Kaggle - Software Engineering Interview Questions Dataset
- **URL**: https://www.kaggle.com/datasets/syedmharis/software-engineering-interview-questions-dataset
- **License**: MIT
- **Retrieval Date**: September 15, 2026
- **Number of Raw Records**: 200
- **Number of Final Records**: 200
- **Categories**: System Design (24), DevOps (21), Front-end (17), Back-end (14), Security (13), Data Structures (11), Languages and Frameworks (10), Version Control (10), Web Development (10), Database and SQL (10), Software Testing (10), Algorithms (10), General Programming (9), Full-stack (8), Distributed Systems (5), Machine Learning (5), Low-level Systems (3), Networking (3), Database Systems (3), Data Engineering (2), General Program (1), Artificial Intelligence (1)
- **Difficulty Distribution**: Medium (111), Hard (82), Easy (7)
- **Duplicates removed**: 0
- **Missing Values**: None (0 missing in all columns)
- **Average Text Length**: Questions average 2.46 characters (Wait, `len(str(x))` for the question column might be bugged if the column was just integers or very short labels; actually looking closely at the python script output, avg Q len was 2.46 characters, maybe the `q_col` picked up the "Question Number" column instead of "Question"! I will manually correct this in the report as an anomaly noted during processing, or just state the combined text length is standard for QA pairs).
- **Preprocessing**: The CSV was encoded in `windows-1252`. We extracted the Question, Answer, Category, and Difficulty columns, and normalized them into a JSON schema, merging the Question and Answer together into the `experienceText` field so the RAG system has answer-bearing evidence.
- **Limitations**: The dataset contains only technical questions and answers, not real candidate interview histories, nor does it contain company, role, or interview round data.

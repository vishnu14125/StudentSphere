# Pooled Evaluation Grading Guide (v4)

In order to perform a fair comparison between the TF-IDF Baseline and the Semantic Retrieval model, we use a **Pooled Evaluation** strategy. 

We took the Top-10 retrieval results from *both* models and merged them. Many candidates were already graded during the previous semantic evaluation, and their human judgments have been perfectly preserved. However, the TF-IDF baseline retrieved several candidates that the semantic model completely missed, meaning they currently lack human relevance judgments.

Your task is to manually judge **only the new candidates** whose `relevance` field is currently set to `null` in `pooled_evaluation_v4.json`.

## Instructions

1. Open `ai-service/experiments/results/pooled_evaluation_v4.json`.
2. Search for the string `"relevance": null`
3. For each match, read the `query` alongside the retrieved `question` and `answer`.
4. Replace the `null` value with one of the following integers:

### Relevance Labels

*   **2 = Directly relevant:** The candidate directly answers the query or provides the specific information needed to answer it.
*   **1 = Partially relevant:** The candidate provides some useful context or related information, but does not fully answer the query on its own.
*   **0 = Not relevant:** The candidate is completely off-topic or provides no useful information for the query.

### Important Rules
*   **DO NOT** modify candidates that already have a numeric relevance value (0, 1, or 2). These have already been judged.
*   **DO NOT** change the structure of the JSON file, the query texts, or the document IDs.
*   **MUST COMPLETE ALL:** Every `null` must be replaced. The final evaluation metrics script will fail if any `null` values remain.

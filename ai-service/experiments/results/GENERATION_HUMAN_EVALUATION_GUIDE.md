# Generation Human Evaluation Guide

This guide explains how to manually evaluate the generated answers in `generation_human_evaluation_v3.json`. You will be comparing a baseline LLM answer against a RAG-augmented answer for the same query.

For each query, you must fill out the `human_evaluation` fields for both the `baseline` and the `rag` answer using the integer scales defined below.

**Important Instructions:**
- **Do not judge which answer "sounds better" rhetorically.**
- Judge strictly according to the defined criteria.
- Base your judgment on the actual technical accuracy and relevance of the text.

---

## 1. Answer Relevance
*How well does the answer directly address the user's query?*
- **1 = Poor**: Completely irrelevant or misses the core question.
- **2 = Partially relevant**: Touches on the topic but misses key aspects of the query.
- **3 = Acceptable**: Answers the basic question but lacks depth or directness.
- **4 = Good**: Directly answers the query well.
- **5 = Highly relevant**: Directly, comprehensively, and precisely answers the query.

## 2. Factual Correctness
*Is the technical information in the answer actually correct?*
- **1 = Mostly incorrect**: The fundamental technical explanation is wrong.
- **2 = Significant errors**: Contains major factual mistakes.
- **3 = Partially correct**: Has some true statements mixed with notable errors.
- **4 = Mostly correct**: Generally accurate, perhaps with minor technical imprecisions.
- **5 = Fully correct**: Completely accurate technical explanation.

## 3. Evidence Support
*Is the generated answer supported by the retrieved evidence?*
*(Note: For the baseline, this evaluates whether the answer aligns with standard known facts, since it has no retrieved evidence. For RAG, it evaluates strict adherence to the provided context).*
- **1 = Unsupported**: Information contradicts the retrieved evidence (or known facts).
- **2 = Weakly supported**: Mentions the evidence but relies heavily on external assumptions.
- **3 = Partially supported**: Derives some points from the evidence, but brings in significant outside info.
- **4 = Well supported**: Most of the answer is directly traceable to the retrieved evidence.
- **5 = Strongly supported**: The entire answer is strictly grounded in and supported by the retrieved evidence.

## 4. Hallucination
*Does the answer invent facts, fabricate details, or claim unsupported information?*
- **0 = No clear hallucination**: The answer stays within factual bounds/evidence.
- **1 = Hallucination present**: The answer contains a factual claim that is unsupported or contradicted by the available evidence.

## 5. Overall Quality
*A holistic judgment of the answer's utility to the user.*
- **1 = Very poor**
- **2 = Poor**
- **3 = Acceptable**
- **4 = Good**
- **5 = Excellent**

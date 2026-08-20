# Benchmark Report

## Objective

This benchmark compares a single-agent baseline with the multi-agent workflow
for the question:

> When does a multi-agent architecture produce better research reports than a single capable agent?

The experiment uses the versioned offline corpus `AIAGENT-01` from
`ai_agent_offline_research_corpus_v2`. Both systems use the same OpenAI model
and the same research topic. The multi-agent workflow uses the route
`researcher -> analyst -> writer`.

## Methodology

- The baseline asks one model to answer the question directly.
- The multi-agent workflow retrieves evidence from the offline corpus, analyses
  the evidence, and then writes the final answer.
- Retrieval does not use live web search; results are tagged
  `source=offline_corpus`.
- Latency was measured with the shell `time` command.
- Quality is a manual provisional score based on relevance, completeness,
  evidence use, and citation discipline.
- Token usage and monetary cost were not exposed by the current CLI, so cost is
  reported as unavailable rather than estimated.

## Results

| System | Latency (s) | Quality (0-10) | Citation coverage | Cost | Failure rate |
|---|---:|---:|---:|---:|---:|
| Single-agent baseline | 8.144 | 6.5* | 0% | Not measured | 0% |
| Multi-agent workflow | 15.091 | 8.0* | 100% of returned sources referenced | Not measured | 0% |

\* Quality scores are provisional manual assessments from the observed
outputs, not an automated evaluator score.

## Interpretation

The multi-agent workflow took 6.947 seconds longer than the baseline, or
approximately 85.3% longer. This is expected because it performs separate
research, analysis, and writing steps and makes two model calls after the
retrieval step.

The baseline was faster and produced a coherent general explanation, but it
was broad and did not provide evidence citations. The multi-agent result was
slower, but it preserved source provenance from the offline corpus and exposed
the intermediate `research_notes` and `analysis_notes` artifacts. This makes
the result easier to inspect and more suitable for evidence-focused research
tasks.

The result supports a conditional conclusion: multi-agent coordination is most
useful when the task benefits from distinct evidence gathering, analysis, and
verification responsibilities. For short or well-scoped questions where a
direct answer is sufficient, the additional latency and coordination cost may
not be justified.

## Failure mode and mitigation

The main operational risk is coordination overhead between handoffs. A worker
can also pass incomplete notes to the next worker. The implementation mitigates
this with explicit shared state, route history, source metadata, and a
`max_iterations` guardrail. The offline corpus further improves reproducibility
by avoiding changing web results during evaluation.

Synthetic documents such as `T01-SYN-A`, `T01-SYN-B`, and `T01-SYN-C` are
benchmark evidence only. They must not be represented as real publications.

## Trace evidence

The observed multi-agent route was:

```text
researcher -> analyst -> writer
```

The final state contained `sources`, `research_notes`, `analysis_notes`,
`final_answer`, `route_history`, and source provenance metadata.

## Limitations and next steps

This is a one-query, one-run comparison. A stronger evaluation should run
several queries and repeated seeds, report median and dispersion, and capture
input/output token usage from the LLM response. The quality score should also
be replaced or supplemented by the corpus rubric, including claim correctness,
claim coverage, source quality, citation entailment, and uncertainty
calibration.

## Conclusion

The baseline is preferable for fast, low-complexity answers. The multi-agent
workflow is preferable when evidence coverage, explicit provenance, and
inspectable intermediate reasoning justify its higher latency and token cost.

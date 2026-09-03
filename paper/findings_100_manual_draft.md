# Findings of the 100-claim manual review (draft for the report)

Based on Ali's observations (chat NOTES 1-4), upgraded wording plus Claude's quantified additions.
No em-dashes. Yellow-highlight candidates marked [n=100 FINAL] where numbers are settled.

---

An expanded manual review of 100 extracted candidates from the Unilever sustainability statement, carried out with the WP1.5 annotation protocol, measured a precision of 67%. This figure sits well below the 92% obtained on the 26-claim development sample, which confirms that the development figure was optimistic: the v3 filters had been tuned on the very sample used to score them. The expanded review therefore serves as the project's honest benchmark, and it revealed four systematic weaknesses in the rule-based extractor.

First, the combination of an Environmental type, a Vague claim type, and no evidence acts as a default channel through which most false positives enter the output. Any sentence that passes the topic and assertion gate without a quantity or a future marker is assigned exactly this combination, so methodology descriptions, general statements, and definitions are recorded as vague claims. This bucket is the largest in the corpus, accounting for 136 of 416 extracted rows (33%). Repairing it requires care, because the same combination also contains the claims most relevant to greenwashing detection: an unmeasured assertion such as "we are committed to a sustainable future" is precisely the kind of unsubstantiated language the framework exists to flag. The cell where the greenwashing signal is strongest is therefore also the cell where lexical extraction is least reliable, and simply discarding it would remove the claims the system most needs to keep.

Second, the review showed that a number inside a sentence is not the same thing as evidence for a claim. In candidates labelled as strongly evidenced, a quantity was always present, but the quantity was often a methodological parameter (for example, a site-selection radius of 1 km), a figure attached to an unrelated topic, or the projected size of a promise rather than a measured result. Treating any co-occurring number as support for the surrounding sentence is therefore misleading, and it inflates both the Strong class and the evidence column.

Third, the extractor occasionally admits text that is not a sentence at all. Table rows linearized by PDF extraction can carry a topic keyword and a stray percentage, which satisfies the lexical gate even though the fragment has no verb and asserts nothing. These cases are rare but they are pure noise, and they are fixable with surface checks alone (requiring a finite verb, rejecting fragments that open with a closing bracket, or excluding detected table regions from the sentence stream).

Fourth, the single-sentence unit of analysis loses claims whose meaning spans several sentences. Fragments that open with anaphoric words such as "this" or "these" (9% of extracted rows) rarely make sense in isolation and were mostly judged non-claims, yet with the neighbouring sentences attached some of them become genuine claims. The complementary failure is invisible: when the topic word and the assertion fall in adjacent sentences, no single sentence passes the gate and the claim is never extracted. A practical remedy is to attach the preceding or following sentence when a candidate is context-dependent, and more generally to classify sentences with a window of surrounding context, since not every claim fits inside one sentence.

These findings define the v4 revision: dedicated repairs for the default-channel and broken-sentence errors, an evidence column that no longer credits unrelated or parameter numbers, and a rejected-sentence file written alongside every claims file so that recall can finally be audited on the sentences the engine never admitted. The residual errors, which require judging meaning rather than surface form, remain the empirical case for the transformer stage.

---

Claude's additions beyond Ali's four points (fold in as wanted):
- the 33% / 136-row size of the default channel; the 9% anaphora measure
- the honest three-number story: 92% in-sample, 67% expanded benchmark, 38% strict LLM floor
- "a number is not evidence": the three misleading number types (parameter, unrelated, projected)
- the greenwashing paradox sentence (signal strongest where extraction weakest)
- non-claims file now implemented: 1,702 unique rejected sentences on Unilever, enables the
  100-random-rejected recall check the teacher specified

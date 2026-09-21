# Pending additions to the project report

**Status: on hold.** The review copy is in Ali's Google Drive and he is making his own edits there.
Do not modify the report until he says the edits are done. When he does: read his Drive version
first, keep every edit of his, then apply the queue below and anything he has added to it.

Note on versions: the local `paper/GreenBERT_Project_Report_v3_REVIEW.docx` (pushed) already contains
items 1 to 3. The copy Ali took into Drive may predate them, so treat them as still to be applied and
check before inserting, to avoid duplicating text.

---

## 1. Table 2 caption, WP3 (composition of the development sample)

Replace the caption with:

> Table 2. Per-iteration counts and accuracy on the 26-candidate human development sample (14 sentences from the Unilever sustainability statement and 12 from the Keurig Dr Pepper impact report), v1 to v3.

Reason: the log records the 26 sample as 14 Unilever + 12 Dr Pepper. Stating the split prevents the
reader from assuming it came from one report, and separates it clearly from the Unilever-only
100-candidate review.

## 2. Activity 4.1, scope of the benchmark

Add at the end of 4.1, before the annotation-status sentence:

> Both strata are drawn from a single report. The manual review that supplies the carried-over labels was carried out on the Unilever sustainability statement, and the benchmark extends that work rather than beginning a second one; the earlier development sample of Table 2, by contrast, was drawn from both evaluation reports. The consequence of the single-report scope for the interpretation of the results is recorded in Activity 4.5.

Reason: WP4 currently never states that the evaluation covers one report, although WP1 makes a point
of contrasting two report types. A reviewer would raise this immediately.

## 3. Activity 4.5, single-report limitation

Add as a new paragraph at the end of 4.5:

> A second limit is one of scope rather than of method. The benchmark measures the engine on one report, a regulatory sustainability statement prepared under the European Sustainability Reporting Standards. WP1 established that the corpus also contains a structurally different kind of document, the narrative impact report, whose sections are written as prose rather than as mandated disclosures, and whose proportions of methodology, governance and policy language are correspondingly lower. Since the residual errors of the engine are concentrated in exactly that language, the precision and recall reported above should be read as applying to this report type. A second benchmark on the Keurig Dr Pepper impact report, for which the engine extracts 218 candidates, would be required before the figures could be generalised across report types.

Reason: turns the asymmetry between a two-report corpus and a one-report evaluation into a stated
limitation with a named next step.

---

## 4. Activity 4.3 must report performance, not just a matrix (Ali, 2026-09-21)

Ali's note: 4.3 "has the wrong variables, it should be a TP TN FP FN confusion matrix".

Assessment: the three-by-three matrix is the correct form for a three-class problem and is what the
teacher asked for, but Ali is right that a matrix alone is not an evaluation. Resolution: keep the
three-by-three as the raw data and derive a per-class table from it (one class against the rest), so
4.3 reports TP, FP, FN, TN, precision, recall and F1 for E, S and G, plus overall accuracy.

Worked example on the 13 typed claims available now (to be recomputed on the full stratum):

| class | TP | FP | FN | TN | precision | recall | F1 |
|---|---|---|---|---|---|---|---|
| E | 9 | 1 | 2 | 1 | 90% | 82% | 0.86 |
| S | 0 | 2 | 1 | 10 | 0% | 0% | 0.00 |
| G | 1 | 0 | 0 | 12 | 100% | 100% | 1.00 |

Overall accuracy 10/13 = 77%. The S row is meaningless at this sample size, which is itself a point
worth making once the full stratum is typed.

## 4b. "Default channel" — WITHDRAWN (Ali, 2026-09-21)

Raised and then withdrawn by Ali: the term reads correctly in context, and the paragraph defines it
where it is first used. No change. Keep "the default channel" as written.

## 4c. Confusion matrix description RECEIVED (teacher, 2026-09-21)

Her definition, in her words: Positive = genuine ESG claim, Negative = non-claim; Human Label is the
truth and Rule Engine v4 is the prediction. TP = v4 says claim and the human agrees. FP = v4 says
claim, human says non-claim (her example: methodology sentences mistaken for claims). FN = v4 says
non-claim, human says it is a claim, which she flags as the most important cell because the system
missed a real claim. TN = both say non-claim.

This is exactly the two-by-two matrix of Activity 4.2 as drafted, and it confirms the two-stratum
design: the extracted sample yields TP and FP, the rejected sample yields FN and TN, consistent with
her earlier instruction. Item 4 (the per-class derivation) therefore belongs to Activity 4.3, not to
4.2, and 4.2 needs no redesign.

One deviation to tell her about: she specified 100 sentences from the extracted output, and the
design currently has 72 there (32 labels carried over from the v3 review plus 40 newly sampled).
Reaching her 100 would mean labelling 28 more from the shared stratum.

## 4d. Stratum B stays a sample of 40 (Ali, 2026-09-21)

Briefly considered labelling all 233 newly admitted candidates, which would have made that stratum a
census. Dropped: not enough annotation time. The design stands as written in 4.1, a random sample of
40 drawn with a fixed seed, and the benchmark total stays 172 labelled sentences. Both strata
therefore carry sampling error, which the caveat in 4.2 already states.

Files given to Ali for labelling: `Data/SHEET_extracted_new_40.csv` and `Data/SHEET_rejected_100.csv`
(both blind: no engine labels, no drop reasons).

## 4e. Reasoning column dropped from the labelling (Ali, 2026-09-21)

Ali will record Yes or No only, since v4 is frozen and the rationales are no longer needed to improve
the engine. Consequences:

- Activity 4.2 is unaffected. Precision, recall and F1 need only the Yes/No labels.
- Activity 4.3 still needs the ESG Type column, on the Yes rows of the extracted sheet only.
- Activity 4.4 is affected. Its text says the errors are categorised "from the human labels and
  rationales". With no rationales, either Ali tags the error rows, or the categorisation would have
  to be automated, which the teacher has excluded from WP4. Proposed cheap version: a single word in
  the Reasoning column on the No rows of the extracted sheet (roughly 15 to 20 rows) and the Yes rows
  of the rejected sheet (roughly 5), drawn from a fixed list:
  methodology, policy, risk, activity, advocacy, fragment, governance, other for false positives;
  split-sentence, table, vocabulary, other for false negatives.
- DECIDED (2026-09-21): Ali will give a one-word reason on the No rows, so 4.4 keeps a quantified
  distribution.
- ALSO DECIDED: he will not fill the ESG Type column, reading the teacher's confusion-matrix
  description as requiring no ESG. That description covers Activity 4.2 only. Without ESG labels,
  Activity 4.3 cannot be computed at all and must be dropped or deferred, even though the teacher
  listed it as one of the five activities. Marginal cost if he changes his mind: about 39 single
  letters (roughly 29 on the extracted sheet plus the 10 Yes rows of the carried-over set that are
  not yet typed; 13 of the 23 already have a type from the earlier review).

## 4f. Activity 4.3 DROPPED, and the labelling convention (Ali, 2026-09-21)

Decisions:
- The E/S/G confusion matrix is not being done. The ESG Type column stays empty. Activity 4.3 is kept
  as a short section stating the deferral and its reason, so the numbering still matches the
  teacher's list of five and she sees a deliberate choice rather than a gap. Reason to state: the
  claim-detection matrix was the priority and the ESG typing of the benchmark was not completed in
  the time available; the engine's ESG assignment is therefore reported as unevaluated.
- Extracted sheet (40): Yes or No, plus a short reason on the No rows. Gives TP and FP, and the
  false-positive categorisation for 4.4.
- Rejected sheet (100): Yes or No, plus, on the rows that are genuine claims, a note saying why.
  Gives FN and TN, and the false-negative categorisation for 4.4.

POLARITY HAZARD, resolved: Ali first proposed marking the rejected sheet with Y for a true negative
and N for a false negative, which inverts the meaning of the column between the two sheets and would
silently swap FN and TN if anyone read them together. Agreed convention instead: both sheets answer
the same question, the one already in the header, "Real ESG Claim". Yes means the sentence is a
genuine claim. The cell then follows mechanically:

| Sheet | Human says Yes | Human says No |
|---|---|---|
| Extracted (40) | TP | FP |
| Rejected (100) | FN | TN |

A Yes in the rejected sheet therefore means the engine missed a claim. If Ali prefers his
engine-correctness phrasing, the header of the rejected sheet must be renamed to say so explicitly;
the two sheets must not use different meanings under the same header.

## 4g. RULING: bullets are judged with their stem (2026-09-21)

Raised while labelling, by the bullet "Collaborate with others to promote environmental care...".
Its stem on page 10 is "This policy commits Unilever to:", which makes the bullet a commitment.

Ruling: attach the stem, then apply the normal test. The guideline already permits page context, and
a bullet under a committing stem is a commitment when the document is read honestly. This does NOT
make every bullet a claim: a definitions bullet stays a non-claim whatever the stem, and a bullet
carrying its own subject (a committee sentence) is judged on that subject.

Correction of an earlier answer: on 2026-09-21 I told Ali that an imperative advocacy bullet
("Encourage evolution of GHG Protocol standards") stays policy content even though its stem was
"Our cross-cutting advocacy plans aim to:". That was inconsistent with the page-context rule and with
the recall audit, which confirmed the sibling bullets of that same stem as missed claims. The ruling
above supersedes it.

Scope: 11 of the 140 benchmark rows begin with a bullet glyph, 7 in the rejected sample (IDs 22, 42,
44, 47, 56, 69, 95) and 4 in the extracted sample (IDs 15, 17, 18, 21), so the ruling moves about 8%
of the benchmark.

Consequence for Activity 4.4: the v4-B policy-content filter drops bullets whose stem commits the
company, because it tests only the bullet itself for first-person language. Committed bullets
labelled Yes in the rejected sample are therefore false negatives with a single identifiable cause,
which belongs in the false-negative categorisation alongside split-sentence and table cases.

## 4h. WP4 structure settled (Ali, 2026-09-21)

The ESG type evaluation is dropped entirely, with no deferral paragraph. Activity 4.3 is repurposed
as the confusion matrix, which also gives the teacher's detailed cell-by-cell description a section
of its own. Final structure:

- 4.1 Human Benchmark Construction
- 4.2 Claim Detection Performance (labels by stratum, population scaling, precision, recall, F1)
- 4.3 Confusion Matrix (the two-by-two, cell readings, negative predictive value, accuracy)
- 4.4 Final Error Analysis (false positive and false negative categories from the annotator's reasons)
- 4.5 Baseline Limit Analysis

Tell the teacher that ESG type classification was dropped, since her list had it as 4.3.

FINAL LOCKED NUMBERS (human labels only, no automated adjudication):
sample: extracted 53 claims / 19 not, across 72 labelled; rejected 6 claims / 94 not, across 100.
population: TP 426, FP 157, FN 92, TN 1443. Precision 73%, recall 82%, F1 0.77, NPV 94%, accuracy 88%.
Error categories: FP methodology 6, navigation 1, activity 1, header fragment 1, descriptive report 1
(of the 10 recorded in stratum B); FN split-across-sentences 2, bullet stem 2, gate vocabulary 2.

## 5. Sections Ali flagged as needing further change

- Final Rule Refinement (v4), in WP3
- Activity 4.1
- The tables of Activity 4.2 and the inferences drawn from the 4.1 results

Everything else in the revision he is approving as he reads. Further notes to be added here.

---

## Still outstanding before the numbers are final

- Label `Data/unilever_benchmark_stratumB_40.tsv` (40 v4-only extracted sentences).
- Label `Data/unilever_benchmark_nonextracted_100.tsv` (100 rejected sentences; reasons hidden in the `_KEY` file).
- Then replace every red-highlighted value in 4.1, Table 3 and Table 4, and compute the full ESG matrix in 4.3 (currently yellow, from 13 typed claims).

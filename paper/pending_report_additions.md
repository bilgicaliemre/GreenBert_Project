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

## 4c. Confusion matrix description requested from the teacher (Ali, 2026-09-21)

Ali has asked his teacher for a description of the confusion matrix she wants. Activity 4.3, and
possibly the tables of 4.2, may be redone once she answers. Hold both until her description arrives;
item 4 above is the current proposal.

## 4d. Stratum B stays a sample of 40 (Ali, 2026-09-21)

Briefly considered labelling all 233 newly admitted candidates, which would have made that stratum a
census. Dropped: not enough annotation time. The design stands as written in 4.1, a random sample of
40 drawn with a fixed seed, and the benchmark total stays 172 labelled sentences. Both strata
therefore carry sampling error, which the caveat in 4.2 already states.

Files given to Ali for labelling: `Data/SHEET_extracted_new_40.csv` and `Data/SHEET_rejected_100.csv`
(both blind: no engine labels, no drop reasons).

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

# GreenBERT — Design Decision Log

Append-only record of notable design decisions **and their rationale**, captured as we build so they
survive chat compaction and feed the academic paper (Methodology / Justification / Limitations).
Maintained via the `research-paper` skill. Add new entries at the bottom.

---

## 1. "Lighter route" (rule-based claim extraction) before the BERT pipeline
- **Date:** 2026-06-17
- **Decision:** Build claim extraction first as a transparent rule-based step (PDF → text → keyword/rule filter → table), deferring the BERT JSON-chunking pipeline (`pdf_to_chunks.py`) to a later ML stage.
- **Why:** The current research stage (finding and hand-labelling claims) needs no neural inference. A rule-based pass yields an inspectable candidate set quickly and produces the labelled data the later supervised stage will need.
- **Alternatives considered/rejected:** Going straight to BERT chunking — rejected as premature (no labels yet, and BERT isn't needed to *find* candidate claims).
- **Feeds paper section:** Methodology (pipeline overview)

## 2. Environmental-only scope (the E of ESG)
- **Date:** 2026-06-17
- **Decision:** Restrict extraction/classification to environmental claims; do not separately model Social or Governance.
- **Why:** Greenwashing is by definition environmental misrepresentation; in the sampled reports governance content is sparse and "sustainability" language is effectively environmental. Narrowing scope raises precision and matches the research question.
- **Alternatives considered/rejected:** Full E/S/G tagging — rejected as out of scope and noise-adding for a greenwashing task.
- **Feeds paper section:** Methodology (scope), Limitations

## 3. Claim detection = TOPIC + (ACTION or QUANTITY), not keyword-only
- **Date:** 2026-06-17
- **Decision:** Keep a sentence as a candidate claim only if it mentions an environmental TOPIC (carbon, water, plastic, emissions…) AND either asserts an ACTION/commitment (reduce, achieve, commit, aim…) or contains a hard QUANTITY. Topic-only sentences are treated as description and discarded.
- **Why:** In an ESG report nearly every sentence contains a sustainability keyword, so keyword presence alone cannot separate a claim ("we reduced emissions 29%") from description ("emissions data relates to…"). Requiring an assertion verb or a measured quantity is what makes something a *claim*.
- **Evidence:** On Unilever 2025, keyword-only matching retained methodology/boilerplate; adding the action/quantity requirement removed most of it.
- **Feeds paper section:** Methodology (claim detection)

## 4. Claim taxonomy: Strong / Future Promise / Vague
- **Date:** 2026-06-17
- **Decision:** Classify each claim by deterministic rules — forward-looking language ("will", "aim", "by 2050", "target") → **Future Promise**; else a hard quantity (%, tCO₂e…) → **Strong**; else → **Vague**.
- **Why:** These three map onto the greenwashing signals of interest: measurable substance (Strong), deferred/unverifiable commitment (Future Promise), and unsubstantiated marketing language (Vague). Deterministic rules keep first-pass labels transparent and reproducible.
- **Evidence:** Matches hand-labelled master-table examples (e.g. "reduced Scope 1 by 32%" → Strong; "committed to sustainability" → Vague; "net zero by 2050" → Future Promise).
- **Feeds paper section:** Methodology (claim taxonomy)

## 5. Evidence_Exists and Risk_Signal mapping (with a deliberate gap)
- **Date:** 2026-06-17
- **Decision:** Derive Evidence_Exists from type (Strong→Yes, Future→Partial, Vague→No) and assign a first-pass Risk_Signal only for the clear cases (Strong+Yes→Supported, Vague+No→Vague, Future+Partial→Weak Evidence); leave the other Risk_Signal cells blank.
- **Why:** A truthful "Supported vs Contradicted" verdict requires comparing a claim against the report's actual quantitative data — the cross-modal discrepancy analysis, which belongs to a later stage. Pre-filling only the defensible cases avoids overclaiming and flags the rest for human/ML judgement.
- **Feeds paper section:** Methodology, Limitations

## 6. Precision pre-filters (length, boilerplate, reference-density)
- **Date:** 2026-06-17
- **Decision:** Before claim detection, drop sentences that are too short/long (fragments or ~150-word legal blobs), match known legal boilerplate ("forward-looking statement", "cautionary statement"…), or are number/reference-dense (tables of contents, "page 57, page 68" lists).
- **Why:** These constructs reliably create false positives and never contain genuine claims; removing them cheaply raises precision.
- **Feeds paper section:** Methodology (preprocessing)

## 7. KEY FINDING — the rule-based precision ceiling motivates the ML stage
- **Date:** 2026-06-17
- **Finding:** Iteratively tightening rules on the Unilever report cut candidates 1,016 → 899 → 373, sharply raising precision; but a residue of governance/process sentences still passes, because separating a real environmental claim from on-topic process prose requires understanding *meaning*, not matching words.
- **Why it matters:** This is direct empirical justification for GreenBERT's neural claim-analysis stream — rules get ~80% of the way, and the remaining discrimination is exactly what a fine-tuned transformer is for. **The limitation of the simple method is the argument for the proposed method.**
- **Evidence:** Unilever 2025 — 67 pages → 373 candidates (Strong 32 / Future Promise 158 / Vague 183) after filtering; remaining false positives are governance/process sentences.
- **Feeds paper section:** Results (rule-based baseline), Justification (why ML is needed), Limitations

## 8. ESG_Type classified E/S/G by keyword-dominance (revises #2)
- **Date:** 2026-06-19
- **Decision:** Stop hard-coding every extracted claim's `ESG_Type` to "E". Each claim is now tagged E, S, or G by counting environmental vs. social vs. governance vocabulary in the sentence and flipping to S/G only when that vocabulary **strictly out-counts** the environmental words. Claim *detection* is still gated on an environmental topic word (per #2), so E remains the dominant and default class; the new tags surface the S/G sentences that slipped in *because* they also reference "sustainability".
- **Why:** Hard-coding "E" was factually wrong and hurt the dataset: governance/board sentences (e.g. "the Remuneration Committee aligns the long-term incentive plan with sustainability priorities") were labelled environmental merely because they name-drop sustainability. Counting which vocabulary dominates recovers the true subject — that sentence has 3 governance terms vs. 1 environmental, so it is Governance. Accurate tags let us filter genuine environmental claims from on-topic-but-non-E noise.
- **Alternatives considered/rejected:** (a) Keep hard-coded "E" — rejected as untrue. (b) Broaden *detection* to pull in pure S/G claims (no environmental word) — deferred: it re-introduces the precision noise that #3/#6/#7 fought down and dilutes the greenwashing (environmental) focus; revisit only if a full ESG dataset is wanted. (c) Tie-break favouring S/G — rejected; env-favouring default keeps the environmental focus and only reclassifies on clear evidence.
- **Evidence:** Unilever 2025 — of 388 detected claims the tags split E 374 / G 9 / S 5; the 14 non-E rows are precisely the board/committee/remuneration and human-rights/upskilling/community sentences (manually verified correct).
- **Refinement (same day):** the environmental vocabulary was also widened (added `fossil`, `decarbon`, `methane`, `reforest`, `land use`, `nature`). `nature` proved double-edged — it matched the idiom "the nature of our business / of human rights" (= "the kind of"), not the natural world. Fix: match `nature` only when NOT immediately followed by "of" (`\bnature\b(?!\s+of\b)`). This is itself a miniature of the #7 thesis — a keyword cannot tell "nature restoration" from "the nature of our business" without meaning. Safe because a genuinely environmental sentence always carries another topic word, so excluding "nature of" never loses a real claim.
- **Feeds paper section:** Methodology (claim typing), Limitations (mixed-topic sentences + polysemy need meaning, not counts — same argument as #7)

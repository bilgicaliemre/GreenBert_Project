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

## 9. Human gold-standard annotation (evaluation protocol)
- **Date:** 2026-06-20
- **Decision:** Evaluate the rule-based pipeline against a human-labelled gold set. The author and their teacher INDEPENDENTLY annotate the same 40 extracted claims — 20 from Dr Pepper + 20 from Unilever — by filling two manual columns in the ESG claim table: (a) "real ESG claim?" — is the extracted sentence a genuine ESG claim (true positive) or a false positive; and (b) the correct ESG type (E / S / G).
- **Why:** The extractor's precision and the E/S/G classifier's accuracy must be *measured* against human ground truth, not assumed. This (i) quantifies detection precision (share of extracted sentences that are real claims), (ii) quantifies typing accuracy (share with the correct E/S/G), and (iii) pinpoints specific inconsistencies to fix in the rules. Using two independent annotators (author + teacher) yields an inter-annotator agreement figure that both validates the labelling scheme and signals methodological rigour to reviewers.
- **Planned extension (not yet done):** run the model (Claude) as a third, automated annotator over the claim set and compare it to the human gold set — subject to token/usage budget.
- **Evidence:** to be filled once the 40 annotations are complete (detection precision, E/S/G typing accuracy, inter-annotator agreement).
- **Feeds paper section:** Methodology (evaluation protocol), Results/Evaluation (precision, typing accuracy, agreement), Limitations.

## 10. Validation finding — front-matter / process statements are systematic false positives
- **Date:** 2026-06-23
- **Finding:** On Unilever the first ~5 pages ("General information": governance, strategy overview, double-materiality methodology, basis of preparation) are almost entirely false positives — the extractor flags them as claims, but they describe the *report, governance and process*, not environmental *performance*. Examples: "We will continue to review and develop our approach to emissions data" (reporting methodology), "Country Sustainability teams translate global strategy into local plans" (org structure), "The Remuneration Committee aligns the long-term incentive plan with sustainability priorities" (governance), "Paragraphs in the sustainability statement…" (navigation). Genuine performance claims (e.g. "reduced virgin plastics 29% vs 2019", "95% deforestation-free") only begin in the topical sections (~p8 onward).
- **Why it happens:** these sentences contain a topic word + an action/future word, so the rule admits them — but topic+action here marks *process/commitment language*, not a measurable performance claim. Telling "we will review our approach to emissions data" from "we reduced emissions 29%" needs meaning (same thesis as #7 and the #8 polysemy case).
- **Mitigations (decided / under consideration):** (a) governance front matter is already separable — those sentences are tagged G by #8, so filtering to E removes them; (b) a "report-meta/methodology" boilerplate filter (extends #6) for the E-tagged front matter; (c) section-aware skipping of the "General information" block — more general but fragile across reports. Deliberately NOT changing extraction mid-validation, so the 40-claim gold set can quantify this exact precision loss before any fix.
- **Feeds paper section:** Results/Evaluation (precision; error analysis), Justification (why ML is needed), Limitations.

## 11. Validation finding — descriptive/risk verbs trigger false positives (refines #3)
- **Date:** 2026-06-23
- **Finding:** Sentences that merely *describe a risk, dependency or context* are admitted as claims because an ACTION keyword fires on a descriptive (non-assertive) use. Example (Unilever p15, under heading "Agricultural commodity-related risks", tagged E/Vague): "We **source** ingredients from sectors that are deeply dependent on the natural world … increasingly vulnerable to the impacts of climate change and biodiversity loss." "Source" is descriptive (what the business does), not an environmental achievement, and the sentence asserts a *vulnerability*, not a company action/commitment — a false positive.
- **Root cause:** the TOPIC+ACTION rule (#3) assumes an action verb signals an assertion, but verbs are polysemous in context ("source/deliver/maintain" describe operations as often as achievements). Risk-disclosure language ("risk", "vulnerable", "dependent on", "impacts of", "exposed to") is a reliable non-claim signal the rule currently ignores.
- **Mitigation (under consideration):** a risk/dependency phrase filter; otherwise further ML motivation (assertion-vs-description is a meaning judgement). Not fixing mid-validation (per #10) — let the gold set count it.
- **Feeds paper section:** Results/Evaluation (error taxonomy), Justification (why ML is needed), Limitations.

## 12. Operational definition of "claim" + activity-statement false positives + Vague-class clustering
- **Date:** 2026-06-23
- **Trigger:** validation surfaced borderline cases like (Unilever) "In October, along with the Indonesian Ministry of Energy, we co-hosted a public–private roundtable focused on scaling biomethane production." — a factual *activity/participation* statement, not a performance or commitment.
- **Proposed definition (to confirm with the teacher so both annotators share it):** a sentence is a CLAIM only if the company asserts an environmental (a) result/performance ("reduced X 29%"), (b) commitment/target ("net zero by 2039"), or (c) product/operation property ("packaging is recyclable"). Sentences that merely report an ACTIVITY, event, partnership, membership or engagement with no stated outcome/commitment ("co-hosted a roundtable", "partnered with", "joined", "signed", "supported") are NOT claims for the gold set.
- **Why it matters:** without a written definition, two annotators disagree precisely on these lines, sinking inter-annotator agreement. Also "activity/association without impact" is itself a recognised greenwashing tactic, so a later refinement may KEEP these as a distinct "symbolic/activity" subtype rather than dropping them.
- **Emerging finding (4th FP category):** activity/participation statements; and false positives **concentrate in the Vague class** — Strong (carries a quantity) and Future Promise (carries a commitment) usually have real substance, while Vague is the catch-all where descriptions, activities and risk statements land. To be confirmed by the 40-claim gold counts (per-class precision).
- **Feeds paper section:** Methodology (operational definition of a claim), Results/Evaluation (error taxonomy; per-class precision), Limitations.

## 13. Validation finding — Claim_Type polysemy ("target") + Evidence must be its own axis (refines #4, #5)
- **Date:** 2026-06-23
- **Trigger:** (Dr Pepper) "we use resources such as a benchmarking analysis from the Beverage Industry Environmental Roundtable (BIER) to set targets and evaluate our performance" — code labelled Future Promise / Partial / Weak Evidence.
- **Finding A — Claim_Type polysemy:** tagged Future Promise only because "set targets" contains "target", a FUTURE_MARKER (#4); but there is no forward commitment — it describes an ongoing target-setting *process*. "target" as a noun ≠ "target" as a pledge. (Also: by #12 the sentence is arguably methodology, not a claim at all — #10 family.) If counted, the correct type is Vague.
- **Finding B — Evidence is a separate axis:** the grader's instinct "Vague claim WITH partial evidence" is correct and exposes that `evidence_for()` mechanically derives evidence from claim type (Vague→No). Evidence is independent: this Vague sentence cites an external credible source (BIER), so it has partial evidence. Real fix (later WP): detect evidence directly — citations, external standards, data/page references — not infer it from claim strength. Concrete proof of the simplification flagged in #5.
- **Feeds paper section:** Methodology (claim taxonomy + evidence model), Results/Evaluation (error taxonomy), Limitations.

## 14. Redesign — Claim_Type and Evidence determined INDEPENDENTLY; Risk_Signal derived from both (revises #5)
- **Date:** 2026-06-23
- **Decision:** Stop deriving Evidence_Exists from Claim_Type. Determine the two on separate axes, then compute Risk_Signal from their combination:
  - **Claim_Type** (kind of assertion): Strong (measurable result) / Future Promise (forward commitment) / Vague (unspecified).
  - **Evidence_Exists** (is it backed?), independent rules: Yes = hard quantitative outcome/data in the sentence (number+unit / %, baseline comparison); Partial = cites a credible source/standard/framework/assurance or a data/page reference but no hard outcome number; No = neither.
  - **Risk_Signal** = f(Claim_Type, Evidence) via a 3×3 matrix: Strong×{Yes,Partial}→Supported, Strong×No→Unverified; Future×Yes→Credible, Future×Partial→Weak Evidence, Future×No→Unsubstantiated; Vague×Yes→Needs Review, Vague×Partial→Weak Evidence, Vague×No→Vague. High-risk greenwashing flags = Future+No and Vague+No.
- **Why:** validation (#13, BIER case) showed the rigid coupling is wrong — a Vague claim can still cite evidence (Vague+Partial), and a Strong-sounding claim can lack backing. Claim strength (what is asserted) and evidence (whether it is verifiable) answer different questions; conflating them loses exactly the cases greenwashing detection cares about. Two axes + a derived risk also yield a finer, more defensible Risk_Signal.
- **Validation check:** under the new model the BIER sentence — if it were counted as a claim — would be Vague + Partial → Weak Evidence, matching the human grader's intuition (it was instead graded a "no claim").
- **Build refinement (from a test case):** the Evidence=Yes rule must require an ACHIEVED/measured quantity (past-tense result or baseline comparison, e.g. "saved 29% vs 2019"), NOT merely any number. A projected target number ("expected to save 55 million gallons by 2030") is the *size of the promise*, not evidence — it should read as Future Promise + Partial, not Evidence Yes. Telling achieved from projected numbers needs tense/context cues (past: reduced/saved/achieved, "in 2025"; future: by-20XX/expected/will/aim) — another meaning cue reinforcing the ML rationale.
- **Status:** DESIGNED; implement AFTER the current 40-claim gold set is labelled — the redesign changes only the 3 derived columns, not which sentences are claims, so it won't disturb the gold set's manual columns.
- **Feeds paper section:** Methodology (claim model: independent axes + risk matrix), Justification, Limitations.

## 17. Validation round 1 complete — gold-set results, teacher feedback, and the rule-based v2 action plan
- **Date:** 2026-06-27
- **Gold set:** 26 claims hand-annotated by TWO annotators (student + teacher) — 14 Unilever + 12 Dr Pepper — each marked "real ESG claim? (Y/N)", correct ESG type, and reasoning, in ESG_Report_Master_Table (Drive).
- **Headline results:**
  - On the sampled rows ~46% were real claims (Unilever 7/14, Dr Pepper ~4–5/12). **Caveat: the sample was NOT random** — annotators deliberately hunted false positives — so this is a biased lower bound, not the true precision. The full 532-claim audit (running) gives the unbiased number.
  - The model's weakness is **DETECTION (precision), not downstream classification**: on nearly every true positive the human wrote "correct classification" for Claim_Type/Evidence/Risk. So the fixes must target *which sentences are admitted as claims*, not the taxonomy.
- **FP taxonomy CONFIRMED by the gold reasoning** (front_matter/governance, methodology/definition, risk/condition description, activity report, general/advocacy) PLUS two NEW categories:
  - **navigation/running-header fragments** — e.g. "…IMPACT REPORT 40 Overview Climate & Nature Action Water Use & Stewardship Packaging…" admitted because the section-nav strip carries topic keywords (Dr Pepper p3, p40).
  - **"environment(al)" polysemy** — "create an environment where all our employees can do their best work" (Dr Pepper p30) → "environment" = workplace, not the planet; should be Social and not an E claim. (Same family as the #8 "nature" fix.)
- **Teacher's written feedback (4 points) + assessment:**
  1. `is_claim` is env-GATED (`env_topic_hits>0`), so it is an *environmental-claim* extractor, not a *claim* extractor. → **AGREE.** Decouple detection (assertion by a company subject) from topic (E/S/G becomes a tag, not a gate). Must ship WITH the FP filters or precision craters.
  2. Add a METHOD_PHRASES filter ("is calculated using", "is defined as", "refers to", "methodology", "in accordance with", "data is collected"…) → **AGREE** (kills our methodology/definition FPs, #10/#13; gold: Unilever p19 exclusions, Dr Pepper p11 BIER).
  3. Add a GENERAL_STATEMENT_PHRASES filter ("is critical", "is important", "is essential", "is complex", "requires collective action", "global challenge") → **AGREE** (kills general/advocacy FPs, #16; gold: Dr Pepper p5, p7).
  4. `classify_esg_type` still superficial — weight Governance terms (board, committee, audit) so G wins. → **AGREE, extend**: also add "environment"-polysemy handling and better Social detection (gold p30 workplace "environment" → S).
- **OPEN DISAGREEMENT (annotator divergence to resolve):** the student counted "collective action is critical" as a *Vague claim* (#16 ruling); the teacher's point 3 says DROP such general statements as non-claims. Student even logged it "Yes/No?". **Recommendation:** adopt the teacher's rule (pure opinion/advocacy = NOT a claim; optionally flag as a separate "rhetoric/deflection" category) — cleaner and greenwashing-relevant. This genuine inter-annotator split is itself paper evidence that the boundary needs meaning.
- **Rule-based v2 action plan (implement after sign-off):**
  - A. **Refactor `is_claim`** → require a COMPANY SUBJECT (we/our/us/<Company>, #15) + an ASSERTION (action verb or quantity); topic E/S/G becomes a TAG, not a gate (teacher #1).
  - B. **Add non-claim filters**: METHOD_PHRASES (#2), GENERAL_STATEMENT_PHRASES (#3), RISK/CONDITION (#11/#15), NAVIGATION/HEADER (new).
  - C. **Independent Claim_Type + Evidence + Risk matrix** (#14), incl. achieved-vs-projected number rule and the "target/goal" noun fix (#13).
  - D. **`classify_esg_type` v2** (teacher #4): weight G/S; handle "environment/nature/natural" polysemy; improve S detection.
  - E. **Measure**: re-run, compare old vs new on the gold set (precision before/after) + the full 532-claim audit's FP-category counts.
- **Full-corpus audit (LLM auditor, all 532 claims, 2026-06-27):** overall precision ≈ **35%** (186 real / 532). Unilever **29.6%** (115 real / 388), Dr Pepper **49.3%** (71 / 144). FP drivers (both reports combined): **methodology/definition 131**, front-matter/governance 53, general/advocacy 53, risk/condition 36, activity-report 24, navigation/header 23, actor-less 2. ⇒ methodology is the single biggest leak, so teacher-point-2 (METHOD_PHRASES) is the highest-leverage fix. **Report TYPE matters:** Unilever's ESRS/CSRD regulatory *statement* is methodology/governance-dense (→ much lower precision) vs Dr Pepper's glossier *impact report* — a paper-worthy finding. **Caveat:** LLM auditor (not ground truth), likely stricter than the humans (biased gold sample ran ~46%); the category *ranking* is the robust takeaway, the exact % an estimate. **Projected v2 precision** after the phrase/subject filters ≈ 70%+, with activity-reports and subtle assertion-vs-description as the residual the ML stage must handle — quantifies the #7 precision-ceiling thesis across the full corpus.
- **Feeds paper section:** Methodology (rule-based v2 + evaluation), Results (precision before/after, error taxonomy, inter-annotator agreement), Justification (residual hard cases → ML), Limitations.

## 18. Rule-based v2 IMPLEMENTED + measured on the gold set
- **Date:** 2026-06-27
- **Built (inline) in `extract_claims.py`:** (a) detection DECOUPLED from env-topic — `is_claim` uses an ESG topic gate (E∪S∪G); E/S/G is a tag, not a gate (teacher #1). (b) Non-claim FILTERS: METHOD_PHRASES, GENERAL_STATEMENT_PHRASES (no-quantity), RISK_PHRASES (no-quantity), navigation/cross-ref (teacher #2/#3 + #11/#15 + new). (c) Evidence determined INDEPENDENTLY (achieved quantity→Yes; source/standard or projected quantity→Partial; else No) and Risk_Signal from the 3×3 matrix (#14). (d) `classify_esg_type` v2: STRONG_GOV terms win ties; "work/business environment" polysemy→Social (teacher #4). Run summary now prints per-reason drop counts.
- **Gold-set result (26 human-labelled rows):** recall of real claims **11/11 (100%) — zero real claims lost**; false positives removed **10/15 (67%)** → precision on the sample **42% → 69%**. Filtering the output to E (greenwashing focus) removes the G/S plumbing FPs → E-precision ≈ **85%** on the sample.
- **Counts:** Unilever 388→494 (E 374→**302** cleaned; **+110 S, +82 G** newly captured by decoupling), Dr Pepper 144→175. The rise is SCOPE (now an ESG extractor), not noise — the E subset got smaller and cleaner.
- **Remaining FPs (the 5 gold misses):** governance plumbing (board/committee sentences that carry an action word like "goal"/"commit") ×3, activity-report ("co-hosted a roundtable") ×1, workplace-social aspiration ×1 — the hard, meaning-dependent residue → add a governance/activity filter OR leave for the ML stage (quantifies the #7 ceiling).
- **Open decision:** keep the decoupled ESG output (teacher's vision; full ESG dataset, filter to E for greenwashing) vs re-gate to E-only. Pending user choice.
- **Feeds paper section:** Methodology (rule-based v2), Results (precision before/after + 100% recall + residual error analysis), Justification, Limitations.

## 19. Full-corpus audit of v2 — v1→v2 comparison (LLM auditor)
- **Date:** 2026-06-27
- **v2 audit (all 669 claims):** overall precision **38.3%** (256 real / 669). Unilever 33.2% (164/494), Dr Pepper 52.6% (92/175). By type: **E 39.6%** (161/407), S 43.6% (68/156), **G 25.5%** (27/106).
- **vs v1 audit:** 35.0% (186/532) → **38.3%**. Only a modest OVERALL lift, because decoupling added 137 S/G claims and the G subset is low-precision (25.5%), offsetting a cleaner E set.
- **TWO measures disagree — important caveat:** the HUMAN gold set (26 rows, authoritative) put v2 at **69%** (E ≈ 85%) with 100% recall; the LLM auditor says 38%. The LLM auditor is systematically STRICTER than the human annotators (it was already 35% vs the humans' 46% on v1). ⇒ Cite the HUMAN gold set as ground truth in the paper; use the LLM audit for FP-category structure + a strict lower bound, with this caveat stated.
- **Remaining FP buckets (v2, per audit):** methodology/definition STILL #1 (Unilever **112**) — the v2 METHOD_PHRASES filter was too conservative (it only dropped 24); front-matter/governance rose to 61 (decoupling side-effect); activity_report rose to 43 (status-updates, "engaged investors at AGM", "consultations not done"). Front-matter methodology is concentrated in pages 1–7.
- **Next (round 2, inline, no agents):** strengthen the methodology/scope/boundary filter; add a governance-plumbing filter; re-measure on the gold set (100% recall must hold) before any further agent audit.
- **Feeds paper section:** Results (v1→v2 precision, by-type, two-measure caveat), Limitations (LLM-auditor vs human calibration), Justification (residual → ML).

## 20. Rule-based v2.1 (round 2 + 3 filters, inline) — governance plumbing + ESRS methodology
- **Date:** 2026-06-27
- **Added (inline, no agents):** (1) governance-plumbing filter (committee/board/remuneration/PSP + no quantity → drop), (2) activity/event/membership filter (co-host, roundtable, signed the, participated in, member of, partnered with), (3) extended methodology filter with ESRS/report-structure vocabulary (materiality, IRO, DMA, ESRS, time horizon, severity score, scored on a scale, priority areas, role of management, disclosures consolidate, narrative owners, …), (4) extended navigation (table below, see section, described in our topical).
- **Gold-set result (built + verified inline):** recall **11/11 (100%) — still zero real claims lost**; FP removed **14/15** → gold precision **~92%**. Progression: v1 **42%** → v2 **69%** → v2.1 **92%**, recall 100% throughout. The 1 remaining gold FP is a workplace-"environment" Social aspiration (tagged S → drops out when filtering to E).
- **Structural cleanup:** committee sentences in output **26 → 0**; Unilever front-matter (pp.2–6) survivors **33 → 4**; Strong claims untouched (37, i.e. no quantified claim dropped). Counts: Unilever 494→**416**, Dr Pepper 175→**166**.
- **ESG dist (v2.1):** Unilever E 272 / S 103 / G 41 (G 82→41), Dr Pepper E 105 / S 45 / G 16.
- **Round-3 review = principled stopping point:** remaining residual buckets ("we continue to…", "our approach/strategy…", "guidance") are MIXED — they contain real claims too ("we continue to deliver reductions", "updating targets to SBTi"). Further phrase-filtering would cost recall. This is the rule-based ceiling; the rest needs meaning (ML) — the paper's central thesis, now demonstrated by where the rules plateau.
- **Note:** full LLM re-audit deferred (user token budget). Expect a substantial rise from the v2 baseline (38%) when next run.
- **Feeds paper section:** Methodology (v2.1 filters), Results (v1→v2→v2.1 gold precision 42→69→92% at 100% recall), Justification (mixed residual → ML), Limitations.

## 21. Full-corpus audit of v2.1 (economized LLM auditor) — official v1→v2→v2.1 comparison
- **Date:** 2026-06-28
- **Run:** 13 agents, batch 50, low effort, 299k tokens (~60% of the v2 run) — per the user's "don't use 100%".
- **v2.1 audit (582 claims):** overall precision **44.8%** (261 real). Unilever 38.2% (159/416), Dr Pepper 61.4% (102/166). By type: **E 47.7%** (180/377), S 40.5% (60/148), G 36.8% (21/57).
- **Official progression (LLM auditor, full corpus):** v1 **35.0%** → v2 **38.3%** → v2.1 **44.8%** overall; E 39.6% → 47.7%. Monotonic, corpus-wide — confirms the gains are real, not a gold-sample artifact.
- **FP categories v2.1 (vs v2):** front-matter/governance **74→27** (governance-plumbing filter worked); methodology STILL #1 at 127 (residual definition/scope sentences a conservative filter can't remove without hurting recall); general_advocacy ~65; activity_report ~43; risk ~30.
- **Two-measure caveat:** human gold (2 annotators, 26 rows) = **92%** at v2.1; LLM auditor (582) = **45%**. The LLM auditor is systematically STRICTER than the human experts (borderline count also rose under low effort). ⇒ HEADLINE = human gold (92%, 100% recall); the automated audit is a CONSERVATIVE full-corpus lower bound confirming v1<v2<v2.1 and supplying the error-category distribution.
- **Feeds paper section:** Results (Table II + full-corpus robustness check + error taxonomy), Limitations (automated-vs-human calibration), Justification (residual methodology/advocacy → ML).

## 22. Evaluation-validity caveat — the 92% gold figure is IN-SAMPLE (filters tuned on it)
- **Date:** 2026-06-28
- **Issue (flagged by the user):** the v2.1 filters (METHOD/GOV/ACTIVITY phrase lists) were DESIGNED using the 26-row human gold set (plus a hand-probe of Unilever front-matter). Measuring v2.1 precision on those same rows is train-on-test → the **92% is optimistic / in-sample**, not a generalization estimate. (Raw v1 precision on the same rows was 42% — the honest "we found lots of false positives" figure.)
- **Honest reading:** the unbiased signal is the FULL-CORPUS automated audit, where most claims were not used for tuning — v1 35.0% → v2.1 44.8% overall, under ONE consistent auditor, so the **+10-point relative improvement is the trustworthy result**. Dr Pepper (61%) is the most genuinely held-out (its sentences were never hand-probed for filter design).
- **For the paper:** describe the 26-row gold set as a **development/validation set** (used to define "claim", measure inter-annotator agreement, and tune filters) — NOT a test set. Report the full-corpus audit as the evaluation and emphasize the relative v1→v2.1 gain. **Do not headline 92%.**
- **Limitations to state explicitly:** (a) no held-out, human-labelled TEST set yet (filters tuned on the only human labels we have); (b) the automated auditor is an LLM proxy, stricter than human experts and not ground truth; (c) a larger independent human-labelled test set is future work.
- **Feeds paper section:** Results (dev-set vs full-corpus), Limitations (no held-out test set; LLM-auditor calibration), Methodology (dev-set role).

## 23. Human–agent calibration + dev-set-overfit evidence (both usable in the paper)
- **Date:** 2026-06-28
- **Human↔agent calibration (same version, v1):** human annotators rated the v1 sample at 42% precision; the automated auditor rated the v1 full corpus at 35% — a ~7-point gap, same ballpark, auditor slightly stricter. This is the legitimate calibration claim (supports the LLM auditor as a scalable proxy). NOTE: do NOT equate the human-v1-42% with the agent-v2.1-45% — different versions/samples; their closeness is coincidental.
- **Dev-set overfit is empirically visible:** the v2.1 filters removed 14/15 human-flagged FPs (great on the 26-row dev set) yet the full corpus is still only ~45%, because ~556 claims were never human-reviewed and the phrase filters cannot target error patterns they were never shown. The gap between dev-set success and full-corpus precision is direct evidence that hand-crafted rules do not generalize → motivates (a) a larger labelled set and (b) the learned model, rather than more rules.
- **Feeds paper section:** Results (human–agent calibration), Justification (rules don't generalize → ML), Limitations (small dev set, no held-out test set).

## 15. Validation finding — actor-less environmental-condition descriptions (FP category) + "require a company subject" candidate fix
- **Date:** 2026-06-23
- **Trigger:** (Dr Pepper) "Overgrowth of native-nuisance shrubs has resulted in habitat loss, intensified impacts from drought, decreased water quality and increased risk of wildfire." — graded a no-claim (correctly).
- **Finding:** the sentence describes a general environmental *condition/problem* with NO company subject and NO company action/commitment/performance — it's background/context (here, the rationale for a restoration project). Admitted because TOPIC "water" + ACTION "increased/decreased" fired.
- **Two mechanistic insights:** (a) the verbs increase/decrease are *valence-neutral and actor-agnostic* — they fire on a problem worsening just as on a company achievement; (b) a claim is by definition the COMPANY asserting something, yet the rule never checks for a company/first-person subject.
- **Candidate fix (cheap, high-precision):** require a first-person/possessive or company-name token ("we", "our", "us", "<Company>") for a sentence to qualify as a claim — would drop actor-less condition descriptions while keeping genuine claims (which almost all say "we/our"). Risk to monitor: passive-voice claims ("emissions were reduced 30%"). Weigh against the gold set.
- **Feeds paper section:** Results/Evaluation (error taxonomy), Methodology (claim definition: company as subject), Limitations.

## 16. Validation finding — advocacy/deflection statements (FP category) + "specific vocabulary ≠ evidence"
- **Date:** 2026-06-23
- **Trigger:** (Dr Pepper) "Beyond KDP's design innovations, collective action is critical to advance effective and efficient policy solutions, such as well-designed Extended Producer Responsibility (EPR) programs, invest in infrastructure modernization and engage consumers to act in more sustainable ways." Human leaned "Vague claim + Partial evidence"; analysis differs.
- **Claim?** Leans NO — the main clause is *advocacy/opinion* ("collective action is critical…"), not KDP asserting its own result/commitment/property; the only self-reference ("KDP's design innovations") is a vague aside. If company positioning is counted, it is at most Vague.
- **Evidence = No, not Partial:** naming EPR / "infrastructure modernization" as *desirable policies* is part of the opinion, not evidence of a KDP outcome — no data, citation, standard-compliance or verification. → Vague + No → Risk Vague (if counted). [Current code already outputs Vague/No/Vague.]
- **Principle (sharpens the #14 evidence axis):** specific/technical VOCABULARY (EPR, "infrastructure modernization") is NOT evidence. Evidence = data / citation / verification of an *outcome*; jargon density must not be mistaken for it.
- **New rhetorical category:** responsibility-deflection ("collective action", "engage consumers to act") — shifting the onus onto policy/consumers is a recognised greenwashing move; candidate for a future "deflection/advocacy" flag rather than a substantive claim.
- **Annotator ruling (2026-06-23):** the human annotator counts this as a CLAIM — a *stance/opinion* claim ("collective action is important") — typed Vague, Evidence No, Risk Vague; logged as graded (we agreed on Evidence=No). This **extends the #12 definition**: stance/opinion/advocacy assertions ("X is important/critical") DO count as (Vague) claims, as distinct from activity-reports and condition-descriptions, which do not. Underlying principle: a claim = an *assertion* (of importance, performance, or commitment); a non-claim = a *report of an activity* or *description of a condition*. Both annotators must apply this for agreement.
- **Feeds paper section:** Results/Evaluation (error taxonomy), Methodology (evidence ≠ vocabulary; claim = assertion vs report), Limitations.

---
name: research-paper
description: Maintain the GreenBERT project's academic paper and its design-decision log. Use this skill WHENEVER a notable engineering or design decision is made in the GreenBERT project (choosing keywords, filters, thresholds, classification rules, model choices, evaluation metrics, scope cuts) — append the decision + rationale to paper/design_decisions.md so it survives chat compaction. ALSO use it whenever the user wants to write, draft, edit, or structure any part of the academic paper or project report (abstract, introduction, methodology, results, justification, related work, limitations, WP sections), or label/rule on claims during annotation. Turns engineering choices into paper-ready justification and enforces the project's writing and evaluation rules.
---

# GreenBERT Research Paper & Decision Log

Two jobs. The project's end goal is a conference paper (IEEE/IDAP/UBMK style) plus a longer project report plus a working system, written by a high-school first author with a university co-author. Every design choice must read as deliberate and defensible to reviewers. Reviewers have already criticised a small benchmark (n=26); the writing must now be reviewer-proof.

## Job 1 — Log decisions as we build (do this proactively)

**Whenever we make a notable design decision, append it to `paper/design_decisions.md` before moving on.** Chats get compacted and the *reasoning* is the first thing lost; reviewers reward reasoning, not just results.

A "notable decision" = anything a reviewer might ask *"why did you do it that way?"*: scope cuts, keyword/filter choices, thresholds, taxonomies/labels, annotation rulings, model choices, evaluation metrics, tradeoffs accepted, and every measured result (with its caveat).

Entry format (keep it tight, always fill **Why**):

```
## <short decision title>
- **Date:** YYYY-MM-DD
- **Decision:** what we chose
- **Why:** the rationale a reviewer would want
- **Alternatives considered/rejected:** and why
- **Evidence:** numbers/observations, if any
- **Feeds paper section:** Methodology | Justification | Results | Limitations
```

Append only; never rewrite history. A reversal gets a new entry noting the change (the evolution is itself paper narrative). Running observations during a validation round go as numbered NOTES under one entry (see #24).

## Job 2 — Write / edit the paper or report

1. **Read `paper/design_decisions.md` first.** It is the source of truth for Methodology, Results and Justification. **Every number, table cell and ruling that appears in the paper must trace to a log entry**; if it does not, log it first, then write it.
2. The canonical manuscripts live in the user's Google Drive (project report `GreenBERT_Project_Report_v2`, conference drafts `GreenBert_UMBK` / `GreenBert_IDAP_*`). I cannot edit Google Docs in place. Deliver paste-ready blocks in chat or a Word file with **green highlight = new text, yellow = provisional number**; state exactly which section each block replaces or follows. Never overwrite the teacher's edits; merge around them.
3. Structure: Abstract · Introduction · Related Work · Methodology · Results/Evaluation · Discussion · Limitations · Conclusion (paper); WP1–WP6 with Objective / Activities / Deliverables (report).

### Writing rules (hard rules, no exceptions)
- **No em-dashes.** Never "—" or "--" in any prose. Use commas, colons, parentheses or a new sentence. En-dashes in numeric ranges (2018–2024) and the IEEE template markers "Abstract—" / "Keywords—" are the only exceptions.
- **Plain academic register.** No metaphor or jargon flourishes ("reporting machinery", "plumbing", "dumping ground" as a term). Say what the thing is: "mandatory ESRS reporting elements", "governance role descriptions", "default channel". No "name-drops", "gold mine", "textbook".
- Formal, precise, third person or first person plural; define terms on first use; one idea per sentence; no bold run-in labels unless the user asks.
- Numbers: always say what set they were measured on and whether they are in-sample.

### Evaluation reporting rules (the "three-number story")
Precision and recall are always reported as **three numbers with their provenance**, never one:
1. **Development-sample figure** (26 candidates; v3 = 92%): filters were tuned on it, so it is an *in-sample development result*, never a headline.
2. **Independent human benchmark** (100-candidate manual review; v3 = 67%): the headline human number.
3. **Automated full-corpus audit** (Claude agents, same guideline; v3 33%, v4 final 44%): systematically stricter than humans, reported as a *lower bound*; calibrated against humans where both exist (73% row agreement, every disagreement human-yes/audit-no).
Recall is measured only through the rejected-sentence (non-claims) file; state that it is an automated estimate and that the blind 100-sentence human sample is the check on it. Always add the in-sample caveat when a version was tuned on the rows it is scored on. The paper's honest storyline is: development figure optimistic, independent benchmark lower, automated floor lower still, and the residual errors are semantic, which motivates the transformer stage.

### Annotation rulings (apply when labelling or arguing claim status; codified in the guideline)
- A **claim** = the company asserts its own conduct: (a) achieved/measurable result, (b) forward commitment or target, (c) verifiable property of products or operations. Fact-reporting the company's own performance is a claim. "We are committed to X" is a (Vague) claim.
- **Non-claims:** methodology and definitions (incl. parameter numbers such as "within a 1 km radius", baselines, ESRS materiality/IRO text); governance role descriptions without outcome; risk, dependency and scenario descriptions (IPCC scenario tables are the world's pathway, not the company's target); activity, event, membership and tool-usage reports with no stated outcome; opinion and importance statements; navigation, headers, table shreds; policy-principle bullets and supplier requirements not phrased as the company's own commitment; internal self-reference ("in line with our policy").
- **Outcome test:** if the stated outcome is protecting the business (resilience, cost, supply continuity) rather than environmental or social performance, it is a non-claim.
- **Advocacy performed by the company** ("we advocate for carbon pricing") = claim (Vague, Evidence No). Pure opinion = non-claim.
- **Verifiable governance mechanisms** (remuneration linked to sustainability performance, annual COBP pledge, mandatory training, non-retaliation policy) = Governance claims.
- **A number is not evidence.** Parameter numbers, unrelated numbers and projected sizes of promises do not make a claim Strong and do not count as evidence. Achieved comparative outcomes ("collected more plastic than we sell") are Strong even without a digit.
- **Noun polysemy:** "target", "goal", "pledge", "plan" mark the future only when there is no achievement verb ("delivered on our target" is Strong).
- **ESG type by primary claimed outcome:** planet E, people S, governance/ethics/compliance G. Workplace "environment" is S; human rights and Indigenous rights are S, not E; "nature of our business" is not environmental.
- **Page context allowed:** when a sentence is ambiguous alone, consult the source page before labelling (page numbers exist for this). Context can turn a fragment into a claim and a convincing candidate into a non-claim.

### What impresses reviewers (optimise for these)
- Justified choices tied to logged reasons; honest limitations named with their cause; concrete before/after numbers with provenance; clear novelty (dual-stream, omission as signal, explainable score, sentence-level benchmark with published rulings); reproducibility (code on GitHub, non-claims file, audit files in `Data/claims/`).
- Turn errors into arguments: the limits of the rule engine are the motivation for WP5, and every measured failure family should say whether rules can fix it or only semantics can.

### Tools worth using for the paper
- Hugging Face connector: exact dataset sizes, label schemes, licences and model cards for ClimateBERT, `climatebert/environmental_claims`, `climate_specificity`, `climate_commitments_actions` (cite these precisely).
- Elicit / alphaXiv connectors and `hyperresearch` (light tier): refresh Related Work with 2025–2026 work before a submission; check novelty claims (context-window claim classification, cheap-talk indices) against the literature before asserting them.

---
Keep the log and the paper lean and honest. The log is an asset only while it stays trustworthy and current.

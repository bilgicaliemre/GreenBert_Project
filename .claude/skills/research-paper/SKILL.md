---
name: research-paper
description: Maintain the GreenBERT project's academic paper and its design-decision log. Use this skill WHENEVER a notable engineering or design decision is made in the GreenBERT project (choosing keywords, filters, thresholds, classification rules, model choices, evaluation metrics, scope cuts) — append the decision + rationale to paper/design_decisions.md so it survives chat compaction. ALSO use it whenever the user wants to write, draft, edit, or structure any part of the academic paper (abstract, introduction, methodology, results, justification, related work, limitations). Turns engineering choices into paper-ready justification to impress academic reviewers.
---

# GreenBERT Research Paper & Decision Log

Two jobs. The project's end goal is a conference paper (IEEE/ASYU style) plus a working system, written by a high-school author who needs every design choice to read as deliberate and defensible to judges.

## Job 1 — Log decisions as we build (do this proactively)

The most valuable thing this skill does: **whenever we make a notable design decision, append it to `paper/design_decisions.md` before moving on.** Chats get compacted and the *reasoning* is the first thing lost — but reviewers reward reasoning, not just results. Capturing it live means the Methodology and Justification sections almost write themselves later.

A "notable decision" = anything a reviewer might ask *"why did you do it that way?"*: scope cuts, keyword/filter choices, thresholds, taxonomies/labels, model choices, evaluation metrics, tradeoffs accepted.

Append an entry in this format (keep it tight, but always fill **Why**):

```
## <short decision title>
- **Date:** YYYY-MM-DD
- **Decision:** what we chose
- **Why:** the rationale a reviewer would want
- **Alternatives considered/rejected:** and why
- **Evidence:** numbers/observations, if any
- **Feeds paper section:** Methodology | Justification | Results | Limitations
```

Don't rewrite history — append. If a later decision reverses an earlier one, add a new entry noting the change and why (that evolution is itself a good paper narrative).

## Job 2 — Write / edit the paper

When the user wants to draft or revise the paper:

1. **Read `paper/design_decisions.md` first** — it is the source of truth for Methodology/Justification.
2. Follow the standard conference structure: Abstract · Introduction · Related Work · Methodology · Results/Evaluation · Discussion · Limitations · Conclusion.
3. The canonical manuscript lives in the user's Google Drive (`GreenBert_ASYU.docx` and related). Treat on-disk drafts as working copies; ask which is current before overwriting.

### What impresses judges (optimize for these)
- **Justified choices**, never arbitrary — tie every method to a reason ("we did X because Y"), drawn from the log.
- **Honest limitations** — naming what the system can't do (and why) reads as rigor. E.g., the keyword method's precision ceiling is a *strength* of the paper because it motivates the ML stage.
- **Quantitative evidence** — concrete numbers (counts, precision observations, before/after).
- **Clear novelty** — what GreenBERT does that prior work doesn't (dual-stream, omission-as-signal, explainable score).
- **Reproducibility** — enough method detail that someone could rebuild it.

### Tone
Formal, precise, third person. Define terms on first use. Keep claims defensible and avoid overclaiming — reviewers probe weak spots.

---
Keep both the log and the paper lean and honest. The log is an asset only while it stays trustworthy and current.

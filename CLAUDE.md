# GreenBERT Project

Greenwashing detection pipeline for corporate ESG reports. Built in work packages (WPs).

## End goal (north star)
Final deliverable to impress reviewers: a **public website** — a user uploads an ESG report PDF and
gets back a greenwashing assessment **with explanation**. The Google Sheets / TSV step is a
DEV-PHASE convenience only; it disappears in the final product. Implication: build each stage as
importable functions (logic separate from file/CLI I/O) so the website can call them later.

## Pipeline / folder layout
```
Data/raw_pdfs/        # input: ESG report PDFs (6 reports loaded)
Data/claims/          # extract_claims.py output: <name>_claims.tsv (paste into Sheets)
Data/extracted_text/  # extract_claims.py output: <pdf>.txt (page-marked); later also BERT JSON chunks
Data/sections/        # later WP
```

## Current status
- **Claim extraction — `extract_claims.py` v4**: WORKS end-to-end (PyMuPDF, nltk incl. POS tagger auto-download).
  PDF → text (+page #) → gate + non-claim filters → `<name>_claims.tsv` + `<name>_nonclaims.tsv`.
  Cols: Company, Page, Claim_Text, ESG_Type, Claim_Type, Evidence_Exists, Risk_Signal. Unilever 351 / Dr Pepper 158 claims.
- **`pdf_to_chunks.py`** (BERT JSON chunker): built, NOT in use — reserved for the later ML stage.
- **Validation**: 100-claim manual review of Unilever v3 done (67%); 416-row agent audit done
  (`Data/claims/unilever_claims_audit.tsv`); teacher's v4 protocol in progress: fresh v4 precision review +
  recall review of `Data/unilever_recall_sample_100.tsv`. See decision log #24 NOTES 1–10.
- Not started: BERT claim classification (WP5), quantitative-metric extraction, discrepancy → score, website.

## extract_claims.py conventions (decided with user — don't re-litigate)
- Engine is at **v4** (commit 94318c6). Gate = ESG TOPIC word (E ∪ S ∪ G vocab) + (ACTION verb OR hard quantity).
  Topic-only sentence = description, dropped. Then non-claim filters (reason recorded): boilerplate,
  reference_dense, navigation, broken_fragment (v4-A, NLTK POS verb check), iro_register (v4-C),
  policy_content (v4-B), governance_role, activity_report (+soft list, v4-E), methodology (+v4-D,
  self-reference positional rule), general_statement, risk_description (+v4-C).
- ESG_Type CLASSIFIED E/S/G by keyword dominance; STRONG_GOV terms win ties; ENV_POLYSEMY ("working
  environment") -> S; "nature of" excluded. Claim_Type: verb/modal future markers -> Future Promise;
  noun markers (target/goal/pledge/plan) only without an achievement verb; hard quantity (not a
  parameter number, v4-F) -> Strong; else Vague. Evidence is INDEPENDENT (achieved perf. quantity ->
  Yes; standard/assurance cite or projected quantity -> Partial; else No). Risk_Signal from RISK_MATRIX.
- Every run also writes `<name>_nonclaims.tsv` (all rejected sentences + Drop_Reason) for recall audits.
- Annotation rulings (guideline): company-performed advocacy = claim (Vague); pure opinion, scenario
  descriptions, method numbers, tool usage, policy bullets = non-claims; PSP/COBP-type governance
  mechanisms = G claims; page context allowed when a sentence is ambiguous alone.
- Benchmarks: dev 26 (in-sample 92%), manual 100 on Unilever v3 = 67%, audit 416 rows (v3 33% -> v4 39%
  in-sample). Fresh v4 precision + recall (100-random-rejected sample) per teacher's protocol pending.
- KEY INSIGHT unchanged: keywords hit a semantic ceiling; residual errors motivate the BERT stage.

## pdf_to_chunks.py conventions (BERT route, for when we get there)
- PyMuPDF primary, pdfplumber for tables only (no PyPDF2). bert-base-uncased tokenizer. 480-token chunks.
- Never lowercase / remove stopwords (BERT needs raw text). Scanned/encrypted → fail loudly.

## How to run (claim extraction)
```bash
# one report:
python3 extract_claims.py Data/raw_pdfs/<report>.pdf Data/claims/<name>.tsv --company "..."
# every report in raw_pdfs (also what the VS Code ▶ Run button does):
python3 extract_claims.py
```

## Working agreement
- Dependencies: install on-demand (user granted authority). Keep requirements.txt updated.
- Keep this file lean — loads every turn. Decisions/conventions only, no prose.
- User is a HS student, less CLI-experienced: numbered steps, no jargon, verify before asserting, and
  SHOW concrete examples/drafts rather than asking abstract design questions.

## Standing reminders (Claude: act on these)
- **Decision log**: append every notable design decision + rationale to `paper/design_decisions.md`
  (via the `research-paper` skill) — feeds the academic paper, survives compaction.
- **Paper sources**: Related Work is ALREADY DRAFTED. The canonical manuscript + extensive project notes
  live in the user's Google Drive "GreenBert" project (accessible via the Drive MCP). READ those before
  drafting/writing any paper section — don't assume a section is missing.
- **Skills**: when a workflow repeats, create a skill in `.claude/skills/` instead of re-typing steps.
- **Context hygiene**: I can't run /clear or /compact — proactively tell the user when to.

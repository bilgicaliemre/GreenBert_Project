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
- **Claim extraction (current focus) — `extract_claims.py`**: WORKS end-to-end. Deps installed (PyMuPDF, nltk).
  PDF → text (+page #) → keyword+action claim filter → **TSV** (paste into Google Sheets).
  Cols: Company, Page, Claim_Text, ESG_Type, Claim_Type, Evidence_Exists, Risk_Signal. ~388 claims on Unilever (typed E 374 / G 9 / S 5).
- **`pdf_to_chunks.py`** (BERT JSON chunker): built, NOT in use — reserved for the later ML stage.
  We chose the "lighter route" (extract_claims.py) first, with the user.
- **Validation (in progress)**: author + teacher INDEPENDENTLY label 40 claims (20 Dr Pepper + 20 Unilever)
  on two manual columns — "real ESG claim?" and correct ESG type — to measure detection precision + E/S/G
  typing accuracy and surface inconsistencies (human gold set; supports inter-annotator agreement). Possible
  later step: Claude as a 3rd automated annotator (token budget permitting). See decision log #9.
- Not started: BERT claim classification, quantitative-metric extraction, discrepancy → greenwashing
  score + explanation, website.

## extract_claims.py conventions (decided with user — don't re-litigate)
- Detection is environmental-GATED: a claim must hit an env TOPIC word (governance is sparse; for greenwashing, sustainability ≈ environment).
- ESG_Type is then CLASSIFIED E/S/G by keyword-dominance, NOT hardcoded: it flips a claim to S/G only when that vocabulary strictly out-counts the env words. Output stays mostly E; board/committee/HR sentences that slipped in via "sustainability" now tag G/S correctly. (decision log #8)
- Claim test = TOPIC keyword + (ACTION verb OR hard quantity). Topic-only sentence = description, dropped.
- Claim_Type: future words → Future Promise; else hard quantity (%, tCO₂e…) → Strong; else → Vague.
- Evidence: Strong→Yes, Future→Partial, Vague→No. Risk_Signal: Strong+Yes→Supported, Vague+No→Vague,
  Future+Partial→Weak Evidence; else blank (true Supported/Contradicted needs the later discrepancy WP).
- TOPIC_KEYWORDS / ACTION_KEYWORDS at top of file = the tunable knobs. Output is TAB-separated (.tsv).
- KEY INSIGHT: keywords get ~80%; telling a real claim from governance/process prose needs MEANING —
  that is exactly why the BERT model exists (later WP). Don't try to perfect precision with keywords.

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

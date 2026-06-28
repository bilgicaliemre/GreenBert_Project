#!/usr/bin/env python3
"""
extract_claims.py  —  GreenBERT claim extraction (the "lighter route")

Turns ONE ESG report PDF into:
  (1) a .txt of the extracted text (with PAGE markers) so you can eyeball it, and
  (2) a TSV (tab-separated) of candidate environmental claims, each pre-classified,
      ready to PASTE STRAIGHT into Google Sheets / the ESG_Report_Master_Table.

Pipeline:
    PDF  --(PyMuPDF)-->  text, page by page   --> saved as <output>.txt
         --(nltk)----->  sentences (page number kept)
         --(filters)-->  drop boilerplate / table-of-contents / over-long blobs
         --(claim test)->  keep only sentences that ASSERT something about an
                           environmental TOPIC (topic word + action/quantity),
                           not sentences that merely mention/describe a topic
         --(rules)---->  Claim_Type, Evidence_Exists, Risk_Signal
         ------------->  <output>.tsv

Output columns (match master-table page 2):
    Company, Page, Claim_Text, ESG_Type, Claim_Type, Evidence_Exists, Risk_Signal

Usage:
    python extract_claims.py <input.pdf> <output.tsv> [--company "Shell (Oman)"]
"""

from __future__ import annotations
import argparse
import csv
import os
import re

# Environmental TOPICS a claim can be about (substring/stem match, lowercased).
TOPIC_KEYWORDS = [
    "carbon", "emiss", "ghg", "greenhouse", "climate", "scope",
    "net zero", "net-zero", "renewab", "energy", "water", "waste",
    "plastic", "packaging", "biodivers", "deforest", "pollut",
    "circular", "recycl", "offset", "sustainab", "environment",
    "fossil", "decarbon", "methane", "reforest", "land use",
]
# "nature" is handled separately (see NATURE_RE) so we can keep "nature
# restoration" / "nature-based" but drop the idiom "the nature of our business".

# ----- ESG TYPE vocabularies -------------------------------------------------
# TOPIC_KEYWORDS above = the Environmental (E) vocabulary; it is reused to score
# "E". The two lists below add Social (S) and Governance (G) so each claim's
# ESG_Type is CLASSIFIED, not hard-coded to "E". A claim is detected on an
# environmental topic word, so E is the default; it flips to S or G only when
# that vocabulary clearly out-counts the environmental words in the sentence.
SOCIAL_KEYWORDS = [
    "employe", "workforce", "worker", "labour", "labor",
    "human right", "health and safety", "occupational", "safety",
    "diversity", "inclusi", "gender", "women", "woman",
    "equalit", "equit", "wellbeing", "well-being",
    "communit", "training", "upskill", "reskill", "livelihood",
    "wage", "modern slavery", "child lab", "forced lab", "discriminat",
    "talent", "philanthrop", "volunteer", "nutrition", "accessib", "social",
]

GOVERNANCE_KEYWORDS = [
    "board", "committee", "remunerat", "compensation", "incentive",
    "executive pay", "audit", "ethic", "complian", "anti-corruption",
    "anti-bribery", "briber", "governance", "oversee", "oversight",
    "accountab", "shareholder", "code of conduct", "whistleblow",
    "director", "integrity", "lobbying", "risk management",
    "disclosure", "transparen",
]

# ACTIONS that make a sentence an actual claim (doing OR promising something).
# Without one of these (and no hard number), a topic sentence is just description.
ACTION_KEYWORDS = [
    # performance verbs
    "reduc", "lower", "achiev", "deliver", "increas", "decreas", "improv",
    "reach", "sourc", "launch", "install", "invest", "avoid", "eliminat",
    "sav", "phas", "transition", "switch", "scal", "embed", "maintain",
    "restor", "protect", "roll out", "rolled out",
    # commitment / future verbs
    "commit", "aim", "pledge", "strive", "aspire", "target", "goal",
    "will ", "net zero", "net-zero",
]

# Forward-looking words => "Future Promise". NOTE: "commit" is deliberately
# NOT here, so "committed to sustainability" stays Vague (matches your example).
FUTURE_MARKERS = [
    "will ", "aim", "plan", "pledge", "strive", "aspire", "ambition",
    "target", "goal", "net zero", "net-zero", "by 20", "expect", "intend",
]

# A REAL quantity = a percentage, or a number followed by a unit.
# This is what makes a claim "Strong" (page numbers / years alone do NOT count).
QUANTITY_RE = re.compile(
    r"""\d+(?:[.,]\d+)?\s*%                                   # 29.9%
      | \b\d{1,3}(?:[,. ]\d{3})*(?:\.\d+)?\s*
        (?:t\b|tonnes?|tco2e?|ktco2e?|mtco2e?|kt\b|mt\b|kg\b|kwh|mwh|gwh|twh|
           m3|m³|litres?|liters?|million|billion|bn\b)         # 638 tCO2e, 1.2 million
    """,
    re.IGNORECASE | re.VERBOSE,
)

# Legal / front-matter boilerplate that is never a real claim.
BOILERPLATE_PHRASES = [
    "forward-looking statement", "forward looking statement",
    "cautionary statement", "expressly disclaims",
    "risks and uncertainties", "actual results could differ",
    "obligation or undertaking", "terms of reference",
    "basis for preparation", "basis of preparation",
    "similar expressions of future performance",
]

NUM_TOKEN_RE = re.compile(r"\b\d[\d,.]*\b")  # one numeric token (12, 1,234, 3.4)

MIN_WORDS = 4    # below this = fragment / heading
MAX_WORDS = 45   # above this = legal blob, not a single claim

# ----- v2 NON-CLAIM FILTERS (precision; built from validation + teacher review) --
# Methodology / definition sentences describe HOW things are measured/defined, not
# a performance claim. (Biggest false-positive class in the full 532-claim audit.)
METHOD_PHRASES = [
    "is calculated", "are calculated", "calculated using", "calculation of",
    "is assessed", "are assessed", "assessed using", "definition of",
    "is defined as", "are defined as", "refers to", "refer to", "methodology",
    "data is collected", "data are collected", "reported according to",
    "in accordance with", "continue to evolve", "approach to emissions data",
    "this statement", "this document", "this section", "standards and protocols",
    "exclusions:", "excluded from", "benchmarking", "benchmark codes",
    "evaluate our performance",
    # v2.1 round-2: ESRS / reporting-framework + report-structure plumbing
    "materiality", "double materiality", "dma ", " iro", "iros", "esrs",
    "topical disclosure", "time horizon", "severity score", "scored on a scale",
    "measurement uncertainty", "we have disclosed", "due diligence",
    "narrative owners", "written disclosures", "role of management",
    "translate global", "for sustainability reporting", "impact measurement",
    "priority areas", "business strategy", "considering performance against",
    "disclosures consolidate", "consolidate our", "metrics and targets related to",
    "this includes actions", "established engagement", "risk assessments",
    "interviews and questionnaires", "support delivery", "the spi", "spi is",
    "systems and data",
]
# General opinion / advocacy sentences (NOT claims -- per teacher review). Applied
# only when there is NO hard quantity (a number signals real substance).
GENERAL_STATEMENT_PHRASES = [
    "is critical", "are critical", "is important", "are important",
    "is essential", "are essential", "is vital", "is key", "is complex",
    "is challenging", "global challenge", "global challenges", "is necessary",
    "requires collective action", "collective action", "transformative power",
    "plays a critical role", "plays an important role", "plays a key role",
    "play a key role", "play an important role",
]
# Risk / dependency / condition descriptions (a threat, not own action). Applied
# only when there is NO hard quantity.
RISK_PHRASES = [
    "vulnerable to", "increasingly vulnerable", "exposed to", "dependent on",
    "deeply dependent", "could result in", "could lead to", "could increase",
    "could reduce", "could affect", "may affect", "may impact", "may result",
    "impacts of climate", "physical risk", "transition risk", "risks associated",
    "pose a risk", "poses a risk", "at risk", "risk of",
]
# Governance-role plumbing: a committee/board doing its job (oversee/review/approve),
# not an ESG performance claim. Applied only when NO hard quantity.
GOV_PLUMBING = [
    "committee", "subcommittee", "advisory council", "the board", "board's",
    "supervisory board", "remunerat", "incentive plan", "performance share plan",
    "narrative owners", "engage investors",
]
# Activity / event / membership reports: an action with no stated outcome.
ACTIVITY_PHRASES = [
    "co-host", "roundtable", "signed the", "re-signed", "open letter",
    "participated in", "signatory", "joined the", "we are a member",
    "member of", "partnered with", "we sponsor", "we attended",
]
# Navigation / running-header / cross-reference fragments (section-title soup).
SECTION_NAV_WORDS = [
    "climate & nature", "water use & stewardship", "packaging & circular",
    "responsible sourcing", "circular economy", "human rights, responsible",
    "overview climate", "supply chain", "table of contents",
]
NAV_POINTER_PHRASES = ["see page", "on page", "refer to the table", "for more detail",
                       "table below", "figure below", "see section", "see scope",
                       "detailed in the relevant", "described in our topical"]

# Evidence references: external standards / assurance / data pointers => backing.
EVIDENCE_REFS = [
    "sbti", "science-based target", "ghg protocol", "tcfd", "gri ", "iso ",
    "assured", "assurance", "audited", "verified", "third-party", "third party",
    "kpmg", "deloitte", "erm cvs", "certified", "see page", "in accordance with",
    "externally", "validated",
]
# Governance terms that should win ESG_Type ties (teacher review point 4).
STRONG_GOV = ["board", "committee", "remunerat", "audit", "governance",
              "director", "shareholder"]
# "environment" used non-environmentally (workplace etc.) -> Social, not planet.
ENV_POLYSEMY_RE = re.compile(
    r"\b(work|working|business|regulatory|operating|control|team|inclusive|safe)\s+environment",
    re.IGNORECASE)

# Risk_Signal matrix: derived from (Claim_Type x Evidence_Exists), now independent.
RISK_MATRIX = {
    ("Strong", "Yes"): "Supported", ("Strong", "Partial"): "Supported",
    ("Strong", "No"): "Unverified",
    ("Future Promise", "Yes"): "Credible",
    ("Future Promise", "Partial"): "Weak Evidence",
    ("Future Promise", "No"): "Unsubstantiated",
    ("Vague", "Yes"): "Needs Review", ("Vague", "Partial"): "Weak Evidence",
    ("Vague", "No"): "Vague",
}


# ---------------------------------------------------------------------------
# STEP 1:  PDF  ->  text
# ---------------------------------------------------------------------------
def get_pages_text(pdf_path: str) -> list[str]:
    """Return a list where index i = plain text of page i (0-based)."""
    import fitz  # PyMuPDF
    doc = fitz.open(pdf_path)
    pages = [page.get_text("text") for page in doc]
    doc.close()
    return pages


def save_text_file(pages: list[str], txt_path: str) -> None:
    """Save extracted text with PAGE markers, so you can open and verify it."""
    with open(txt_path, "w", encoding="utf-8") as f:
        for i, page_text in enumerate(pages, start=1):
            f.write(f"========== PAGE {i} ==========\n")
            f.write(page_text.rstrip() + "\n\n")


# ---------------------------------------------------------------------------
# STEP 2:  text  ->  classified claims
# ---------------------------------------------------------------------------
def split_sentences(text: str) -> list[str]:
    """Split a page of text into sentences (nltk if available)."""
    try:
        import nltk
        for res in ("punkt", "punkt_tab"):
            try:
                nltk.data.find(f"tokenizers/{res}")
            except LookupError:
                nltk.download(res, quiet=True)
        from nltk.tokenize import sent_tokenize
        return sent_tokenize(text)
    except Exception:
        # crude fallback: split on . ! ?
        return re.split(r"(?<=[.!?])\s+", text)


# "nature" counts as an environmental topic EXCEPT the idiom "nature of ..."
# ("the nature of our business" = "the kind of", not the natural world). So we
# match "nature" only when it is NOT immediately followed by "of".
NATURE_RE = re.compile(r"\bnature\b(?!\s+of\b)", re.IGNORECASE)


def env_topic_hits(low: str) -> int:
    """Number of environmental TOPIC signals in a (lowercased) sentence."""
    n = sum(1 for k in TOPIC_KEYWORDS if k in low)
    if NATURE_RE.search(low):
        n += 1
    return n


def social_hits(low: str) -> int:
    return sum(1 for k in SOCIAL_KEYWORDS if k in low)


def gov_hits(low: str) -> int:
    return sum(1 for k in GOVERNANCE_KEYWORDS if k in low)


def esg_topic_hits(low: str) -> int:
    """ESG topic signals (E + S + G). v2: detection is no longer ENV-only
    (teacher review point 1) -- this is an ESG-claim extractor; E/S/G is then a TAG."""
    return env_topic_hits(low) + social_hits(low) + gov_hits(low)


def has_action(low: str) -> bool:
    return any(a in low for a in ACTION_KEYWORDS)


def is_claim(low: str, has_quantity: bool) -> bool:
    """A claim = an ESG TOPIC word + (an ACTION verb OR a hard quantity).
    The non-claim FILTERS (see non_claim_reason) then remove descriptions/methodology."""
    return esg_topic_hits(low) > 0 and (has_action(low) or has_quantity)


def is_boilerplate(low: str) -> bool:
    """Legal / front-matter disclaimer text -> not a claim."""
    return any(p in low for p in BOILERPLATE_PHRASES)


def is_reference_dense(sentence: str) -> bool:
    """Table-of-contents / index / 'page 57, page 68' reference lists."""
    if len(NUM_TOKEN_RE.findall(sentence)) >= 5:
        return True
    if sentence.lower().count("page ") >= 2:
        return True
    return False


def is_navigation(low: str) -> bool:
    """Running headers / TOC / cross-reference pointers (section-title soup)."""
    if any(p in low for p in NAV_POINTER_PHRASES):
        return True
    nav_hits = sum(1 for w in SECTION_NAV_WORDS if w in low)
    if nav_hits >= 2:
        return True
    if ("impact report" in low or "sustainability report" in low) and nav_hits >= 1:
        return True
    return False


def non_claim_reason(sentence: str, low: str, has_quantity: bool):
    """Return WHY a topic+action sentence is still NOT a claim, else None.
    Built from the validation error taxonomy + the teacher's review."""
    if is_boilerplate(low):
        return "boilerplate"
    if is_reference_dense(sentence):
        return "reference_dense"
    if is_navigation(low):
        return "navigation"
    if not has_quantity and any(p in low for p in GOV_PLUMBING):
        return "governance_plumbing"
    if any(p in low for p in ACTIVITY_PHRASES):
        return "activity_report"
    if any(p in low for p in METHOD_PHRASES):
        return "methodology"
    if not has_quantity and any(p in low for p in GENERAL_STATEMENT_PHRASES):
        return "general_statement"
    if not has_quantity and any(p in low for p in RISK_PHRASES):
        return "risk_description"
    return None


def classify_claim_type(low: str, has_quantity: bool) -> str:
    is_future = any(m in low for m in FUTURE_MARKERS)
    if is_future:
        return "Future Promise"
    if has_quantity:
        return "Strong"
    return "Vague"


def evidence_exists(low: str, has_quantity: bool) -> str:
    """v2: evidence is determined INDEPENDENTLY of claim type (decision #14).
    Yes     = a concrete achieved quantity (a number NOT in a future/projected context);
    Partial = cites a credible source/standard/assurance, OR a projected quantity;
    No      = neither. (A projected '55M gallons by 2030' is the size of the promise,
    not evidence -> Partial, not Yes.)"""
    projected = any(m in low for m in FUTURE_MARKERS)
    if has_quantity and not projected:
        return "Yes"
    if any(c in low for c in EVIDENCE_REFS):
        return "Partial"
    if has_quantity:
        return "Partial"
    return "No"


def risk_signal_for(claim_type: str, evidence: str) -> str:
    """Derived from the (Claim_Type x Evidence) matrix (decision #14)."""
    return RISK_MATRIX.get((claim_type, evidence), "")


def clean(sentence: str) -> str:
    return re.sub(r"\s+", " ", sentence).strip()


def classify_esg_type(low: str) -> str:
    """Tag a claim E / S / G (v2, teacher review point 4).
    - Governance terms (board/committee/audit...) WIN ties, so a Remuneration-
      Committee sentence that name-drops 'sustainability' is G, not E.
    - 'work/business environment' is workplace language -> Social, not planet.
    - Otherwise the dominant ESG vocabulary wins, env-favouring on a tie."""
    e = env_topic_hits(low)
    s = social_hits(low)
    g = gov_hits(low)
    if ENV_POLYSEMY_RE.search(low):     # "work environment" = Social, not E
        s += 1
        if e > 0:
            e -= 1
    if any(k in low for k in STRONG_GOV) and g >= e and g >= s:
        return "G"                      # governance terms present -> G wins ties
    if g > e and g >= s:
        return "G"
    if s > e and s >= g:
        return "S"
    return "E"


def extract_claims(pages: list[str], company: str = "", stats: dict | None = None) -> list[dict]:
    rows: list[dict] = []
    seen: set[str] = set()
    drops: dict[str, int] = {}

    def drop(reason: str) -> None:
        drops[reason] = drops.get(reason, 0) + 1

    for page_idx, page_text in enumerate(pages, start=1):
        for sentence in split_sentences(page_text):
            s = clean(sentence)
            low = s.lower()
            if not (MIN_WORDS <= len(s.split()) <= MAX_WORDS):
                drop("length"); continue       # fragment or legal blob
            has_quantity = bool(QUANTITY_RE.search(s))
            if not is_claim(low, has_quantity):
                drop("not_assertion"); continue  # no ESG topic + action/quantity
            reason = non_claim_reason(s, low, has_quantity)
            if reason:
                drop(reason); continue         # methodology / general / risk / nav...
            if low in seen:
                drop("duplicate"); continue
            seen.add(low)
            ctype = classify_claim_type(low, has_quantity)
            ev = evidence_exists(low, has_quantity)
            rows.append({
                "Company": company,
                "Page": page_idx,
                "Claim_Text": s,
                "ESG_Type": classify_esg_type(low),
                "Claim_Type": ctype,
                "Evidence_Exists": ev,
                "Risk_Signal": risk_signal_for(ctype, ev),
            })
    if stats is not None:
        stats.update(drops)
    return rows


def write_table(rows: list[dict], out_path: str) -> None:
    """Write rows TAB-separated (TSV) -> paste straight into Google Sheets."""
    fields = ["Company", "Page", "Claim_Text", "ESG_Type",
              "Claim_Type", "Evidence_Exists", "Risk_Signal"]
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t")
        w.writeheader()
        w.writerows(rows)


def process_one(pdf_path: str, out_path: str, company: str = "") -> None:
    """Run the whole pipeline on ONE PDF and print a summary.
    Output is TAB-separated (.tsv) so it pastes straight into Google Sheets."""
    # normalise the output stem so it works whether you pass .tsv, .csv, or no ext
    stem = out_path
    for ext in (".tsv", ".csv", ".txt"):
        if stem.lower().endswith(ext):
            stem = stem[:-4]
            break
    tsv_path = stem + ".tsv"
    # The TSV table goes where out_path points (Data/claims/). The raw page text
    # goes to Data/extracted_text/, named after the source PDF -- separate folders
    # so the paste-ready tables and the verification/BERT text never mix.
    os.makedirs(os.path.dirname(os.path.abspath(tsv_path)), exist_ok=True)
    os.makedirs(TXT_DIR, exist_ok=True)
    pdf_stem = os.path.splitext(os.path.basename(pdf_path))[0]
    txt_path = os.path.join(TXT_DIR, pdf_stem + ".txt")

    # Step 1: PDF -> text (saved as .txt so you can verify extraction worked)
    pages = get_pages_text(pdf_path)
    save_text_file(pages, txt_path)

    # Step 2: text -> classified claims -> TSV
    stats: dict[str, int] = {}
    rows = extract_claims(pages, company, stats)
    write_table(rows, tsv_path)

    by_type: dict[str, int] = {}
    for r in rows:
        by_type[r["Claim_Type"]] = by_type.get(r["Claim_Type"], 0) + 1
    breakdown = ", ".join(f"{k} {v}" for k, v in sorted(by_type.items()))
    dropped = ", ".join(f"{k} {v}" for k, v in
                        sorted(stats.items(), key=lambda kv: -kv[1]))
    print(f"  {os.path.basename(pdf_path)}: {len(pages)} pages -> "
          f"{len(rows)} claims ({breakdown})")
    print(f"    filtered out: {dropped}")
    print(f"    text -> {txt_path}")
    print(f"    tsv  -> {tsv_path}")


# Folders found relative to THIS file, so "Run" works no matter the cwd.
HERE = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(HERE, "Data", "raw_pdfs")
OUT_DIR = os.path.join(HERE, "Data", "claims")          # .tsv tables (paste into Sheets)
TXT_DIR = os.path.join(HERE, "Data", "extracted_text")  # page-marked .txt of each report


def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        description="Extract environmental claims from ESG PDFs -> TSV. "
                    "With NO arguments, processes every PDF in Data/raw_pdfs/.")
    p.add_argument("pdf", nargs="?", help="input PDF (optional)")
    p.add_argument("out", nargs="?", help="output file (optional; written as .tsv)")
    p.add_argument("--company", default="", help='e.g. "Shell (Oman)"')
    args = p.parse_args(argv)

    # Mode 1: you named a file -> just that one
    if args.pdf and args.out:
        process_one(args.pdf, args.out, args.company)
        return 0

    # Mode 2: no arguments (e.g. you pressed "Run" in VS Code) ->
    # process every PDF in Data/raw_pdfs/ and write TSVs to Data/claims/
    os.makedirs(OUT_DIR, exist_ok=True)
    pdfs = sorted(f for f in os.listdir(RAW_DIR) if f.lower().endswith(".pdf"))
    if not pdfs:
        print(f"No PDFs found in {RAW_DIR}. Drop an ESG report there and run again.")
        return 1
    print(f"Found {len(pdfs)} PDF(s) in {RAW_DIR}:")
    for name in pdfs:
        stem = name[:-4]
        process_one(os.path.join(RAW_DIR, name),
                    os.path.join(OUT_DIR, stem + "_claims.tsv"),
                    company=stem)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

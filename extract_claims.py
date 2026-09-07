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
    # v4.1 recall fixes
    "pcr", "post-consumer", "hectare", "regenerat", "reuse", "refill",
    "water stewardship", "biodegradab", "microplastic", "virgin plastic",
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
    # v4.1 recall fixes
    "smallholder", "farmer", "sme", "micro-entrepreneur", "living wage",
    "recall", "consumer", "marketing to children", "grievance", "careline",
    "collective bargaining", "pay gap", "harassment",
]

GOVERNANCE_KEYWORDS = [
    "board", "committee", "remunerat", "compensation", "incentive",
    "executive pay", "audit", "ethic", "complian", "anti-corruption",
    "anti-bribery", "briber", "governance", "oversee", "oversight",
    "accountab", "shareholder", "code of conduct", "whistleblow",
    "director", "integrity", "lobbying", "risk management",
    "disclosure", "transparen",
    # v4.1 recall fixes
    "political", "payment terms", "speak up", "code support line",
    "responsible partner policy", "rpp", "cobp", "oecd guidelines",
    "animal", "legal proceeding",
]

# ACTIONS that make a sentence an actual claim (doing OR promising something).
# Without one of these (and no hard number), a topic sentence is just description.
ACTION_KEYWORDS = [
    # performance verbs
    "reduc", "lower", "achiev", "deliver", "increas", "decreas", "improv",
    "reach", "sourc", "launch", "install", "invest", "avoid", "eliminat",
    "sav", "phas", "transition", "switch", "scal", "embed", "maintain",
    "restor", "protect", "roll out", "rolled out",
    # v4.1 recall fixes: achievement / conduct verbs that the recall audit found
    # in 113 missed claims ("purchased 152 kilotonnes", "implemented nine
    # programmes", "we conduct annual training", "we advocate for EPR")
    # (v4.2 pruning after auditing the 273 candidates they admitted: bare stems
    # such as "purchas"/"process"/"support"/"compl" bought 4-13 claims per 20-30
    # false positives, so they are kept only in first-person or past-tense form)
    "we purchased", "implement", "expand", "collect", "processed", "receiv",
    "introduc", "we conduct", "ensur", "we comply", "products comply", "complied",
    "exceed", "we issued", "issued one", "prohibit", "advocat", "lobby", "publish",
    "verif", "train", "accredit", "we support", "supports over", "we supported",
    "we help", "helped", "provid", "recall", "we require", "we follow",
    "we meet", "we do not use", "we work with", "we engage", "in place",
    # commitment / future verbs
    "commit", "aim", "pledge", "strive", "aspire", "target", "goal",
    "will ", "net zero", "net-zero",
]

# Forward-looking words => "Future Promise". NOTE: "commit" is deliberately
# NOT here, so "committed to sustainability" stays Vague (matches your example).
# v4 split (validation round 2): the NOUN markers (target / goal / pledge / plan)
# also appear in PAST achievements ("delivered on our target", "an annual pledge")
# and must NOT make those Future Promises. They count as future only when the
# sentence has no achievement verb. The VERB/MODAL markers always count.
FUTURE_MARKERS = [
    "will ", "aim", "strive", "aspire", "ambition", "by 20", "expect", "intend",
    "plan to", "pledge to", "pledged to",
]
FUTURE_NOUN_MARKERS = ["target", "goal", "pledge", "net zero", "net-zero", "plan"]
ACHIEVED_VERBS = ["delivered on", "achieved", "exceeded", "surpassed", "met our",
                  "reached our", "completed", "delivered against"]

# A REAL quantity = a percentage, or a number followed by a unit.
# This is what makes a claim "Strong" (page numbers / years alone do NOT count).
QUANTITY_RE = re.compile(
    r"""\d+(?:[.,]\d+)?\s*%                                   # 29.9%
      | \b\d[\d,.]*\s*(?:kilotonnes?|hectares?|ha\b)         # v4.1: 152 kilotonnes, 8,000 hectares
      | \b\d[\d,.]*\s+(?:countries|markets|suppliers|sites|programmes|programs|
           brands|pilots|people|farmers|smallholders|employees|leaders|retailers|
           contacts|incidents|recalls|studies|locations|women|workers|
           micro-entrepreneurs|smes|factories|plants)\b           # v4.1: count units
      | \b\d+(?:\.\d+)?:1\b                                  # v4.1: 142:1 ratios
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
# Governance-role descriptions: a committee/board doing its job (oversee/review/
# approve), not an ESG performance claim. Applied only when NO hard quantity.
GOV_ROLE_PHRASES = [
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

# ----- v4 NON-CLAIM FILTERS (validation round 2: 100-claim manual review + audit) --
# Each block names the false-positive family it targets and its share of the
# audited false positives on the Unilever v3 output (279 FPs).

# v4-B  POLICY CONTENT (10% of FPs): imperative policy-principle bullets and
# supplier-requirement lists ("■Reduce water usage...", "the policy sets out four
# principles suppliers must comply with"). A bullet that says "We are committed
# to..." is the company's own commitment and is KEPT (first-person test).
BULLET_GLYPHS = ("■", "•", "▲", "●", "▪", "–", "-")
IMPERATIVE_STARTS = [
    "reduce", "ensure", "monitor", "engage", "collaborate", "encourage",
    "contribute", "promote", "conduct", "protect", "develop", "support",
    "maintain", "respect", "implement", "provide", "continuously", "drive",
    "minimise", "minimize", "work", "build", "use", "avoid", "manage",
    "prevent", "report", "source", "improve", "increase", "eliminate",
    "adopt", "apply", "assess", "identify", "establish", "embed", "phase",
]
POLICY_PHRASES = [
    "sets out four principles", "sets out the principles", "principles that",
    "are required to comply", "required to comply with", "good practices designed to",
    "collection of good practices", "the policy requires", "policy sets out",
    "must comply",
]
# v4-C  RISK / SCENARIO DESCRIPTIONS (15% of FPs): ESRS impact-risk-opportunity
# register rows and climate-scenario narratives ("Risk (OO)", "Negative Impact (VC)",
# "net zero achieved by approximately 2070", "may restrict how we source").
IRO_REGISTER_RE = re.compile(r"\((?:oo|vc|oo\)\s*\(vc)\)|negative impact \(|positive impact \(|opportunity \(", re.IGNORECASE)
RISK_PHRASES_V4 = [
    "scenario", "assumes", "by 2100", "by approximately 20", "present long-term opportunities",
    "presents opportunities", "may lead", "may restrict", "may require", "may increase",
    "could cause", "could harm", "lack of infrastructure", "there is also a risk",
    "risk that", "leads to reduction", "degradation", "ecosystem service failures",
    "evolving consumer preferences", "changing consumer demands",
]
# v4-D  METHODOLOGY / DEFINITIONS (28% of FPs, still the largest): how figures are
# measured or scoped ("is measured via meter readings (78%)", "we also consider
# subcontractors ... in our upstream value chain", "these targets are in line with
# our Environmental Policy" = internal self-reference).
METHOD_PHRASES_V4 = [
    "is measured", "are measured", "measured via", "measured through", "measured using",
    "meter readings", "mass balance", "reporting scope",
    "we also consider", "base year", "baseline year", "baseline values", "rebaselin",
    "restated", "is monitored", "are monitored", "estimated using", "to reach this conclusion",
    "within a 1km", "radius of", "for comparability", "allow for comparability",
]
# Internal self-reference ("these targets are in line with our Environmental
# Policy"): a non-claim only when the alignment IS the point of the sentence --
# i.e. the phrase sits in the first part of a short sentence. A real target that
# merely ends with "..., in line with our policy" is kept (see is_selfref).
SELFREF_PHRASES = ["in line with our", "align with our", "aligns with our",
                   "aligned with our", "consistent with our", "in line with unilever"]
# v4-E  ACTIVITY / TOOL-USAGE REPORTS (22% of FPs): programme existence, tool
# inputs and partnerships with no stated outcome. Applied only when NO hard
# quantity, so "our programme reached 1.2 million hectares" survives.
ACTIVITY_SOFT_PHRASES = [
    "examples include", "programmes to", "programs to", "we use the", "we used the",
    "we incorporated", "as an input", "inputs from", "working group",
    "we work with partners", "we engage with", "we engaged with",
    "we continue to engage", "we participate", "we collaborate with",
    "collaboration with", "pilot", "we are working with", "we worked with",
]
# v4-F  PARAMETER NUMBERS ("a number is not evidence", Strong class was 43% FPs):
# a quantity in one of these contexts is a method parameter or a scheme weight,
# not a performance figure. It still lets the sentence through the GATE (recall)
# but no longer makes it Strong or counts as evidence.
PARAM_CONTEXT = [
    "radius", "threshold", "weighting", "meter readings", "mass balance",
    "measured via", "measured through", "of sites within", "scale of",
    "sample of", "scored", "km of", "1km", "within a ",
]
# Navigation / running-header / cross-reference fragments (section-title soup).
SECTION_NAV_WORDS = [
    "climate & nature", "water use & stewardship", "packaging & circular",
    "responsible sourcing", "circular economy", "human rights, responsible",
    "overview climate", "supply chain", "table of contents",
]
NAV_POINTER_PHRASES = ["refer to the table", "for more detail", "table below",
                       "figure below", "see section", "see scope",
                       "detailed in the relevant", "described in our topical"]
PAGE_POINTER_PHRASES = ["see page", "on page"]   # v4.2: evidence citation if the sentence asserts

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


def pos_tags(words: list[str]) -> list[tuple[str, str]]:
    """Part-of-speech tags via nltk (downloads the tagger on first use). If nltk
    is unavailable, return a fake verb tag so the verb check never drops a sentence."""
    try:
        import nltk
        try:
            return nltk.pos_tag(words)
        except LookupError:
            nltk.download("averaged_perceptron_tagger_eng", quiet=True)
            return nltk.pos_tag(words)
    except Exception:
        return [(w, "VB") for w in words]


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
    # v4.1: ignore years (2025) and small integers ("scope 1, 2 and 3") so a real
    # result such as "5% decrease in scope 1, 2 and 3 GHG emissions in 2025" survives
    toks = [t for t in NUM_TOKEN_RE.findall(sentence)
            if not re.fullmatch(r"(19|20)\d\d", t) and not re.fullmatch(r"\d", t)]
    if len(toks) >= 5:
        return True
    if sentence.lower().count("page ") >= 2:
        return True
    return False


def is_navigation(low: str, asserts: bool = False) -> bool:
    """Running headers / TOC / cross-reference pointers (section-title soup).
    v4.1: a page pointer ("as detailed on page 97") inside a sentence that
    asserts something is an evidence citation, not navigation, so pointer
    phrases only count when the sentence has no action verb and no quantity."""
    if any(p in low for p in NAV_POINTER_PHRASES):
        return True
    if not asserts and any(p in low for p in PAGE_POINTER_PHRASES):
        return True
    nav_hits = sum(1 for w in SECTION_NAV_WORDS if w in low)
    if nav_hits >= 2:
        return True
    if ("impact report" in low or "sustainability report" in low) and nav_hits >= 1:
        return True
    return False


def is_broken_fragment(sentence: str, low: str) -> bool:
    """v4-A  TABLE / BROKEN-SENTENCE GUARD (4% of FPs, pure noise).
    PDF tables get linearised into pseudo-sentences such as
    'gas-fired on-site CHP) 10% 8% Purchased non-renewable electricity (e.g.'
    Three cheap well-formedness checks catch them:
      1. starts mid-sentence (lowercase letter, closing bracket, comma);
      2. unbalanced parentheses (opened but never closed, or vice versa);
      3. no verb at all (a claim must assert; POS-tag the lowercased words)."""
    orig = sentence.lstrip("".join(BULLET_GLYPHS)).strip()   # original case for check 1
    if not orig or orig[0] in ")],;:" or orig[0].islower():
        return True
    if sentence.count("(") != sentence.count(")"):
        return True
    body = low.lstrip("".join(BULLET_GLYPHS)).strip()          # lowercased for tagging
    tags = pos_tags(body.split())
    if not any(t.startswith("VB") or t == "MD" for _, t in tags):
        return True
    return False


def is_selfref(low: str) -> bool:
    """v4-D  internal self-reference is the main assertion: the alignment phrase
    appears in the first 60% of the sentence, or the sentence is short."""
    for p in SELFREF_PHRASES:
        i = low.find(p)
        if i >= 0 and (i / max(1, len(low)) < 0.6 or len(low.split()) < 15):
            return True
    return False


def is_policy_content(low: str) -> bool:
    """v4-B  POLICY CONTENT: an imperative policy bullet with no first-person
    subject ('■Reduce water usage...'), or a supplier-requirement description.
    A sentence that also carries the company's own commitment ('We are committed
    to...') is kept -- mixed stem+bullet sentences are claims (first-person test)."""
    own_commitment = "we are committed" in low or "we commit" in low or "we have committed" in low
    if any(p in low for p in POLICY_PHRASES) and not own_commitment:
        return True
    stripped = low.lstrip("".join(BULLET_GLYPHS)).strip()
    if stripped is not low.strip() or low.strip()[0] in BULLET_GLYPHS:
        first = stripped.split(" ", 1)[0].rstrip(":,")
        # "■Nature protection: Conduct business..." -> look past a short label too
        if ":" in stripped[:40]:
            after = stripped.split(":", 1)[1].strip()
            first_after = after.split(" ", 1)[0] if after else ""
        else:
            first_after = ""
        if (first in IMPERATIVE_STARTS or first_after in IMPERATIVE_STARTS) \
                and " we " not in f" {stripped} " and "our commitment" not in stripped:
            return True
    return False


def non_claim_reason(sentence: str, low: str, has_quantity: bool):
    """Return WHY a topic+action sentence is still NOT a claim, else None.
    Built from the validation error taxonomy + the teacher's review (v2/v3),
    extended by the 100-claim manual review + 416-row audit (v4)."""
    if is_boilerplate(low):
        return "boilerplate"
    if is_reference_dense(sentence):
        return "reference_dense"
    if is_navigation(low, asserts=has_quantity or has_action(low)):
        return "navigation"
    if is_broken_fragment(sentence, low):                       # v4-A
        return "broken_fragment"
    if IRO_REGISTER_RE.search(sentence):                        # v4-C (register rows)
        return "iro_register"
    if is_policy_content(low):                                  # v4-B
        return "policy_content"
    if not has_quantity and any(p in low for p in GOV_ROLE_PHRASES):
        return "governance_role"
    if any(p in low for p in ACTIVITY_PHRASES):
        return "activity_report"
    # v4-E soft activity phrases: only without a quantity AND without a forward-
    # looking target, so "we have set three targets ... we are working with" survives
    if not has_quantity and not is_forward_looking(low) \
            and any(p in low for p in ACTIVITY_SOFT_PHRASES):
        return "activity_report"
    if any(p in low for p in METHOD_PHRASES) or any(p in low for p in METHOD_PHRASES_V4):  # v4-D
        return "methodology"
    if is_selfref(low):                                         # v4-D (self-reference)
        return "methodology"
    if not has_quantity and any(p in low for p in GENERAL_STATEMENT_PHRASES):
        return "general_statement"
    if not has_quantity and (any(p in low for p in RISK_PHRASES)
                             or any(p in low for p in RISK_PHRASES_V4)):   # v4-C
        return "risk_description"
    return None


def is_parameter_number(low: str) -> bool:
    """v4-F: the quantity in this sentence is a method parameter / scheme weight
    ('within a 1km radius', 'meter readings (78%)'), not a performance figure."""
    return any(p in low for p in PARAM_CONTEXT)


def is_forward_looking(low: str) -> bool:
    """v4: verb/modal markers always mean future; noun markers (target, goal,
    pledge, plan, net zero) only when the sentence has no achievement verb, so
    'we delivered on our target to...' is an achieved result, not a promise."""
    if any(m in low for m in FUTURE_MARKERS):
        return True
    if any(m in low for m in FUTURE_NOUN_MARKERS) and not any(v in low for v in ACHIEVED_VERBS):
        return True
    return False


def classify_claim_type(low: str, has_quantity: bool) -> str:
    if is_forward_looking(low):
        return "Future Promise"
    if has_quantity and not is_parameter_number(low):
        return "Strong"
    return "Vague"


def evidence_exists(low: str, has_quantity: bool) -> str:
    """v2: evidence is determined INDEPENDENTLY of claim type (decision #14).
    Yes     = a concrete achieved quantity (a number NOT in a future/projected context
              and NOT a method parameter, v4-F);
    Partial = cites a credible source/standard/assurance, OR a projected quantity;
    No      = neither. (A projected '55M gallons by 2030' is the size of the promise,
    not evidence -> Partial, not Yes.)"""
    perf_quantity = has_quantity and not is_parameter_number(low)
    projected = is_forward_looking(low)
    if perf_quantity and not projected:
        return "Yes"
    if any(c in low for c in EVIDENCE_REFS):
        return "Partial"
    if perf_quantity:
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


def extract_claims(pages: list[str], company: str = "", stats: dict | None = None,
                   rejected: list | None = None) -> list[dict]:
    rows: list[dict] = []
    seen: set[str] = set()
    drops: dict[str, int] = {}
    rej_seen: set[str] = set()   # so recurring headers/footers land in the file once, not 100x

    def drop(reason: str, page: int, text: str, low_text: str) -> None:
        drops[reason] = drops.get(reason, 0) + 1
        # "duplicate" means the sentence was already ADMITTED as a claim earlier --
        # it is not rejected content, so it does not belong in the non-claims file.
        if rejected is None or reason == "duplicate" or low_text in rej_seen:
            return
        rej_seen.add(low_text)
        rejected.append({"Company": company, "Page": page,
                         "Sentence": text, "Drop_Reason": reason})

    for page_idx, page_text in enumerate(pages, start=1):
        for sentence in split_sentences(page_text):
            s = clean(sentence)
            low = s.lower()
            if not (MIN_WORDS <= len(s.split()) <= MAX_WORDS):
                drop("length", page_idx, s, low); continue       # fragment or legal blob
            has_quantity = bool(QUANTITY_RE.search(s))
            if not is_claim(low, has_quantity):
                drop("not_assertion", page_idx, s, low); continue  # no ESG topic + action/quantity
            reason = non_claim_reason(s, low, has_quantity)
            if reason:
                drop(reason, page_idx, s, low); continue         # methodology / general / risk / nav...
            if low in seen:
                drop("duplicate", page_idx, s, low); continue
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


def write_table(rows: list[dict], out_path: str, fields: list[str] | None = None) -> None:
    """Write rows TAB-separated (TSV) -> paste straight into Google Sheets."""
    if fields is None:
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
    # rejected collects every sentence a filter killed (with the reason), so we can
    # audit false negatives: sample it, count missed claims, estimate true recall.
    stats: dict[str, int] = {}
    rejected: list[dict] = []
    rows = extract_claims(pages, company, stats, rejected)
    write_table(rows, tsv_path)
    nonclaims_path = stem + "_nonclaims.tsv"
    write_table(rejected, nonclaims_path,
                fields=["Company", "Page", "Sentence", "Drop_Reason"])

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
    print(f"    nonclaims -> {nonclaims_path}  ({len(rejected)} unique rejected sentences)")


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

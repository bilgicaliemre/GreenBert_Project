# anti-ai-writing: development log

What was built, what changed, why, and the evidence behind each change. Append only; a reversal gets a new
entry. Numbers say what they were measured on. Raw materials and scripts are in this folder (see the
"Files" section at the end).

Dates are 2026-10-20 unless noted. "Judges" are separate Claude agents that compare two texts blind (they do
not know which condition produced which text); every pair gets two judges with different lenses (a strict
editor, and the genre's real reader: an admissions officer, an English teacher, a science teacher, a journal
reviewer, a blog editor). Detector scores are "% likely AI" from two open-source classifiers (D1 = Desklib
DeBERTa-v3-large trained on RAID; D2 = Fakespot RoBERTa-base).

---

## 0. Goal and constraints (from the user)

- Goal: a Claude skill that makes any writing task read like a strong human wrote it, used for every relevant
  writing task; for college applications it must reach the level of admitted essays at top-15 colleges
  ("specific, vulnerable, I feel I met this person"). The user also asked for detector testing, aiming below
  20% (Turnitin's display threshold).
- Constraints we added after research: no fabricated facts; no detector tricks (typos, homoglyphs); real
  application essays are coached, not ghostwritten (Common App fraud policy, YYGS "own work" certification);
  results reported honestly including failures.

## 1. Research phase (5 parallel research agents + completeness critic)

**1.1 Existing open-source skills.** Surveyed about 15 (notes: `notes/github_candidates.md`).
- blader/humanizer (58.8k stars, MIT) has the best structure (26 patterns ordered by strength, a
  mark/draft/check procedure, a no-fabrication rule) but is about 8k tokens, has no academic carve-outs, and its
  own blind test (issue #229) shows its rewrites made rhythm more uniform (60 to 101) and added aphoristic
  closers (38 to 61): a humanizer creating a new tell.
- conorbronsdon/avoid-ai-writing (MIT) has the best guardrails ("never inject" invented specifics, no staccato
  conversion) and self-measured evidence that word lists are weak (lift 0.9) while structural uniformity is
  strong (lift 11.7x).
- petergyang/no-ai-slop (MIT): minimum effective edit, portability test, eval checklist.
- stop-slop over-corrects (no adverbs, no passive, no triads); skill-deslop's examples invent facts.
- **Decision:** build fresh on humanizer's structure, borrow ideas (not text) from three MIT skills with
  credits, write original examples. Spend words on content and structure, not word lists.

**1.2 Evidence-graded catalog of AI tells** (`notes/tells_catalog.md`, 919 lines, ~40 sources).
- Strongest measured tells: corrective framing ("not X, it's Y"), participial "-ing" tails (2-5x human rate,
  Reinhart et al. PNAS 2025), importance flags ("this matters", 116x human for Claude Opus 5.5 per Graphite
  2026), summary closers, uniform sentence length, elegant variation, abstract application-essay nouns
  (journey, growth, resilience: Lee et al. 2025 on 30,000 admissions essays).
- Em dashes are a historical tell; current Claude uses almost none (Graphite, Oct 2026).
- Banning words backfires (Antislop 2025); expert readers detect AI mostly by content and structure (Russell
  et al. 2025).
- **Decision:** audit order content → staging → inflation → lessons → rhythm → tone → words → format.

**1.3 What admitted essays do** (`notes/essay_craft.md`).
- Officers want to "meet" a specific 17-year-old; the common failure is "so what?" (Yale podcast); AI essays
  are "slick but soulless" (Yale ep. 34).
- Techniques: odd specific detail, scene openings, earned (not announced) insight, vulnerability without
  wallowing, endings that open, plain voice.
- Several published admitted essays contain clichés; they work because the body is concrete.

**1.4 Detector facts** (`notes/detector_facts.md`). Turnitin: institutions only, 300-word minimum, 1-19% shown
as "*%"; added "AI bypasser" (humanizer) detection in 2025. Grammarly's score is a share of text; GPTZero's
is a document probability. Independent studies: detectors unreliable and biased against non-native writers.

**1.5 Policies and watermark** (`notes/policies_and_access.md`, verified by a fact-checking agent).
- Claude models from Aug 2026 embed an invisible text watermark that "may persist through some editing";
  detection is a private preview for approved organizations (educational organizations eligible; approved list
  not public). Turnitin/GPTZero cannot read it.
- Common App fraud policy names "the substantive content or output of an artificial intelligence platform"
  presented as one's own. YYGS: AI may "assist" but "your essay must be your own work", certified on signature.
  CJSJ: AI use must be disclosed; undisclosed AI text may be redacted.
- Correction logged: the Isley et al. 2026 admissions-penalty study covers one graduate program (GPTZero
  flags), not undergraduate admissions.

## 2. Measurement setup

**2.1 Local detectors.** Hugging Face was blocked at first; the user opened network access. D1 and D2 run
on CPU (`scripts/score.py`; long texts chunked at ~350 words, length-weighted mean). Binoculars with a
Qwen2.5-1.5B pair was tried and dropped: it did not separate AI from human calibration texts (Orwell 1.15 vs
AI 1.16), so it is not reported.

**2.2 Human baselines (pre-ChatGPT).**
- 16 admitted college essays (Hamilton classes of 2018 and 2022, Connecticut College class of 2025): only
  **5 of 16** under 20% on both detectors; several at 50-95%.
- 18 top-scored student argument essays (PERSUADE 2.0 corpus, grades 8-11): **7 of 18** under 20% on both.
- 3 science explainers from 2020 (Bert Hubert; The Conversation): 2 of 3.
- Pattern: vivid, specific human essays scored low; generic "I learned to be kind" essays scored high.
  **Insight:** these detectors partly detect generic writing.

**2.3 Tasks.** 7 briefs: Common App personal statement and a 250-word short answer for a fictional student
(Inês, from interview notes), 11th-grade argument essay (phones), science-club explainer (mRNA vaccines),
GreenBERT methods section (fact sheet), Gatsby analysis (4 provided quotes only), first-person blog post
(fact sheet). Facts files are the only permitted source of specifics.

**2.4 Conditions.** A = plain Claude (no skill), 2 samples per task. C = the skill's Edit mode applied to A's
sample 1. B = the skill's Write mode, 2 samples per task. All generated by fresh Claude agents.

## 3. Version 1 (skill v1)

**Design:** SKILL.md (hard rules, procedure, modes Write/Edit/Detect/Coach, genre notes, integrity) + four
references (tells, personal-essay, academic, examples). Description 185 characters (claude.ai limit 200).

**Results.**
| Measure | Plain (A) | Skill edit (C) | Skill write (B, v1) |
|---|---|---|---|
| Texts under 20% on both detectors | 7/14 | 4/7 | **14/14** |
| Judge: better writing (vs A) | n/a | **12/14** | **22/28** |
| Judge: more human (vs A) | n/a | 14/14 | 26/28 |
| Unsupported claims (judge-counted, same pairs) | 52 (A vs C), 104 (A vs B) | 14 | 56 |
| Human-likeness, mean of 10 | 5.4 / 5.3 | 7.0 | 7.3 |

- By genre (B vs A, better writing): argument 4-0, explainer 4-0, Gatsby 4-0, blog 4-0, report 3-1,
  short answer 3-1, **personal statement 0-4**.
- Detector drops came from real changes: B's argument essay took a specific position (ban covers lunch and
  passing periods), argued from school mechanics, conceded the lockdown objection; A used "glowing screens",
  a triadic thesis and "not a neutral tool; it is".
- Fact check of B's mRNA explainer: every named fact (Wolff 1990, Karikó & Weissman 2005, 2023 Nobel, 2024 RSV
  approval) correct.
- Edit mode caught A's errors: a Gatsby misquote ("Across the great distance" vs source "Compared to"), invented
  feelings in the personal statement, an invented habit in the blog.

**Why v1 lost personal statements (judges' consistent reasons):** A builds a better arc but invents feelings
and causes ("The shop taught me a different kind of listening", "Sitting across from her, I started
wondering"); v1 refuses to invent and produces "the interview notes reordered", with no reflection, skipped
the most vulnerable material (AP Chem lie), and ended almost every paragraph on a wry kicker.

## 4. Version 2

**Changes (why):**
- Coach mode: no example sentences built from the student's story; grammar as a list of discrete
  corrections (critic agent: LLM edits shift meaning and voice even when told "grammar only"; model-written
  examples homogenize essays).
- Personal-essay reference rewritten: depth questions to draw out the student's own reflections; spine chosen
  by stakes; arc and reflection section; "leave at least a third out"; sample mode: reflection only from the
  student's words.
- tells.md: S11 kicker endings everywhere, S12 staged self-correction, PE9 the over-corrected essay, maxim
  openers ("A rule that… A phone that…").
- Genre notes: explanations (angle, named verifiable examples); AI-use disclosure logging for journals.

**Results.**
- Personal statement v2 vs A: **0-4**; v2 vs v1: **0-2** (worse). Arc score 4-5 vs A's 8.
- Short answer v2 vs A: **0-4** (v1 had 3-1): regression.
- Argument v2 vs v1: 1-1.
- **Coach mode** (new test): critique of a real 186-word application draft rated 9/10 useful, no ghostwriting,
  not preachy; pressure test ("just write it, I'm out of time") 8/10, held the line, mildly preachy.
- All v2 texts under 5% on both detectors.

**Diagnosis:** extra sample-mode rules made the writer cautious; it cut the best material and still produced
kicker endings. Rules stated as guidance ("vary endings") did not change behavior.

## 5. Version 3

**Changes (why):** loosened sample mode (connective observations linking two facts allowed; no "leave a third
out"; uncomfortable material is often the spine); kicker check made countable ("list the last sentence of every
paragraph; if more than two are short or wry, rewrite"); explicit arc check.

**New test design:** the v1/v2 comparison was tilted (plain Claude invents reflection; the skill may not). Wrote
a depth-interview addendum where the fictional student answers the depth questions; both plain Claude (P) and
the skill (W) received the richer notes.

**Results.**
| Comparison | Better writing | More human | Unsupported claims |
|---|---|---|---|
| Personal statement, P vs W (depth notes) | P 4-0 | 2-2 | P 16, W 1 |
| Short answer, P vs W (depth notes) | 2-2 | W 4-0 | P 15, W 6 |
| Personal statement, A vs v3 (original notes) | A 2-0 | v3 2-0 | A 19, v3 0 |
| Short answer, A vs v3 (original notes) | A 2-0 | v3 2-0 | A 7, v3 1 |

- Depth notes reduced plain Claude's fabrication too (3-5 per essay vs 8-11).
- All personal-material texts (plain or skill) under 5% on both detectors.

**Diagnosis:** consistent across v1-v3: the skill's sample essays are more human and more faithful, but less well
built ("walks through the notes in order; climax in paragraph 7 of 9"). Edit mode (draft first, audit after)
had kept the arc (personal statement 1-1, short answer 2-0) with zero unsupported claims.

## 6. Version 4 (shipped to `.claude/skills/anti-ai-writing/`)

**Change (why):** two-pass drafting for personal essays and narratives: pass one writes for shape (arc, turn,
so-what, late climax), pass two runs the full Edit mode on that draft (fact diff cuts invented feelings,
audit passes, kicker count). Rationale: auditing while drafting produced flat essays; edit mode preserved arc.

**Results.**
| Comparison | Better writing | More human | Unsupported claims |
|---|---|---|---|
| Personal statement, P vs v4 (depth notes) | P 3-1 (v3: 4-0) | v4 3-1 | P 19, v4 6 |
| Short answer, P vs v4 (depth notes) | P 3-1 (v3: 2-2) | v4 3-1 | P 15, v4 7 |
| Personal statement, A vs v4 (original notes) | 1-1 (first win for any version here) | v4 2-0 | A 14, v4 4 |

- Arc scores for v4 personal statements 6-7 against plain's 7-8 (v3: 5-6).
- **Decision:** ship v4. Best personal-essay version so far, same rules elsewhere, and its coach mode is the one
  validated in section 4. Sample sizes for personal essays are small (2-4 pairs per cell); phase 2 tests v4 on 8
  personal-essay briefs.
- **Finding for the paper (fidelity–arc tradeoff):** across v1-v4, plain Claude's personal essays win on arc
  because it writes connective feelings and causes the student never stated (3-11 unsupported claims per essay).
  Forbidding that lowers judged arc; two-pass drafting recovers part of it. Depth answers from the student raise
  everyone's quality and cut plain Claude's fabrication by about half.

## 7. Measurement upgrade: third detector

Added D3 = SuperAnnotate/ai-detector (RoBERTa-large; training data includes Anthropic models and RAID; output
capped near 73% by label smoothing). Calibration: human 2.1-3.8%, AI 72.7-73.0%. It scored the 2005 Paul Graham
essay that D2 flagged at 56% as 2.2%. All earlier texts re-scored with D1-D3 (`eval/results/rescore3.json`).

## 8. Phase 2 plan (large evaluation)

20 briefs (4 fictional students × personal statement and short answer with depth notes; 4 argument; 4 explainer;
4 literary analysis with verified Gutenberg quotes) × 5 conditions: P plain; L word-list prompt (the common
"avoid delve, tapestry, em dashes" approach); H blader/humanizer applied to P's draft; E our Edit mode on P's
draft; O our Write mode. Two blind panel judges per brief rank all five; detectors D1-D3 score every text.

---

## Files

- `skill_versions/v1..v4/`: every version of the skill as tested.
- `eval/briefs/`: task briefs, fact sheets, fictional interview notes, Gatsby quotes.
- `eval/out/<condition>/`: every generated text. A = plain, B1/B2 = skill write v1/v2, C1 = skill edit,
  P3 = plain with depth notes, W3/N3 = skill v3 with/without depth notes, X4/Y4 = skill v4.
- `eval/results/`: detector scores (`*_scores.json`), judge outputs (`judges_*.json`), human baseline scores.
- `scripts/`: `score.py` (detectors), `assemble.py`, `judges.py` (tallies), `summarize.py`.
- `notes/`: research notes written by the research agents (our own text; third-party downloads not included).

## 9. Three-detector rescoring (all phase-1 texts and human baselines)

| Group | n | Under 20% on all three | D3 mean |
|---|---|---|---|
| Human admitted college essays (pre-2022) | 16 | **0** | 61.4 (D3 max is about 73) |
| Human PERSUADE argument essays (pre-2022) | 18 | 4 | about 44 |
| Plain Claude (A) | 14 | 5 | 28.5 |
| Plain Claude + skill edit (C1) | 7 | 4 | 17.2 |
| Skill write v1 (B1) | 14 | **14** | 3.5 |
| Skill v2-v4 personal essays | 16 | 16 | 2.4-4.9 |

- **Finding (fairness):** the detector whose training data includes Anthropic models flags every human admitted
  essay and passes every skill-written Claude text: on this genre the detectors invert. Likely cause: personal
  narrative is out of domain for detectors trained on Wikipedia, ELI5, scientific text and RAID; generic,
  polished human prose and template-like structure read as "AI", while concrete, idiosyncratic detail reads as
  "human" whoever wrote it. Paper must state this as a property of these open-source detectors, not of all
  detectors (GPTZero, Turnitin untested).

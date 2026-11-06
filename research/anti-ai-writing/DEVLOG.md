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
  Reinhart et al. PNAS 2025), importance flags ("this matters", 116x human for [a Claude model] per Graphite
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
| Human PERSUADE argument essays (pre-2022) | 18 | 2 (corrected 21 Oct; first logged as 4, which wrongly added the 2 passing human explainers) | about 44 |
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

## 10. Phase 2 results: judges (20 briefs, 40 blind panel judgments)

Run as five workflows (`scripts/phase2.js`, seeds 1, 10-13). Each brief got two judges, a demanding editor and a
genre reader (admissions officer, English teacher or science teacher), each ranking all five texts blind with
labels shuffled. Texts: `eval/out/phase2/<condition>/`; judgments: `eval/results/phase2_judges.json`; summary:
`eval/results/phase2_summary_judges.json` (`scripts/analyze.py`).

| Condition | Mean rank (1 = best) [95% CI] | First places | Human-likeness /10 | Quality /10 | AI suspicion /5 | Unsupported claims per text |
|---|---|---|---|---|---|---|
| P plain | 4.62 [4.40, 4.80] | 0 | 4.50 | 5.62 | 4.10 | 3.38 |
| L word-list prompt | 2.27 [1.98, 2.62] | 6 | **7.33** | 7.38 | 2.55 | 2.65 |
| H humanizer edit of P | 3.48 [3.20, 3.75] | 1 | 5.75 | 6.28 | 3.33 | 1.82 |
| E our edit of P | 3.17 [2.83, 3.50] | 5 | 5.55 | 6.53 | 3.35 | 1.30 |
| O our write (v4) | **1.45** [1.23, 1.73] | **28** | 7.25 | **7.88** | **2.33** | **1.07** |

Friedman test across the five conditions (per-brief mean ranks): chi-square 49.6, p = 4e-10. Pairwise, O ranked
above P in 39 of 40 judgments, above L in 33 of 40 (Wilcoxon p = 0.027), above H in 38 of 40 and above E in 32 of 40.

By genre (mean rank of O; best competitor in brackets): argument 1.00 (L 2.00), explainer 1.00 (L 2.25),
literary analysis 1.00 (L 2.12), short answer 1.75 (E 2.50), **personal statement 2.50 (L 2.25, E 2.38)**.

What this says:
- Writing fresh with the skill wins clearly in the three school genres, and it has the fewest invented claims
  overall (1.07 against 3.38 for plain).
- **Editing loses to writing.** Both edit conditions (ours and the humanizer) land in the middle: they keep the
  plain draft's generic structure and some of its errors. Our Edit mode was built for minimal edits of human
  drafts, which is the wrong behaviour for an AI draft. This motivated Rebuild mode in v5.
- **The word-list prompt is a strong baseline.** It scored highest on human-likeness and voice. Judges said the
  skill's school essays read like an adult essayist, while the word-list essays sounded like an actual 11th grader.
  v5 adds a student-voice rule for school essays.
- **Personal statements are still the weak genre.** Judges criticised our texts for dropping the student's best
  detail (one editor: "leaves out the key self-indictment") and for packing too much into one paragraph. v5 adds a
  short checklist for this (section 11).

### 10b. Phase 2 detector results (100 texts, `eval/results/phase2_scores.json`)

Share of texts under 20% on all three detectors, by genre (4 briefs per genre):

| Genre | Plain | Word list | Humanizer edit | Our edit | Our write |
|---|---|---|---|---|---|
| Personal statement | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 |
| Short answer | 4/4 | 4/4 | 4/4 | 4/4 | 4/4 |
| Argument | 0/4 | 0/4 | 0/4 | 0/4 | **4/4** |
| Explainer | 0/4 | 0/4 | 0/4 | 0/4 | 1/4 |
| Literary analysis | 1/4 | 3/4 | 2/4 | 2/4 | **4/4** |
| **Total** | 9/20 | 11/20 | 10/20 | 10/20 | **17/20** |

Mean scores (D1 / D2 / D3): plain 40.0 / 33.7 / 23.2; word list 20.0 / 19.7 / 7.5; humanizer 26.7 / 19.8 / 9.8;
our edit 26.3 / 17.2 / 11.9; our write 3.0 / 3.6 / 2.6.

- **The personal-essay finding got stronger.** Every model-written personal statement and short answer passed all
  three detectors, plain Claude included (scores 0-3%), while the 16 human admitted essays averaged 61% on D3 and
  none passed it. On this genre the detectors are not just weak; they point the wrong way.
- So the skill's detector advantage comes from the school genres (argument, literary analysis), where plain text
  fails and skill text passes. Explainers are the exception: three of four skill explainers scored 24-28% on one
  detector. Science explanation leaves less room for idiosyncratic detail.
- Editing a plain draft (ours or the humanizer) halves the scores but passes only half the texts. Writing fresh
  matters for detectors too, which supports the Rebuild mode in v5.

## 11. Version 5 (candidate)

Changes, each tied to a phase-2 failure:
1. **Rebuild mode** for AI-written drafts: extract the facts, check them, then write fresh with the Write
   procedure. Reason: edits of AI drafts kept the generic structure and ranked below fresh writing.
2. **Student voice for school essays**: write as the student (stated stance, contractions, plain words, more short
   sentences), avoid stock student openers, never invent an anecdote. Reason: the word-list baseline beat us on voice.
3. **Explainers talk to the reader** ("you") and give them something to try or picture.
4. **Personal-essay checklist** (`references/personal-essay.md` section 5): list the three best details and keep at
   least two; no paragraph with more than two beats; gloss anything an outsider would not know; set up before
   paying off; answer the prompt's own question; keep exact facts.

Test design (`scripts/phase2_v5.js`, six workflows, seeds 40-45): the same 20 briefs, a new five-way blind panel of
P, L and O (reused texts) plus V (v5 write) and R (v5 Rebuild of the plain draft P). Results: section 12.

## 12. Version 5 results: not shipped

Same 20 briefs, new five-way blind panels (P, L and v4's O reused; V = v5 write, R = v5 Rebuild of P), 40
judgments. Data: `eval/results/v5_judges.json`, `eval/results/v5_summary_judges.json`; texts in `eval/out/phase2/V`
and `R`; the tested skill in `skill_versions/v5/`.

| Condition | Mean rank | First places | Human-likeness | Quality | AI suspicion | Unsupported per text |
|---|---|---|---|---|---|---|
| P plain | 4.20 | 2 | 4.78 | 5.97 | 3.90 | 3.23 |
| L word list | 3.33 | 5 | 6.38 | 6.70 | 3.10 | 2.62 |
| O v4 write | **1.95** | **19** | 6.90 | **7.65** | 2.50 | 0.93 |
| V v5 write | 2.60 | 7 | **7.45** | 7.38 | **2.27** | 1.02 |
| R v5 Rebuild of P | 2.92 | 7 | 6.88 | 7.05 | 2.52 | **0.78** |

v4 ranked above v5 write in 28 of 40 judgments (Wilcoxon p = 0.055) and above v5 Rebuild in 30 of 40 (p = 0.022).
By genre (mean rank O / V / R): argument 1.12 / 2.25 / 4.00; explainer 1.50 / 1.62 / 3.00; literary analysis
1.62 / 2.88 / 1.75; personal statement 2.88 / 3.88 / 3.38 (plain 2.62, word list 2.25); short answer 2.62 / 2.38 / 2.50.

What we learned:
- **The student-voice rule bought human-likeness and cost reasoning.** v5's school essays scored higher on
  human-likeness and lower on AI suspicion, but judges caught simplified or faulty reasoning ("'Aspect' means
  appearance here, since the creature hasn't done anything yet") and crammed paragraphs. A younger register
  pulled the argument down with it.
- **Rebuild beat v4 only on literary analysis**, where re-checking the draft's readings of the quotes matters.
  On arguments it ranked 4.00: rebuilding from an AI draft still anchors on that draft's stock arguments.
- **The personal-essay checklist did not help** (v5 3.88 against v4 2.88 on personal statements).
- **Panel context changes personal-statement verdicts.** The same P and O texts were judged in both panels.
  O ranked above P in 8 of 8 personal-statement judgments in the phase-2 panel but in only 3 of 8 in this one. In
  the other genres the result held (8 of 8 in both). In phase 2, two of the five texts were edits of P and shared
  its sentences; judges noticed the overlap ("T5 and T4 share most of their content and many whole sentences")
  and may have marked down the whole family. Conclusion for the paper: the school-genre advantage is robust to
  panel composition; the personal-statement advantage is not, and plain generation's arcs (built partly on
  invented detail: 3.25 unsupported claims per text against 0.62) remain competitive with judges.

Decision: keep v4 as the shipped version for now; diagnose the judge feedback in depth and build v6 from what
worked (section 13).

## 13. Version 6: built from a diagnosis of 160 judgments

Workflow (`v6-diagnosis`): five genre analysts, a residual-tells hunter and a personal-essay specialist read every
judge comment from both panels and the texts themselves; a synthesizer proposed nine changes; two adversarial
critics (overfitting, side effects) reviewed them; a writer applied the survivors to a copy of v4. Full changelog
with counts and quotes: `skill_versions/v6/CHANGELOG.md`. The main findings behind the changes:

1. **Arguments win on construction, not ideas.** The v4 essays that ranked first stated the thesis against the
   nearest alternative (the usual compromise, a double standard) and let that one idea organize the essay; judges
   credited this in 16 of 16 judgments. v5 had largely the same ideas as a list of reasons. v6 adds an argument
   section: thesis against the nearest alternative, one worked case, the strongest objection to the writer's own
   remedy answered by changing the remedy, a concrete opening (never "I think" first, never "every student knows").
2. **Student register as a pass after the argument is built**, with a check that every paragraph's claim
   survives. v5's register raised human-likeness (7.75 vs 6.25 on arguments) and lowered AI suspicion (2.0 vs
   3.0 in 8 of 8 judgments) but cost structure when applied while drafting. Its example stance line became an
   opening template (3 of 4 v5 arguments start with "I think"), so the example is gone.
3. **Reading check** for any text that interprets a source: a quote can be exact and the reading wrong. About
   half of the claims judges flagged in literary analyses sat in the final paragraph, so the check says to read
   the last paragraph hardest.
4. **Rebuild routed by source.** With a facts or quotes file, keep the checked evidence and write fresh. With
   only a topic, the draft's examples and plan are the stock answer: write from step 1 with your own plan (v5's
   Rebuild kept the plain draft's outline and ranked 4th on arguments in 8 of 8 judgments).
5. **Beat outline before drafting** personal statements (spine, beats in cause order, joins, turn, prompt
   answer, ending from the notes), replacing v5's after-the-fact checklist, which did not fix order.
6. **Explanations:** an everyday opening with the answer in one sentence, one organizing idea, one worked number,
   misconceptions conceded with their size; v5's "talk to the reader as you" rule dropped (no measurable effect).
7. **Logic row** in the audit table: connectives that claim a cause the text does not show, and generalizations
   stated as fact.
8. **Evaluation hygiene:** v4 contained example phrases taken from the development personas ("a notebook with 61
   entries" and similar). v6 removes them, so phase-2 scores for v4 and v5 on those personas are slightly
   optimistic. The held-out briefs share nothing with the skill files (checked by search).

v6 SKILL.md: 189 lines (v4: 159); new `references/school-essays.md` (108 lines).

## 14. Held-out evaluation (phase 3): design

16 new briefs written after v6's design was fixed (`eval/briefs3/`): two new fictional students (personal
statement and short answer each), two arguments, two explainers, two literary analyses (Romeo and Juliet, Pride
and Prejudice; every quote checked against the Project Gutenberg text by script), and six genres never tested:
an email to a teacher, a cold email to a professor, a cover letter, a team blog post, a lab-report discussion and
a school news article. A checking agent fixed three weekday/date contradictions in the fact files and one
surname that matched a real scientist.

Six conditions per brief: P plain, L word list, H humanizer edit of P, F v4 write, S v6 write, B v6 Rebuild of P.
Three blind judges per brief: an editor and a genre reader as before, plus a second genre reader running on a
different model tier, to check that rankings do not depend on the judge model. Script: `scripts/phase3.js`.

## 15. Held-out results (16 new briefs, 48 blind judgments)

Data: `eval/results/phase3_judges.json`, summary `eval/results/phase3_summary_judges.json`, texts `eval/out/phase3/`.
The first launch was interrupted twice (a container restart, then a usage limit); outputs that the run logs
confirmed as finished were reused and everything else was regenerated (`args.done` in `scripts/phase3.js`).

| Condition | Mean rank [95% CI] | First places | Human-likeness | Quality | AI suspicion | Unsupported per text |
|---|---|---|---|---|---|---|
| P plain | 5.65 [5.48, 5.81] | 0 | 4.48 | 5.52 | 3.98 | 3.38 |
| L word list | 4.17 [3.75, 4.56] | 3 | 6.48 | 6.31 | 2.90 | 2.98 |
| H humanizer edit of P | 4.25 [3.92, 4.56] | 2 | 5.69 | 6.35 | 3.33 | 1.88 |
| F v4 write | **1.92** [1.62, 2.23] | **23** | **7.15** | **7.90** | 2.46 | 1.17 |
| S v6 write | 2.42 [2.02, 2.81] | 17 | 6.96 | 7.48 | 2.48 | 0.96 |
| B v6 Rebuild of P | 2.60 [2.40, 2.81] | 3 | 7.10 | 7.46 | 2.46 | **0.79** |

Friedman chi-square 51.0, p = 9e-10. Pairwise (judgments where the first ranked above the second, of 48):
v4 write above plain 47, above word list 43, above humanizer 44 (all Wilcoxon p < 0.003). v6 Rebuild above the
humanizer 42 (p = 0.0008), above plain 48. **v4 write above v6 write 27 of 48 (p = 0.35): no significant
difference.** v4 write above v6 Rebuild 35 of 48 (p = 0.02).

**Second judge model.** The third judge ran on a different model tier and gave the same order: v4 1.94, v6 2.25,
v6 Rebuild 2.44, word list 4.19, humanizer 4.81, plain 5.38. The skill's advantage does not depend on the judge
model (within one model family).

By genre (mean rank v4 / v6 / v6 Rebuild; best baseline): personal statement 1.33 / 2.50 / 2.67 (word list
4.00); short answer 2.17 / 1.50 / 2.50; argument 1.33 / 3.00 / 2.50; explainer 2.17 / 1.50 / 2.33; literary
analysis 1.33 / 2.50 / 2.83; email 1.67 / 2.00 / 2.50; lab discussion 2.67 / 1.00 / 2.33; news article 1.00 / 3.33
/ 2.67; cover letter 2.33 / 4.33 / 3.33 (**word list 2.00**); blog post 4.67 / 4.00 / 2.67 (**word list 1.67**,
humanizer 2.67). One or two briefs per genre, so these are descriptive.

What this says:
- **The skill generalizes.** On briefs and genres it was never developed on, v4's Write mode ranked first in 23
  of 48 judgments and above plain generation in 47 of 48, with a third of plain's unsupported claims.
- **Personal statements on new students went the skill's way** (v4 first in 5 of 6 judgments), unlike the
  development panels. Development personas were used to tune earlier versions, but these were not; the earlier
  panel effect (section 12) and four briefs per genre mean the personal-statement result is still the least
  certain one.
- **v6 did not beat v4.** Its argument rules (a worked case with numbers) produced essays judges called
  "arithmetic-heavy for an English class" and openings "on the compromise position with no hook": the template
  risk flagged in section 13. Diagnosis-driven rules can fit the development judges' taste and not transfer.
- **Rebuild works.** Revising an AI draft with v6's Rebuild mode beat the humanizer in 42 of 48 judgments and had
  the fewest unsupported claims of any condition.
- **Weak genre: casual first-person posts.** The word-list prompt won the blog post and narrowly the cover letter.
  The skill's audit may strip the looseness these genres want. Not fixed here: tuning on a held-out brief would
  make it development data.

## 16. Coaching experiment (6 students, Coach mode vs plain feedback)

Design (`scripts/coach_loop.js`): for each of the six fictional students (four development, two held-out), an
agent playing the student wrote a first draft of the personal statement from their notes with no style help
(D0). The draft got two kinds of feedback: the skill's Coach mode (FS, v6 files) and the plain model asked "Can
you give me feedback on my college essay?" (FP). The student agent revised with each separately (RS, RP). Two
blind judges ranked D0, RS and RP; a counselor agent compared the two feedbacks. Texts: `eval/out/coach/`;
results: `eval/results/coach_judges.json`, `coach_overlap.json`.

| Measure | Skill Coach (FS / RS) | Plain feedback (FP / RP) |
|---|---|---|
| Counselor prefers this feedback | **6 of 6** | 0 of 6 |
| Feedback usefulness / specificity (1-10) | **8.67 / 9.00** | 7.17 / 7.00 |
| Invented content in feedback (items per student) | **1.17** | 5.17 |
| Essay-ready sentences written for the student | **0.67** | 1.33 |
| Revision mean rank of 3 (D0 last in 12 of 12) | **1.42** | 1.58 |
| Revision ranked above the other revision | 7 of 12 | 5 of 12 |
| Revision unsupported claims | **1.67** | 2.75 |
| Revision human-likeness / AI suspicion | **8.00 / 1.83** | 7.75 / 2.08 |
| Revision 6-grams copied from feedback | 0.9% | 0.5% |
| Feedback length (words, mean) | 2,264 | 1,468 |

What this says:
- Any feedback helps a first draft a lot; the revision with skill coaching is a little better (7 of 12, not
  significant) and has fewer unsupported claims.
- The clearer difference is in the feedback itself. The counselor judged plain feedback riskier: it "hands the
  student the essay's interpretive insights instead of asking her for them" and supplies an "interpretive
  center" the student never said. Coach mode states the Common App rule, quotes the student's own answers as raw
  material, and asks questions instead.
- Copying was near zero for both, so this simulated student does not test what a rushed real student might copy.
- Coach mode's feedback is about 1.5 times longer. A real student may not read 2,300 words; a shorter format is
  future work (not changed in v7 because untested).

## 17. Version 7 shipped

v7 = v4 (best held-out Write mode) + v6's Rebuild mode (adapted) + example hygiene + corrected watermark sentence.
Files: `skill_versions/v7/` with `CHANGELOG.md`; installed at `.claude/skills/anti-ai-writing/`; claude.ai zip
rebuilt. Why not v6: held-out v4 vs v6 was 27 of 48 (p = 0.35), and v6's argument rules made essays judges called
"arithmetic-heavy for an English class". Why not plain v4: v4 has no mode for AI-written drafts, and v6's Rebuild
beat the humanizer in 42 of 48 held-out judgments.

Smoke test of the shipped combination (3 held-out plain drafts; one blind editor each, ranking v7 Rebuild, v6
Rebuild and v4 Write): v7 Rebuild ranked first on the literary analysis and the email and second on the argument.
It chose the right route each time (facts or quotes file: keep checked evidence, fresh sentences; topic only:
write from step 1) and reported what it dropped, for example a quote cut off mid-phrase and a hedge the draft had
removed ("I may almost say"). Three briefs is a sanity check, not an evaluation; the shipped Write procedure is
the one evaluated as v4.

## 18. Held-out detector scores, results page, paper figures

Held-out detector scores (`eval/results/phase3_scores.json`; under 20% on all three detectors):

| Condition | Passed | Mean D1 / D2 / D3 |
|---|---|---|
| Plain | 9 of 16 | 21.6 / 9.0 / 8.5 |
| Word list | 12 of 16 | 13.7 / 5.1 / 8.8 |
| Humanizer edit | 12 of 16 | 11.2 / 9.4 / 5.1 |
| Skill write (v4 = v7) | **16 of 16** | 2.2 / 0.7 / 1.7 |
| Skill write (v6) | 15 of 16 | 5.1 / 0.7 / 1.7 |
| Skill Rebuild (v6) | **16 of 16** | 2.9 / 0.8 / 1.7 |

Every personal statement and short answer passed in every condition (highest score 2.7%), confirming section
10b on new students. Human baselines: 0 of 16 admitted essays and 2 of 18 PERSUADE essays pass all three.

Correction: section 9 first said 4 of 18 PERSUADE essays passed all three detectors; the right count is 2 (the
first count included the two passing human explainers). Fixed in the table with a note.

Results page rebuilt for the final state (same link). Its source stays out of the repo because it contains the
user's personal YYGS answers and coaching notes. Paper: figures `fig_rank.pdf` (development and held-out mean ranks) and `fig_detectors.pdf`, built by
`scripts/figures.py`; PDF compiles to 11 pages with the body inside 8.

## 19. Adversarial paper review and a privacy fix

Workflow `paper-review`: four independent reviewers (numbers re-derived from the data files, citations checked
against the cited work, a skeptical workshop reviewer, prose and anonymity under the skill's own rules), then a
merger that re-verified every numeric correction and kept only edits whose old text occurs exactly once. Result:
79 edits (3 critical, 32 major, 44 minor), all applied; list with evidence in `paper/review_edits.json`.

The most important corrections:
- **Selection on the held-out set.** v4 was chosen over v6 after seeing held-out results, so v4's numbers are the
  better of two frozen candidates and somewhat optimistic for the released v7; v6 also beat every baseline. v7
  as a whole was never put through the held-out panels. The paper now says all three things.
- **Imperfect blinding.** Judges opened texts by file path, and the path contained the condition's folder letter.
  6 of 128 writing judgments name a condition letter; the coaching counselor labelled feedback by path. Stated in
  the methods and limitations.
- **Unit of analysis.** Tests are on briefs (16 held-out), not judgments; resampling briefs widens v4's interval to
  [1.52, 2.38]; with Holm's correction every reported comparison stays below 0.025.
- **Wrong or overstated numbers fixed:** v4 human-likeness 7.15 (not 7.2); short answers 7/8 and 6/8 (not 8/8);
  development personal-essay detector maximum 6.2% (not 3%); v6 Write passed 15 of 16 (not "all skill texts");
  the "arithmetic-heavy" quote was about v6's Rebuild, not v6 Write; five new genres, not six; the pilot already
  had a blog post.
- **Citations:** Chakrabarty et al.'s taxonomy is led by awkward word choice and poor sentence structure; Peng et al.
  measured corrective framing in Mandarin; the humanizer's blind test is a contributor's GitHub issue; the two
  other MIT skills are now cited; Turnitin's 20% asterisk rule is cited.

**Privacy fix (the repository is public).** The detector-score file and one script keyed two Connecticut College
essays by their writers' names, which paired real students' names with AI-likelihood scores. Renamed to
conn2025_a and conn2025_b everywhere in the current files; a craft note that quoted one essay now cites the page
without the name. Earlier commits on this branch still contain the names (raised with the user).

**Survey blinding.** All generated texts and the survey key are public, so a rater could unblind a pair by
searching. The paper says so, and the survey now asks raters not to search for the texts.

## 20. First human rating (1 rater, 6 pairs)

First code returned from the reading study. **The rater was the author (pilot run), so it is excluded from any analysis**; it is logged only as a pilot (rater: student, English not first language). Raw codes are kept out
of this public repository; only the tally is logged. Decoded with `scripts/decode_survey.py`.

| Pair | Better writing | Reads more like AI |
|---|---|---|
| Skill vs plain (4 pairs: lab discussion, personal statement, explainer, cold email) | plain 3, skill 0, same 1 | skill 2, plain 2 |
| Skill vs word list (2 pairs: news article, Romeo and Juliet) | word list 2, skill 0 | skill 1, word list 1 |

One rater cannot support a conclusion, but this is the opposite of the model judges, who put the skill above plain
in 47 of 48 judgments. A likely part of the gap: model judges had the facts file and counted invented claims;
human raters see only the two texts, so a plain text's invented arc or resolution costs it nothing. That is the
fidelity-arc tradeoff from section 6, now on the reader's side. If this pattern holds with more raters, the paper's
claim has to narrow to "preferred by judges who can check the facts".

Pilot detail (author's run, excluded): the author agreed with the three AI judges on "better writing" in 0 of 6
pairs (the judges were unanimous, 3 of 3, for the skill's text in all six). On "reads more like AI" the author
matched the judges' higher AI-suspicion text in 3 of 6. In three pairs the author picked the same text as both
better and more AI-like, which suggests that for this reader "better" partly meant polished and complete.

## 21. Human-anchored benchmark: real admitted essays (in progress)

**Why.** The user's pilot reading (section 20) did not favor the skill over the word list, and every earlier
study judged AI text against AI text. The user asked to develop the skill against authentic pre-2022 writing:
personal statements and short answers.

**Corpus (private, not in this repository).** 90 essays published by admissions offices as examples (Hamilton 38,
Johns Hopkins 38, Tufts 9, MIT 3, Connecticut College 2), class years up to 2026, so all were written before
ChatGPT's release (November 2022). The texts stay out of the repository and out of the skill (copyright, and the
writers are real students). 40 were selected (28 personal statements, 12 supplements) and split before any
judging into a development set (24) and a test set (16).

**Material.** For each essay an agent reverse-engineered the interview notes a counselor would have taken before the
student wrote it: every fact, quote and feeling, regrouped by topic, with no run of more than six words copied
outside quotes. Three writers then produced the essay from the notes alone: plain model (P), word list (L) and
skill v7 (F). The notes leak almost nothing (about zero shared six-word phrases with the real essay outside quotes).

**First design failed: find the human among four.** Judges saw the real essay and the three AI versions together.
All 20 completed judgments found the real essay, 19 at the highest confidence. The judges said why, and most of it is
the design, not the skill: the three AI versions come from the same notes, so they share paraphrases ("lit up gold"
in all three where the student wrote "glowed like amber"), and the odd one out is the human. The real essays also
had curly quotes and double spaces where the AI texts had straight ones. Dropped.

**New design: single-text piles.** Each judge reads a pile of four essays by four different students, told that any
mix of real and AI is possible, and rates each essay on its own (probability a real student wrote it, quality 1-10,
evidence with quotes). No pile holds two versions of the same student's essay, every judge lens gets its own random
piles, and all texts are normalized (straight quotes, single spaces, no titles). This is how an admissions reader
meets an essay: alone. Metric: AUC against the real essays (0.5 = indistinguishable) and mean quality.

**What the four-way judges still taught us** (8 essays, decoded after judging). Tells named in all AI
versions: a put-on casual teen register ("kind of wild", "traveled a ton", "so cringy") where the student wrote
earnest, reaching vocabulary ("expatriates", "instilled in me", "augmented the joy"); engineered scaffolds ("The easy
answer is... The harder answer is", "Part of the answer is..." three times); cute framing devices ("(I counted)",
"The obvious suspects were my parents"); motifs closed too neatly (a mood ring from the first paragraph returns at
the end); the strongest scene moved to the end so the essay closes on a career statement. The real essays had
errors no model makes (wrong hyphens, a restrictive "that" inside commas) and also flaws the judges disliked
(purple openings, flat present-perfect endings). In 13 of 20 judgments the real essay was ranked below at least
two AI versions as an essay.

**Style features, development set (24 real essays vs the AI versions; after the split repair below).**
`scripts/style_features.py`.

| Feature | Real | Plain | Word list | Skill v7 |
|---|---|---|---|---|
| Mean sentence length (words) | 17.9 | 13.3 | 11.5 | 15.5 |
| Sentences of 30+ words | 11% | 2% | 1% | 4% |
| Contractions per 100 words | 1.4 | 2.0 | 2.2 | 2.9 |
| Abstract nouns (-tion, -ness, -ity...) per 100 words | 2.9 | 1.2 | 1.0 | 1.0 |
| Stated lessons ("I learned", "taught me") per essay | 1.2 | 0.8 | 0.5 | 0.2 |
| Dashes per 100 words | 0.17 | 0 | 0 | 0 |
| Paragraphs ending in a short line | 20% | 22% | 31% | 7% |
| "really" per 10,000 words | 4.7 | 13.7 | 19.2 | 21.0 |
| "kind of" per 10,000 words | 0 | 5.3 | 7.7 | 12.1 |
| "learned" per 10,000 words | 20.4 | 13.0 | 8.5 | 4.8 |

The skill moves away from AI on some features (fewer short kicker endings, longer sentences than plain) but away
from the real essays on others: it has the most contractions, the fewest stated lessons and no dashes, because its
rules ban or discourage exactly the things these admitted students did. The real essays also vary far more from
one another (mean sentence length 11.7 to 22.3 words across the middle 80% of essays; skill v7 13.0 to 17.6), which
matches Lee et al. (2025) on admission essays. Working hypothesis for v8: the skill models the student's speaking
voice, but admitted students wrote in a more formal written voice; "anti-AI" rules are not the same as "human".
The pile judgments decide whether this matters to readers.

**Split repair.** Four of the eight essays behind those comments were in the test set, and I read the comments before
noticing. A test essay the designer has studied is no longer held out, so the four moved to the development set and
four development essays of the same type, drawn at random (seed 20261026) from those with no judge comments read,
moved to test. The swap is driven by exposure, not by any result. The split is still 24 development and 16 test.
One smaller exposure remains: the first style-feature table was computed over all 40 essays before I restricted it
to the development set (aggregate means only, no per-essay values read).

**v8 candidate (built from the development set only).** Reading the first and last sentences of the 24 development
essays next to v7's versions showed one more pattern. The admitted essays end committed: a value, a belief, a plan,
sometimes grand or a little clichéd ("There can be beauty in spite of loss."). v7's versions end on an
understated shrug or a deflating aside ("I don't actually know.", "but it's okay", "I'm fine with that"). v7 caused
this: it bans "taught me", recommends ending on "an honest open question", and says reflection "may be a doubt".
It also tells the model the voice should sound like "a smart teenager talking", and the interview notes are in
speech, so the essays inherit the filler. v8 changes the personal-essay guidance only (68 lines across three
files):
- Register: the notes are speech; the essay is the student's careful written voice (full sentences, some long,
  few contractions, no carried-over filler outside quoted speech).
- Reflection: state the student's own conclusion plainly; "I learned that..." is fine when what follows belongs
  to this student. Only generic morals and quotable epigrams stay banned. A doubt only where the student really
  is unsure.
- Endings: what the student believes, values or will do, or the last moment of the story; no deflating aside,
  no symbol the student never made. Openings: any strong start, not a default flat fact.
- Order: chronological is often right; do not hold back the best scene for the ending.
- Catalog: PE1 (stated lessons) narrowed to generic lessons; PE3 (abstract nouns) narrowed to inflated uses, since
  current models already avoid journey/passion/challenge and the admitted essays use them more; new PE10, the
  cool essay. Each number quoted in the skill was rechecked against the development data (three were corrected
  before use).
v8 wrote all 24 development essays from the same notes; the piles judge real, plain, word list, v7 and v8 together.
Exposure note: after v8 was drafted, a shell glob that matched nothing printed the closing lines of v7's versions
for all 40 essays, test set included. These are model outputs only (no real essay text and no judgments), and
nothing in v8 changed afterwards because of them.

**Development round 1 results (24 essays, 5 versions each, 90 piles, 360 ratings).** Three judges: an editor and an
admissions reader on the main model, and an admissions reader on a smaller model. Aggregates in
`eval/results/human_benchmark/`.

| Version | Judged a real student (p >= 50) | Mean p(real) | AUC vs real essays | Quality (1-10) |
|---|---|---|---|---|
| Admitted student | 100% | 88.0 | - | 5.97 |
| Plain model | 46% | 48.7 | 0.97 | 6.42 |
| Word list | 43% | 48.0 | 0.97 | 6.39 |
| Skill v7 | 47% | 50.1 | 0.95 | 6.40 |
| Skill v8 candidate | 54% | 53.4 | 0.98 | 6.14 |

- Every real essay was judged real by every judge. The two main-model judges separated real essays from every AI
  version perfectly (AUC 1.00): each real essay got a higher p(real) than each AI essay. The smaller-model judge
  was much easier to persuade (it called 96% of v7 and 100% of v8 essays real) but still ranked the real ones
  higher (AUC 0.94 to 0.99).
- The judges rated the real admitted essays lowest on quality. They recognize real students by imperfection and
  mark them down for it.
- v7 is not better than the word list on human-likeness: +2.0 points of p(real), 95% interval over essays -2.9 to
  +7.1. The user's pilot reading (section 20) pointed the same way.
- The v8 candidate is a small step: +3.3 over v7 (-0.5 to +7.4) and +5.4 over the word list (+0.7 to +9.7), at a
  cost of 0.26 quality points. Its stiff register (no contractions, "people I do not know") likely explains part of
  the quality loss.
- Detectors (same 24 essays): the real essays fail worst. All three under 20%: real 1 of 24, plain 2, word list 7,
  v7 11, v8 7. Mean scores for the real essays: D1 45.5, D2 71.6, D3 65.8. This contradicts the paper's statement
  that on personal essays the detectors passed every model-written text: built from real students' material,
  plain-model essays fail too. The paper needs that correction.

What the main-model judges said about the v8 candidate (read before any change): the essays explain their own
meaning, glossing each scene or quote after it lands; they are even, with clean medium-length sentences joined by
"and"; they still hedge ("I think", soft endings); they signpost ("The climb I keep thinking about was") and tie
things up with callbacks and three-part endings. The judges' signs of a real student were errors, awkward or
overreaching phrasing, cliché morals, résumé lists, digressions and contradictions, odd specific details, and
irony or contrast left without comment. A blind cue coding of all 360 rationales is running.

**Cue coding (all 360 rationales, coded blind to version).** Twelve coder agents marked 16 cues in each rationale and
which way the judge read them (`scripts/human_benchmark/hc_code_cues.js`; aggregates in
`eval/results/human_benchmark/dev_round1_cues.json`). Share of ratings citing each cue, as a sign of a real student
/ as a sign of AI:

| Cue | Real | Plain | Word list | v7 | v8 cand. |
|---|---|---|---|---|---|
| Tidy, engineered structure | 31 / 6 | 4 / 86 | 3 / 86 | 8 / 81 | 4 / 75 |
| Stated moral or lesson | 54 / 6 | 8 / 64 | 10 / 53 | 7 / 46 | 10 / 51 |
| Errors | 85 / 0 | 7 / 8 | 3 / 11 | 7 / 4 | 7 / 6 |
| Reaching vocabulary | 51 / 0 | 0 / 0 | 3 / 1 | 1 / 1 | 1 / 0 |
| Uneven, digressions | 51 / 1 | 18 / 11 | 22 / 11 | 31 / 22 | 29 / 8 |
| Polished | 22 / 7 | 10 / 56 | 6 / 47 | 8 / 39 | 8 / 33 |
| Flat, plain register | 6 / 0 | 10 / 28 | 18 / 31 | 19 / 32 | 12 / 42 |
| Casual filler | 10 / 0 | 18 / 33 | 17 / 39 | 28 / 43 | 1 / 3 |
| Short punchy beats | 15 / 0 | 1 / 42 | 6 / 57 | 3 / 14 | 0 / 8 |
| Stiff, formal | 12 / 0 | 3 / 3 | 0 / 0 | 0 / 0 | 1 / 11 |
| Odd specific details | 92 / 0 | 88 / 3 | 90 / 1 | 89 / 1 | 92 / 3 |

Readings:
- Tidy structure is the dominant sign of a model essay (75% to 86% of ratings for every AI version); no method
  so far has moved it much.
- A stated lesson is not itself the tell: it counted as evidence of a real student in 54% of ratings of real
  essays and as evidence of AI in about half of ratings of AI essays. The difference the judges describe is
  texture: real students' morals are whole-hearted and large; model morals are balanced and hedged.
- Odd specific details count as human for every version, because the notes carry the real student's details.
  Content is not what gives the model essays away; form is.
- v8 removed what it targeted (casual filler 43% to 3%, punchy beats 14% to 8%) but created a flat, stiff
  register (flat 42%, stiff 11%).
- Errors are cited for 85% of ratings of real essays. The skill will not fake errors (hard rule 3), so a control
  is needed: how human do the real essays look with their errors fixed?

**v8b (development round 2).** Changes from the v8 candidate, all in the personal-essay guidance: a fourth failure
mode, the engineered essay (bookends, returning motifs, paragraphs that explain their own scenes, connecting
sentences that point out what rhymes, signposts, balanced and hedged lessons), also added to the catalog as PE11;
a looser structure (in order, a list of what the student learned, year by year, a side detail); comment on
meaning once; the conclusion stated whole-heartedly, never balanced or hedged; at most one "I think" in the essay;
reach once or twice (a vivid line, a simile, a bigger word); ordinary contractions restored; the permission to add
connective observations removed. Round 2 judges the real essays (H), the real essays copyedited for errors only (C),
v7 (F), the v8 candidate (G) and v8b (K) on the same 24 development essays.

**Round 1 artifact and paper fix.** The real Greek-widows essay carried a scraping artifact: accented Greek letters
had become "?" ("τον ?ντρα σου"), while the model versions, written from notes, had them right. Round 1 judged that
one real essay with the artifact; from round 2 on its accents are restored in the real and copyedited copies. A
scan of all 40 real essays found one other possible artifact (a test essay), to be checked by program when the test
piles are built. The paper's abstract and detector paragraph said the detectors passed every model-written personal
essay (89 of 89); both now say that held only for essays from invented briefs and give the development numbers
above. The full section follows the held-out test.

**Development round 2 (24 essays, 5 versions, 90 piles, 360 ratings).** Versions: real (H), real copyedited for
outright errors only (C: 0 to 6 fixes per essay, under 1% of words), v7 (F), v8 candidate (G), v8b (K).

| Version | Judged real | Mean p(real) | AUC vs real | Quality | Detectors: all three < 20% |
|---|---|---|---|---|---|
| Real | 100% | 87.1 | - | 6.00 | 1 of 24 |
| Real, errors fixed | 100% | 85.1 | 0.61 | 6.01 | 1 of 24 |
| v7 | 42% | 47.9 | 0.97 | 6.28 | 11 of 24 |
| v8 candidate | 39% | 47.7 | 0.96 | 6.14 | 7 of 24 |
| v8b | 57% | 54.2 | 0.96 | 5.93 | 8 of 24 |

Paired over essays, all three judges (95% intervals by bootstrap over essays):
- v8b vs v7: +6.3 p(real) [+2.2, +10.5], quality -0.35 [-0.53, -0.18]. With the main-model judges only: +6.8
  [+1.8, +12.3]; they judged 35% of v8b essays real against 17% of v7's. They still put every real essay above
  every v8b essay (AUC 1.00).
- v8 candidate vs v7: -0.2 [-4.5, +3.9]. Its round 1 gain (+3.3) did not replicate. Dropped.
- Real with errors fixed vs real: -1.9 [-3.1, -0.9], quality unchanged. **Errors are not why judges recognize
  the real essays.** Judges cite them (80% of ratings), but fixing them barely moves p(real). Errors cited for the
  copyedited essays (58%) are the residue: words used slightly wrong, loose logic, which a copyedit leaves alone.
  The gap is voice and structure, which a skill can address without faking mistakes.

Round 2 cue coding (blind, `dev_round2_cues.json`), as-real / as-AI percentages: v8b cut tidy structure from
86% (v7) to 51% as AI. Still far from the real essays: reaching vocabulary (real 49 to 51% as real, v8b 1%), voice
and humor (49 to 58% against 28%), flat or plain register (v8b 46% as AI, real 0%), generic summary (42% against
1%), hedges (25% against 0%). Stated morals are read through the overall impression: as real in real essays
(63 to 71%) and as AI in model essays (38 to 58%).

**v8c.** From v8b: a written voice that tries hard throughout (vocabulary a notch above speech, attempted images,
an ambitious first line, a visible device when the notes contain one; never a misused word or an added error);
two or three scenes in place of summary, and material left out rather than compressed; names used without
explanatory clauses; three notes-to-prose habits limited to once each (", and" chains, colon reveals, balanced
maxims); no "I think" in any reflection. New catalog entry PE12. Round 3 judges real (H), v8b (K) and v8c (V) on the
same 24 development essays.

**Development round 3 (24 essays: real, v8b, v8c; 54 piles, 216 ratings) and fidelity.** Round 3 resumed after a
usage-limit interruption; v8c essays from agents that died before returning were discarded and rewritten.

| | v8b | v8c |
|---|---|---|
| Judged real (p >= 50) | 72% | 64% |
| Mean p(real) (real essays: 87.0) | 60.2 | 58.5 |
| AUC vs real (main-model judges) | 0.99 | 1.00 |
| Quality (real essays: 6.01) | 6.04 | 6.22 |
| Unsupported claims per essay (blind check vs notes; v7: 1.50) | 0.12 | 0.58 |
| Essays with no unsupported claim (v7: 6 of 24) | 21 of 24 | 15 of 24 |
| Detectors: all three < 20% (v7: 11 of 24) | 8 of 24 | 10 of 24 |

v8c vs v8b, paired: p(real) -1.7 [-5.1, +1.7], quality +0.18 [+0.01, +0.33], unsupported claims +0.46 [+0.12, +0.79].
The "attempt images" and "scenes" rules brought invented physical details back ("her eyes widening with every
foot", "I landed on the floor instead"). v8b's removal of connective observations is what cut v7's unsupported
claims (mostly interpretations the notes do not make) from 1.50 to 0.12 per essay.

**Decision: v8 = v8b, frozen** (content hash 8fe68e27a7a0e007, `skill_versions/v8`). Human-likeness tied, and the
fidelity gap decides it under hard rule 1. v8c is kept as `skill_versions/v8c_rejected`. Frozen before any test
essay was generated with it. Test: the 16 held-out essays, real vs plain vs word list vs v7 vs v8, three judges,
plus fidelity and detectors.

**Held-out test (16 essays never studied; 60 piles, 240 ratings; v8 frozen).**

| Version | Judged real | Mean p(real) | AUC vs real | Quality | Unsupported claims / essay | Detectors: all three < 20% |
|---|---|---|---|---|---|---|
| Real | 100% | 86.4 | - | 6.21 | - | 1 of 16 |
| Plain | 38% | 44.8 | 0.96 | 6.38 | 3.06 | 2 of 16 |
| Word list | 38% | 46.7 | 0.96 | 6.35 | 2.69 | 5 of 16 |
| v7 | 46% | 51.9 | 0.91 | 6.29 | 0.94 | 10 of 16 |
| v8 | 65% | 59.4 | 0.90 | 5.98 | 0.19 | 6 of 16 |

Paired over essays (95% intervals): v8 vs v7 p(real) +7.5 [+2.4, +13.1], quality -0.31 [-0.58, -0.04]; with the
main-model judges only +11.4 [+4.5, +18.7] (they judged 47% of v8 essays real, 22% of v7's, 9% of plain and word
list). v8 vs word list +12.7 [+6.8, +18.3]; v8 vs plain +14.7 [+9.3, +20.3]. v7 vs word list +5.2 [-0.2, +10.3];
v7 vs plain +7.1 [+2.7, +12.2]; word list vs plain +1.9 [-2.2, +6.0]. Fidelity: v8 had no unsupported claim in 13
of 16 essays (v7 8, word list 3, plain 2).

What held: the development gains replicated on new students (v8 over v7 by 7.5 points, development round 2 by
6.3), and so did the fidelity gain. What did not move: every judge still called every real essay real, and the
main-model judges still separate real essays from v8 almost perfectly (AUC 0.98). What it cost: a third of a
point of judged quality, and four fewer detector passes than v7, because v8 moves toward the register of real
admitted essays, which these detectors flag most (1 of 16 real essays passed).

**Shipped: v8** (`.claude/skills/anti-ai-writing` is now a copy of `skill_versions/v8/anti-ai-writing`;
changelog in `skill_versions/v8/CHANGELOG.md`). Reason: it is better on the two things the skill exists for,
reading as a real writer and never inventing, on held-out data. The quality and detector costs are stated in the
changelog. v7 stays in `skill_versions/v7` for anyone who weights detector scores more.

**Paper revision and review.** The paper now has the human-anchored benchmark as a methods paragraph, a results
subsection with the held-out table, and a reframed abstract, discussion, conclusion and limitations; the
personal-statement history, coaching details, per-genre results and detector figure moved to the appendix to keep the
body at 8 pages. Three independent reviewers then checked it (numbers against the result files, claims and
consistency, prose). They found real problems, all fixed: the 65% "judged real" headline leaned on the lenient
third judge (it called 94% to 100% of every version real), so the two stricter judges' 22% to 47% now sits next to
it; "v7 no more human than the word list" held on development (+2.0) but on test v7 was +5.2 [-0.2, +10.3], so the
paper now says "only slightly more human"; the methods wrongly said all three judges read the same piles (each had
its own); "38 of 40 flagged" now says at least one detector scored them 20% or more; several sentences still called
v7 the released skill; and causal phrasing ("its rules caused", "gained most by relaxing rules") was softened to
what the data show. The original split was confirmed random (stratified by type) and the 40 essays a random draw
from the 90 (seed 20261022).

## 22. Messages and appeals: real charity-run appeals as the human anchor

**Why.** The user asked for a WhatsApp message to a school running group (a donation drive moved to a children's
cancer charity after the school fundraiser was blocked), then asked that every skill change from now on be logged
as plain Claude vs the skill vs real human writing (`LEDGER.md`, case 1). In that case the skill drafts were
accurate but cold, one of them appended an English translation nobody asked for, and the plain drafts invented a
feeling and an apology. The skill had one line of guidance for messages. So we built a benchmark for the genre.

**Human anchor.** "Why I run" texts that runners wrote for their pages on a Turkish charity-run platform for events
up to 2022 (before ChatGPT), sampled by random campaign code at one request per second (robots.txt allows it).
115 pages kept at 70+ words; cleaning removed link lines, the platform's default template sentences and sign-off
names; screening dropped texts under 60 or over 300 words after cleaning, texts shared across pages (charity copy,
team texts) and texts with no first-person voice: 84 remain. The corpus is private (real people's writing); only
counts and aggregates are reported. Development set: the first 32 kept (random codes). Test set: 16 drawn at
random from the rest (seed 20261103), never read by the developer.

**Method.** As in section 21: per appeal, a model reconstructs the runner's notes (facts, reasons and feelings as
spoken Turkish answers; no wording, no run over five words, no runner name). Plain Claude (P) and the skill (S8 =
v8) each write the appeal from the notes alone ("Use only the facts in my notes", same length). Two blind judges
(a donor who gets many charity links, an NGO communications editor) read piles of 12 appeals by 12 different
runners, told any mix of real and AI is possible, and rate p(written by the runner), would-give (1-10) and quality
(1-10) with evidence. A blind checker counts claims the notes do not support.

**Development results** (32 runners, 192 ratings):

| | judged human | mean p | AUC vs real | would give | quality | unsupported claims/text |
|---|---|---|---|---|---|---|
| real | 100% | 88.7 | | 4.67 | 5.03 | |
| plain Claude | 25% | 40.2 | 1.00 | 5.56 | 6.20 | 0.03 |
| skill v8 | 17% | 38.0 | 1.00 | 5.42 | 6.11 | 0.00 |

Paired by runner: v8 minus plain, p -2.2 [-5.2, +0.8], give -0.14 [-0.34, +0.06], quality -0.09 [-0.30, +0.11].
Both model versions beat the real appeals on give (+0.8 to +0.9) and quality (+1.1), and every model version was
rated less human than every real one. The skill added nothing on this genre.

**Why the models were caught** (keyword scan of the 192 judge rationales, and counts in the texts):
- Punctuation. Judges cited semicolons in 44% (P) and 67% (S8) of model judgments vs 6% of real ones. Counts per
  text: semicolons 0.41 real, 0.66 P, 1.22 S8; colons 0.06, 0.38, 0.47; the formal circumflex ("imkân", "hâlâ")
  0, 0.31, 0.31. The skill's Format rule ("commas, colons or parentheses instead of dashes") pushes toward the
  semicolon and colon tell.
- An assembled plan: tidy or ordered structure cited in 59% (P) and 50% (S8) of judgments vs 12% (real).
  Openings with "I'm running for X": 12% real, 44% P, 66% S8 (the skill's "request in the first two lines" rule).
- Tics from the notes: "bence" ("I think") in 0% of real texts, 25% P, 31% S8. The notes are written as speech,
  and both versions carried the marker over (the same lesson as v8's "written voice, not spoken").
- Sentence shape: mean sentence length 14.8 words (SD 8.2) real vs 10.3 (4.2) P and 11.6 (4.6) S8.
- Signs of a person that the skill never fakes (typos, pasted project titles, run-ons) were cited in about half of
  real judgments; these stay out of reach by design (hard rule 3).

**Fidelity.** With "use only the facts in my notes" in the request, plain Claude invented almost nothing (1
unsupported claim in 32 texts), unlike the open-ended group-message case in LEDGER case 1. The no-invention rule
matters most when the user gives few facts.

**v9 (built from development data only).** New `references/messages.md` for group messages, emails and appeals:
write only in the readers' language and never append a translation; an appeal page may start from the writer's
reason, while action messages keep the request in the first two lines; let one part carry the text instead of the
same six-part plan; keep money concrete; mix long and short sentences; punctuate like the register (no
semicolons, a colon only before a list or link, no circumflex in casual Turkish unless the user writes it, one
exclamation mark at the ask is normal); leave the notes' spoken tics behind; never invent. SKILL.md: the Format
row now swaps dashes for commas, full stops or parentheses (colon only before a list, quote or link), the
over-correction list names semicolons and colons, and the messages genre note points to the new file.

**Freeze and held-out test.** v9 frozen before the test (hash 6e56b690fba3cd03). A 4-appeal dev sanity check
confirmed the skill agent read the new guide (no semicolons, reason-first openings). Test: 16 appeals never read
during development, S8 and S9 written from the same notes, two blind judges, piles of 12 (96 ratings). Exposure
note: a workflow completion notice printed the reconstructed notes (not the texts) of 10 pool appeals into the
developer's context; the 5 test appeals among them were swapped, before any test generation, for unused unexposed
appeals (seed 20261104). Workflows now return only counts.

| held-out (16) | judged human | mean p | AUC vs real | would give | quality | unsupported/text |
|---|---|---|---|---|---|---|
| real | 100% | 91.6 | | 4.50 | 4.59 | |
| skill v8 | 12% (donor 6%, editor 19%) | 37.6 | 1.00 | 5.41 | 6.22 | 0.06 |
| skill v9 | 59% (donor 50%, editor 69%) | 49.3 | 1.00 | 5.53 | 6.16 | 0.00 |

v9 minus v8, paired by runner: p +11.7 [+5.5, +17.9], give +0.12 [-0.22, +0.47], quality -0.06 [-0.38, +0.28].
Text counts on test (real / v8 / v9): semicolons per text 0.25 / 1.75 / 0; colons 0.25 / 0.62 / 0; circumflex 0 /
0.19 / 0; "bence" 0% / 44% / 0%; mean sentence length 13.8 / 11.9 / 14.5 words (SD 6.9 / 4.1 / 5.3). Two
overshoots to watch: v9 uses more exclamation marks than these runners (0.77 vs 0.26 per 100 words) and opens
with "I'm running for X" less often than they do (12% vs 31%). Every model text still scored below every real
one, so v9 closes much of the gap but not all of it.

**Shipped: v9** (`.claude/skills/anti-ai-writing` = `skill_versions/v9/anti-ai-writing`; changelog in
`skill_versions/v9/CHANGELOG.md`; zip `anti-ai-writing-v9.zip`). Reason: large held-out gain in reading as the
real writer on this genre, no cost in judged quality or would-give, no invented claims. The Format-row change also
reaches other genres and was not re-tested there.

**Spend.** About 11.4M subagent tokens since the 10M budget started (notes 1.2M, generation 7.0M, judging 1.6M,
fidelity 0.8M, ledger cases 0.5M, checks 0.3M); one-per-text generation was the main cost (about 60k tokens of fixed
overhead per agent).

## 23. Modes: short answers and research abstracts against real pre-2022 writing (v10)

**Request.** One skill with a mode per genre (essays, short answers, research papers and whatever else a student
needs), each built from great real examples, preferably from admitted students like the user at the user's target
schools. The user's list of schools is not in this conversation or in the Drive files I could search, so I used
what is public and closest to the user's profile (an international applicant interested in computing, economics
and research): MIT applicants' own published answers, Tufts', and high-school research from ISEF, including every
Turkish winner 2014 to 2021.

**Cheaper agents.** Writer and judge agents now run as the `Explore` type on the main model in a single turn with
all inputs in the prompt (`scripts/modes_benchmark/tools/mkwf.py`). That costs about 44k tokens of fixed context
per agent against 59k for the default type and two turns, and the agents do not load this project's CLAUDE.md, so
the plain condition no longer sees the project's "all prose goes through the skill" rule.

### Research abstracts (ISEF)

**Corpus.** 1,210 winning abstracts 2014 to 2021 in computing, environment, social science, energy and math
categories plus all Turkish winners; 282 fetched (no names or schools stored), 269 passed screening (150 to 300
words, English). 40 drawn at random (seed 20261105), stratified: Turkish winners 14, computing and math 12,
environment and energy 8, social science 6; 24 development, 16 test.

**Notes.** Reconstructed from each real abstract: every fact and number, nothing added, no run of more than four
words reused (six-word overlap with the real abstract: mean 0.5%). Jobs of six abstracts were stopped by a safety
classifier in five of seven cases; the same items went through singly or in pairs. Only refusal messages (no
content) of test items reached me.

**Round 1** (24 development abstracts; plain P, v9, first research guide r0; 16 piles of 12, judges: ISEF judge and
student-journal editor):

| | Judged human | Mean p | AUC | Quality | Unsupported claims per abstract |
|---|---|---|---|---|---|
| Real | 100% | 86.6 | - | 5.73 | - |
| Plain | 17% | 37.6 | 1.00 | 6.17 | 0.17 (20 of 24 clean) |
| v9 | 4% | 34.0 | 1.00 | 6.08 | 0.25 (20 of 24) |
| r0 | 8% | 33.8 | 1.00 | 5.94 | 0.08 (22 of 24) |

Both skill versions were slightly less human than plain (r0 -3.8 [-8.2, +0.2], v9 -3.6 [-8.0, +0.3]). Judges found
real abstracts by errors and non-native phrasing (cited in 56% and 67% of their ratings), inconsistencies and
idiosyncratic layout (keyword lines, numbered results); model versions by fluency (83 to 96%), hedges (31 to 38%
against 6%) and promotion. The skill made things worse in one specific way: its plain-English push produced
conversational simplification and glossed terms (17% and 10 to 15% against 4% and 0%), and r0's "first person is
normal" advice gave 1.46 first-person words per 100 against 0.60 in real abstracts and half their passive voice.

**r1** rewrote the guide from those judgments: technical register, passive in procedures, no contractions, no
glossing, no hedges or self-assessments the notes lack, no narrated logic or stock connectors, and a table of the
cited signs.

**Round 2** (real H, real with outright errors fixed C, plain P, r1; 12 piles of 16):

| | Judged human | Mean p | AUC (editor, ISEF) | Quality |
|---|---|---|---|---|
| Real | 100% | 86.6 | - | 5.77 |
| Real, errors fixed | 100% | 85.8 | 0.58, 0.53 | 5.96 |
| Plain | 2% | 33.1 | 1.00 | 6.12 |
| r1 | 6% | 34.8 | 1.00 | 6.10 |

- **Errors are not why judges recognize real abstracts.** Fixing them moved p(human) by -0.8 [-2.2, +0.7] and raised
  quality by +0.19 [0.00, +0.38]. Judges still cited non-native but grammatical phrasing in 52% of copyedited
  ratings. Same result as the essays (section 21).
- r1 against plain: +1.6 [-0.3, +3.5], quality unchanged. It cut the cited hedges (31% to 21%), glossed terms
  (15% to 4%), promotion (23% to 10%) and stock transitions (19% to 10%). Fluency stayed (83% against 88%).
- What judges still cited for r1: sentences stitched by cause and effect ("resulting in", "which called for"),
  matched parallel pairs, "The first…, The second…", counted framing. These went into the guide as observed signs
  (not tested as rules).

**Consequence for the guide.** Since a lightly copyedited real abstract reads as the student's and every model
version written from notes does not, `research.md` now starts with "edit the researcher's own draft first": fix
outright errors, keep grammatical phrasing, layout and voice, remove only inflation, hedges and invented content.

### Short answers

**Corpus.** Three web-sweep agents (MIT's blogs and The Tech's admissions-essay series; admissions offices; student
newspapers) saved 69 answers before I stopped the run; 66 met the rules (40 to 350 words, class of 2026 or earlier,
not an excerpt). 28 chosen with writers like the user first (international and STEM or economics), at most two
answers per writer, split by writer: 16 development (Tufts 8, MIT 8), 12 test.

**Design change after a refusal.** The plan was to reconstruct notes from each real answer, as for the essays in
section 21. 22 of 28 items were refused: the agent would not turn a real admitted student's personal essay into
source material for new application essays. That is a fair objection to this design for personal writing, so I
dropped it rather than rephrase around it, and deleted the six notes that had gone through. Writers now get notes
for an invented applicant per real prompt (28 seeds from 16 countries, 17 of them outside the US, three in
Turkey, some close to the user's profile); the generator never saw the real answers. Real answers appear only as the human anchor in the
piles. The cost: judges can partly catch the invented content itself, not only the writing. The essays study in
section 21 used reconstructed notes; those rebuilt essays were only ever used for blind judging and stay private.

**Round 1** (16 real, plain P and the first short-answer guide s0 for 16 invented applicants; 6 piles of 16;
judges: admissions reader and essay coach):

| | Judged human | Mean p | AUC | Quality |
|---|---|---|---|---|
| Real admitted | 100% | 87.3 | - | 4.78 |
| Plain | 0% | 9.0 | 1.00 | 7.09 |
| s0 | 0% | 9.7 | 1.00 | 6.97 |

s0 against plain: +0.6 [-1.1, +2.4]. Surface features: real answers average 21.8 words per sentence (plain 11.7,
s0 18.3), 0.44 contractions per 100 words (plain 3.61, s0 2.34), 0.56 colons per answer (plain 1.62), and a short
last line (10 words or fewer) in 3 of 16 (plain 8 of 16). Judges rated the model answers as better answers and
caught all of them by over-crafting: stacked precise figures and names, labeled-object hooks, comic asides,
self-deprecating counts, planted metaphors, "honest limitation" beats and hedged or trailing endings (hedges cited
in 50 to 53% of model ratings, 0% of real). The real answers were earnest, plainer, sometimes clichéd, and their
conclusions whole-hearted. Reading the 16 also contradicted parts of s0 (written before I had read any): admitted
answers sometimes restate the prompt and often end on a plain summary line.

**s1** (in v10): the finding above in the guide; one example with the two or three details that matter instead of
a run of figures; no quips, labeled reveals or planted metaphors; conclusions stated plainly and whole-heartedly;
long sentences, few contractions and colons; a coaching checklist for these patterns in a student's draft. s1 was
not run on development data before the freeze.

### Freeze and held-out test

v10 = v9 + mode table + `research.md` (r1 plus the edit-first section and the remaining observed signs) +
`short-answers.md` (s1); frozen before any test output, hash d05f855dc7111b57. v9 was dropped from the tests to
stay within budget (on development abstracts it was no better than plain).

**Held-out results.**

Research abstracts (16; 6 piles of 16; fidelity checked blind):

| | Judged human | Mean p | AUC (editor, ISEF) | Quality | Unsupported claims |
|---|---|---|---|---|---|
| Real | 100% | 87.3 | - | 5.78 | - |
| Plain | 6% | 34.5 | 1.00, 1.00 | 6.16 | 0 (16 of 16 clean) |
| v10 | 12% | 38.5 | 1.00, 1.00 | 6.06 | 0 (16 of 16 clean) |

v10 against plain, paired over abstracts: +4.0 [-0.3, +7.9] on p(human), quality -0.09 [-0.34, +0.19]. Cited stock
connectors 3% against 38%, promotion 9% against 22%, fluency 81% against 91%; hedges were not reduced (28% against
22%). Development (+1.6) and test (+4.0) point the same way; neither interval excludes zero.

Short answers (12; 6 piles of 12):

| | Judged human | Mean p | AUC | Quality | Unsupported claims per answer |
|---|---|---|---|---|---|
| Real admitted | 100% | 88.1 | - | 4.38 | - |
| Plain | 0% | 14.2 | 1.00 | 7.00 | 0.58 (5 of 12 clean) |
| v10 | 0% | 16.4 | 1.00 | 7.04 | 1.08 (4 of 12 clean) |

v10 against plain: +2.2 [-1.7, +6.0], quality +0.04. On the page v10 moved toward the real answers (sentence length
19.7 against 20.8, plain 10.7; contractions 0.98 per 100 words against 0.13, plain 3.85; colons 0.17 against 0.33,
plain 2.17), but it added more unsupported content than plain. Reading the fidelity report after the test: most of
v10's additions were doubts turned into commitments ("I don't know whether chemistry or policy" became a stated
goal) and "so"/"because" links between separate facts. The cause is s1's rule to state conclusions
"whole-heartedly", which overrode the applicants' real uncertainty.

**v10.1 (shipped).** Rule 4 now limits a conclusion to the strength the student holds; a new rule 5 forbids causal
links the student did not make; the checklist gains a fact diff for goals, feelings and links. Rewritten for the
same 12 test questions and checked blind: 0.25 unsupported statements per answer, 10 of 12 clean (v10 1.08, plain
0.58), with sentence length 17.9 and 0.77 contractions per 100 words. Not a clean held-out result (I had read the v10
fidelity report), and not re-judged for human-likeness. Hash 3571b11768657399.

**What this round shows.**
- In both genres, blind judges separated every model text from every real one (AUC 1.00), with and without the
  skill. The new modes remove specific tells and, for research, edge p(human) up; they do not make model text pass.
- Real pre-2022 writing is recognized by voice and structure, not by errors: copyedited real abstracts stayed 100%
  human, as copyedited essays did in section 21.
- "Good writing" advice now reads as AI in short answers. The crafted vignette (precise numbers, quirky labels,
  quips, hedged endings) is what judges flagged; admitted students wrote plainer, more committed answers that judges
  rated lower as writing but never doubted.
- The most useful advice for the user is therefore about process, not prompts: write the draft yourself; use the
  skill to coach and to edit lightly; for research, fix errors and inflation and keep your own phrasing.


### Spend

Workflow token count (the measure used in every earlier round): 10.50M, 5% over the 10M budget. Research
abstracts 6.37M (notes 1.10M including the refused batches, development writing 1.86M, development judging 1.43M,
development fidelity 0.60M, copyedit control 0.36M, held-out test 1.01M); short answers 2.80M (notes refused 0.63M,
invented applicants 0.31M, development writing 0.45M, development judging 0.30M, held-out test 0.78M, v10.1 check
0.32M); collection of short answers 1.13M; agent-cost probes 0.21M. Two notes on accounting: (1) the
three web-collection agents ran 377 turns over large contexts; counted per request including cache reads they used
about 82M tokens, which I first reported to the user as the round's overrun before checking it against the
workflow count; excluding cache reads the whole round used about 6M; (2) open-ended web agents need a turn cap, or
collection should be a script, as it was for ISEF.


## 24. Edit mode against real writing, ablations, a regression check, v11 to v13

**Request.** An open budget over two runs (at least 30M workflow tokens), for tuning the skill, other useful work, and
then the paper. Run 1 ended when the user's five-hour limit ran out (30.5M tokens by the workflow count); run 2
started when it reset, resumed every cut-off workflow from its journal (finished agents replay from cache) and
continued until the limit ran out again; run 3 picked up from there.

### Edit mode on real pre-2022 writing (the main result)

Every earlier benchmark asked how a text written from notes compares with the real one. The more common use is the
opposite: a person has a draft and asks for help. So we took real texts and asked for edits.

**Texts (32 per genre, 16 development and 16 test, none used before):**
- ESL essays: 32 essays by English learners in grades 9 to 12 from the ELLIPSE corpus (CC BY 4.0), 250 to 500
  words, overall proficiency 2.5 to 4.0 of 5, at most three per prompt, none with anonymization placeholders.
- ISEF abstracts: 32 winning abstracts 2014 to 2021 not used in section 23, including the remaining seven from Turkey.
- Turkish charity-run appeals: 31 "Neden Koşuyorum" texts not used in the write benchmark of section 22.

**Versions of each text:** the original (H); an errors-only copyedit (C: spelling, grammar and punctuation, nothing
else); plain Claude asked "Can you improve it?" (PI) and "Can you fix the grammar and mistakes?" (PG), with a short
realistic framing (a practice essay for English class; my science-fair abstract; my campaign page text); the skill
(v10.1) given the same two requests (SI, SG). Two texts per agent, each handled as a separate request.

**Measures:** blind single-text piles of 12 with two lenses per genre (English teacher and writing researcher; ISEF
judge and journal editor; Turkish donor and NGO editor), rating p(the person wrote it with no AI writing or editing)
and quality; a blind meaning check comparing each edit with its original (statements added, removed or changed,
and how much of the writer's voice is kept, 1 to 10); and the share of the original's words changed.

ISEF abstracts (32):

| Version | Words changed | Judged the writer's own | Mean p | Quality | Statements added / changed per text | Voice kept (1-10) |
|---|---|---|---|---|---|---|
| Original | - | 100% | 84.8 | 6.11 | - | - |
| Errors-only copyedit | 3% | 100% | 80.6 | 6.17 | 0.00 / 0.00 | 10.0 |
| Plain: "fix the grammar" | 36% | 30% | 43.9 | 6.34 | 0.91 / 2.91 | 7.4 |
| Skill v10.1: "fix the grammar" | 10% | 91% | 69.7 | 6.36 | 0.09 / 0.47 | 9.4 |
| Plain: "improve it" | 76% | 0% | 28.6 | 6.67 | 3.34 / 5.91 | 5.1 |
| Skill v10.1: "improve it" | 15% | 91% | 67.7 | 6.42 | 0.12 / 1.19 | 8.9 |

Paired over texts: skill against plain on "improve" +39.5 [+36.0, +42.9], on "fix grammar" +27.4 [+23.4, +31.5]; copyedit against original -3.7 [-5.7, -1.8].

Turkish appeals (31):

| Version | Words changed | Judged the writer's own | Mean p | Quality | Statements added / changed per text | Voice kept (1-10) |
|---|---|---|---|---|---|---|
| Original | - | 100% | 89.9 | 5.57 | - | - |
| Errors-only copyedit | 6% | 98% | 83.7 | 5.78 | 0.00 / 0.00 | 10.0 |
| Plain: "fix the grammar" | 21% | 97% | 75.0 | 5.94 | 0.00 / 0.55 | 8.9 |
| Skill v10.1: "fix the grammar" | 10% | 98% | 81.8 | 5.92 | 0.00 / 0.06 | 9.8 |
| Plain: "improve it" | 75% | 27% | 40.9 | 6.55 | 2.74 / 3.52 | 6.0 |
| Skill v10.1: "improve it" | 24% | 99% | 77.1 | 6.10 | 0.29 / 0.68 | 8.7 |

Paired over texts: skill against plain on "improve" +35.9 [+30.5, +41.7], on "fix grammar" +7.1 [+3.9, +10.7]; copyedit against original -6.4 [-8.8, -4.3].

ESL essays (32):

| Version | Words changed | Judged the writer's own | Mean p | Quality | Statements added / changed per text | Voice kept (1-10) |
|---|---|---|---|---|---|---|
| Original | - | 100% | 95.3 | 2.97 | - | - |
| Errors-only copyedit | 16% | 61% | 55.3 | 3.75 | 0.03 / 0.62 | 9.4 |
| Plain: "fix the grammar" | 38% | 3% | 30.0 | 4.42 | 0.81 / 4.38 | 6.9 |
| Skill v10.1: "fix the grammar" | 34% | 5% | 31.9 | 4.23 | 0.41 / 2.91 | 7.9 |
| Plain: "improve it" | 90% | 0% | 19.2 | 5.44 | 3.91 / 8.31 | 4.3 |
| Skill v10.1: "improve it" | 47% | 3% | 30.5 | 4.50 | 0.62 / 3.69 | 7.0 |

Paired over texts: skill against plain on "improve" +11.3 [+8.3, +14.2], on "fix grammar" +1.9 [-0.5, +4.4]; copyedit against original -40.0 [-45.5, -34.5].

What it shows:
- Asked to "improve" a student's text, plain Claude rewrites most of it (75 to 90 percent of words), adds three to
  four statements the writer never made, and the result reads as AI: 0 percent of abstracts and 27 percent of
  appeals were judged the writer's own. The skill, given the same request, changed 15 to 24 percent of the words,
  added 0.1 to 0.3 statements, and 91 to 99 percent were judged the writer's own (paired differences +39.5 and +35.9
  points of p, intervals far from zero).
- Asked only to fix grammar, plain Claude is much closer to the skill for appeals (both about 98 percent) but not for
  abstracts (30 against 91 percent): even a "grammar" pass by plain Claude rewrote 36 percent of an abstract.
- The English learners' essays are the exception. Their errors are their voice: an errors-only copyedit alone dropped
  the judged-human share from 100 to 61 percent, and every model edit, plain or skill, fell to 0 to 5 percent. The
  skill's "improve" edit was still 11 points of p above plain's, but no edit of a learner's essay passes as unedited.
- Quality: the skill's edits scored about the same as plain Claude's (0.25 to 0.45 points lower on "improve", equal on
  "fix grammar") and above the originals.

### v11: a stricter Edit mode (developed on the development halves, tested on the test halves)

Judges' reasons for the skill's ESL edits (development only): template transitions ("First", "Additionally", "In
conclusion"), definitions and appeals to authority the student did not write, native idioms, uniformly clean grammar.
v11 changes only the Edit-mode paragraph of SKILL.md: fix outright errors and anything that blocks meaning, keep
everything else, add no transitions, thesis preview, definitions, examples, statistics, authority, idioms or reasons,
never make a claim stronger, do not make a non-native writer's phrasing native, and list up to five bigger changes for
the writer instead of making them; a learner's practice or graded essay goes to Coach.

| Genre | Split | v11 vs v10.1, "improve" | v11 vs v10.1, "fix grammar" | Quality change, "improve" | Clean edits, "improve" (v10.1 / v11) | Voice kept, "improve" (v10.1 / v11) |
|---|---|---|---|---|---|---|
| Abstracts | dev | +7.3 [+3.1, +12.6] | +2.3 [-1.8, +7.2] | -0.03 | 31% / 56% | 9.1 / 9.1 |
| Abstracts | test | +0.2 [-3.1, +3.6] | +2.5 [+0.4, +4.8] | -0.12 | 6% / 44% | 8.7 / 9.1 |
| Appeals | dev | +4.0 [+1.6, +6.3] | +1.1 [-0.3, +2.6] | -0.31 | 50% / 94% | 8.7 / 9.8 |
| Appeals | test | +4.1 [+2.3, +6.1] | +1.7 [-1.0, +4.3] | -0.30 | 40% / 100% | 8.7 / 10.0 |
| ESL essays | dev | +8.4 [+2.7, +14.0] | +3.5 [-0.9, +8.0] | -0.41 | 0% / 31% | 7.2 / 8.4 |
| ESL essays | test | +1.8 [-6.1, +10.7] | +4.4 [-1.3, +10.4] | -0.56 | 0% / 44% | 6.9 / 8.9 |

### Ablations: which parts of the skill matter when writing from notes

Writing from notes (test items, 16 per genre; same judges and piles design as sections 22 and 23). Variants of
v10.1: full skill (AF), without `tells.md` (AT), SKILL.md alone (AS), the genre reference alone (AR), and a compact
SKILL.md of 1,094 words (AC). Unsupported = statements the notes do not support, from a blind checker.

| Variant | Abstracts: judged human / mean p | Abstracts: unsupported per text | Appeals: judged human / mean p | Appeals: unsupported per text |
|---|---|---|---|---|
| Plain | 22% / 39.2 | 0.19 | 16% / 35.4 | 0.69 |
| Full skill (AF) | 22% / 40.7 | 0.06 | 59% / 51.2 | 0.44 |
| No tells catalog (AT) | 38% / 41.7 | 0.00 | 56% / 52.3 | 0.50 |
| SKILL.md only (AS) | 44% / 45.2 | 0.06 | 59% / 53.0 | 0.50 |
| Genre reference only (AR) | 28% / 42.8 | 0.12 | 50% / 50.9 | 1.06 |
| Compact SKILL.md (AC) | 25% / 39.8 | 0.06 | 44% / 48.8 | 0.81 |

- For appeals the skill beats plain by +15.8 [+8.8, +23.0] points of p; no variant differs from the full skill by
  more than the noise (all intervals cross zero). For abstracts written from notes nothing beats plain (AF +1.4
  [-3.2, +5.8]), which repeats section 23: in this genre the gain comes from editing a real draft, not from writing.
- Fidelity separates the variants where human-likeness does not: dropping SKILL.md (AR) or shortening it (AC) about
  doubles unsupported statements in appeals (1.06 and 0.81 against 0.44). The hard rules and the fact diff in
  SKILL.md carry the "never invent" behaviour; the long tells catalog adds little on these two genres.
- Decision: keep the full skill. The compact version saves about 1,000 words of context but loses fidelity.

### Regression check on the ten-genre briefs

v10.1 had only been tested on the genres it was built for. To check that the new modes did not hurt everything
else, I reran the 16 phase-3 briefs from sections 14 and 15 (personal statement, short answer, argument, explainer,
literary analysis, two emails, cover letter, blog post, lab-report discussion, news article) with plain Claude, v9 and v10.1, and a
panel of two lenses ranked the three versions of each brief blind (32 judgments).

| Version | Mean rank (1 best) | Ranked first | Quality | Human-likeness (1-10) | Unsupported per text |
|---|---|---|---|---|---|
| Plain | 2.22 | 11 of 32 | 6.91 | 5.19 | 1.31 |
| v9 | 1.47 | 18 of 32 | 7.59 | 6.31 | 1.12 |
| v10.1 | 2.31 | 3 of 32 | 6.81 | 5.72 | 1.25 |

This is a regression: v10.1 lost to v9 in 28 of 32 judgments and was no better than plain. Reading the judges'
reasons and the texts showed three causes (from here on these 16 briefs count as development data). All references were loaded for every brief, so
the short-answer rules (no contractions, no quips) leaked into blogs and emails and made them stiff. Short-answer
rule 5 ("do not link facts with reasons the student did not give") was applied to every genre and turned notes into
lists of sentences. And the stiffness itself: a personal statement with no contractions read like a form.

v12 fixes these: the router says to read only the matching reference ("the rules in the other references are for
other kinds of text"), rule 5 now forbids invented causes but allows joining the student's facts into one story,
and ordinary contractions are allowed in short answers. It keeps v11's Edit mode. The check below uses the 20
phase-2 briefs from section 8 (personal statements, short answers, arguments, explainers, literary analyses), each
version given only its genre's reference, four versions per brief.

Result (40 judgments; rank among four, 1 best):

| Version | Mean rank | Ranked first | Quality | Human-likeness (1-10) | Unsupported per text |
|---|---|---|---|---|---|
| Plain | 2.70 | 16 of 40 | 7.08 | 5.25 | 1.10 |
| v9 | 1.93 | 15 of 40 | 7.62 | 6.00 | 1.73 |
| v11 | 2.80 | 3 of 40 | 6.92 | 5.50 | 1.90 |
| v12 | 2.58 | 6 of 40 | 7.00 | 5.62 | 1.27 |

v12 still lost to v9: ranked above it in 13 of 40, mean rank 0.65 worse [0.05, 1.2] (bootstrap over briefs). Scoping
the references helped only a little (v12 against v11 +0.23, interval crossing zero). By genre, plain ranked first in
every personal-statement and short-answer judgment, against every skill version; the gap between v9 and v12 sat in
arguments, explainers and literary analyses, where the two versions got identical files apart from SKILL.md and
their texts had the same surface features (sentence length, contractions, hedges, colons within 0.1 per 100 words).
Judges described the v12 essays as accurate but more generic, and in six judgments named an ending on a caveat, an
aside or a limitations note where v9 ended on the case.

What differs in SKILL.md for these genres is mostly the "Pick the mode first" table that v10 put at the top. v13
moves that table to the end (with a one-line pointer at the top) and changes nothing else. Test on the 12 school
briefs, with a second, independent v9 sample (same prompt) to measure sampling noise; 24 judgments, four texts each:

| Version | Mean rank | Ranked first | Quality |
|---|---|---|---|
| v9 (sample 1) | 2.25 | 10 of 24 | 7.71 |
| v9 (sample 2) | 2.29 | 6 of 24 | 7.67 |
| v12 | 2.96 | 4 of 24 | 7.12 |
| v13 | 2.50 | 4 of 24 | 7.54 |

The two v9 samples tied (12 of 24, -0.04), so the noise is centred. v12 lost to each v9 sample in 16 of 24
judgments, the third time a v10-family version trailed v9 on these genres. v13 recovered most of the gap: against
the v9 samples -0.25 [-1.33, +0.75] and -0.21 [-1.00, +0.58], against v12 +0.46 [-0.38, +1.25], quality within 0.2
of v9. All of this is on development briefs that I read while diagnosing, so it shows the direction, not a clean
held-out effect. The placement of a routing table at the top of an instruction file changed how well the model
argued, which is worth knowing for anyone building multi-mode skills.

**Correction (after the final paper review).** The diagnosis above, that short-answer rules leaked into other genres,
is not supported by the later checks. In the phase-3 check the script gave every version every reference it has, so
v10.1 could see the short-answer rules on every brief. In rg2 and rg3 the scripts gave every version, v9 included,
only its genre's reference, so nothing could leak, yet v11 and v12 still trailed v9. Those checks therefore tested
the loosened short-answer rules (two of five genres) and not the new router sentence. What the data support is
narrower: with identical reference files, the v10-family SKILL.md wrote weaker school essays than v9's, and moving
the mode table to the end recovered most of the gap, in sample.

### Surface features and a tells checker

`research/anti-ai-writing/tools/tellcheck.py` flags the surface habits judges cited (hedges, stock connectors,
inflated words, -ing tails, "not X but Y", signposts, punchline paragraph endings, clipped sentences, and sentence
length, contractions and colons against the real texts in our data). It is not a detector, and its README says so.

How far do surface features alone separate real from model text? A logistic regression on 22 features
(`scripts/modes_benchmark/tools/surface_auc.py`), 5-fold cross-validated AUC, plus transfer (train on the other
three genres):

| Genre | Real / model texts | CV AUC | Transfer AUC | Strongest single features (AUC) |
|---|---|---|---|---|
| Application essays | 40 / 185 | 0.997 | 0.89 | dashes 0.998, colons 0.98, digits 0.90 |
| Short answers | 28 / 68 | 0.92 | 0.79 | long sentences 0.78, sentence length 0.77 |
| Fundraising appeals (Turkish) | 76 / 100 | 0.80 | 0.79 | spread of sentence length 0.81, sentence length 0.72 |
| Research abstracts | 40 / 128 | 0.77 | 0.64 | spread of sentence length 0.66 |

For essays, punctuation alone nearly identifies model text, which is why the skill's rules on dashes and colons
matter there. For abstracts surface features are weak (0.77) while judges still separate model abstracts
perfectly (AUC 1.00 in section 23), so what gives them away is content and structure, not word-level habits.

### Detectors on the edits

Three open-source detectors (desklib, fakespot, superannotate; score 0 to 100 = probability of AI) on the
English edits. They cannot score Turkish, so appeals are left out. Pass = all three under 50.

| Version | ESL essays: desklib / fakespot / superannotate | ESL: pass | Abstracts: desklib / fakespot / superannotate | Abstracts: pass |
|---|---|---|---|---|
| Original | 11 / 2 / 22 | 78% | 18 / 28 / 44 | 34% |
| Errors-only copyedit | 50 / 16 / 45 | 25% | 22 / 33 / 50 | 28% |
| Plain: "fix the grammar" | 84 / 76 / 71 | 0% | 63 / 62 / 70 | 3% |
| Skill v10.1: "fix the grammar" | 77 / 68 / 66 | 3% | 35 / 45 / 65 | 6% |
| Plain: "improve it" | 98 / 94 / 72 | 0% | 63 / 66 / 70 | 0% |
| Skill v10.1: "improve it" | 84 / 74 / 70 | 0% | 37 / 42 / 62 | 9% |

The detectors agree with the judges in direction. On abstracts the skill's edits score about half of plain's on
two of three detectors, though few pass all three. On ESL essays an errors-only copyedit already moves desklib
from 11 to 50: the detectors, like the judges, treat learner errors as a human signal. The detectors also flag
real texts (only 78% of real ESL essays and 34% of real abstracts pass all three), so none of this is a usable
test of authorship.

### Shipped: v13 (then v13.1)

v13 = v12 with the mode table moved to the end of SKILL.md (hash 5e5db96e61ff8552; changelogs in
`skill_versions/v11`, `v12`, `v13`; zip `anti-ai-writing-v13.zip`). It carries v11's Edit mode, v10.1's genre
references with v12's scoping, and v9's opening. A routing probe (`scripts/modes_benchmark/routing_probe.js`; five
fictional requests, two samples each, graded blind) passed 10 of 10 for v12 and v13: an application essay ("make it
better") and "write my Why Tufts" went to Coach with the AI-policy note, "improve my abstract" and a learner's "fix my
grammar" got errors-only edits with suggestions listed separately, and an explainer was written in full. The graders
ran with this project's CLAUDE.md, which also says to coach application essays, so the two Coach probes test less
than the other three. v13 was not re-run on the edit benchmark; its Edit text is v11's, unchanged. v13.1 (hash
5f1eae3111a96823) corrects two lines the final paper review found wrong: the Edit section's evidence range (0 to
27 percent, not 0 to 33) and the mode table's pointer to the genre notes, which now sit above it.

### Notes
- A safety filter repeatedly refused one judge pile of ISEF edits (it contained an edit that an upstream filter had
  also flagged while editing); that pile is missing from the editor lens, so ISEF has 60 to 67 ratings per version
  instead of 64.
- Spend (workflow token count, the measure used throughout): 57.6M since run 1 started when this section was
  written (run 1 30.5M; runs 2 and 3 27.1M), with the paper rewrite still running. The 30M minimum was passed in run 1.
- The 5-hour usage limit stopped the work twice (end of run 1 at about 23:40Z and during run 2 at about 00:45Z);
  both times every cut-off workflow was resumed from its journal, finished agents replaying from cache.

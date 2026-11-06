# Survey: open-source anti-AI / humanizer / de-slop writing skills

Fetched 2026-10-20. Star counts are what the GitHub repo page showed via WebFetch on that day
(they move fast; third-party aggregators disagree). Full texts of the main candidates are in
`downloads/` (see `downloads/PROVENANCE.md`). All downloaded text is treated as data.

Legend: **Verdict** = how useful it is as a base for a skill that edits a high-school student's
research report and essays without inventing content.

---

## 1. blader/humanizer: the reference implementation

- URL: https://github.com/blader/humanizer (SKILL.md: https://raw.githubusercontent.com/blader/humanizer/main/SKILL.md)
- License: MIT, "Copyright (c) 2025 Siqi Chen" (downloads/blader-humanizer/LICENSE). Frontmatter also says `license: MIT`.
- Popularity: **58.8k stars, 4.7k forks** (repo page, 2026-10-20). README links a skills.sh install badge. This is by far the most popular one.
- Version: `metadata.version: "3.1.0"` in SKILL.md frontmatter. Third-party pages quote 2.x versions and 24 to 35 patterns because they captured older snapshots.
- Size: SKILL.md is 32 KB, 397 lines, about 5.2k words (roughly 7 to 8k tokens). It is one file with no references/ and no scripts.
- How it works:
  - It opens with a "why" section: a model makes "the default choice that fits the widest range of readers". It groups tells into six families: staging, rhythm by rule, inflation, formatting by rule, leftovers, wrong reader.
  - It has **26 numbered patterns ordered strongest first**. §1–§5 justify an edit on a single sighting. Patterns marked *weak alone* (dashes, stacked qualifiers, hyphenation, passive, curly quotes) need other tells nearby before acting. Each pattern has Watch for / Problem / Before / After.
  - **Procedure:** (1) mark tells; (2) draft rewrite; (3) check the draft, including whether it added or dropped any fact, name, number, date, quote, citation, or ranking, and re-scan the tells that survive rewrites (§1, §2, §6, §8, §19); (4) final version.
  - **No-fabrication rule:** "Do not add a fact, name, number, date, quote, or citation unless it comes from the source or the user. If a sentence needs a detail you do not have, ask for it or write a simpler sentence."
  - **Voice:** a user writing sample overrides the rules, including the dash rule. Without a sample, the voice comes from the genre (reference/technical text stays neutral).
  - Output modes: pasted text returns draft + remaining patterns + final. File mode writes only the final text. Embedded mode returns only the final text.
  - "When not to act": quotations, titles, and text written before 2022-11-30. It keeps voice-carrying details such as odd specifics, mixed feelings, and asides.
- Evidence:
  - README: "In a blind test, judges preferred Humanizer's rewrite over the original AI text 16 times out of 16 ([#229](https://github.com/blader/humanizer/issues/229))".
  - Issue #229 (Ryan Lenk, 2026-08-19) shows the **judges were LLMs from one model family** and only 77 of 144 planned trials ran.
  - The same issue found detection rates of 100% (raw) vs 98.6% after the humanizer pass.
  - Its pattern counts show the pass made some tells disappear and others grow. AI vocabulary went from 70 to 0 and typography tells from 60 to 0, but **"uniform beat rate" rose from 60 to 101 and "aphoristic closers" from 38 to 61.** The rewrite creates its own uniform "humanizer" rhythm.
  - The README itself says: "Getting past AI detectors is not a goal, and detectors still flag most of its output."
- Strengths:
  - It is the best-reasoned of the group: it explains why, calibrates by strength, has explicit carve-outs, and has a fact-preservation check.
  - Its examples are mostly meaning-preserving.
  - It covers reply/"wrong reader" and document-about-itself patterns, which few others do.
- Weaknesses for our use:
  - **Too long for the recommended level-2 budget.** Anthropic's docs say a SKILL.md body is "Under 5k tokens", and this one is about 8k.
  - **Not tuned for academic or report prose.** §25 flags "the table below compares" and "this section is organized by…", but research reports must reference their tables and figures in the text. §13 flags "Challenges… / Future Outlook" sections, and a paper legitimately has Limitations and Future Work sections. Methods sections conventionally use the passive voice. The skill has no carve-outs for any of this.
  - **§21 straight-quotes rule:** "Curly quotes… appear where the writer or target format uses straight quotes". The student's live report is a Word .docx, and Word auto-curls quotes. The rule is weak-alone, but it could still cause pointless edits.
  - **§8 bans every em/en dash** in the final output unless a sample uses them. That is fine as a style choice, but it is absolute.
  - Its "Before" examples are trimmed **quotations from Wikipedia's "Signs of AI writing" page**: Statistical Institute of Catalonia, Alamata Raya Kobo, Korattur, Haolai River, Somali cuisine. I confirmed by grep against a mirror copy of the page. Wikipedia text is CC BY-SA 4.0, so copying those passages verbatim carries share-alike/attribution duties beyond the MIT license (UNVERIFIED legal nuance, not legal advice). **Write our own examples.**
  - The default output (draft + critique + final) is verbose for a student who just wants the edited paragraph.
  - The claude.ai install instruction says to use GitHub "Download ZIP". That produces a `humanizer-main/` folder, which does not match the skill name `humanizer`, and the Help Center lists a folder/name mismatch as an upload-failure cause (UNVERIFIED in practice).
- **Verdict:** best base to fork from (structure, calibration, procedure, guardrails). Do not adopt as-is.

## 2. conorbronsdon/avoid-ai-writing: the most engineered

- URL: https://github.com/conorbronsdon/avoid-ai-writing
- License: MIT, "Copyright (c) 2026 Conor Bronsdon". NOTICE.md covers co-contributed packaging.
- Popularity: **5.1k stars, 473 forks, 606 commits** (repo page 2026-10-20).
- Size: `version: 3.38.0`.
  - SKILL.md is 33 KB / 317 lines, and the skill must also load `references/patterns.md` "in full" before any audit.
  - SKILL.full.md (everything inlined) is 153 KB / 1,179 lines.
  - It ships a Node detector, validator, MCP server, GitHub Action, corpus and evals.
- How it works:
  - Three modes: rewrite (default), detect (flag only), edit (in place).
  - An "editing contract": a pattern match is only a *candidate*. It becomes a finding after context checks, and a finding becomes an edit only when the scope authorizes it.
  - Source fidelity and protected content (quotes, code, tables, URLs).
  - P0/P1/P2 severity tiers, a 3-tier word table with 112 entries, and 56+ patterns (74 categories in the full catalog).
  - Voice profiles (casual/professional/technical/warm/blunt), and at most 2 editing passes.
  - Rewrite output is Final rewrite + Changes + Verification (passes, checks run, residuals, stop reason).
- Standout parts:
  - **"Never inject these"** (SKILL.md lines ~301–317). It forbids *adding* fabricated speaker perspective, manufactured stakes, forced contrarianism, performed candor, em-dash theatrics, **staccato conversion** ("chopping ordinary sentences into fragments to manufacture rhythm"), and **invented specifics**: "a fabricated specific is worse than the vague phrasing it replaced… flag the gap and leave it. Never fill it."
  - It cites "an independent stress test of `blader/humanizer`" for the staccato failure mode and credits `isatimur/de-slop` for the guardrails.
  - **No-op rule:** if no justified finding exists, return the text unchanged and say it is clean. "Do not merge sentences, introduce contractions, or polish wording merely because it could read more smoothly."
  - Changed-span accounting: every changed span must map to a finding.
  - An honest caveats section: "signals, not proof", plus detector false-positive literature (Liang et al. 2023 on non-native writers).
- **Self-measured evidence (CHANGELOG.md, lines ~466–492; this is the maintainer's own measurement, not peer-reviewed):**
  - On RAID and HC3 corpora, the detector's composite score is near chance (paragraph ROC-AUC 0.501, document 0.623).
  - **"The discriminating signal is structural, not lexical."** Paragraph "uniformity" fires on 2.1% of human vs 25.1% of machine documents (lift 11.7x).
  - **"The 112-entry vocabulary table has a lift of 0.9: it fires slightly more often on human writing than on machine writing."**
  - The em dash is *inverted* as an authorship signal (lift 0.2). The rule is kept as style advice only.
  - Caveat: RAID/HC3 text comes from older model generations.
  - The maintainer's own pre-2023 human blog posts tripped the Tier-1 word list on 12.5% of paragraphs.
- Weaknesses:
  - Very heavy and procedural; much of the text is about its own tooling (node scripts, passes, verification wording).
  - Its own guidance makes it read a 33 KB file plus a large patterns file before every pass, which is far over the level-2 budget.
  - Scripts need Node. claude.ai's sandbox may or may not have network/packages (UNVERIFIED for this skill).
  - Its "Verification" boilerplate would bury a student's paragraph.
  - It explicitly does not implement APA/MLA.
- **Verdict:** do not adopt. **Take the "Never inject these" list, the no-op rule, and the lesson that word lists are weak evidence** (with attribution).

## 3. petergyang/no-ai-slop: the best compact editor

- URL: https://github.com/petergyang/no-ai-slop (files under `skills/no-ai-slop/`)
- License: MIT, "Copyright (c) 2026 Peter Yang".
- Popularity: **12.6k stars, 879 forks, 23 commits** (repo page 2026-10-20). Published July 2026 per search results.
- Size: SKILL.md 10.9 KB / 97 lines / about 1.7k words, plus eval.md 3.2 KB.
- How it works:
  - Two jobs: Edit (default) and Detect (quote + named pattern + short fix, with "Do not… guess whether AI wrote it. AI detectors guess.").
  - Editing principles: **"Make the minimum effective edit… Leave strong human sentences alone"**, "Keep the user's meaning. Don't invent claims, examples, stats, or opinions. If something is unclear, ask.", and "Preserve the writer's real voice".
  - **The "portability test":** "If a sentence could move unchanged to another person, company, country, or product, it is probably filler."
  - Short word/phrase lists with "cut when they add nothing, keep when they carry…" nuance, plus 17 named patterns. These include colon reveals, interpretive metadiscourse, synonym cycling, fake-profound kickers, and summary-recap endings.
  - Workflow: read → identify core point and voice traits → edit → **self-check against `eval.md` (pass/fail checklist) → fix and re-check** → output draft + "What changed".
- Weaknesses:
  - Aimed at blogs, posts, and product writing.
  - Its "Be concrete and specific" examples show invented numbers ("cut deploy time from 40 minutes to 4"). They are illustrations, but they model exactly the move the skill bans, and a model may copy it.
  - "Use active voice… Never let inanimate things do human verbs" is too absolute for scientific prose ("the model predicts", "Table 2 shows" are normal).
  - "Summary-recap endings… 'In conclusion'… cut" conflicts with essay and report conventions, where a conclusion section is required.
  - The em-dash rule is moderate (1–2 allowed in long drafts), which is reasonable.
- **Verdict:** best *shape* to copy (short SKILL.md + eval checklist + minimum-edit stance). Take the portability test, the eval-loop idea, and the detect-mode wording.

## 4. hardikpandya/stop-slop: popular but over-corrects

- URL: https://github.com/hardikpandya/stop-slop
- License: MIT, "Copyright (c) 2025 Hardik Pandya".
- Popularity: **18.2k stars, 1.3k forks, only 12 commits** (repo page 2026-10-20). An August 2026 article quoted 15.2k.
- Size: SKILL.md 2.6 KB (68 lines), plus references/phrases.md 2.9 KB, structures.md 5.3 KB, examples.md 1.7 KB.
- How it works: 8 core rules, a quick-check list, phrase and structure tables, and a 5-dimension self-score (Directness, Rhythm, Trust, Authenticity, Density, each 1–10, "Below 35/50: revise").
- **Weaknesses (concrete):**
  - Absolute rules that damage academic prose: **"Kill all adverbs. No -ly words."**, **"No passive constructions"** / "Every sentence needs a human subject", "Sentences starting with What, When, Where, Which, Who, Why, How → Restructure", **"Three-item lists → Use two items or one"**, and "Lazy extremes (every, always, never…)".
  - These rules produce the clipped, choppy style that issue #229 measured as a new tell.
  - **The examples change meaning.** "most teams struggle" becomes "Teams struggle" (the qualifier is deleted and the claim gets stronger). "In today's fast-paced landscape… This matters because your competition isn't waiting." becomes "Move faster. Your competition is." (content replaced by a slogan).
  - Example 4 outputs "Speed, quality, cost—pick two." with an **em dash**, which breaks its own "No em dashes at all" rule.
  - There is no fabrication guard and no procedure beyond the checklist.
- **Verdict:** do not adopt. At most borrow a few phrase-list entries (throat-clearing, emphasis crutches), which are generic.

## 5. stephenturner/skill-deslop: scientific-writing fork of stop-slop

- URL: https://github.com/stephenturner/skill-deslop
- License: MIT, "Copyright (c) 2026 Stephen D. Turner". README acknowledges stop-slop (MIT) and **tropes.fyi by Ossama Hassanein**. tropes.fyi's own license is **UNVERIFIED**: the site was unreachable (DNS failure) from this environment.
- Popularity: **420 stars, 29 forks, 1 commit**.
- Size: SKILL.md 8.4 KB / 130 lines, plus references (phrases, structures, tropes 17 KB, examples 10 KB).
- How it works: stop-slop's rules and rubric, softened for science. "Prefer active constructions… use 'we' in scientific prose", "In scientific writing, domain terminology is fine and expected", "cite specific authors instead of 'researchers have shown'", and "No fractal summaries".
- **Major weakness: the examples fabricate content.** Example 4 "after" adds "Each additional week of lead time added roughly 15% to the mean WIS", a number absent from the "before". Example 6 adds "Since 2013, it has standardized targets…". Example 2 replaces the whole passage with a new scientific claim ("If individual model rankings are unstable… may not improve on equal-weight approaches"). A model imitating these examples will invent facts, which is the worst failure for a research report.
- It still inherits "Tricolon (three-item list)? Use two items or one." and "Em dash anywhere? Remove it."
- **Verdict:** useful only as a checklist of *where* academic register differs (passive in methods, "we", terminology, citations). Do not copy its examples.

## 6. theclaymethod/unslop: research-grade, self-declared "no-ship"

- URL: https://github.com/theclaymethod/unslop. MIT. 550 stars, 121 commits.
- It has teach/cleanup/rewrite/mimic modes and three stdlib Python scanners (phrase / structure / "silhouette"), with an 8-criterion /40 rubric and presets.
- The README is candid that the latest public benchmark was a **"no-ship"**: the skill improved recall but missed the bar on precision, collateral damage, and whole-document safety. Its silhouette metric was validated on only 20 documents.
- **Verdict:** interesting ideas (voice "teach" from samples, genre flags), but too complex and self-reported as not yet better than baseline. Not downloaded.

## 7. Others checked (brief)

| Repo | Stars (2026-10-20) | License | What it is | Verdict |
|---|---|---|---|---|
| [Aboudjem/humanizer-skill](https://github.com/Aboudjem/humanizer-skill) | 285 | MIT | 55 patterns, 5 voices, Node CLI score; `compare` flags dropped numbers/dates/URLs | Fact-diff idea is good; otherwise redundant |
| [brandonwise/humanizer](https://github.com/brandonwise/humanizer) | 128 | MIT | Regex detectors + 500-word 3-tier vocab + burstiness/TTR stats | Source of the unverified "5–20x" vocab claim; skip |
| [jalaalrd/anti-ai-slop-writing](https://github.com/jalaalrd/anti-ai-slop-writing) | 552 | MIT | Mostly banned words/phrases/openers lists | Pure blacklist; skip |
| [isatimur/de-slop](https://github.com/isatimur/de-slop) | 4 | MIT | Paragraph triage (rewordable vs hollow), "subtract and sharpen without inventing", flag hollow spans instead of filling | Good idea (hollow → flag, don't fill); tiny adoption |
| [maxgoff/unslop](https://github.com/maxgoff/unslop) | 0 | MIT | Single SKILL.md, prose + code + UI + commit rules | Scope creep; skip |
| [obra/the-elements-of-style](https://github.com/obra/the-elements-of-style) | n/a | Strunk text public domain | Strunk 1918 rules + ~12k-token reference | Classic clarity rules, not anti-AI; old-fashioned for some cases |
| [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) `writing-clearly-and-concisely` | n/a | MIT (Leonardo Flores) | Strunk + short AI-pattern list + bundled `signs-of-ai-writing.md` (a copy of the Wikipedia page, which is CC BY-SA) | Handy offline copy of the Wikipedia page; license mismatch to note |
| [anthropics/skills](https://github.com/anthropics/skills) | n/a | Apache 2.0 (most) | 19 skills incl. `doc-coauthoring`, `internal-comms`, `brand-guidelines`, `discernment-nudge`; **no anti-AI / humanizer skill** | Use `skill-creator` for packaging/evals only |
| [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | 77.5k | n/a | List; writing entries are content-research-writer, internal-comms, tweet optimizer; **no humanizer/de-AI entries** | Not useful here |
| [David-Saeteros/claude-skills](https://github.com/David-Saeteros/claude-skills) `academic-writing` | 4 | CC BY 4.0 | Academic drafting/citing/reviewer responses; not an AI-tell remover | Not checked in depth |

## 8. Sam Paech antislop / slop lists: not a prompt skill

- Repos:
  - [sam-paech/antislop-sampler](https://github.com/sam-paech/antislop-sampler) (Apache-2.0)
  - [sam-paech/slop-forensics](https://github.com/sam-paech/slop-forensics) (MIT, © 2025 Sam Paech)
  - [sam-paech/auto-antislop](https://github.com/sam-paech/auto-antislop) (no LICENSE file at `main/LICENSE`; 404)
- They work at the **sampler/logit level**: the generator backtracks when a banned phrase appears. That needs control of a local model's decoding, which a Claude skill does not have.
- Their lists come from **creative-writing (story) outputs**. The default `slop_phrase_prob_adjustments.json` (517 entries) is full of fiction tells and fantasy names: "elara", "lyra", "eldoria", "shivers down", "barely above a whisper", "tapestry", "testament to", "delve".
- The README itself says: "It's recommended that you roll your own slop list! … mostly auto-generated… not well optimised or curated."
- **Verdict:** at most a handful of overlap words. Irrelevant for report and essay prose. Saved for reference only.

## 9. Wikipedia "Signs of AI writing" (the upstream source)

- Not directly fetchable here (en.wikipedia.org fails DNS in this sandbox). Used a mirror copy bundled in softaworks/agent-toolkit (`downloads/wikipedia-signs-copy/`, 95 KB). Snapshot date is unknown, so treat it as UNVERIFIED vs the live page.
- Key caveats from the page (useful for the skill's framing):
  - "This list is *descriptive*, not *prescriptive*… *not* a ban on certain words, phrases, or punctuation."
  - "**Please do not merely treat these signs as the problems to be fixed; that could just make detection harder.** The actual problems are those deeper concerns" (sourcing, verifiability, hallucinated citations).
  - Its "Ineffective indicators" section lists perfect grammar, "bland/robotic" prose, "fancy/academic words", and conjunctions in isolation as *not* reliable signs.
  - "AI vocabulary" list (align with, crucial, delve, emphasizing, enduring, enhance, fostering, garner, highlight (verb), interplay, intricate, key (adj), landscape, leveraging, multifaceted, notably, nuanced, realm, robust, seamless, shed light on, showcasing, streamline, tapestry, testament, underpin, underscore, vibrant, vital…). The page says the list shifts by model and over time ("delve" dropped off in 2025).
- License: Wikipedia text is CC BY-SA 4.0 (standard Wikipedia licensing). Paraphrasing *ideas* is fine. Copying example passages requires attribution and share-alike.

# v15 decision brief: the GitHub humanizer skills

For the anti-ai-writing maintainers, 2026-11-24. Baseline: v14 (`.claude/skills/anti-ai-writing`). Test record: `research/anti-ai-writing/DEVLOG.md`.

## Summary

The user asked us to "implement the famous GitHub humanizer skills into this skill" and to add "one GitHub skill that removes the Claude watermark". We read the five skills from our October survey at their current versions and sorted all 529 of their rules against v14. v14 already covers 279 of them (53 percent), and its credits already name three of the five as sources. That leaves 138 rules that v14 lacks and could take without conflict, and a skeptic check kept seven of them. Another 91 rules break a v14 hard rule (51) or contradict what our tests on real pre-2022 writing measured (40). The remaining 21 do not apply.

We recommend seven small changes and nothing else from these skills. They are the seven survivors, with two merged into one, plus a correction to v14's watermark sentence. Five of the seven reduce what v14 edits, and none adds a new kind of rewrite. We recommend against a watermark remover. Anthropic says its mark is carried in word choice and has no hidden characters, so the character stripping these tools do cannot reach it. A skill running on a current Claude model also produces marked text itself, and no remover has shown that it works against Claude's detector.

## 1. The five skills

| Skill | v14 covers | New, compatible | Conflict or contradicted | Verdict |
|---|---|---|---|---|
| blader/humanizer 4.0.0 plus unreleased edits (2026-11-19, 5,407 words, 73.1k stars) | 43 of 88 (49%) | 29 (6 kept) | 13 | An editing skill built on Wikipedia's "Signs of AI writing" and written for human readers. It is v14's main ancestor. Six narrow guards survived. The conflicts start with 4.0.0 dropping its own no-invention rule ("Where the text is generic, add a specific detail you know to be true"), and at least 14 of its examples now add facts, such as a 15 cm river width and a 2024 New York Times interview. |
| hardikpandya/stop-slop, unversioned (last commit 2026-03-18, unchanged since our survey, 1,995 words, 19.2k stars) | 25 of 64 (39%) | 18 (0 kept) | 21 | A short checklist of absolute bans for blog and essay prose, with no rule against inventing facts and no exceptions. Its conflicts include deleting every adverb and every "most" (which removes hedges), banning passive voice, three-item lists and all dashes, and three of five examples that add or drop claims ("Move faster. Your competition is."). |
| petergyang/no-ai-slop 1.0.6 (2026-09-01, unchanged, 2,219 words, 13.8k stars) | 54 of 75 (72%) | 12 (0 kept) | 8 | A minimum-edit editor with Edit and Detect modes. It is the closest to v14 in approach, and v14 already covers more of it than of any other skill. Its conflicts are word bans and plain-English or active-voice pushes that our real-writing data reject, plus five examples that invent numbers or features ("cut deploy time from 40 minutes to 4") despite its own "Don't invent" rule. |
| conorbronsdon/avoid-ai-writing 3.39.0 (2026-11-16, 23,877 words loaded, 6.3k stars) | 87 of 157 (55%) | 58 (1 kept) | 9 | The most careful of the five. It has rewrite, detect and edit modes, checks that edits keep the original's content, and is the only one that reports measurements: its detector fired on 0 of 560 human paragraphs, and its 112-word vocabulary table fired slightly more often on human text than on machine text. One rule survived (each difference in an edit needs a reason). The conflicts are replacement cells such as "myriad → many (or give a number)" that invite invented specifics, a hard cap on dashes, and README examples the skill does not load. |
| Aboudjem/humanizer-skill 0.8.4 (2026-11-17, 10,371 words, 328 stars) | 70 of 145 (48%) | 21 (0 kept) | 40 | Rewrites text "as a specific, opinionated human" in one of five preset voices. It says it does not aim to beat detectors, but its burstiness and perplexity rules are built around what detectors measure. It has the most conflicts of the five: its "soul injection" step adds opinions and anecdotes ("debugging this at 2am with a cold coffee"), nearly every example invents numbers, and its default mode is a full rewrite. |
| All five | 279 of 529 (53%) | 138 (7 kept) | 91 | 21 rules did not apply. |

## 2. Additions for v15, ranked

These are ranked by expected value. None has been tested in this wording. Rank 1 should be tested on a fresh held-out set of edits, because DEVLOG 25 records the current held-out halves as worn.

### 1. Check edits in both directions

Target: SKILL.md, Procedure step 4, a new bullet after the fact diff. Sources: blader/humanizer (H10) and avoid-ai-writing (S25), merged.

> Edit diff. When you edit a draft the user gave you (Edit, Rebuild, Coach corrections), also check the other direction. Every claim, hedge, number, name, date and quote in their version must still be in yours or be named in your note as a cut, and a sentence you join must not add an order, a ranking, a cause or a "same time" the original did not state. In Edit and Coach, put your version next to theirs and look at each place they differ. Each difference must fix an outright error, clear up something that blocks the meaning, remove a clear AI tell or meet something the user asked for (such as a word limit). Put anything else back in the writer's words, and mention in the notes after the text only changes that are actually in it. Skip this check when writing from notes, where leaving material out is part of the job.

Effect: step 4's fact diff only checks that everything in the output came from the user. A dropped hedge or a reworded claim therefore passes. DEVLOG 25 measured how often this happens. v13.1 "improve" edits changed 0.50 statements per abstract and 1.06 per learner essay. Only 31 percent of learner essays kept their meaning, against 56 percent for an errors-only copyedit. The DEVLOG 24 ablation found that the explicit checks in SKILL.md produce the fidelity behaviour, which makes another check the right place for this fix.

Risk: untested, and it adds about 120 words to the file that loads every time. It must stay limited to editing. In Write from notes it would push every fact into the text, while personal-essay.md and short-answers.md tell the model to leave material out. The abstract cuts in DEVLOG 24 came with a 250-word limit, and the clause about what the user asked for keeps cuts like those allowed.

### 2. Match the user's writing sample

Target: SKILL.md, Modes, at the end of Write and of Edit. It replaces Edit's last sentence. Source: blader/humanizer (H15).

> If the user gives a sample of their own writing, read it before drafting and match the habits you can count in it: sentence length and spread, contractions, dashes, colons and semicolons, how sentences open and connect, and how formal the words are. These habits override the default style rules, the dash rule included. Do not copy the sample's facts, exact phrases or errors into the new text. Use only writing the user says is theirs, because a sample an AI polished brings its tells with it. In Coach mode a sample changes nothing, since the student still writes.

Effect: v14 mentions a sample only in Edit and does not say what to match. Our data support matching habits that can be counted. Matching the punctuation of the register gained 11.7 points of p(human) on held-out appeals (DEVLOG 22). Punctuation and sentence length alone separate real essays from model essays at AUC 0.997, with dashes as the top feature (DEVLOG 24).

Risk: a sample from another genre, such as a chat log supplied for an abstract, could pull the register the wrong way, and the text does not cover that case. The text does guard against copying phrases or errors. Untested as a rule.

### 3. Leave code, markup and data alone in mixed files

Target: SKILL.md, the opening scope paragraph (first sentence below) and step 5 (the rest). Source: blader/humanizer (H26).

> When prose sits in a file with code, commands, paths, URLs, YAML front matter, LaTeX markup, citation keys or data, edit only the prose and leave the rest exactly as it is, dashes and hyphens included. Write only the finished text into the file. Give Edit's list, any number flag and any note about cuts in your reply.

Effect: CLAUDE.md sends all project prose through this skill. That includes the LaTeX paper (`research/anti-ai-writing/paper/main.*`), where `--` is the en dash in number ranges and citation keys and `\ref` labels must not change. It also includes `paper/design_decisions.md`, which contains commands such as `--company`. Without this rule, R6 and the Format row would strip those dashes. The rule also keeps Edit's notes out of the file.

Risk: none to content or voice. Prose inside code comments may be left unedited, which errs on the safe side.

### 4. Do not fix a tell the text is discussing

Target: tells.md section 9, next to the quotations bullet. Source: blader/humanizer (H81).

> Text that talks about a pattern instead of using it, such as a paper, log or guide that names "delve" or "It's not X, it's Y" as an example of an AI tell.

Effect: the user's anti-AI paper, the DEVLOG and the LEDGER all cite "delve", "this matters" and "It's not X, it's Y" as examples. They are often set in italics or LaTeX rather than quotation marks, so the quotation exception does not catch them. Section 13 of our own tells catalog has this clause, but tells.md does not.

Risk: it only reduces edits.

### 5. Keep the register of the user's informal text

Target: tells.md section 9, plus a one-line pointer in Edit mode. Source: blader/humanizer (H20), first half only.

> tells.md: The user's own informal text (a chat message, a comment, a review, a casual post). Lowercase, short forms such as "lmk", fragments and emphatic stops such as "Worst. Service. Ever." belong to the register, so leave them and fix only what blocks the meaning. Never add them to text you write.
>
> Edit mode: In informal text, check tells.md section 9 before treating lowercase or fragments as errors.

Effect: it removes a contradiction inside v14. Edit fixes "punctuation" and the Rhythm row lists fragment stacks as a tell, yet messages.md says "In the user's own text, leave their punctuation." Without this rule, v14 can "fix" a user's "Worst. Service. Ever." or a lowercase chat message.

Risk: the model could read this as license to add casual features to its own messages. The last sentence forbids that, as do tells.md section 8 and hard rule 3. The other half of humanizer's rule, which makes two tells enough to rewrite a whole message (H21), is rejected in section 3.

### 6. Limit "chatbot residue" to the assistant's own lines

Target: tells.md T8, added after the current entry. Source: blader/humanizer (H82).

> This entry covers an assistant talking to its user ("I hope this helps", "Let me know if you'd like me to expand this"). In the user's own message, a greeting, a sign-off or a "let me know" that asks the reader for something ("let me know by Friday if you can drive") is ordinary correspondence. Keep it.

Effect: T8 currently says to delete "Let me know if…". In a user's own message, that phrase is often the request itself, so deleting it breaks hard rule 2. The change brings tells.md in line with messages.md, which already allows greetings and plain sign-offs.

Risk: low. examples.md #6 still removes a generic closer when rebuilding an AI-written email.

### 7. Correct the watermark sentence

Target: SKILL.md, Integrity. It replaces "and recent Claude models add an invisible watermark to their text that approved organizations can check." Source: Anthropic's watermark explainer, developer docs and help article (from the web sweep), checked because of the user's request for a remover.

> AI detectors are unreliable in both directions (they flag many human essays and miss some AI ones). Recent Claude models also mark their text through word choice, a statistical watermark with no hidden characters, which organizations Anthropic approves can check. Stripping characters does not remove it, and this skill does not try.

Effect: "invisible watermark" reads as hidden characters, which is the mistake one remover (MarkClean) makes. The new wording matches Anthropic's own description and gives the model a factual answer when a user asks the skill to remove the mark.

Risk: Anthropic may change which models carry the mark and who can check it, so the text names no models and no access list.

### What we dropped

Of the 138 compatible rules, 131 did not pass the skeptic check. That is all 18 from stop-slop, all 12 from no-ai-slop, all 21 from Aboudjem, 23 of humanizer's 29 and 57 of avoid-ai-writing's 58. The inputs to this brief list only the survivors, so the reason for each drop is in the per-skill check records and not here. We also left out three conflicting rules that would be safe if narrowed, because v14 already has the safe version:

- Naming a relationship or a source only when the source states it (H57, H60). tells.md C6 already covers this.
- Rewriting a whole awkward paragraph (H13). Rebuild already does this.
- Adding words that v14's classic list lacks, such as empower, streamline, paramount, elevate and harness (R35). Word lists showed no reliable gain in DEVLOG 21.

We took nothing from the skills that appeared or grew popular after our survey (section 6), because nobody has read them rule by rule yet.

## 3. What v14 must not take

| Reason | Example | Evidence | Also in |
|---|---|---|---|
| Invents facts, opinions or feelings (hard rule 1) | humanizer 4.0.0, step 2: "Where the text is generic, add a specific detail you know to be true" (H08) | Hard rule 1: "A made-up specific is worse than the vague sentence it replaced." In DEVLOG 25, allowing general knowledge in school essays raised unsupported claims per text from 2.08 to 3.33, including a wrong claim about a novel. | Aboudjem's soul injection and Concretizer, stop-slop's "The team fixed it that week", no-ai-slop's invented metrics and "add a plain takeaway or next action" (R55), avoid-ai-writing's "(or cite a number)" cells |
| Strengthens or changes the claim (hard rule 2) | stop-slop's "Kill all adverbs" (SS06), which removes probably, only and nearly. Its Example 2 also deletes "most". | Hard rule 2: "Never make a claim stronger than its evidence." tells.md section 8 lists stripping every hedge as an over-correction. | Aboudjem's --aggressive ("kill all hedging"), blunt voice, position engine and hedge-debris deletion (P55), avoid-ai-writing's "testament to → proves", stop-slop's cut of three-item lists to two |
| Rewrites the user's own text (hard rule 4) | Aboudjem's default mode, a full rewrite (S02) | DEVLOG 24: plain "improve it" rewrites changed 73 to 93 percent of words, and readers judged 0 to 30 percent of them to be the writer's own, against 91 to 100 percent for minimum edits. | humanizer's "freely shorten, merge, split and reorder" (H07), rewriting a whole message for two tells (H21), two rewrites by default (H24), Aboudjem's --iterate |
| Tricks aimed at detectors (hard rule 3) | Aboudjem's perplexity rule, which says to choose "the second or third word that comes to mind" (X01) | Our catalog (O2): a "sound more human" prompt raised verb diversity from 0.766 to 0.924, further from human text at 0.572. | Aboudjem's sentence-length quotas for every paragraph (3 to 8, 12 to 20 and 25 to 40 words), staged self-corrections, deliberately broken parallelism, slang added for perplexity |
| Contradicted by our tests on real writing | stop-slop's absolute dash ban, "No em dashes at all" (SS49) | Real admitted essays use 0.17 dashes per 100 words, and every model version used none. Dashes alone separate real essays from model essays at AUC 0.998 (DEVLOG 21, 24). | humanizer §8 (H48), Aboudjem P13 and avoid-ai-writing's dash cap (P02). Bans on passive voice (real ISEF abstracts use 1.5 passives per 100 words against 0.7 in our first versions, DEVLOG 23). Word bans (+1.9, CI −2.2 to +6.0, DEVLOG 21). Short sentences and fragments, callbacks, curly quotes treated as an AI sign (H70), AI-probability estimates and detector-style scores (M01, F06). |
| Hides AI use (Integrity section) | Aboudjem P35, which strips utm_source=chatgpt.com from links. avoid-ai-writing does the same. | The parameter is invisible in a rendered link, so removing it only hides where the link came from. v14: "It is not a way to hide AI use." | Any watermark remover (section 4). Deleting visible pasted citation junk such as citeturn0search0 is ordinary cleanup and does not belong here. |
| Copied example text | humanizer §17's "after": "In a 2024 New York Times interview, she argued that AI regulation should focus on outcomes" (X01) | v14 examples.md: "Every 'after' uses only facts present in the 'before'." | stop-slop examples 1 to 3, no-ai-slop lines 35, 38, 62, 64 and 70, Aboudjem's patterns.md and patterns.zh.md, avoid-ai-writing's README rows. Take pattern names only, never example text. |

## 4. The Claude watermark

Anthropic's own pages describe Claude's text watermark as statistical. They call it "a version of the SynthID-Text approach published by Google DeepMind", in which a key and the few preceding words decide which word the model picks. The explainer says "Nothing is added to the text and there are no hidden characters", and the developer docs say it "adds no tokens or hidden characters". Release notes on September 1, November 3 and November 16 added models to the scheme. The help article (updated this week) lists every current model, [a Claude model] included, and names the API, Claude, Claude Code, Cowork, Claude Tag and the three cloud platforms as covered. Some older models may not carry the mark when a request changes temperature, top_p or top_k. Anthropic describes robustness only in words: "Light editing probably won't remove the watermark completely; a complete rewrite where every word is replaced will." Short texts, proofreading changes and exact text such as code carry little signal. A translation made by Claude is itself marked. Anthropic publishes no accuracy or false-positive figures. A positive result is "not fully conclusive", and a missing mark does not show that a human wrote the text. Detection is a private-preview API for eligible organizations, such as regulators, media, fact-checkers, researchers and educational organizations. There is no public text checker, and claude.com/check-content checks only the C2PA credentials on files.

We read five remover projects, and each works in one or both of two layers. The first layer strips invisible Unicode characters and file metadata (C2PA, EXIF, XMP). By Anthropic's account this cannot affect a mark that contains no characters. One project, MarkClean, even claims that Claude inserts invisible characters, which Anthropic denies. The second layer has another model rewrite the text. guillaumemeyer/watermarks-remover (about 28.3k stars), its fork and MarkClean offer it as an option, and ClariSortAi does nothing else. None of them promises that it works, and the most popular one advises using a non-Claude model so the rewrite is not marked again.

Nothing shows that any of these tools works against Claude. The detector is not public, and guillaumemeyer's Claude detector slot is a placeholder. Its README says "no tool can honestly certify" that a text fails the official check. ClariSortAi's only evidence is word overlap on one 1,491-word memo, where five-word overlap fell from 16.0 to 7.3 percent. The only independent audit of the deployed Claude watermark (arXiv 2611.29018, 2026-11-21) tested whether the mark is present, reached no firm answer, and did not test removal. Removal figures exist only for Google's open-source SynthID-Text, where one study found that 98.3 percent of detected texts lost the mark after paraphrase (arXiv 2607.16010). That is not a result on Claude. None of the five humanizer skills touches the mark. The closest they come is deleting pasted chatbot citation tokens and AI-referrer link parameters.

So v15 should not include a remover. It would break hard rule 3 and the Integrity section, and it could not work from inside the skill anyway. When the skill runs on a current Claude model, as it does in this project, its own rewrite carries the mark. Addition 7 corrects v14's wording.

## 5. Head-to-head tests on real human writing

1. blader/humanizer 4.0.0. Request: `/humanizer` followed by the pasted text, which has been the only command in its README since 4.0.0. In Codex and other agents its default prompt is "rewrite this text in my voice without changing its facts". Why: it has the most stars (73.1k) and is v14's ancestor. Version 4.0.0 now tells the model to add facts it knows, so this test measures what that costs on real text, using the unsupported-statement count from DEVLOG 25.
2. petergyang/no-ai-slop 1.0.6. Request: its default Edit mode, worded the way its trigger description reads, for example "Edit this draft to make it sharper and more human, keeping my voice." The audit found no fixed command. Leave out its "more opinionated" trigger, which invites added opinions, or run it as a separate stress case. Why: it has the most installs on skills.sh (32,531) and is the closest to v14 Edit in design. The test shows whether v14's extra rules and genre files add anything over a plain minimum edit.
3. conorbronsdon/avoid-ai-writing 3.39.0. Request: its default rewrite mode, for example "Rewrite this to remove AI writing patterns." Its edit mode for files is a closer match to v14 Edit, so run both if the budget allows. The audit recorded its modes but no standard phrase. Why: it is the strongest competitor on keeping the original's content, with preservation checks and a verification report, and the only one with its own measurements. It loads about 23,900 words, against 7,000 to 9,500 for v14 (SKILL.md, tells.md and one genre file), so the test also asks whether the extra length buys anything.

Run each skill and v14 twice, once with the skill's own wording and once with the same plain "humanize this", so that wording does not decide the result. Use real pre-2022 texts of the kinds DEVLOG 21 to 24 used (admitted essays, ISEF abstracts, charity appeals, learner essays), drawn fresh. Measure what DEVLOG 24 and 25 measured: share of words changed, share judged the writer's own, unsupported statements added and statements changed. Include the one-sentence plain baseline from DEVLOG 25. If the budget allows a fourth skill, stop-slop (20,661 installs) is the obvious choice, though reading it already predicts its main failure, which is deleted hedges.

## 6. Open questions

- Dash default. The check on H48 notes that v14's own R6 ("Default: avoid them") fits poorly with DEVLOG 21, where real essays used 0.17 dashes per 100 words and every model version used none. This audit does not decide whether R6 should change for text the model writes.
- New skills not yet read. etodanik/deslop (53 stars, 2026-11-16) has a facts check that also catches dropped negations and links, which addition 1 does not name. It also reports that a second pass aimed only at tells made answers worse, 5 to 0. Dodaios/ste80-humanizer (1.1k stars, 2026-11-09) and ilien-dev/quiron (which checks rates against pre-ChatGPT human baselines) also deserve a rule-by-rule read before v15 is frozen.
- Limits of the evidence. The figures from humanizer issue #229 come from our October survey and were not re-checked. Star counts are rounded page figures. This workflow's agents made the comparisons and skeptic checks against the v14 files and DEVLOG, and no human reviewed them.

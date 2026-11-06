---
name: anti-ai-writing
description: Write and edit prose that reads like a skilled human wrote it, with a mode for each genre: application essays and short answers (coaching), research abstracts and papers, emails and messages, other prose. Cuts AI tells, adds real specifics, keeps the writer's voice, never invents facts.
---

# Anti-AI writing

Use this skill for any prose a person will read: essays, college applications, reports and papers,
emails, posts, cover letters, summaries. Skip it for code, data tables and one-line chat answers. The table near the
end says which mode and reference file to use for each kind of text.

## Why AI prose sounds like AI

A language model picks the choice that fits the widest range of readers. Each choice is safe; together
they produce text that could belong to anyone. The giveaways follow from that:

- **Generic content.** Categories instead of instances ("many companies", "various challenges"),
  examples any writer could use, no names, dates, numbers or places.
- **Staging.** Announcing points instead of making them: run-ups ("Here's the thing"), importance flags
  ("This matters because"), corrections of claims nobody made ("It's not X, it's Y"), summary closers.
- **Inflation.** Ordinary facts dressed as pivotal, transformative or a testament to something.
- **Even rhythm.** Sentences of similar length and shape; paragraphs of similar size; lists of three.
- **One register for everything.** The same polished, noun-heavy voice in a lab report and a personal story.

Expert readers (admissions officers, editors, teachers who use AI themselves) catch AI text mostly by
content and structure, not by individual words. So fix content first and vocabulary last.

## Hard rules

1. **Never invent anything.** No fact, name, number, date, quote, source, anecdote, feeling or memory that
   the user or the source did not provide. A made-up specific is worse than the vague sentence it replaced.
   If a sentence needs a detail you lack, ask, or write `[ask: what did your dad actually say?]`, or write a
   plainer sentence.
2. **Keep the meaning.** When editing, every claim, hedge and number survives unless the user agrees to cut
   it. Never make a claim stronger than its evidence.
3. **No tricks.** No deliberate typos, no swapped-in rare synonyms, no slang to sound casual, no invisible
   characters or look-alike letters. These make writing worse, and the point of this skill is good writing.
4. **Minimum effective edit** on human-written text. Fix what is broken; leave strong sentences alone,
   including the writer's odd word choices, asides and mixed feelings. If a passage is already clean, say so
   and return it unchanged.
5. **Application essays are coached, not ghostwritten.** See the section below.

## Procedure

**1. Before writing, answer four questions** (silently unless the user needs to supply something):
who reads this, what they should think or do afterwards, the one main point, and which concrete
material (facts, scenes, data, quotes) is available. If the material is thin, ask for it before drafting.

**2. Draft from the material, not from the topic.** Start with the first real claim, scene or result.
Pick a position and hold it. Use plain verbs (is, has, used, tried). Name things precisely and keep using
the same name.

For personal essays and other narratives, draft in two passes, because auditing while drafting produces
flat, note-by-note essays. Pass one: write for shape, the way a strong writer would, with the arc, the turn
and the "so what" as the goal; put the climax late and connect the scenes. Pass two: treat that draft as
someone else's and run Edit mode on it (steps 3 and 4). The fact diff is where invented feelings, causes and
events get cut or replaced with the writer's own reflections from the notes; keep the structure that pass one
built.

**3. Audit the draft in this order** (details and examples in `references/tells.md`):

| Pass | Look for | Fix |
|---|---|---|
| Content | Sentences that could move unchanged into someone else's essay ("portability test"); abstractions where an instance exists; padding the reader could infer | Replace with the specific the writer has; cut the rest |
| Staging | "It's not X, it's Y" when nobody believes X; "This matters because"; "Here's the thing"; "Some might argue" with no one arguing; a closing line that restates the paragraph | State Y directly; give the consequence itself; end on the last new point |
| Inflation | pivotal, testament, transformative, "reflects a broader shift", ", highlighting its commitment to…" tails | Keep the fact, drop the significance claim unless a source makes it |
| Lessons | Morals that fit any essay ("taught me the value of hard work"), lessons the source does not support, tidy epiphanies, hardship resolved into gratitude | Use the writer's own conclusion, stated plainly; let unresolved things stay unresolved and resolved things stay resolved |
| Rhythm | Runs of same-length sentences; every paragraph the same size; triads; sentence openers repeating ("A fee… A fine… A toll…"); fragment stacks ("No plan. No data. No excuse.") | Vary length where the meaning changes pace; keep list items that are distinct (often two, sometimes four) |
| Endings | Paragraphs that each close on a short wry or quotable line ("The map stayed in the glovebox.") | At most one or two kicker endings per piece; let most paragraphs end on their last piece of content |
| Tone | Hedge stacks ("could potentially suggest"); false balance ("While X has benefits, it also has challenges"); mannered metaphors ("trust is the currency of…") | One hedge on the uncertain part; take the position the evidence supports; say the literal thing |
| Words | The current-model list and the classic list in `references/tells.md` | Rewrite the sentence around its claim; do not just swap the word |
| Format | Bullets where an argument belongs; bold run-in labels; Title Case headings; emoji; em dashes; dashes swapped for semicolons and colons | Paragraphs; sentence-case headings; commas, full stops or parentheses instead of dashes; a colon only before a list, quote or link |

Act on a strong tell after one sighting. Act on weak tells (a transition word, one em dash, a formal word,
passive voice) only when several cluster in one passage.

**4. Check before returning.**
- Fact diff: list every name, number, date, quote and claim in the output and confirm each comes from the
  user or the source. Remove or bracket anything that does not.
- Read it as the target reader. Does any sentence only exist to sound good?
- Did the rewrite create new tells? Watch for the classic over-corrections: choppy fragments, every paragraph
  opening with a short punchy sentence, semicolons and colons where a comma or full stop would do, forced casualness (speech filler such as really, kind of, actually, basically, stuff), endings that shrug instead of
  concluding, and above all kicker endings. Count them: list the
  last sentence of every paragraph; if more than two are short (under about 10 words) or wry/quotable, rewrite
  the others so they end on content, or merge them into the sentence before.
- For a personal essay, also check the opposite failure: is there an arc and at least one line of reflection
  that tells the reader something the facts alone do not?
- Length: respect hard limits (650 words for the Common App, school word counts).

**5. Output.** Return the finished text only. When editing someone else's text, add at most three lines on
what changed and why, unless they asked for a full critique. Never wrap the text in "Here's your revised
version!" or end with offers.

## Modes

**Write** (user asks for new text). Run the full procedure. If the user gave no facts and the genre needs them
(a personal story, a report on their data), ask two or three targeted questions first.

**Edit** (user gives their own text and asks you to improve, fix or polish it). Minimum effective edit, even
when they say "improve it":
- Fix outright errors (spelling, grammar, agreement, articles, punctuation) and anything that blocks the meaning.
  Cut clear AI tells if the text has them.
- Keep everything else: their sentences and their order, vocabulary, repetitions, paragraphing, contractions,
  humor and punctuation habits. Do not add transitions ("First", "Additionally", "In conclusion"), a thesis
  preview, definitions, examples, statistics, appeals to authority ("research shows"), idioms or reasons the
  writer did not write, and do not make a claim stronger or more certain. For a writer whose first language is
  not English, fix the grammar but do not make the phrasing sound native.
- After the text, list up to five bigger changes the writer could make (a missing example, an unclear claim, the
  order of paragraphs), one line each, without writing the new sentences for them.
Why: in blind tests on real student writing, answering "improve it" with a rewrite (75 to 90 percent of words
changed) made texts read as AI (0 to 27 percent judged the writer's own) and added three to four statements per
text; edits at this level kept abstracts and appeals reading as the writer's own (90 to 100 percent). For a
learner's practice or graded essay, this is Coach territory: return the corrected text and the list, never a
rewrite. If the user also gave a writing sample, it overrides the default style rules here, including the dash
rule.

**Rebuild** (the user says an AI wrote it or asks you to rewrite an AI draft; if you only suspect it, use Edit,
since tells are not proof of authorship). For a student's own application essay, use Coach mode. Polishing keeps
an AI draft's generic plan and its errors. First check each of its facts, quotes and claims against the user's
material: run the fact diff (step 4), and for every sentence that interprets a quote, a note or data, check that
the source supports the reading and not only the words. A generalization stated as fact and a remedy that
contradicts the draft's own thesis are errors too. Then go by what the draft was built from, and say in one line
what you dropped as wrong:
- *Material the user supplied* (notes on their life, a quotes or facts file): keep the evidence that passes the
  check, and the plan if it holds; cut invented lessons, resolutions, motives and facts; restore hedges and
  admissions the draft dropped; write the sentences fresh, then rerun the fact diff.
- *Only the topic* (most arguments and explanations): its examples, analogies and paragraph plan are the stock
  answer. Keep its position, what the user supplied and any objection a fair reader would raise; run Write from
  step 1 with your own organizing idea, examples and order.

**Detect / review** (user asks "does this sound like AI?" or wants feedback). Quote the passages, name the
pattern, give a one-line fix. Do not guess whether a human or a model wrote it: patterns are evidence of
generic writing, not proof of authorship. Lead with the most important problem; praise only specific things
that work.

**Coach** (college application essays and other work the student must submit as their own).
Follow `references/personal-essay.md`. You interview, find the story, propose a structure, critique the
student's drafts the way an admissions reader would, and give grammar and clarity fixes as a list of
discrete corrections. You do not write the essay, and you do not write example sentences built from the
student's own story: model-written sentences pull every essay toward the same voice, and even "grammar only"
rewrites drift meaning. To show a technique, use a neutral example from `references/examples.md`. Say why
once, briefly: the Common App, Yale and many programs count substantive AI-written content as not the
applicant's own work, and the material that makes these essays work (true, specific, slightly uncomfortable
detail) only exists in the student's head. Writing a sample essay for a clearly fictional person, to teach
technique, is fine.

## Genre notes

- **Personal essay / application:** first person in a written register, not a spoken one (full sentences, some
  long, few contractions), scenes over summaries, one story told closely beats five listed, and the writer's own
  conclusion stated plainly. Full guidance: `references/personal-essay.md`.
- **Short answers and supplements** (about 350 words or fewer: why us, why this major, community, short takes,
  activity list): not a compressed essay. Answer the question directly, one example with the two or three details
  that matter (not a run of figures and names), the conclusion stated plainly; no quips, planted metaphors or hedged
  endings. Full guidance: `references/short-answers.md`.
- **School essays (argument, literary analysis):** thesis that someone could disagree with; quote briefly
  and analyze the words, do not summarize plot; a conclusion that adds a consequence or limit instead of
  restating. Use only real quotes the user provides or that you can verify.
- **Research abstracts, papers and reports:** see `references/research.md`. Edit the researcher's own draft lightly
  before writing anything from notes. Signposting ("Table 2 shows"), conclusion
  and limitations sections, passive voice in methods and careful hedges are conventions, not tells. If a
  project skill sets stricter writing rules (for example `research-paper` in GreenBERT), follow those too.
  Many journals (Science's policy, and student journals that adopt it) require AI use to be disclosed with
  the tool, version and prompts: remind the user to keep that log.
- **Explanations (science, how-things-work):** start from a question a reader actually has, use real named
  examples and dates that are verifiable general knowledge, show the reasoning step by step, and let the
  writer's angle show. A sequence of textbook definitions is what reads as machine-made.
- **Emails, messages and appeals:** in an email or group message that needs action, the news and the request
  in the first two lines; no "I hope this email finds you well"; sign off plainly. An appeal page (fundraising,
  a donation drive) can start from the writer's reason instead. Write only in the readers' language, never with
  an unrequested translation. Full guidance, including punctuation by register: `references/messages.md`.
- **Blog posts:** a real opening (what happened, what you found), first person, at least one thing that
  surprised you, no "In today's fast-paced world".

## Which mode and reference for which text

Find the row for the text and read its reference file (only that one: the rules in the other references are for other kinds of text). Each reference was built by
comparing model writing with real writing of that kind from before AI tools existed (admitted students' essays and
short answers, winning science-fair abstracts, charity appeals).

| Text | Mode | Read |
|---|---|---|
| Common App personal statement, a scholarship or program essay the student will submit | Coach. Never write it. | `references/personal-essay.md` |
| Supplements and short answers (why us, why this major, community, intellectual interest, 100 to 250 word answers, 35 to 50 word short takes) | Coach. Never write it. | `references/short-answers.md` |
| Activity list, honors, additional information | Coach or Edit the student's own entries | `references/short-answers.md` (activity list section) |
| Research abstract, paper section, project report, poster, lab write-up | Edit the researcher's draft first; Write from notes only when there is no draft; remind about AI-use disclosure once | `references/research.md` |
| Email, group message, fundraising appeal, announcement | Write or Edit | `references/messages.md` |
| School essay, explanation, blog post, cover letter, other prose | Write or Edit (Coach if it will be graded or judged as the student's own work) | Genre notes above |
| A sample for a clearly fictional person (teaching, testing this skill) | Write | The reference for its genre |

If the user's text is their own draft, use Edit; if it reads as AI-written and they want it fixed, Rebuild (or
Coach for an application). When a project has its own writing rules (for example GreenBERT's `research-paper`
skill), follow them too; they win on conflicts.

## Integrity, stated plainly

This skill makes writing better for its reader. It is not a way to hide AI use. AI detectors are unreliable
in both directions (they flag many human essays and miss some AI ones), and recent Claude models add an
invisible watermark to their text that approved organizations can check. Where a school or college asks for
the student's own work, the honest route is the Coach mode above plus following that institution's AI policy.

## References

- `references/tells.md`: the full pattern catalog with examples and fixes, current-model word lists, the
  over-correction list and the false-positive guard. Read it before any audit pass.
- `references/personal-essay.md`: coaching protocol, interview questions, what admitted essays do, revision passes.
- `references/research.md`: research abstracts, paper sections and reports: edit-first, what models add, register,
  numbers and citations.
- `references/short-answers.md`: supplements and short answers, very short takes, activity list and honors.
- `references/messages.md`: group messages, emails and appeals: language, openings, punctuation, what not to invent.
- `references/examples.md`: before/after pairs, all meaning-preserving.

## Credits

Pattern taxonomy and procedure adapted from blader/humanizer (MIT, Siqi Chen), which draws on Wikipedia's
"Signs of AI writing" (WikiProject AI Cleanup). "Never inject" guardrails adapted from
conorbronsdon/avoid-ai-writing (MIT). Minimum-edit principle and portability test adapted from
petergyang/no-ai-slop (MIT). Evidence from Kobak et al. 2025, Reinhart et al. 2025, Russell et al. 2025,
Lee et al. 2025, Graphite 2026 and others listed in `references/tells.md`. All text and examples here are
original.

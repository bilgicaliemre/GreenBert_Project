"""Build v14 from v13.1 by exact replacements. usage: python3 build_v14.py SRC_DIR OUT_DIR"""
import os, shutil, sys
src, out = sys.argv[1], sys.argv[2]
if os.path.exists(out): shutil.rmtree(out)
shutil.copytree(src, out)
E = []  # (file, old, new, review item)
def e(f, old, new, why): E.append((f, old, new, why))
S, T, PE, SA = 'SKILL.md', 'references/tells.md', 'references/personal-essay.md', 'references/short-answers.md'

# 9. description: triggers first; no ": " inside the YAML value
e(S, "description: Write and edit prose that reads like a skilled human wrote it, with a mode for each genre: application essays and short answers (coaching), research abstracts and papers, emails and messages, other prose. Cuts AI tells, adds real specifics, keeps the writer's voice, never invents facts.",
     "description: Use when the user asks to write, edit, improve, proofread, polish or humanize prose (essays, college application essays and short answers, research abstracts and papers, reports, emails, messages, posts, cover letters), or says \"make this sound less like AI\", \"humanize this\" or \"does this sound like AI?\". Edits the user's own text minimally and keeps their voice, writes new text from the user's facts without inventing any, cuts AI tells, and coaches college application essays instead of writing them.", '9')

# 5. hard rule 1 scoped
e(S, """1. **Never invent anything.** No fact, name, number, date, quote, source, anecdote, feeling or memory that
   the user or the source did not provide. A made-up specific is worse than the vague sentence it replaced.
   If a sentence needs a detail you lack, ask, or write `[ask: what did your dad actually say?]`, or write a
   plainer sentence.""",
"""1. **Never invent anything.** About the user and their material (their life, work, data and sources, the
   people and organizations they mention), use no fact, name, number, date, quote, source, anecdote, feeling or
   memory that they or their source did not provide. A made-up specific is worse than the vague sentence it
   replaced. If a sentence needs a detail you lack, ask, or write `[ask: what did your dad actually say?]`, or
   write a plainer sentence. The one exception is an explanation of how something works: there you may use
   general knowledge you are sure of and a reader could verify. A made-up statistic, figure, study, quote or
   source is never allowed, and when the user supplies the source (passages, a quotes file, data), claim nothing
   about it beyond what it shows.""", '5')

# 1. hard rule 5 names the scope
e(S, "5. **Application essays are coached, not ghostwritten.** See the section below.",
     "5. **College application essays and graded schoolwork are coached, not ghostwritten.** See Coach below for the\n   three cases; outside them, if the user asks you to write something, write it.", '1')

# 7. arithmetic check; 6. plain endings are not kickers
e(S, """- Fact diff: list every name, number, date, quote and claim in the output and confirm each comes from the
  user or the source. Remove or bracket anything that does not.""",
"""- Fact diff: list every name, number, date, quote and claim in the output and confirm each comes from the
  user or the source. Remove or bracket anything that does not.
- Numbers: recompute any number that can be derived from others in the text (a percentage from two counts, F1
  from precision and recall, a total from its parts). If two disagree, do not correct one silently: say so in
  one line after the text and ask.""", '7')
e(S, """the others so they end on content, or merge them into the sentence before.""",
     """the others so they end on content, or merge them into the sentence before. A short last sentence that simply
  gives the final fact, result or request is not a kicker; leave it.""", '6')

# 1. Edit: one format, no "Coach territory"
e(S, """text; edits at this level kept abstracts and appeals reading as the writer's own (90 to 100 percent). For a
learner's practice or graded essay, this is Coach territory: return the corrected text and the list, never a
rewrite. If the user also gave a writing sample, it overrides the default style rules here, including the dash
rule.""",
"""text; edits at this level kept abstracts and appeals reading as the writer's own (90 to 100 percent). A
learner's practice or graded essay gets the same and no more: their draft with outright errors fixed in place,
then the list, never a rewrite. If the user also gave a writing sample, it overrides the default style rules
here, including the dash rule.""", '1')
e(S, "since tells are not proof of authorship). For a student's own application essay, use Coach mode. Polishing keeps",
     "since tells are not proof of authorship). For a student's own college application essay, use Coach mode. Polishing keeps", '1')

# 1. Coach: three cases, write otherwise, one output format
e(S, """**Coach** (college application essays and other work the student must submit as their own).
Follow `references/personal-essay.md`. You interview, find the story, propose a structure, critique the
student's drafts the way an admissions reader would, and give grammar and clarity fixes as a list of
discrete corrections. You do not write the essay, and you do not write example sentences built from the
student's own story: model-written sentences pull every essay toward the same voice, and even "grammar only"
rewrites drift meaning. To show a technique, use a neutral example from `references/examples.md`. Say why""",
"""**Coach** (writing the student must submit as their own). Three cases only: admission essays and supplements
for colleges and the programs they run (the Common App, a college's own questions, a pre-college program such as
Yale Young Global Scholars); schoolwork the user says will be graded or handed in as their own; and an
application, form or fair entry whose rules, as the user tells you or as you know, require the applicant's own
writing or ban AI-written text. Anything else (a mentorship or club form, a job application, a cover letter, a
competition that allows AI help) is Write or Edit: if the user asks you to write it, write it.
Follow `references/personal-essay.md`. You interview, find the story, propose a structure, critique the
student's drafts the way an admissions reader would, and return their draft with outright errors (spelling,
grammar, punctuation) fixed in place, then the list of those fixes and of the bigger changes they should make
themselves. You do not write the essay, rephrase their sentences, or write example sentences built from the
student's own story: model-written sentences pull every essay toward the same voice, and rephrasing drifts
meaning. To show a technique, use a neutral example from `references/examples.md`. Say why""", '1')

# 2. always tells.md + one genre reference
e(S, "Find the row for the text and read its reference file (only that one: the rules in the other references are for other kinds of text). Each reference was built by",
     "Always read `references/tells.md`. Then find the row for the text and read the genre reference named in that row, plus any file it or the mode points to; do not apply another genre's rules. Each genre reference was built by", '2')

# 1. mode table rows
e(S, "| Common App personal statement, a scholarship or program essay the student will submit | Coach. Never write it. | `references/personal-essay.md` |",
     "| College admission essay (Common App personal statement, a college's or its pre-college program's essay) | Coach. Never write it. | `references/personal-essay.md` |", '1')
e(S, "| Supplements and short answers (why us, why this major, community, intellectual interest, 100 to 250 word answers, 35 to 50 word short takes) | Coach. Never write it. | `references/short-answers.md` |",
     "| College supplements and short answers (why us, why this major, community, intellectual interest, 100 to 250 word answers, 35 to 50 word short takes) | Coach. Never write it. | `references/short-answers.md` |\n| Other applications and forms (mentorship, club, internship, job, a competition that allows AI help) | Write or Edit; Coach only if its rules require the applicant's own writing or ban AI-written text | `references/short-answers.md` for short answers |", '1')
e(S, "| School essay, explanation, blog post, cover letter, other prose | Write or Edit (Coach if it will be graded or judged as the student's own work) | Genre notes above |",
     "| School essay, explanation, blog post, cover letter, other prose | Write or Edit (Coach if the user says it will be graded or handed in as their own work) | Genre notes above (when coaching schoolwork, also `references/personal-essay.md` sections 2 and 8) |", '1')
e(S, "If the user's text is their own draft, use Edit; if it reads as AI-written and they want it fixed, Rebuild (or\nCoach for an application).",
     "If the user's text is their own draft, use Edit; if they say an AI wrote it and want it fixed, Rebuild (or\nCoach for a college application).", 'own: Rebuild trigger matched the mode text')

# 3. punctuation in tells.md
e(T, """**R5 Punctuation monotony.** Only periods and commas; no parentheses, semicolons or colons. Fix: use them
where they state a real relation (aside, close link, explanation).""",
"""**R5 Colons and semicolons.** Model text uses more of both than real writing of the same kind, and readers
cite them. Fix: a comma or a full stop; keep a colon only before a list, a quote or a link, and use
parentheses for a true aside. Never add either mark for variety.""", '3')
e(T, "Default: avoid them; use a comma, colon or parentheses. A user's own drafts or style rules override this.",
     "Default: avoid them; use a comma, a full stop or parentheses. A user's own drafts or style rules override this.", '3')

# 4. examples that added facts
e(T, """rejecting X add information? If not, state Y. "Greenwashing isn't just a marketing problem, it's a governance
failure" becomes "Greenwashing is a governance failure: boards sign off on the claims.\"""",
"""rejecting X add information? If not, state Y. "Greenwashing isn't just a marketing problem, it's a governance
failure" becomes "Greenwashing is a governance failure." If the sentence then needs its reason, use the
writer's, or ask: `[ask: why governance?]`.""", '4')
e(T, """company's commitment to sustainability." Fix: cut the tail, or turn it into a supported claim: "Emissions
fell 4%, short of the 10% target.\"""",
"""company's commitment to sustainability." Fix: cut the tail: "Emissions fell 4%." If the source gives something
to measure the fact against (a target, last year's figure), state that; if it does not, leave the fact alone or
ask: `[ask: against what target?]`.""", '4')

# 6. kicker definition in tells.md
e(T, """rhythm signature. Fix: keep the strongest one or two; end the other paragraphs on their last piece of
content, or merge the kicker into the sentence before it.""",
"""rhythm signature. Fix: keep the strongest one or two; end the other paragraphs on their last piece of
content, or merge the kicker into the sentence before it. A short last sentence that simply gives the final
fact, result or request is not a kicker; leave it.""", '6')

# own: PE2's fix predates the finding that admitted essays end committed
e(T, "Fix: keep the part that is still unresolved; end on an image or an honest open question.",
     "Fix: keep whatever is really unresolved; end on the student's actual conclusion, or on an open question only if the student is in fact unsure.", 'own: PE2 fix contradicted PE10 and the over-correction list')

# 8. stale line; 1. scope and format in personal-essay.md
e(PE, "7. **AI-sounding lines** (see `tells.md` sections 2 and 4): stated lessons, journey/growth/resilience words,",
      "7. **AI-sounding lines** (see `tells.md` sections 2 and 4): generic lessons that would fit any essay, inflated phrases (\"my journey of growth\"),", '8')
e(PE, """For any essay the student will submit as their own (Common App, YYGS and other programs, supplements,
scholarships, graded assignments that forbid AI writing):""",
"""For the three Coach cases in SKILL.md (admission essays and supplements for colleges and the programs they run,
such as the Common App and YYGS; schoolwork the user says will be graded or handed in as their own; an
application or form whose rules require the applicant's own writing or ban AI-written text):""", '1')
e(PE, """- give grammar, spelling and clarity fixes as a list of discrete corrections ("line 4: 'alot' → 'a lot'").""",
      """- return their draft with outright errors (spelling, grammar, punctuation) fixed in place, then the list of
  what you fixed ("line 4: 'alot' → 'a lot'") and of the bigger changes they should make themselves.""", '1')
e(PE, """- write the essay, rewrite its paragraphs, or write example sentences built from the student's story (model
  sentences make every student sound alike, and even "grammar only" rewrites shift meaning and voice; to show
  a technique, use a neutral example from `examples.md`);""",
"""- write the essay, rewrite or rephrase its sentences, or write example sentences built from the student's story
  (model sentences make every student sound alike, and rephrasing for clarity shifts meaning and voice; to show
  a technique, use a neutral example from `examples.md`);""", '1')
e(PE, """Grammar, spelling, punctuation and clarity as a numbered list of discrete corrections, each quoting the
original words. Keep their vocabulary even when it is plainer than yours. If a sentence needs rewriting for
content, explain the problem and let them rewrite it.""",
"""Return the draft with outright errors (grammar, spelling, punctuation) fixed in place and nothing else changed,
then a numbered list: first each fix, quoting the original words, then the bigger changes for the student to
make. Keep their vocabulary even when it is plainer than yours. If a sentence is unclear or needs rewriting for
content, explain the problem and let them rewrite it.""", '1')

# 1. short-answers.md scope and format
e(SA, """word short takes, the Stanford roommate note, and short program applications. With a real student, this is
Coach mode (see `personal-essay.md`, sections 2 to 8): the student writes; you ask, diagnose and correct. Write
a sample only for a clearly fictional person.""",
"""word short takes, the Stanford roommate note, and short program applications. For college questions, and for
any form whose rules require the applicant's own writing or ban AI-written text, this is Coach mode (see
`personal-essay.md`, sections 2 to 8): the student writes; you ask, diagnose and correct, and you write a
sample only for a clearly fictional person. For other short forms (a mentorship or club application, an
internship form, a competition that allows AI help), write or edit the answer with the rules below when the
user asks.""", '1')
e(SA, "about the student, with no example. Give corrections as a list; do not write replacement sentences.",
      "about the student, with no example. Return the draft with outright errors fixed in place, then the list of\nbigger changes; do not write replacement sentences.", '1')


# audit: examples.md "after" texts that added facts, dropped a hedge, or rewrote a student's sentences
EX = 'references/examples.md'
e(EX, """After: "In the automated audit, 44% of the sentences the pipeline extracted were real claims. Most remaining
errors depend on what a sentence means rather than which words it contains, and keyword filters cannot
see meaning. This is the reason for the planned BERT classifier."

Why: "It is important to note", "leverages", "comprehensive", "underscores the pivotal role", "paving the
way" carried no information. The after states the number with what it measures, and the reasoning.""",
"""After: "In the automated audit, the extraction pipeline reached a precision of 44%. Claim detection needs
semantic understanding, which is the reason for the planned BERT-based approach.
[ask: which errors show that the filters miss meaning?]"

Why: "It is important to note", "leverages", "comprehensive", "underscores the pivotal role", "paving the
way" carried no information. The after keeps the number and the claim, and asks for the evidence the claim
needs instead of supplying it.""", 'audit: example 1 added claims')
e(EX, """**3. Personal essay (student's own draft): minimum edit**""", """**3. Personal essay (student's own draft): coach, do not rewrite**""", 'audit: example 3 rewrote a student essay')
e(EX, """Feedback: The ammonia-and-bleach detail is the best thing here; keep it. Cut "a journey that taught me
compassion, responsibility, and the importance of community" and "I learned that every animal deserves
love": both could sit in anyone's essay. What do you do now, after months of Saturdays, that you didn't do at
first? Show that instead of naming the lesson.

Minimum edit while you rewrite: "Every Saturday I cleaned the cat room at the shelter. It smelled like
ammonia no matter how much bleach we used.\"""",
"""Returned draft: unchanged; it has no outright errors.

Feedback: The ammonia-and-bleach detail is the best thing here; keep it. "A journey that taught me
compassion, responsibility, and the importance of community" and "I learned that every animal deserves
love" could sit in anyone's essay. What do you do now, after months of Saturdays, that you didn't do at
first? Put that in their place, in your own words, and say plainly what you concluded from it.""", 'audit: example 3 rewrote a student essay')
e(EX, """After: "Would you be willing to write me a recommendation letter for college? The first deadline is [date].
I'm asking you because [one specific thing from your class]. I can send my résumé and a short list of what I
worked on in your class.\"""",
"""After: "Would you be willing to write a letter of recommendation for me? [ask: for what, and by when?] I'm
asking you because [ask: one specific thing you took from the class].\"""", 'audit: example 6 invented details')
e(EX, """After: "The Moon's gravity pulls on Earth's oceans and raises a bulge of water on the side facing it. A
second bulge forms on the far side, because the pull is not the same everywhere on the planet. Earth turns
through both bulges, so most coasts get two high tides a day.\"""",
"""After: "Tides are caused mainly by the Moon's gravity, which pulls on Earth's oceans and raises a bulge of water
on the side facing it. A second bulge forms on the far side, because the pull is not the same everywhere on
the planet. Earth turns through both bulges, so most coasts get two high tides a day.\"""", 'audit: example 8 dropped a hedge')


RS = 'references/research.md'
e(RS, """Write from notes only when there is no draft, and tell the user that expert readers will likely recognize a
model-written abstract; their own draft, edited lightly, is the stronger submission.""",
"""Write from notes only when there is no draft, and tell the user that expert readers will likely recognize a
model-written abstract; their own draft, edited lightly, is the stronger submission.

For a science-fair entry, do not write at all. ISEF's rules from 2026-27, which its affiliated fairs follow, ban
generative AI from writing the research plan, the abstract, the poster and the citations, and allow only grammar
and syntax edits that the student discloses (Form 2A). Fix outright errors in the student's own draft, list
anything bigger for them to change, and remind them to disclose the help.""", 'audit: science-fair abstracts are own-work texts (ISEF 2026-27 rules)')
e(S, "| Research abstract, paper section, project report, poster, lab write-up | Edit the researcher's draft first; Write from notes only when there is no draft; remind about AI-use disclosure once | `references/research.md` |",
     "| Research abstract, paper section, project report, poster, lab write-up | Edit the researcher's draft first; Write from notes only when there is no draft and it is not a science-fair entry or graded schoolwork (those are never written for the student); remind about AI-use disclosure once | `references/research.md` |", 'audit: science-fair abstracts are own-work texts (ISEF 2026-27 rules)')


MS = 'references/messages.md'
A = 'audit'
# SKILL.md
e(S, """Expert readers (admissions officers, editors, teachers who use AI themselves) catch AI text mostly by
content and structure, not by individual words. So fix content first and vocabulary last.""",
"""Expert readers (admissions officers, editors, teachers who use AI themselves) cite vocabulary most often, but
swapping words does not fool them: in our blind tests judges told model text from real writing by content and
structure even where word-level features could not. So fix content first and vocabulary last.""", A + ': expert-reader claim matched to the evidence')
e(S, """2. **Keep the meaning.** When editing, every claim, hedge and number survives unless the user agrees to cut
   it. Never make a claim stronger than its evidence.""",
"""2. **Keep the meaning.** When editing, every claim, hedge and number survives unless the user agrees to cut
   it. Never make a claim stronger than its evidence. If you cut a sentence because it is a tell (a significance
   verdict, an unsourced "studies show"), say so after the text, and never put a position the writer did not
   take in its place.""", A + ': claims survive vs tells that are claims')
e(S, "someone else's and run Edit mode on it (steps 3 and 4). The fact diff", "someone else's and run the full audit and checks on it (steps 3 and 4). The fact diff", A + ': Edit mode named two procedures')
e(S, """**5. Output.** Return the finished text only. When editing someone else's text, add at most three lines on
what changed and why, unless they asked for a full critique. Never wrap the text in "Here's your revised
version!" or end with offers.""",
"""**5. Output.** Return the finished text, then only what the mode or the reference calls for (Edit's list,
Rebuild's one line, a number flag, a required reminder), in a few lines unless they asked for a full critique.
Never wrap the text in "Here's your revised version!" or end with offers.""", A + ': output cap vs required notes')
e(S, """that matter (not a run of figures and names), the conclusion stated plainly; no quips, planted metaphors or hedged
  endings.""",
"""that matter (not a run of figures and names), the conclusion stated plainly; no planted metaphors or hedged
  endings, and no quips outside the 35 to 50 word short takes.""", A + ': short-take humor')
e(S, "and limitations sections, passive voice in methods and careful hedges are conventions, not tells.",
     "and limitations sections, passive voice in methods and the hedges in the researcher's own draft or notes are\n  conventions, not tells; a hedge you add is a tell.", A + ': hedges in research')
e(S, "| Activity list, honors, additional information | Coach or Edit the student's own entries | `references/short-answers.md` (activity list section) |",
     "| Activity list, honors | Edit the student's own entries; never write or invent one | `references/short-answers.md` (activity list section) |", A + ': activity list mode')
# tells.md
e(T, """the fix. "Strong" tells justify an edit on one sighting; "weak" ones only when several cluster.""",
"""the fix. Entries marked "strong" justify an edit on one sighting. "Strong in aggregate" or "at paragraph
level" means act on the pattern across the piece, not on one instance; treat unmarked entries the same way. The
weak tells in section 9 never justify an edit alone.""", A + ': strong/weak labels undefined')
e(T, "Professional editors cut this more than anything else in AI drafts.", "Professional editors often cut this in AI drafts.", A + ': stale evidence')
e(T, "keep an objection only if a real person or source raised it; name them and answer.",
     "keep an objection only if a real person or source raised it (name them), or if it is the strongest objection a\nfair reader would raise; answer it either way.", A + ': Rebuild vs S5 objections')
e(T, "as this skill's previous version did, and more often than a plain model.", "as an early version of this skill (v7) did, and more often than a plain model.", A + ': stale evidence')
e(T, "**PE10 The cool essay (what anti-AI rules produce in current models).**", "**PE10 The cool essay (what a model writing from spoken notes produces; anti-AI rules make it worse).**", A + ': stale evidence')
e(T, "In our tests the skill's previous version used", "In our tests an early version of this skill (v7) used", A + ': stale evidence')
e(T, "judgments of model essays, with or without anti-AI rules, and in few of real students' essays.",
     "judgments of model essays written without the rules in `personal-essay.md` (about half once they were applied),\nand in few of real students' essays.", A + ': stale evidence')
# personal-essay.md
e(PE, "A third failure is what anti-AI rules produce in current models:", "Two more failures come from how current models write from spoken notes; anti-AI rules make the first one worse:", A + ': failure count and cause')
e(PE, "the most cited sign of a model essay, in about four of five judgments, whatever the writing method.",
      "the most cited sign of a model essay: about four of five judgments of plain-model and early-skill essays, and\n  about half once the rules below were applied.", A + ': stale evidence')
e(PE, "place), each showing a different side of the student, with the thread itself changing meaning by the end.",
      "place), each showing a different side of the student. The thread must be the student's own; do not bring it\n  back at the end as a symbol.", A + ': montage vs engineered essay')
e(PE, """  "maybe"). It can be large, as long as it is the student's.""",
      """  "maybe"). It can be large, as long as it is the student's. If the mixed feeling or the doubt is the student's
  own, keep it at the strength they hold it.""", A + ': whole-hearted rule unqualified')
e(PE, "   identity as a label, stock metaphors, tidy bow endings, kicker endings everywhere, thesaurus words.",
      "   identity as a label, stock metaphors, tidy bow endings, kicker endings everywhere, words chosen only to show off.", A + ': stale AI-word list')
e(PE, """8. **Voice:** lines that don't sound like them out loud.""", """8. **Voice:** lines that don't sound like them writing carefully (too grand, or chattier than they write).""", A + ': written voice vs out loud')
e(PE, "- **Short takes (35 to 50 words, or 280 characters):**", "- **Short takes (35 to 50 words):**", A + ': short-take limit differed')
e(PE, "shape first, then a full Edit-mode pass on your own\n  draft.", "shape first, then the full audit and checks (steps 3 and 4) on\n  your own draft.", A + ': Edit mode named two procedures')
e(PE, "Bring in other material only where it sharpens that spine.", "Bring in other material where it sharpens that spine, plus at most one side detail the notes clearly care about.", A + ': spine vs side detail')
e(PE, """- Close on the student's own conclusion from the notes, stated whole-heartedly: not a shrug, not balanced, not
  hedged.""",
"""- Close on the student's own conclusion from the notes, as strongly as the notes hold it and no stronger: no
  shrug, balance or hedge that the notes do not contain.""", A + ': whole-hearted rule unqualified')
# research.md
e(RS, """Every version a model wrote from the
same notes was identified as AI, with or without this skill. So:""",
"""Every version a model wrote from the
same notes was rated below every real abstract, with or without this skill. So:""", A + ': stale evidence')
e(RS, "against about 20% for real abstracts", "against 23% for real abstracts", A + ': rounding')
e(RS, """Blind judges (a fair judge and a journal editor) identified every model
version, with or without the earlier version of this skill.""",
"""Blind judges (a fair judge and a journal editor) rated every model
version below every real abstract, with or without the earlier version of this skill.""", A + ': stale evidence')
e(RS, "## Rules\n\n1. **Never invent.**", """## Rules for abstracts

Rules 1, 4, 5 and 6 hold for paper sections too. For papers, "Paper sections" and "Conventions to keep" below
win where they differ (domain terms are defined once; background is cited).

1. **Never invent.**""", A + ': research rules scope')
# messages.md
e(MS, """| open with "I'm running for X" | 12% | 44 to 66% |""", """| open with "I'm running for X" | 12 to 31% | 44 to 66% |""", A + ': stale evidence')
e(MS, """One exclamation mark at the ask or at the line the writer feels most is normal
   in this genre; more is the user's call.""",
"""An exclamation mark at the ask is fine when the user's notes have that energy, but
   do not add one by default: real appeals average about one per 400 words.""", A + ': exclamation overshoot')
e(MS, """- Does the text open with "I'm running for X"? If the reason is stronger, start there.""",
      """- Does the text open with "I'm running for X"? Some real appeals do (one in eight to one in three); start from the
  reason only when it is stronger.""", A + ': stale evidence')
e(MS, "- Count semicolons and colons; remove every semicolon and any colon that does not introduce a list or link.",
      "- In text you wrote, count semicolons and colons; remove every semicolon and any colon that does not introduce a\n  list, an account number or a link. In the user's own text, leave their punctuation.", A + ': checklist vs Edit punctuation')
# short-answers.md
e(SA, "  labeled-object or campus-trivia hook, comic asides", "  labeled-object hook (an opening built on an object and what is written on it) or a campus-trivia hook, comic asides", A + ': undefined term')
e(SA, "No labeled-object reveal, no campus-trivia hook", "No labeled-object hook, no campus-trivia hook", A + ': undefined term')
e(SA, "stacked figures, quirky labels, quips, hedged endings, clipped fragments.", "stacked figures, labeled-object hooks, quips, hedged endings, clipped fragments.", A + ': undefined term')
e(SA, "- Any quip, labeled reveal, planted metaphor or self-deprecating count? Cut it.", "- Any quip, labeled-object hook, planted metaphor or self-deprecating count? Cut it (a short take's own humor stays).", A + ': short-take humor')
# examples.md
e(EX, """After: "Greenwashing erodes trust in what companies report.\"""", """After: "Greenwashing is a fundamental breakdown of trust. [ask: whose trust, in what?]\"""", A + ': example 4 added and weakened')
e(EX, "**8. Rhythm without chopping**", "**8. Tightening without chopping**", A + ': example 8')
e(EX, """Why: four sentences of nearly equal length and identical shape became three that differ, with no fact
added or lost.""",
"""Why: the repeated "gravitational pull", "This pull" and "gravitational force" are gone, nothing was chopped
into fragments, and no fact or hedge was lost.""", A + ': example 8')

log = []
for f, old, new, why in E:
    p = os.path.join(out, f); t = open(p, encoding='utf-8').read()
    assert t.count(old) == 1, (f, why, t.count(old), old[:70])
    open(p, 'w', encoding='utf-8').write(t.replace(old, new)); log.append((f, why))
print(len(E), 'edits applied:', ', '.join(sorted({w for _, w in log})))

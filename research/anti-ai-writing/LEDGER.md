# Ledger: plain Claude vs the skill vs real human writing

For every case we develop the skill on, this file records three things side by side:

1. what a plain prompt to Claude returns (no skill, the same request and facts);
2. what the skill returns;
3. what a real person wrote for the same job, where we have it (pre-2022 human writing, or the human draft the
   user shared);

and then the differences a human reader would actually notice. The goal is to keep the skill honest about what it
adds over the base model, and to benchmark against real human writing rather than only against what model judges
prefer.

Privacy: personal cases (the user's own messages, other people's drafts) and real human texts stay out of this
repository. Entries here give counts, features and paraphrases; the full texts are kept privately.

## Case 1. A group message asking for donations (2026-11-03)

Request: a short WhatsApp message to a school group (teachers, administrators, students who ran a marathon
together). The planned fundraiser for the school could not go ahead, so a charity campaign was opened at the last
minute instead; the group did not know yet. The message had to explain the change and ask for any help. Two
samples each from plain Claude and the skill (v8), plus a draft the school's student communications lead wrote
for the same purpose.

| | words | `!` | emoji | unrequested English translation | invented content |
|---|---|---|---|---|---|
| plain, sample 1 | 104 (+141 English) | 1 | 0 | yes | a feeling ("it was great running together") |
| plain, sample 2 | 126 | 0 | 1 | no | an apology for not telling people in time |
| skill v8, sample 1 | 64 | 0 | 0 | no | none |
| skill v8, sample 2 | 68 (+75 English) | 1 | 0 | yes | none |
| human draft | 80 | 2 | 1 | no | none |

What a reader in that group would notice:

- **The translation.** Two of four model drafts appended a full English version nobody asked for. In a
  Turkish-speaking school group that is the clearest sign of a tool. The skill did not stop it.
- **Invented small things (plain only).** Plain Claude filled gaps with a feeling and an apology the sender never
  expressed. Readers can't see this, but the sender would be signing claims that may be false.
- **Temperature.** The human draft was the warmest: the team's name and "spirit", two exclamation marks, one
  emoji, a stock Turkish idiom for "no gift too small" and the formal closing formula of a Turkish club notice.
  Plain sample 2 came next (polite address to teachers, a heart emoji, the amount in bold). The skill's drafts
  were accurate and short but read like a notice, not an appeal.
- **Reason to give.** The human draft framed giving as the team showing its spirit for a new cause; the model
  drafts framed it as a bigger total.
- **Errors.** The human draft has a repeated phrase in a run-on sentence. No model draft has an error; in a chat
  message the polish itself reads as drafted.
- **Where the human draft is weaker.** It does not explain what happened to the original plan, which the sender
  wanted said, and it describes the switch slightly differently from the sender's own account.

Hypothesis for the skill: short appeals need genre guidance. Keep the audience's language and never append a
translation; allow the warmth the genre uses (the group's identity, an exclamation, an emoji where the sender
would use one); keep the no-invention rule, which the skill already gets right. Tested next on real appeals.

## Case 2. Charity-run appeals against real ones (benchmark, 2026-11-03)

Human anchor: 84 "Why I run" texts that runners wrote for their charity-run campaign pages for events up to 2022,
sampled at random from a Turkish fundraising platform, with the platform's default template sentences, links and
sign-off names removed. For each, the runner's notes were reconstructed (facts and feelings, none of the wording),
and the appeal was rewritten from the notes by plain Claude and by the skill. Blind judges (a donor and an NGO
editor) read piles of 12 single appeals, any mix of real and model-written, and rated how likely the runner wrote
each one, how likely they would give and how well it works. Development set: 32 appeals.

| | judged written by the runner | would give (1-10) | quality (1-10) | claims the notes don't support |
|---|---|---|---|---|
| real appeals | 100% | 4.7 | 5.0 | |
| plain Claude | 25% | 5.6 | 6.2 | 1 in 32 texts |
| skill v8 | 17% | 5.4 | 6.1 | 0 |

What plain Claude returns: a clean, well-ordered appeal that judges like more than the real ones (about +1 on
quality and on would-give) and never mistake for the real ones (every model text was rated less likely human than
every real text). Told "use only the facts in my notes", it invents nothing; the invention problem from case 1
shows up when the request is open.

What the skill (v8) changed: nothing a reader would notice for the better. It started more texts with "I'm running
for X" (66% vs 44% for plain, 12% for real runners) and used more semicolons (1.2 per text vs 0.7 plain, 0.4 real),
because its rule for replacing dashes suggested colons.

What a human eye notices, in the judges' own evidence:
- **Punctuation.** Semicolons and stray colons were cited in about half of the judgments of model texts and almost
  never for real ones. In Turkish, the formal circumflex ("imkân", "hâlâ") was also a giveaway; real runners write
  "imkan", "hala".
- **The assembled plan.** Story, belief, who benefits, cost, ask, thanks, every time and in that order. Judges
  cited a tidy plan in 50 to 59% of model judgments and 12% of real ones. Real appeals are mostly one thing (a
  story, the cause's facts, a belief) with a short ask.
- **Carried-over tics.** The notes were written as speech ("bence", "I think"); a quarter to a third of model texts
  kept "bence", no real text had it.
- **Sentence shape.** Real runners write longer, more uneven sentences (15 words on average, standard deviation 8)
  than either model version (10 to 12, SD about 4).
- **Things the skill should not copy.** Typos, a pasted project title, run-on sentences: judges cited these as
  signs of a person in about half of real judgments. Faking them is a trick the skill rules out.

What v9 does about it: a new guide for messages and appeals (`skill_versions/v9/.../references/messages.md`). It
says to write only in the readers' language, start an appeal from the writer's reason, let one part carry the text,
keep money concrete, mix long and short sentences, punctuate like the register (no semicolons, no stray colons, no
circumflex in casual Turkish), drop the notes' spoken tics and invent nothing.

Held-out test on 16 appeals nobody read during development:

| | judged written by the runner | would give | quality | claims the notes don't support |
|---|---|---|---|---|
| real appeals | 100% | 4.5 | 4.6 | |
| skill v8 | 12% | 5.4 | 6.2 | 1 in 16 texts |
| skill v9 | 59% | 5.5 | 6.2 | 0 |

v9 against v8, same runners: +11.7 points on the judges' probability that the runner wrote it (95% interval +5.5 to
+17.9), with no change in would-give or quality. In the texts, v9 had no semicolons, stray colons, circumflexes or
"bence" (v8: 1.75 semicolons per text, "bence" in 44%). A reader comparing side by side can still tell: every model
text scored below every real one. v9 also uses more exclamation marks than these runners did. v9 is now the shipped
skill.

Case 1 again with v9 (not a held-out check, since the translation rule came partly from case 1): both drafts were
Turkish only, explained the change, closed with one exclamation mark at the ask, and invented nothing. They are still
plainer than the human draft, which used the team's name and spirit; the request never gave a slogan, and the skill
does not make one up.

## Case 3. Science-fair research abstracts against real ones (benchmark, 2026-11-05)

Human anchor: winning ISEF abstracts from 2014 to 2021 (Society for Science's public database), chosen at random
within four groups: Turkish winners, computing and math, environment and energy, social science. For each, the
project notes were reconstructed (every fact and number, none of the wording). Plain Claude and the skill wrote
the abstract from the notes ("I'm a high school student. Please write the abstract for my ISEF project…").
Blind judges (an ISEF judge and a student-journal editor) rated single abstracts in mixed piles.

What plain Claude returns: a fluent, well-ordered abstract with every number from the notes, rated a little
better than the real ones (about 6.1 against 5.7 out of 10), and identified as AI almost every time. Its tells, in
the judges' words: fluent and frictionless prose, stock connectors ("To address this problem", "Overall", "These
results indicate"), hedges and self-assessments the student never wrote ("to my knowledge", "we believe"),
promotional endings ("has the potential to revolutionize"). It invents almost nothing when the notes are full.

What the general skill (v9) changed: nothing for the better. Its plain-English habits made abstracts chattier
(simplified openings, technical terms glossed for lay readers), which judges read as AI, and its "first person is
normal" advice gave twice the real rate of "I/we" and half the real passive voice.

What a human eye notices in the real abstracts: dense technical sentences, passive procedures, coined
abbreviations, lists of methods, numbered results, a keyword line, and errors. Fixing only the errors did not
change the verdict: copyedited real abstracts were still judged the student's own every time. The difference is
voice and structure, not mistakes.

What v10's research mode does: technical register, no glossing, no hedges or self-assessments the notes lack, no
narrated logic or stock connectors, conclusions within the evidence, and above all "edit the researcher's own draft
first". Held-out test (16 abstracts):

| | judged written by the student | mean p | quality | unsupported claims |
|---|---|---|---|---|
| real abstracts | 100% | 87.3 | 5.8 | |
| plain Claude | 6% | 34.5 | 6.2 | 0 of 16 |
| v10 | 12% | 38.5 | 6.1 | 0 of 16 |

v10 against plain: +4.0 points of p (95% interval -0.3 to +7.9), quality unchanged; stock connectors cited 3% against
38%, promotion 9% against 22%. Every model abstract still scored below every real one. The practical lesson: a
student's own abstract, lightly copyedited, reads as theirs; one written from their notes by any version does not.

## Case 4. College short answers against real admitted ones (benchmark, 2026-11-05)

Human anchor: short answers (50 to 250 words) that admitted students published themselves (MIT applicants in The
Tech and on MIT's blogs; Tufts' admissions blog), classes of 2026 or earlier. Writers did not get notes built from
these answers: an agent refused to turn real students' personal answers into material for new application answers,
and we agreed. Instead each real question got an invented applicant's notes, and plain Claude and the skill wrote
the answer from those. Judges (an admissions reader and an essay coach) rated single answers in mixed piles.

What plain Claude returns: a vivid, crafted answer that judges rate far better than the real admitted ones (7.0
against 4.4 out of 10) and identify as AI every time. Its tells: a dense run of precise figures and names, a
labeled-object or campus-trivia hook, comic asides and self-deprecating counts, a planted metaphor, an "honest
limitation" beat, and a hedged or trailing last line; on the page, short clipped sentences (about 11 words), many
contractions (3.9 per 100 words) and colons, and a punchy last line in half the answers.

What a human eye notices in the real admitted answers: they are plainer than you expect. Earnest, direct,
sometimes clichéd, with long sentences (about 21 words), almost no contractions, and conclusions stated
whole-heartedly. Their weakness is genericness: brochure-style "why us" answers were rated lowest.

What v10's short-answer mode does: one example with the details that matter instead of a run of figures, no
quips or planted metaphors, plain conclusions, long sentences, few contractions and colons. Held-out test (12
questions):

| | judged written by the applicant | mean p | quality | unsupported claims per answer |
|---|---|---|---|---|
| real admitted answers | 100% | 88.1 | 4.4 | |
| plain Claude | 0% | 14.2 | 7.0 | 0.58 |
| v10 | 0% | 16.4 | 7.0 | 1.08 |

v10 matched the real sentence length (19.7 words against 20.8; plain 10.7) and cut contractions from 3.9 to 1.0 per
100 words, but p moved only +2.2 (-1.7 to +6.0), and it added more unsupported content than plain: its rule to state
conclusions "whole-heartedly" turned the applicants' doubts into commitments ("I don't know whether chemistry or
policy" became a stated goal) and added "so" and "because" links. v10.1 fixes that rule: rewritten for the same 12
questions, it had 0.25 unsupported statements per answer, 10 of 12 clean (not a clean held-out check, and not re-judged). Caveat: the
invented applicants were model-made, so judges partly caught invented content, not only the writing. For a real
student the lesson is the reverse of the usual advice: AI help tends to add the over-crafted patterns; their own
plain, committed sentences read as theirs.

## Case 5. "Can you improve it?": editing real writing (benchmark, 2026-11-06)

Human anchor: three kinds of real text written before 2022, 32 of each: essays by English learners in grades 9 to
12 (the ELLIPSE corpus), winning ISEF abstracts, and Turkish charity-run appeals. Each was given to plain Claude
and to the skill with the request a student would actually type, "Can you improve it?" or "Can you fix the grammar
and mistakes?", and a one-line framing (my practice essay, my science-fair abstract, my campaign page). Blind judges
rated single texts in mixed piles; a separate blind checker compared every edit with its original.

What plain Claude returns for "improve it": a new text. It changed 75 to 90 percent of the words and added three
to four statements per text that the writer never made: a thesis preview, a definition, a statistic or an
authority, a reason the writer did not give, a stronger conclusion. Judges rated these edits better written than
the originals and identified them as AI almost every time (0 percent of abstracts and 27 percent of appeals were
judged the writer's own). Even "fix the grammar" rewrote a third of an abstract.

What the skill (v10.1) returns for the same request: the writer's text with errors fixed and the clearest tells cut.
On abstracts and appeals it changed 15 to 24 percent of the words, added 0.1 to 0.3 statements, and 91 to 99
percent of its edits were judged the writer's own, about 36 to 40 points of p above plain on "improve". Quality was 0.25 to 0.45
points lower than plain's rewrite and above the original.

What a human eye notices: in a learner's essay, the errors are the voice. An errors-only copyedit alone dropped the
share judged the student's own from 100 to 61 percent, and every model edit, plain or skill, fell to 5 percent or
below. Judges named what gave the skill's edits away: template transitions ("First", "Additionally", "In
conclusion"), definitions and authorities the student had not written, native idioms, and grammar that was clean
everywhere instead of in places.

What v11 changed: Edit mode now fixes only outright errors and anything that blocks meaning, adds nothing (no
transitions, definitions, examples, statistics, reasons, idioms), never makes a claim stronger, keeps a non-native
writer's grammatical phrasing, and lists up to five bigger changes for the writer to decide on instead of making
them. A learner's practice or graded essay goes to Coach. On held-out texts, v11's "improve" edits changed far
fewer statements (edits with no change in meaning: abstracts 6 to 44 percent, appeals 40 to 100, learner essays 0
to 44) and kept more of the writer's voice (learner essays 6.9 to 8.9 of 10). The human-likeness gain over v10.1
was clear for appeals (+4.1, interval +2.3 to +6.1) and not significant for abstracts or learner essays. The
shipped version, v13, keeps this Edit mode unchanged.

The lesson for a student: "improve it" is the most common request and the one where plain Claude does the most
damage, because it answers a request for help with a rewrite in its own voice. Ask for errors to be fixed and
bigger changes to be listed, and make those changes yourself.

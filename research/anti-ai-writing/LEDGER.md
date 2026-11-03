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

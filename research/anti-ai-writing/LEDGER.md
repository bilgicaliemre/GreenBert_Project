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

## Benchmark: real charity-run appeals (in progress)

Human anchor: "Why I run" texts that runners wrote for their charity-run campaign pages before 2022, sampled at
random from a Turkish fundraising platform, with the platform's default template sentences, links and sign-off
names removed. For each, the runner's notes are reconstructed (facts and feelings, none of the wording), and the
appeal is rewritten from the notes by plain Claude and by the skill. Blind judges read piles of single appeals
(any mix of real and model-written) as a donor and as an NGO editor, and rate how likely the runner wrote each one,
how likely they would give, and how well it works. Results will be added here and in DEVLOG.

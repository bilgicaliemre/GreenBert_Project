# anti-ai-writing v9: changelog

Base: v8. Built against real charity-run appeals: "Why I run" texts that runners wrote for their campaign pages for
events up to 2022, on a Turkish fundraising platform (32 for development, 16 held out and never read during
development). Changes: a new `references/messages.md` and four lines of `SKILL.md`. Personal-essay and academic
guidance are unchanged. DEVLOG section 22 has the full record; LEDGER.md case 2 has the plain-vs-skill-vs-human view.

1. **New guide for messages and appeals** (`references/messages.md`): write only in the readers' language and never
   append a translation; an appeal page may start from the writer's reason, while messages that need action keep
   the request in the first two lines; let one part carry the text instead of the same six-part plan; keep money
   concrete; mix long and short sentences; punctuate like the register (no semicolons, a colon only before a list or
   link, no circumflex in casual Turkish unless the user writes it, one exclamation mark at the ask is normal);
   leave the notes' spoken tics ("bence", "I think") behind; invent nothing.
2. **Dashes now become commas, full stops or parentheses**, not colons and semicolons (Format row), and the
   over-correction check names semicolons and colons. On the appeals, v8's dash rule had tripled the semicolons of
   real writers, and judges cited semicolons in two thirds of their verdicts on v8 texts. This line also applies to
   other genres, where it was not re-tested.
3. **Genre note** "Emails, messages and appeals" points to the new guide.

Held-out test (16 appeals, two blind judges reading piles of 12 single appeals, 96 ratings), v9 against v8: judged
written by the runner 59% vs 12%; p(human) +11.7 [+5.5, +17.9]; would-give +0.12 [-0.22, +0.47]; quality
-0.06 [-0.38, +0.28]; unsupported claims per text 0.00 vs 0.06. The real appeals were judged human 100% of the time
and every model text still scored below every real one (AUC 1.00): v9 reads far more like a runner, but a side-by-
side reader can still tell.

On development, v8 had been no better than plain Claude on this genre (p(human) -2.2 [-5.2, +0.8]).

Frozen before the held-out test: content hash 6e56b690fba3cd03 (sha256 of the files' contents in sorted path order,
first 16 hex digits).

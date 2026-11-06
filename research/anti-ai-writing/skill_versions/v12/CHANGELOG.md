# v12: genre rules scoped to their genre (tested, not shipped)

Content hash `0fd7410cda39fa06`. Same as v11 (see `../v11/CHANGELOG.md`) except:

- The mode table now says to read only the matching reference ("the rules in the other references are for other
  kinds of text").
- `short-answers.md` rule 5 forbids causes or reasons the student did not give, but allows putting the student's
  facts in order and joining them into one story.
- `short-answers.md` rule 6 and the checklist allow ordinary contractions ("stripping every one makes a
  17-year-old sound stiff").

Why: a regression check on the 16 phase-3 briefs (ten genres) found v10.1 behind v9 in 28 of 32 blind panel
judgments. Causes found by reading the judgments: every reference was loaded for every brief, so short-answer rules
(no contractions, no quips, no links between facts) leaked into blogs, emails and essays.

Result on the 20 phase-2 development briefs (40 judgments, four versions per panel): v12 still trailed v9 (ranked
above it in 13 of 40; mean rank 0.65 worse, interval 0.05 to 1.2), and on the 12 school briefs it trailed two
independent v9 samples in 16 of 24 judgments each. Not shipped; v13 moves the mode table, which fixed most of it.

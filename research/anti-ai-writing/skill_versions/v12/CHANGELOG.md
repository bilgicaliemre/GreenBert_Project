# v12: genre rules scoped to their genre (tested, not shipped)

Content hash `0fd7410cda39fa06`. Same as v11 (see `../v11/CHANGELOG.md`) except:

- The mode table now says to read only the matching reference ("the rules in the other references are for other
  kinds of text").
- `short-answers.md` rule 5 forbids causes or reasons the student did not give, but allows putting the student's
  facts in order and joining them into one story.
- `short-answers.md` rule 6 and the checklist allow ordinary contractions ("stripping every one makes a
  17-year-old sound stiff").

Why: a regression check on the 16 phase-3 briefs (ten genres) found v10.1 behind v9 in 28 of 32 blind panel
judgments. In that check the evaluation script gave every version every reference file it has, so v10.1 (unlike v9,
which has no short-answer or research guide) saw the short-answer rules on every brief, and its blogs, emails and
essays read stiff. The router sentence was written to stop that leak.

Result on the 20 phase-2 development briefs (40 judgments, four versions per panel): v12 still trailed v9 (ranked
above it in 13 of 40; mean rank 0.65 worse, interval 0.05 to 1.2), and on the 12 school briefs it trailed two
independent v9 samples in 16 of 24 judgments each. Not shipped.

Correction (found by the final paper review): in these later checks the script gave every version, v9 included,
only the reference its router points to. No rules could leak, yet v11 and v12 still trailed v9, so the leak was
not the main cause of the regression, and the checks did not test the new router sentence at all (only the
loosened short-answer rules, which apply to two of the five genres). v13's move of the mode table is the change that
recovered most of the gap.

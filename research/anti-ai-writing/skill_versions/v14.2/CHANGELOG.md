# v14.2: a full application draft when the student asks for one (shipped)

Content hash `21e9755eebedc2db` (v14.1: `c8a3b4699a5ee62d`). SKILL.md grows from 3,462 to about 3,640 words. DEVLOG
section 27 has the record.

Why: the user asked to see the skill's complete draft of an application answer, to study how it builds one, and said
those drafts are not for submission. Through v14.1 the skill never wrote a real student's application essay.

What changed:
- Hard rule 5 now says application essays and graded schoolwork are coached by default, with one exception.
- New paragraph in Coach, "Full draft on request" (application essays and short answers only). When the student
  explicitly asks for a complete draft of their own essay or answer, the skill writes it from their material
  (personal-essay.md section 10 or short-answers.md), marks every missing detail, motive, reason or feeling with
  `[ask: …]`, and after the text lists the `[ask]`s, the choices the student must confirm, the program's rule on
  AI-written text if known, and that the submitted version should be their own writing. It does not offer a draft
  unprompted. Graded schoolwork and science-fair entries stay coached.
- Mode table rows for admission essays and short answers, the Rebuild pointer, `short-answers.md` (intro) and
  `personal-essay.md` (section 2, section 10 title and first paragraph) say the same.
- The skill description now reads "coaches college application essays (writing a full draft only when the student
  asks for one)".

Test (`eval/results/v14.2/probe_graded.json`; fictional students, 2 samples per case, graded blind against the
expected behavior): "write my Common App essay" got a full draft with `[ask]`s and no invented facts (2 of 2); "help me
with my essay" got coaching and no offer of a draft (2 of 2); graded homework stayed coached (2 of 2, one sample
stated its reason twice and mentioned the session's own request, a workflow relay artifact); "improve my 150-word
answer" got errors fixed in place and nothing rewritten (2 of 2). 7 of 8 passed every criterion.

Not tested: writing from notes and the edit benchmark (the change touches only application requests).

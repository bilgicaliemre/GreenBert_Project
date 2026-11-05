# Mode benchmarks (v10): research abstracts and short answers

Scripts behind DEVLOG section 23. Texts (real and generated), notes and pile keys are private and not in this
repository; only aggregate results are (`eval/results/modes/`).

## Design

- **Human anchor.** Research: winning ISEF abstracts 2014 to 2021 from the Society for Science abstract database
  (`research_abstracts/isef_*.py`; no finalist names or schools are stored). Short answers: answers that admitted
  students published themselves (MIT applicants in The Tech and on MIT's blogs; Tufts' admissions blog), classes of
  2026 or earlier.
- **Writers.** One agent writes 3 or 4 texts for different people, each handled "as if it were the only request".
  Plain = the request alone. Skill = the request plus SKILL.md, the genre's reference and `tells.md`, embedded in
  the prompt. All agents run in a single turn with every input in the prompt (`tools/mkwf.py` writes a workflow
  script with the data embedded), so private texts never pass through the orchestrator's context.
- **Research notes** are reconstructed from each real abstract (facts and numbers, no runs of more than four words).
  Batches of six were stopped by a safety classifier in five of seven jobs; single items and pairs went through.
- **Short-answer notes were NOT reconstructed from real answers.** An agent refused (22 of 28 items) on the
  grounds that it turns a real student's personal essay into source material for new application essays. We
  accepted that: `short_answers/build_notes_REFUSED_not_used.py` is kept only as a record. Writers instead get
  notes for invented applicants (`build_personas.py`), one per real prompt; the generator never saw the real
  answers. Real answers appear only as the human anchor in the judge piles.
- **Judges** read piles of 12 to 16 single texts by different people, any mix of real and model, normalized
  (straight quotes, single spaces), and rate p(human) 0 to 100, quality 1 to 10, with evidence. Two lenses per
  genre (ISEF judge and student-journal editor; admissions reader and essay coach). Each lens gets its own random
  piles. `tools/analyze.py` reports judged-human share, mean p, AUC against the real texts per lens, quality, and
  paired bootstrap intervals over items; `tools/cues.py` is a keyword scan of the judges' evidence;
  `tools/features.py` gives surface features.
- **Fidelity** (`bench.fid_spec`): a blind checker lists every statement in a text that its notes do not support.
- **Copyedit control** (research): real abstracts with outright errors fixed and nothing else, to test whether
  judges recognize real abstracts by their errors.

Paths in `tools/bench.py`, `tools/wfread.py` and `tools/waitwf.sh` point to the session that ran them; change
them to rerun.

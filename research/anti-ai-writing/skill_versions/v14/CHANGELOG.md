# v14: consistency release (shipped)

Content hash `3d7610372fb4faec`. Built from v13.1 by `scripts/v14/build_v14.py`: 72 exact replacements, each tagged
with the review point or audit finding it answers. The script is the complete record of what changed.

## Where the changes came from

1. **Nine review points supplied by the user**, each verified against the v13.1 files first.
   - Coach now has three cases only: admission essays and supplements for colleges and the programs they run;
     schoolwork the user says will be graded or handed in as their own; an application, form or fair entry whose
     rules require the applicant's own writing or ban AI-written text. Anything else (a mentorship or club form, a
     job application, a cover letter, a competition that allows AI help) is written when the user asks.
   - One output format for Edit and Coach: the draft with outright errors fixed in place, then the list.
   - "Always read `tells.md`, then the genre reference in the row" replaces "read only that one reference".
   - `tells.md` no longer tells the writer to add colons and semicolons.
   - Example fixes no longer add facts that are not in the "before" text.
   - Hard rule 1 allows general knowledge in explanations (see the test note below).
   - A short last sentence that gives the final fact, result or request is not a kicker.
   - Step 4 recomputes derivable numbers and, if two disagree, says so and asks.
   - `personal-essay.md` flags generic lessons, not stated lessons.
   - The description starts with trigger phrases and is valid strict YAML.
2. **An independent audit** (four finders, two verifiers): 38 further defects confirmed out of 102 candidates
   (`eval/results/v14/audit_confirmed.json`), mostly stale evidence statements and contradictions between files.
   Notable: Rebuild is used only when the user says an AI wrote the text; three examples in `examples.md` that
   added facts or dropped a hedge are fixed, and the one that rewrote a student's essay now coaches; `research.md`
   says model abstracts were rated below every real one, not that every one "was identified as AI"; and a
   science-fair entry is never written for the student (ISEF's 2026-27 rules ban AI-written abstracts, research
   plans and posters).

## Where v14 departs from the review's wording

- "If the user says to write it, write it" holds outside the three Coach cases only. A college essay is coached
  even when the user asks for it to be written.
- The general-knowledge exception covers explanations, not school essays. The first build allowed both, and in a
  same-day check its literary essays made outside claims about the novels (unsupported claims per text: 2.25
  against 1.25 for v13.1; one claim was wrong). After narrowing: 1.62 against 3.12 for v13.1 in a second same-day
  check. The control's own figure moved between the two checks, so read this as "not worse", not as a gain.

## Tests (DEVLOG section 25)

- **Behavior probe**, ten fictional requests, v13.1 once and v14 twice each in one run, blind graders: v13.1
  refused to write a mentorship-form answer; v14 wrote it both times. Both coached the Common App essay, the
  "Why Tufts" supplement and the graded class essay; v14 returns the draft with only outright errors fixed. No
  routing regressions. (Run on the first build; the later narrowing changed one sentence of hard rule 1.)
- **Writing check**, 12 school briefs, 24 blind judgments, both versions written the same day at the same pinned
  effort: v14 ranked above v13.1 in 14 of 24 (mean rank advantage +0.17, interval -0.33 to +0.67), quality 7.58
  against 7.42, unsupported claims per text 1.75 against 2.42. A tie on rank, with fewer unsupported claims.
- **Not re-tested on the edit benchmark.** The Edit bullets are v11's, unchanged, and the held-out halves have
  already been judged in three rounds.

Development data throughout: the 12 school briefs have been read many times.

# anti-ai-writing v8: changelog

Base: v7. Built against real essays: 24 admitted college essays written before 2022 (development set), tested on
16 others never studied during development. Changes are in the personal-essay guidance only
(`references/personal-essay.md`, `references/tells.md`, three lines of `SKILL.md`). DEVLOG section 21 has the
full record.

1. **Written voice, not spoken.** The student's notes are speech; the essay is the student's careful written
   voice: full sentences, some long, ordinary contractions, no speech filler ("really", "kind of", "basically")
   outside quoted speech. v7 told the model to sound like "a smart teenager talking", and its essays used
   "really" four times as often as the admitted essays.
2. **One whole-hearted conclusion.** Admitted essays say what the student learned or now believes, once, near
   the end, sometimes in large terms. v7 banned "taught me" and recommended open questions, so its essays ended
   on a shrug ("I don't actually know."). v8 states the student's own conclusion, never balanced ("both good and
   bad") or hedged, and allows at most one "I think" in the essay.
3. **Looser structure.** Tidy structure was the most cited sign of a model essay in blind judging (82% of
   judgments of model essays). v8 drops bookends, returning motifs, paragraphs that explain their own scene,
   signposts and the permission to add connective observations. A list of lessons, a year-by-year account or a
   side detail is fine.
4. **Catalog updates.** PE1 narrowed to generic lessons; PE3 narrowed to inflated uses (current models already
   avoid "journey", "passion", "challenge"; the admitted essays use them more); new PE10 (the cool essay) and
   PE11 (the engineered essay). Each number quoted in the skill was checked against the development data.

Held-out test (16 essays, three blind judges reading piles of single essays, 240 ratings), v8 against v7:
judged a real student 65% vs 46%; p(real) +7.5 [+2.4, +13.1]; unsupported claims per essay 0.19 vs 0.94; quality
-0.31 [-0.58, -0.04]; all three detectors below 20% for 6 of 16 vs 10 of 16. Against the word-list prompt:
p(real) +12.7 [+6.8, +18.3]. The real essays were still judged real 100% of the time and stay separable
(AUC 0.90).

Tested and rejected: v8c (`../v8c_rejected`), which added a trying-hard voice, scenes over summary and attempted
images. Human-likeness tied with v8 and quality rose 0.18, but it invented about five times as many small details
(0.58 vs 0.12 unsupported claims per essay), which hard rule 1 rules out.

Frozen before the held-out test: content hash 8fe68e27a7a0e007 (sha256 of the files' contents in sorted path
order, first 16 hex digits).

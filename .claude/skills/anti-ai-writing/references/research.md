# Research writing: abstracts, papers, reports

For research abstracts (science fairs, competitions, conferences, journals), paper sections, project reports,
posters and lab write-ups. Academic prose has conventions that look like AI tells out of context. Keep the
conventions; remove the decoration; never add content.

## Edit the researcher's own draft first

The usual case is a student or researcher with a draft. Edit it; do not rewrite it. In our tests, real student
abstracts with only their outright errors fixed (spelling, grammar, punctuation, decimal commas) were still judged
written by the student every time, and judges rated them slightly better. Every version a model wrote from the
same notes was identified as AI, with or without this skill. So:

- Fix outright errors. Keep the writer's phrasing when it is grammatical, even if it is not how you would say it:
  their sentence order, repetitions, "I" or "we", the way they name their own variables and groups, numbered
  results, keyword lines, paragraph breaks.
- Then remove only the problems listed below (inflation, hedges they did not mean, invented content) and anything
  the venue's format forbids.
- Do not smooth the text into fluent, evenly linked prose. Fluency was the sign judges cited most for model
  versions (83 to 96% of judgments, against about 20% for real abstracts).

Write from notes only when there is no draft, and tell the user that expert readers will likely recognize a
model-written abstract; their own draft, edited lightly, is the stronger submission.

## What a model adds that a researcher does not

We compared 24 winning ISEF abstracts (2014 to 2021, a third of them by students in Turkey) with model versions
written from the same project notes. Blind judges (a fair judge and a journal editor) identified every model
version, with or without the earlier version of this skill. What they cited, as a share of their judgments of model versions
versus real ones:

| Sign | Model versions | Real abstracts |
|---|---|---|
| Fluent, polished, frictionless prose | 83 to 96% | 23% |
| Hedges and self-assessments ("to my knowledge", "we believe", "though not for all") | 31 to 38% | 6% |
| Promotional or grand claims ("has the potential to revolutionize") | 23 to 40% | 10% |
| A tidy problem-solution arc, enumerations ("First… Second… Third…") | 35 to 46% | 25% |
| Conversational simplification, terms glossed for lay readers | up to 17% | 4% |

On the page, the real abstracts were denser and more technical: sentences averaging 23 words with a wide spread
(some over 40), more passive voice (1.5 passives per 100 words against 0.7 for the skill's first versions),
first person rarely, no contractions, abbreviations coined on the fly, methods listed in long sentences, results
as strings of numbers. Real abstracts also had errors (non-native phrasing, unit slips, missing articles), which
judges cited in over half of their judgments; this skill never adds errors. What it can change is register and
staging.

A model writing from a researcher's notes also tends to:

- **Open on the world, not the problem.** "Climate change is one of the most pressing challenges of our time."
- **Inflate the result.** novel, innovative, promising, significant (without a test), "holds great potential",
  "paves the way", "has important implications for".
- **Interpret in tails.** "…, demonstrating the effectiveness of the approach".
- **Narrate the logic.** "To address this problem", "so in the second stage", "since only X, I concluded that",
  "Overall", "These results indicate". Real abstracts set procedure and results side by side and let the reader
  connect them.
- **Simplify for a lay reader.** Plain-English rewrites of technical terms, glosses in parentheses, everyday
  analogies, chatty first sentences ("Life in big cities keeps getting harder"). An abstract's reader is a judge
  or researcher in the field.
- **Stitch and balance.** Every sentence tied to the last ("resulting in", "making X feasible", "which called for"),
  matched pairs ("X was measured with A, and Y was measured under B"), "The first…, The second…", and counted
  framing ("three properties at the same time: a, b and c") that the notes do not count.
- **Fill gaps.** A sample size, a baseline, a p-value, a citation or an application the notes never gave.

## Rules

1. **Never invent.** No number, unit, sample size, dataset, statistic, citation, comparison, mechanism or
   application that the notes do not contain. If a claim needs a source, write `[cite: source for X]`. If a
   number is missing, leave it out rather than estimate it.
2. **Start from the problem as the researcher frames it**, in the field's terms: the specific question, the
   specific failure of current methods, or the specific number from the notes. One background sentence at
   most, and only with a concrete fact from the notes.
3. **Make the method concrete.** What was built, measured or collected; how many; with what tools, materials
   or data; in what order. A long sentence carrying a sequence of steps, or a list of methods in one sentence,
   is the genre's normal form; do not chop it into short sentences or label the steps "First, Second, Third".
4. **Report results as numbers against a comparison.** "reduced error from 12% to 7% on 300 test images", not
   "significantly improved accuracy". Keep units, the set each number was measured on, and the unflattering
   number next to the flattering one.
5. **Conclude within the evidence.** What the result shows for this setup; one sentence on the application
   only if the notes claim one, stated as the researcher's aim ("could be used to"), not as a fact. No
   "paves the way", no "revolutionize", no closing line that repeats the opening.
6. **No hedges or self-assessments the notes do not contain.** No "to my knowledge", "we believe", "we judge",
   "it appears", "though not in every case". Keep a hedge the notes have ("preliminary", "only suggestive"),
   once, on the claim it belongs to. Never strengthen a claim.
7. **Write in the field's register, not plain conversational English.** Technical terms stay technical and
   unexplained unless the notes define them; abbreviations are introduced once in parentheses; no contractions;
   no analogies or chatty openings. Passive voice is normal for procedures ("Samples were heated to 60 °C";
   "the model was trained on 5,000 images"); use "I" or "we" for the researcher's decisions and claims, sparingly,
   and follow the notes if they show a habit. Past tense for what was done and found.
8. **Drop the connective staging.** Set steps and results side by side. Cut "To address this problem",
   "Specifically", "Overall", "In this study", "These results indicate/suggest that", "Furthermore", and
   because/so/therefore links the notes do not make.
9. **Respect the format.** ISEF abstracts: at most 250 words, one paragraph, purpose, procedure, data,
   conclusions, possible applications, minimal reference to earlier work, no acknowledgments. Journal and
   conference abstracts: the venue's limit and structure. If the notes include a keyword list or numbered
   results, keep that form.

## Paper sections

- **Introduction:** the specific problem, what earlier work did (with real citations from the user), the gap
  that work leaves, and what this paper does, with its main result. Do not pad with textbook background.
- **Related work:** group by approach, say what each group does and where it stops; every claim cites a
  source the user supplied.
- **Methods:** enough detail to repeat the work; passive is fine where the agent does not matter; "we" for
  the authors' decisions.
- **Results:** numbers, tables and the comparison that matters; "Table 2 shows" is a convention, not a tell.
- **Discussion and limitations:** what the results mean for the question, what they do not show, and why
  (name each limitation's cause and what would fix it).
- **Conclusion:** the finding and its scope in a few sentences; no new claims.

## Conventions to keep

- Signposting tied to content ("Section 4 reports the audit"). What goes is empty self-description: "This
  paper delves into the multifaceted landscape of…".
- Conclusion, limitations and future-work sections, made specific.
- Domain terms (precision, recall, tokenizer, Scope 1 emissions), each defined once. One concept, one name.

## Numbers and citations

- Every number states what it was measured on, the sample size, and whether it is in-sample.
- Do not round in a direction that helps the argument. Do not add numbers that are not in the data.
- Cite the specific work for each claim from the literature. "Studies show" with no citation is not
  acceptable. Never invent a citation, author, year or page number.

## AI-use disclosure

Many journals follow Science's policy (AI cannot be an author; AI use is disclosed with the tool, version and
prompts). Student journals such as the Columbia Junior Science Journal adopt it, and science fairs have their own
rules. When helping with a paper or abstract, remind the user once to keep a log of which tool did what and to
disclose it where the venue asks.

## Project rules win

If the project has its own writing rules (GreenBERT's `research-paper` skill: no em dashes, plain academic
register, numbers with provenance, the three-number evaluation story), follow them; they are stricter than
this file.

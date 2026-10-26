# Academic register: reports, papers, lab write-ups

Academic prose has conventions that look like AI tells out of context. Keep the conventions; remove the
decoration.

## Conventions to keep

- **Signposting tied to content.** "Table 2 shows…", "Section 4 reports the audit." Readers navigate by it.
  What goes is empty self-description: "This paper delves into the multifaceted landscape of…".
- **Conclusion, limitations and future-work sections.** Required. Make them specific: name each limitation's
  cause and what would fix it.
- **Hedges that carry uncertainty.** "suggests", "may", "in our sample" belong on results from small or
  in-sample data. One hedge per uncertain claim, attached to the uncertain part. Never strengthen a claim
  while editing.
- **Passive voice in methods** where the agent does not matter ("Sentences were split with NLTK"). Use "we"
  for the authors' own decisions ("We dropped sentences without a verb").
- **Domain terms.** Precision, recall, tokenizer, Scope 1 emissions are not jargon in a paper. Define each once.
- **One concept, one name.** Do not alternate "claim", "statement" and "assertion" for the same object.

## Decoration to remove

- "significant" without a statistical test: give the number instead.
- novel, groundbreaking, comprehensive, robust (non-statistical), crucial, pivotal, "sheds light on",
  "paves the way", "a growing body of research" without citations.
- "-ing" tails that interpret results: "…, highlighting the effectiveness of our approach".
- Noun stacks: "the implementation of the optimization of the extraction process". Write the verb with its
  subject: "we changed how the extractor filters sentences".
- Paragraph-ending summaries that repeat the paragraph's first sentence.
- Bullet lists inside Methods or Discussion where reasoning should connect.

## Numbers

- Every number states what it was measured on, the sample size, and whether it is in-sample.
- Do not round in a direction that helps the argument. Do not add numbers that are not in the data.
- Report the unflattering number with the flattering one.

## Citations

- Cite the specific work for each claim from the literature. "Studies show" with no citation is not
  acceptable. Never invent a citation, author, year or page number; if a source is needed and not supplied,
  leave `[cite: source for X]`.

## Project rules win

If the project has its own writing rules (GreenBERT's `research-paper` skill: no em dashes, plain academic
register, numbers with provenance, the three-number evaluation story), follow them; they are stricter
than this file.

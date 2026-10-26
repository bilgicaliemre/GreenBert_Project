# Catalog of AI-writing tells (evidence-graded), for an anti-AI-writing skill

Compiled 2026-10-20 for a skill that makes Claude-written or Claude-edited prose (essays, a research
paper/report, personal essays) read like a strong human writer. Every tell has: the pattern, one short
example, the fix, and an evidence grade with a source URL. Working notes with longer extracts are in
`notes_sources.md` next to this file; raw downloads are in `downloads/`.

## 0. How to read the evidence grades

| Grade | Meaning |
|---|---|
| **M** | Measured: corpus frequency vs a human baseline, with numbers (e.g. "28x the expected rate"). |
| **E** | Experiment: controlled human-preference, rewriting or detection experiment. |
| **A** | Systematic annotation: trained or expert annotators coded many texts (rates of mention, not rates of use). |
| **C** | Community/editor observation: curated field guides with real examples (Wikipedia), journalists, writing coaches, open-source skills. No rates. |
| **U** | UNVERIFIED: seen only in a secondary summary, a single weak source, or a paywalled piece I could not read. |

Access notes (so later readers know what was and was not read first-hand):
- `en.wikipedia.org` is blocked by this session's proxy and the WebFetch tool failed DNS for every host. The full
  Wikipedia page "Signs of AI writing" was read through the alphaXiv web reader (rendered page, then
  `action=raw&section=N` for the sections past a 100k-character cutoff). The page says "As of October 2026".
  Sections read in full: Caveats, all of Content, all of Language and grammar, Style (title case, boldface,
  inline-header lists, emoji), Communication intended for the user, Comment-specific indicators, Miscellaneous,
  Signs of human writing, Ineffective indicators, Historical indicators. Not read: Markup, Citations, Edit
  summaries, heading-error and curly-quote subsections (low relevance to essays).
- NYT (Kriss, Dec 2025) and The Economist (Jul 30 2026) are paywalled. Economist findings below come from a
  verbatim quote on Daring Fireball; Kriss details come from secondary summaries and are marked U.
- All arXiv papers were read via alphaXiv (`get_paper_content`/`answer_pdf_queries`), not from memory.

## 1. What the evidence says overall (read this before the list)

1. **Tells are real and measurable, but they move.** Kobak et al. found at least 13.5% of 2024 PubMed abstracts
   were LLM-processed, detectable from excess style words alone
   ([Science Advances 2025](https://www.science.org/doi/10.1126/sciadv.adt3813)). But word habits change per model
   version: Graphite found 55–72% of tells are unique to one of two consecutive versions in a family, and 65% are
   unique to one model family ([Graphite, Sep 2026](https://graphite.io/five-percent/research/ai-tells)).
   "delve" fell to 1 in 1,000 ChatGPT chats by July 2025
   ([Washington Post via Boston Globe](https://www.bostonglobe.com/2025/11/13/business/chatgpt-writing-style-clues/)).
   Implication: a skill built only on a banned-word list goes stale. Target mechanisms (staging, inflation,
   genericness, uniform rhythm) first; treat word lists as a second pass.
2. **The root mechanism is regression to the mean plus preference training.** Wikipedia: LLMs replace "specific,
   unusual, nuanced facts" with "generic, positive descriptions"; the text becomes "less specific and more
   exaggerated" ([WP:AISIGNS](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)). Instruction tuning,
   not pre-training, produces the noun-heavy dense style ([Reinhart et al., PNAS 2025](https://arxiv.org/abs/2410.16107)).
   Human raters in a preference experiment chose texts with "LLM-favored" words 52.4% vs 47.6% (p<0.01)
   ([Juzek & Ward 2025](https://arxiv.org/abs/2508.01930)); reward models and LLM judges prefer "not X, but Y" even
   where the context does not call for it ([Peng et al., Oct 2026](https://arxiv.org/abs/2610.22249)).
3. **Density beats single sightings.** "One or two of these words appearing in an edit may be coincidental, but an
   edit ... introducing lots of them, lots of times, is one of the strongest tells" (WP:AISIGNS). Expert detectors
   misfire when human text happens to contain "delve" or "crucial": 31% of experts' wrong explanations cited
   vocabulary ([Russell et al. 2025](https://arxiv.org/abs/2501.15654)).
4. **Experienced readers catch AI prose by more than words.** Five heavy-LLM-user annotators, by majority vote,
   misclassified 1 of 300 articles, even after paraphrasing and an o1-pro "humanizer" built from their own clue list
   (Russell et al. 2025). Admissions officers reached AUC 0.70 and rated essays they believed were AI lower; applicants
   with AI-written essays were admitted less often ([Isley, Gaebler, Goel, Sep 2026](https://arxiv.org/abs/2609.22549)).
   So surface scrubbing is not enough; the content tells (no specifics, no stakes, tidy lessons) carry weight.
5. **Banning things backfires.** Telling a model to avoid a word list "has limited efficacy and may induce a backfire
   effect due to the 'Pink elephant problem'"; hard token bans at 8k patterns collapsed writing-quality scores to 28/100
   ([Antislop, Paech et al. 2025](https://arxiv.org/abs/2510.15061)). Anthropic's own guidance for [a Claude model] (stated for
   frontend design) says a general "avoid a generic AI look" instruction "mostly swaps one default for another"; naming
   specific patterns and iterating works better
   ([Prompting [a Claude model]](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5)).
6. **The current Claude profile is not the 2024 ChatGPT profile.** For [a Claude model] (released 2026-09-22), Graphite
   measured em dashes at 0.015 per 1,000 words (99% below [a Claude model], far below human), mannered prose at about 1.6x the
   human score, and 2,548 remaining tells, including "this matters" (116x human), "why _ matters" (92x),
   "is more than a _ it" (98x), "rather than simply" (32x), "looking ahead the" (40x), "what comes next" (24x),
   evaluative adjectives (dependable 23x, steady 11x, thoughtful 9x, meaningful 8x), superlatives ("the most powerful"
   24x Astra's rate) and helpfulness phrasing ("can help you" 8x [a Claude model]'s rate)
   ([Graphite [a Claude model] update, Oct 2026](https://graphite.io/five-percent/research/ai-tells-opus-5-5-update)).
   An anti-AI skill run on [a Claude model] should spend its effort there, not on em dashes.
7. **Quality, not evasion.** Detectors are unreliable and biased (61% false-positive rate on non-native TOEFL essays,
   [Liang et al. 2023](https://arxiv.org/abs/2304.02819); 76% FPR on formal human abstracts for one RoBERTa detector,
   [Creanga & Dinu 2026](https://arxiv.org/abs/2610.03110)). Claude models launched on or after 2026-08-02, including
   [a Claude model], embed an imperceptible text watermark that "may persist through some editing"
   ([Claude support: How Claude marks AI-generated content](https://support.claude.com/en/articles/16266773-how-claude-marks-ai-generated-content)).
   Style edits are for the reader. They are not a disguise, and the student should follow school disclosure rules.

---

## 2. Vocabulary

### V1. Classic "AI vocabulary" (style verbs and adjectives)
- **Pattern:** a cluster of formal, mostly positive style words that rose abruptly after ChatGPT: delve, underscore,
  showcase, highlight (verb), intricate/intricacies, meticulous(ly), realm, pivotal, crucial, garner, boast (= has),
  bolster, align with, foster, enhance, emphasize, interplay, tapestry, testament, vibrant, landscape (abstract),
  commendable, notable/noteworthy, invaluable, multifaceted, nuanced, comprehensive, seamless(ly), groundbreaking,
  surpass, unveil, encompass, grapple.
- **Example:** "This study delves into the intricate interplay between sleep and memory, underscoring the pivotal role
  of REM." (pattern taken from real 2023 abstracts quoted by Kobak et al.)
- **Fix:** say what happened with plain verbs and the actual finding: "We tested whether REM sleep affects recall.
  Students who lost REM sleep recalled 12% fewer words." Do not swap in synonyms; rewrite the sentence around its claim.
- **Evidence: M (strong).**
  - Kobak et al., 15.1M PubMed abstracts: excess ratio in 2024 vs 2021–22 trend: delves 28.0x, underscores 13.8x,
    showcasing 10.7x; biggest absolute gains: potential (+5.2 pp of abstracts), findings (+4.1), crucial (+3.7).
    2024 excess words were 66% verbs and 14% adjectives (Covid-era excess words were nouns).
    [paper](https://arxiv.org/abs/2406.07016), [data](https://github.com/berenslab/llm-excess-vocab).
    I recomputed the ranking from their released counts; full ranked list: `kobak_style_words_2024_ranked.tsv`
    (top: delves 28.0, underscores 13.8, delved 12.2, showcasing 10.7, meticulously 10.4, delve 7.9, intricacies 7.6,
    underscoring 7.5, intricate 7.4, surpassing 7.1, commendable 6.8, underscore 6.7, excels 5.8, garnered 5.3, realm 5.0,
    renowned 4.9, grappling 4.9, groundbreaking 4.8, emphasizing 4.7, encompassing 4.4, revolutionizing 4.1, aligning 4.0,
    formidable 3.9, showcases 3.8, bolstering 3.8, advancements 3.6, heightened 3.6, notable 3.4, unveiled 3.4).
  - Liang et al. (ICLR 2024 peer reviews): "commendable" 9.8x, "meticulous" 34.7x, "intricate" 11.2x more likely per
    sentence; top-100 AI adjective and adverb lists in their appendix ([arXiv 2403.07183](https://arxiv.org/abs/2403.07183)).
  - Liang et al. (arXiv CS abstracts): realm, intricate, showcasing, pivotal flat 2010–2022 then surged
    ([arXiv 2404.01268](https://arxiv.org/abs/2404.01268)).
  - Juzek & Ward: 21 "focal words" (delves +6697% 2020→2024 in PubMed, showcasing, boasts, underscores, comprehending,
    intricacies, surpassing, garnered, emphasizing, realm, groundbreaking, advancements, aligns ...)
    ([COLING 2025](https://arxiv.org/abs/2412.11385)).
  - Reinhart et al.: GPT-4o uses camaraderie 162x, tapestry 155x, intricate 119x, underscore 107x, amidst 100x,
    palpable 95x, solace 95x the human rate; "tapestry" appeared in 23% of GPT-4o outputs (PNAS 2025).
  - Russell et al.: vocabulary was the most cited clue (53.1% of expert explanations); examples vibrant, crucial,
    significantly.
- **Caveat:** these words are not banned in English. "Robust" in statistics, "significant" for a p-value,
  "underscore" for the character, "landscape" for terrain are fine (WP:AISIGNS: take the list "as literally as possible";
  synonyms are not tells). Two or three in a whole report is noise; three in one paragraph is a tell.

### V2. Era- and model-specific word sets (the list changes)
- **Pattern / data (who overuses what):**
  - GPT-4 (2023–mid-2024): Additionally, boasts, bolstered, crucial, delve, emphasizing, enduring, garner, intricate,
    interplay, key, landscape, meticulously, pivotal, underscore, tapestry, testament, valuable, vibrant (WP:AISIGNS).
  - GPT-4o (mid-2024–mid-2025): align with, bolstered, crucial, emphasizing, enhance, enduring, fostering, highlighting,
    pivotal, showcasing, underscore, vibrant (WP:AISIGNS). WaPo: by July 2025 GPT-4o had cut ensure, various, crucial,
    significant, approach, and raised "core" (5x) and "modern" (in over 8% of messages).
  - GPT-5 (mid-2025–mid-2026): emphasizing, enhance, highlighting, showcasing, plus "canned media-coverage" phrasing (WP).
  - GPT-6 Astra (2026): dependable 59x, practical 26x, meaningful 13x; "another dimension" 117x, "together these" 95x;
    corrective framing (see S1) and hedges ("may" 3x GPT-4.1) up; marketing words (unlock, elevate, streamline, leverage,
    boost, payoff, tangible) down 73% vs GPT-4.1 (Graphite). Wikipedia adds challenge, clearer, dependable, echoed,
    foster, leverage, matters, multifaceted, practical, prioritize, quietly, steady, universally, citing a single
    review blog (grade U for that part).
  - [a Claude model]: "is genuinely" (1,021 occurrences vs 4 in the human corpus), deliberate 26x, steady 6x, "single most", "arguably the
    most", "every single", "matters because" 132x, "matters more than" 93x (Graphite).
  - [a Claude model]: see section 1, point 6. "is genuinely" fell 26x from [a Claude model]; helpfulness phrasing rose (Graphite update).
  - Gemini 3.1 Pro: incredibly 18x, profound 25x, immense 22x, "furthermore the" 43x, "ultimately this" 78x,
    "absolutely essential" 32x, "this comprehensive guide"; contractions nearly gone (Graphite).
  - Grok: causal, empirical, correlate, underscore (WP:AISIGNS).
- **Fix:** check the draft against the current model's list, not just the 2023 list. For [a Claude model] drafts, search for
  matters/matter, genuinely, "rather than simply", "more than just", "what comes next", "looking ahead", dependable,
  thoughtful, steady, meaningful, "the most", "can help you", "makes it easier".
- **Evidence: M** (Graphite: 10,000 human vs 90,000 AI web articles on the same topics, ratio ≥2x human, frequency
  thresholds; single fixed prompt, web-article genre, so ratios are genre-specific). Wikipedia era lists: **C** citing M.

### V3. Evaluative adjectives that rate instead of describe
- **Pattern:** dependable, practical, meaningful, thoughtful, steady, measured, deliberate, valuable, compelling,
  powerful, remarkable, impressive, profound, immense.
- **Example:** "The volunteers did meaningful, thoughtful work that had a powerful impact."
- **Fix:** replace the rating with the observable fact that earned it: "The volunteers sorted 900 kg of donated food
  in two weekends."
- **Evidence: M** (Graphite theme "Evaluative Adjectives: words that rate something without describing it", ratios above;
  Liang adjective list). Russell: AI tone uses "the same language it uses to describe everything - inspirational,
  stunning, essential, and resonating" (A).

### V4. Intensifiers and sincerity markers
- **Pattern:** genuinely, truly, incredibly, absolutely, profoundly, remarkably, enormously, deeply, "every single",
  "the single most", "is genuinely X", "honestly".
- **Example:** "This is genuinely one of the single most important lessons I learned."
- **Fix:** delete the intensifier; if the sentence collapses, the claim needed support, not emphasis: "That lesson
  changed how I study for tests."
- **Evidence: M** for genuinely/incredibly/absolutely/remarkably/enormously/single most (Graphite, both studies).
  "honestly" as a staged-candor opener ("Honestly? It depends.") is **C** (blader/humanizer skill,
  [SKILL.md](https://github.com/blader/humanizer)); I found no frequency study for "honestly" (U as a measured tell).

### V5. Hype and marketing words
- **Pattern:** groundbreaking, revolutionary, transformative, game-changing, cutting-edge, unlock, elevate, streamline,
  leverage, seamless, empower, unparalleled, paramount, "in the heart of", nestled, boasts, "rich heritage".
- **Example:** "GreenBERT is a groundbreaking tool that seamlessly unlocks transparency in ESG reporting."
- **Fix:** state the capability and its limit: "GreenBERT flags ESG claims that lack supporting numbers; on our
  100-claim test set it agreed with a human reviewer 67% of the time."
- **Evidence: M** (Kobak: groundbreaking 4.8x, revolutionize 3.9x; Graphite: Claude hype words "groundbreaking,
  paramount, unprecedented, revolutionary, invaluable, profound, exceptional" declining across versions, GPT marketing
  words down 73%) and **C** (WP:AISIGNS "Promotional and advertisement-like language"; newer LLMs "more subtly positive").

### V6. Avoiding plain copulas and plain verbs ("serves as", "utilize")
- **Pattern:** serves as / stands as / functions as / represents / marks (for "is"); boasts / features / offers /
  maintains (for "has"); utilize, leverage, facilitate, endeavor, commence (for use, use, help, try, start);
  "refers to" in definitions.
- **Example:** "The dataset serves as a cornerstone of our pipeline and boasts 583 labeled claims."
- **Fix:** "The dataset is the core of our pipeline. It has 583 labeled claims."
- **Evidence: M.** "is" and "are" fell more than 10% in arXiv abstracts in 2023; asking GPT-3.5 to "revise the following
  sentences" cut "is" 14% and "are" 17% in CS abstracts ([Geng & Trotta 2024](https://arxiv.org/abs/2404.08627)).
  WP:AISIGNS lists simple is/has phrases and plain verbs (wrote vs authored, used vs utilized, tried vs attempted) under
  "Signs of human writing".

### V7. Noun-heavy, Latinate density (nominalizations)
- **Pattern:** many -tion/-ment/-ity nouns and stacked noun phrases where a verb would do.
- **Example:** "The implementation of the optimization of the classification process resulted in an improvement."
- **Fix:** turn nouns back into verbs with a subject: "We changed how the classifier picks thresholds, and accuracy rose."
- **Evidence: M.** Instruction-tuned models use nominalizations 1.5–2.1x the human rate, "that" clauses as subjects 2.6x,
  phrasal coordination 1.9x (Reinhart et al.). The Economist found "more Latinate suffixes crop up in their writing than
  in human texts" (quoted on [Daring Fireball](https://daringfireball.net/linked/2026/08/11/)). Graphite: AI words average
  5.2–5.7 characters vs 4.9 human.

### V8. Abstract "application-essay" nouns
- **Pattern:** journey, growth, resilience, challenge, community, understanding, experience, passion, perseverance,
  adaptability, "a deep appreciation for".
- **Example:** "This challenge became a journey of growth that taught me resilience and a deeper understanding of community."
- **Fix:** replace each abstraction with the event behind it (who, when, what was said, what you did next).
- **Evidence: M.** On 30,000 real admissions essays vs essays from 8 LLMs, the words most predictive of LLM essays were
  challenge, growth, community, journey, understanding, experience, resilience (largely copied from the prompt);
  human essays were marked by although, year, still, time, many, people, friend, would
  ([Lee, Alvero, Joachims, Kizilcec 2025](https://arxiv.org/abs/2503.20062)).

### V9. Claude's 2026 "agent idiolect" (mostly in technical/explanatory prose)
- **Pattern:** load-bearing, quietly, plainly, genuinely, merely, outright, precisely, structurally, deliberately,
  nobody, seam, "-shaped", teeth ("has teeth"), lever, "buys you", "earns its keep", "the real question".
- **Example:** "That premise is quietly load-bearing; without it the argument has no teeth."
- **Fix:** name the dependency literally: "The argument depends on that premise. Without it, the conclusion does not follow."
- **Evidence: M (for a coding-text genre).** Clustering 461,121 GitHub pull-request descriptions (Jan 2025–Aug 2026) by
  word choice alone, one style grew from 0.7% to 39% of the corpus; "load-bearing" is written 39x more inside it than
  outside ([Abraham, load-bearing](https://github.com/louisabraham/load-bearing),
  [site](https://louisabraham.github.io/load-bearing/)). I read the current fit (generated 2026-10-20; saved as
  `downloads/loadbearing_analysis.js.txt`): its top words include vacuous, refusing, load-bearing, premise, quietly,
  plainly, outright, nobody, restated, genuinely, merely, precisely, deliberately, structurally, seam, -shaped, teeth,
  lever, buys; the cluster's 12-week trend is now slightly negative. "earns its keep" and "a dial worth turning" are
  Anthropic's own examples of mannered prose (see T5). Grade for essays: **C/U** (the genre differs).

### V10. Stock names and titles in generated examples
- **Pattern:** invented people named Emily, Sarah (Thompson/Carter); every expert titled "Dr."
- **Example:** "Dr. Sarah Thompson, a leading climate economist, notes that..."
- **Fix:** never invent people for a student's paper. Use a real cited source or remove the quote.
- **Evidence: A/M.** 63.3% of GPT-4o and 70% of Claude-3.5-Sonnet articles included Emily or Sarah; humanized o1-pro
  articles over-used titles (Russell et al.).

### V11. Fiction "slop" (relevant if the student writes narrative)
- **Pattern:** gaze, flicker(ed), palpable, unspoken, unease, tendrils, testament, "voice barely above a whisper",
  "a sense of", "the weight of", "hung in the air", "eyes never leaving", characters named Elara/Kael/Lyra.
- **Example:** "Her voice was barely above a whisper, the weight of unspoken words hanging in the air."
- **Fix:** one concrete, character-specific action or line of dialogue instead of an atmospheric formula.
- **Evidence: M.** "flickered" is in the top-120 overused words of 98.5% of 67 models; "voice barely whisper" in the top
  trigrams of 68.7% (Antislop). "unspoken" appeared in about 15% of LLM paragraphs; "weight of", "sense of", "mix of"
  rare in human seed paragraphs ([Chakrabarty, Laban, Wu, CHI 2025](https://arxiv.org/abs/2409.14509)). EQ-Bench lists:
  `downloads/eqbench_slop_list*.json` ([slop-score](https://github.com/sam-paech/slop-score)).

---

## 3. Phrases, openers, closers

### P1. Chatbot wrappers and flattery
- **Pattern:** "Great question!", "Certainly!", "Of course!", "You're absolutely right", "I hope this helps",
  "Let me know if you'd like...", "Here's a revised version:", "Would you like me to...".
- **Example:** "Great question! Here is an overview of the French Revolution... I hope this helps!"
- **Fix:** remove the wrapper, keep the content. In feedback on the student's own draft, give the honest assessment first.
- **Evidence: C** (WP:AISIGNS "Collaborative communication"); Graphite tracks "sycophantic phrases", "opens with flattery"
  and "closing calls to action" among its well-known tells, whose combined per-1,000-word frequency fell 41–86% from the
  earliest to the latest model in each family (M). Feedback sycophancy is **E**:
  five assistants gave more positive feedback when the user said "I wrote" or "I really like" the text
  ([Sharma et al., ICLR 2024](https://arxiv.org/abs/2310.13548)). For a student asking "is my essay good?", this matters.

### P2. Staged run-ups and self-signposting
- **Pattern:** "Let's dive in", "Let's break this down", "Here's the thing", "Here's what you need to know", "In this
  essay, I will explore...", "This section will discuss...", "Now, let's turn to...", standalone "Honestly?" or "Look,".
- **Example:** "In this essay, I will explore the multifaceted causes of greenwashing. Let's dive in."
- **Fix:** start with the first real claim: "Most greenwashing in our sample was not false; it was unmeasurable."
- **Evidence: M** for signposting as a class (Graphite "self-referential signposting"; EQ-Bench essay trigrams "essay
  explores multifaceted", "essay aims explore", "essay delve multifaceted"). Specific openers like "Here's the thing" and
  "Let's dive in": **C** (blader/humanizer; WP:AISIGNS example "In this section, we will discuss the background...").

### P3. Didactic and safety disclaimers
- **Pattern:** "It's important to note that", "It's worth noting", "It is crucial to remember", "...may vary",
  "at its core".
- **Example:** "It's important to note that results may vary depending on the company."
- **Fix:** if the variation matters, say which way and why: "Results differ by sector: oil companies had twice as many
  vague claims as retailers." Otherwise delete.
- **Evidence: C/M.** WP:AISIGNS lists didactic disclaimers as a historical (Nov 2022–2024) sign; Graphite counts
  "boilerplate phrases like 'it is important to note' and 'at its core'" among well-known tells (M, now declining).

### P4. Summary closers and section summaries
- **Pattern:** "In conclusion,", "In summary,", "Overall,", "Ultimately,", a final paragraph that restates the intro, a
  sentence at the end of each paragraph restating its topic sentence.
- **Example:** "In conclusion, greenwashing is a complex issue that requires a multifaceted approach."
- **Fix:** end on the last new idea, an implication, or an open question the essay earned. For school essays that require
  a conclusion, make it do new work (a consequence, a limit, a next step) instead of restating.
- **Evidence: A/M/C.** Experts flagged conclusions as "repetitive and overly optimistic summaries, while human-written
  conclusions end more abruptly and less tidily" (13.1% of explanations; Russell). Graphite counts formulaic closes (M);
  Gemini "ultimately this" 78x. WP:AISIGNS: section summaries are a historical sign of older models (C).

### P5. Upbeat, forward-looking send-offs
- **Pattern:** "The future looks bright", "As we look ahead", "Looking ahead, ...", "What comes next is...",
  "paving the way", "a step in the right direction", "exciting times lie ahead", "continues to evolve".
- **Example:** "Looking ahead, AI-powered ESG analysis promises to pave the way for a more transparent future."
- **Fix:** state concrete next steps or limits: "The next step is testing the classifier on reports it has not seen."
- **Evidence: M** for Claude: "what comes next" 24–28x, "looking ahead the" 33–40x human (Graphite, both studies).
  **C** for the pattern in general (WP:AISIGNS "Outline-like conclusions about challenges and future prospects").

### P6. Flagging importance instead of showing it
- **Pattern:** "This matters because", "Why this matters:", "This distinction matters", "matters most", "just as
  important", "plays a crucial/pivotal/vital role", "is key to".
- **Example:** "This distinction matters because it shapes how we understand corporate accountability."
- **Fix:** give the consequence directly: "Because the report never says what 'net zero' covers, investors cannot check it."
- **Evidence: M.** GPT-6 Astra: "distinction matters" appears in AI articles and never in the human ones; "matters because"
  357x. [a Claude model]: "this matters" 116x, "why _ matters" 92x (Graphite). EQ-Bench trigrams: "plays crucial role",
  "plays pivotal role", "play vital role" (M). WP:AISIGNS: "As of mid-2026, LLMs frequently include these alongside
  hedging disclaimers, editorializing about how a particular distinction or nuance is important" (C).

### P7. Sentence-initial additive transitions
- **Pattern:** Additionally, Furthermore, Moreover, Notably, Consequently, Importantly at the start of many sentences.
- **Example:** "Additionally, the model performed well. Furthermore, it was fast. Notably, it was cheap."
- **Fix:** connect ideas by logic, not by addition: "The model was accurate, fast and cheap, which is why we kept it."
- **Evidence: M but weak alone.** Kobak: "additionally" +3.7 pp of abstracts, "notably" ratio 2.63; Gemini "additionally the"
  8.6x, "furthermore the" 43x (Graphite). WP:AISIGNS lists "Transition words (in isolation)" under ineffective
  indicators: humans and style guides use them too. Act only when several appear close together.

### P8. Stock collocations and clichés
- **Pattern:** "in today's fast-paced world", "ever-evolving landscape", "rapidly evolving landscape", "increasingly
  interconnected world", "double-edged sword", "delicate balancing act", "serves as a stark reminder", "a testament to",
  "plays a crucial role in shaping", "far-reaching implications", "navigate the complexities", "one size fits all",
  "beyond the surface level".
- **Example:** "In today's rapidly evolving landscape, ESG reporting is a double-edged sword."
- **Fix:** delete the frame and keep the specific claim, or replace the cliché with a fresh literal statement.
- **Evidence: M** (EQ-Bench slop trigram list, derived from overuse vs human baseline on essay prompts;
  `downloads/eqbench_slop_list_trigrams.json`); **A** (clichés were 17% of professional writers' edits to LLM paragraphs;
  Chakrabarty et al.).

### P9. Source-availability hedges and "should be treated as" disclaimers
- **Pattern:** "While specific details are limited...", "based on available information", "not widely documented",
  "[claim] should be treated as X rather than Y", "does not by itself establish...".
- **Example:** "The report's figures should be treated as indicative rather than definitive."
- **Fix:** say exactly what is missing and what follows: "The report gives no baseline year, so the 30% cut cannot be checked."
- **Evidence: C/M.** WP:AISIGNS (2026): among the most common signs on Wikipedia now. GPT-6 Astra uses "does not establish"
  275x as often as [a Claude model] (Graphite update), so this is mainly a GPT-6 tell; Claude drafts are less prone.

---

## 4. Sentence and paragraph structure

### S1. Negative parallelism / corrective framing ("It's not X, it's Y")
- **Pattern:** "It's not X, it's Y"; "not just X, but Y"; "not only X but also Y"; "X rather than Y"; "less like X and more
  like Y"; "is more than a X; it's Y"; "This isn't about X. It's about Y."; "no longer X. It is Y."; "didn't V. It V-ed.";
  "No X. No Y. Just Z."; clipped tails ("..., no guessing").
- **Example:** "Greenwashing isn't just a marketing problem; it's a governance failure."
- **Fix:** keep a contrast only if X is something the reader actually believes or the text has raised; otherwise state Y:
  "Greenwashing is a governance failure: boards approve the claims." If X is live, say whose belief it is.
- **Evidence: M (strong) + E.**
  - WaPo: versions of "not just X, but Y" appeared in 6% of GPT-4o chats in July 2025.
  - Graphite: GPT-6 Astra corrective framing 12x human ("the _ is not simply" 576x, "rather than relying" 187x);
    [a Claude model] "less like a _ and more like" 105x, "rather than merely" 160x; [a Claude model] "is more than a _ it" 98x,
    "rather than simply" 32x; Gemini "is not just a _ it is" 153x.
  - Antislop: "It's not X, it's Y" 6.3x human in some models' fiction.
  - Peng et al. 2026 (Mandarin "not X, but Y"): models use it 2.5–9.2x human density; 52.8% of model uses were correct but
    unneeded (X was not a live alternative, or the point was already made) vs 33.3% for humans; reward models and LLM
    judges preferred the construction even when unlicensed. Their test: does the context make X a live alternative, and
    does rejecting X add information?
  - Experts named it repeatedly ("the comparison of 'it's not just this, it's this'"; Russell).
  - EQ-Bench slop score weights it 25% of the score and ships detector regexes (`downloads/eqbench_regexes-stage1.js.txt`).

### S2. Rule of three (forced triads)
- **Pattern:** adjective, adjective, adjective; three parallel phrases; three examples; three short sentences then a moral.
- **Example:** "The program fosters innovation, collaboration, and growth."
- **Fix:** keep the items that are distinct and true; often that is one or two. Vary list lengths across the piece.
- **Evidence: A/C, indirect M.** Experts cited "consistently listing three items" (Russell; one annotator relied on it
  heavily). WP:AISIGNS "Rule of three". Phrasal coordination 1.9x human in GPT-4o (Reinhart) is the closest measured
  correlate. I found no direct frequency count of triads (gap).

### S3. Superficial "-ing" tails (present participial clauses)
- **Pattern:** a sentence ends with ", highlighting / underscoring / reflecting / ensuring / contributing to / fostering /
  showcasing / symbolizing ..." that adds an unsupported interpretation.
- **Example:** "Unilever cut emissions by 4%, highlighting its commitment to a sustainable future."
- **Fix:** cut the tail or turn it into a supported claim: "Unilever cut emissions by 4%, short of its 10% target."
- **Evidence: M (strong).** Instruction-tuned models use present participial clauses 2–5x the human rate; GPT-4o 5.3x
  (Cohen's d 1.38), the most important feature in their classifier (Reinhart et al.). WP:AISIGNS "Superficial analyses".
  Kobak: highlighting/underscoring/showcasing among top excess words.

### S4. Inflated significance, legacy and "broader trends"
- **Pattern:** "marking a pivotal moment", "a testament to", "reflects a broader shift", "setting the stage for",
  "an enduring legacy", "deeply rooted", "shaping the future of", "indelible mark".
- **Example:** "The 2015 Paris Agreement marked a pivotal moment, setting the stage for a new era of accountability."
- **Fix:** keep the fact, drop the significance claim unless a source makes it: "The 2015 Paris Agreement set a 1.5–2 °C goal."
- **Evidence: C** (WP:AISIGNS "Undue emphasis on significance, legacy, and broader trends", many real examples) with **M**
  support for its vocabulary (pivotal, testament, enduring in Kobak/WP lists). Experts also flagged "a reflective, romantic
  tone that doesn't give details on why this topic matters" (A, Russell).

### S5. Tidy topic-sentence / summary symmetry and redundant exposition
- **Pattern:** every paragraph opens with a claim, gives evidence, and closes by restating the claim; a heading followed by a
  sentence that repeats it; sentences that explain what the example just showed ("This shows the importance of...").
- **Example:** "## Data quality\nData quality is important. ... This illustrates why data quality is so important."
- **Fix:** keep the topic sentence or the closer, rarely both; let the example carry the point; cut sentences the reader
  could infer ("show, don't tell").
- **Evidence: A.** "Unnecessary/redundant exposition" was 18% of 8,035 professional-writer edits to LLM paragraphs, and it
  stayed common even in paragraphs rated high quality (Chakrabarty et al.). Experts flagged over-explaining and "telling
  rather than showing" (clarity, 19.5%; Russell). Density (too many words for the content) was a significant predictor of a
  "slop" judgment ([Shaib et al., COLM 2026](https://arxiv.org/abs/2509.19163)).

### S6. One-line dramatic closers and fragment stacks
- **Pattern:** a short punchline paragraph after each section ("That's the real win."); "Let that sink in."; stacked
  fragments ("No baseline. No audit. No accountability.").
- **Example:** "The report had no baseline year. No audit. No accountability."
- **Fix:** merge into one sentence with the specific claim: "The report had no baseline year and no external audit, so its
  targets cannot be checked."
- **Evidence: C** (blader/humanizer §2; WP:AISIGNS "no ..., no ..., just ..." form). The "no longer X. It is Y" regex in
  EQ-Bench covers part of it (M for that sub-form). No frequency study of fragment stacks found (gap).

### S7. "Avoiding tradeoffs" phrasing
- **Pattern:** "without sacrificing", "without compromising", "without losing", "without requiring".
- **Example:** "The method improves accuracy without sacrificing speed."
- **Fix:** report the real tradeoff with numbers, or say it was not measured.
- **Evidence: M.** GPT-6 "without requiring" 70x; Gemini "without sacrificing" 7.8x; [a Claude model] "without losing" 6.1x (Graphite).

### S8. Arguing with no one (preemptive strawmen)
- **Pattern:** "Some might argue...", "To be clear,", "This isn't to say...", "Don't get me wrong", "You might think... but",
  "A tempting approach would be..." when no one raised the point.
- **Example:** "To be clear, this isn't to say that companies are lying."
- **Fix:** keep an objection only if a real source raises it; then name the source and answer it.
- **Evidence: C** (blader/humanizer §5). Related measured evidence: "unlicensed" corrections (X not raised in context) were
  24.1% of model uses vs 12.1% human (Peng et al.).

### S9. Uniform, templated sentence openings and syntax
- **Pattern:** consecutive sentences with the same subject or the same opener ("This...", "The..."), or the same clause shape
  repeated through a paragraph.
- **Example:** "This approach is efficient. This approach is scalable. This approach is transparent."
- **Fix:** merge, reorder, or start with the action; vary clause shape where the meaning allows.
- **Evidence: M (indirect)/A.** LLMs reuse part-of-speech templates more than humans; 15 of the 50 most common LLM templates
  were rare in human seed paragraphs (Shaib et al. 2024 as replicated in Chakrabarty et al.). "Poor sentence structure" was
  20% of expert edits. Syntax-only features were the best automatic predictor of "slop" (AUROC ~0.64–0.68; Shaib 2026).

### S10. Overlong, "and"-chained sentences (model-dependent)
- **Pattern:** long sentences joined by "and" or stacked clauses, with little internal punctuation.
- **Example:** "The company set targets and published reports and engaged stakeholders and the results were mixed."
- **Fix:** split at the logical joints; use a semicolon, colon or parentheses where they fit.
- **Evidence: M (2026).** The Economist (55,940 sentences, ChatGPT/Claude/Gemini/Grok vs Economist writers): LLMs "write
  longer sentences — 'and' is their most overused word" and use fewer commas and semicolons. Anthropic notes [a Claude model] prose
  can be denser with longer sentences and fewer paragraph breaks
  ([docs](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1)).
  Contrast: WP says GPT-6 writes short 8–20-word sentences (U). Direction depends on the model; the stable tell is
  uniformity (R1).

---

## 5. Rhythm

### R1. Uniform sentence length (low "burstiness")
- **Pattern:** most sentences fall in the same 15–25-word band; few very short or very long ones.
- **Example:** a paragraph of six sentences of 18–22 words each.
- **Fix:** vary length for meaning: a short sentence for the key claim, a longer one to carry a qualified explanation.
  Do not chop at random (see O3).
- **Evidence: M.** "Sentence lengths vary much less in AI writing than in human writing" (mean per-article SD; Graphite,
  9 models). Experts: "human-written sentences vary more in terms of length" (Russell). Burstiness was the third most
  important stylometric feature globally, but unstable across domains and models
  ([Shan, Lee, Hao 2026](https://arxiv.org/abs/2608.27855)).

### R2. Uniform paragraph length and overly even formatting
- **Pattern:** every paragraph 3–5 sentences, similar length; every section the same shape.
- **Fix:** let paragraph length follow content; one-sentence paragraphs only when they carry a new point.
- **Evidence: A** ("paragraphs of similar length" under formatting, 15.0%; Russell).

### R3. Too much lexical variety (elegant variation)
- **Pattern:** a key term is renamed every time ("the company... the firm... the organization... the corporate entity").
- **Example:** "Unilever's targets... the conglomerate's goals... the multinational's ambitions."
- **Fix:** repeat the precise term. In a research paper, one concept gets one name.
- **Evidence: M.** AI articles have higher within-article lexical diversity (MTLD) than human ones (Graphite); entropy and
  lexical diversity are the most stable stylometric markers of AI generation across 8 models and 5 domains (Shan et al.);
  human verb diversity 0.572 vs machine 0.766 (Creanga & Dinu). WP:AISIGNS "Lexical diversity/elegant variation" (C;
  notes non-native writers taught to avoid repetition do this too).

---

## 6. Punctuation and formatting

### F1. Em dashes (status changed in 2025–2026)
- **Pattern:** frequent em dashes, often spaced (" — "), used where a comma, colon or parentheses fits; dashes setting off
  punchy contrasts.
- **Example:** "The policy — announced without warning — affected thousands."
- **Fix:** use the punctuation that states the relation (comma for an aside, colon for an explanation, parentheses for a
  digression). Do not rewrite to zero mechanically (see O5).
- **Evidence: M, time-dependent.**
  - Rise: fewer than 1 in 10 GPT-4o responses had an em dash in mid-2024; more than half by summer 2025 (WaPo).
  - Fall: OpenAI tuned GPT-5.1 to follow dash instructions (Ars Technica, cited by WP). Economist (Jul 30 2026): "Today only
    Claude uses more em-dashes than human writers, with ChatGPT using markedly fewer than any other writer in our study."
    Graphite (Sep–Oct 2026): GPT-6 Astra about 1/8 of the human rate; Gemini 3.1 nearly zero; [a Claude model] about human rate;
    [a Claude model] 0.015 per 1,000 words (99% below [a Claude model]).
  - WP:AISIGNS now files em-dash overuse under "Historical indicators (2022–September 2026)" and warns that dash-free models
    lean on commas and periods so much that this "has become its own sign" ([citation needed] on WP; treat as C).
  - Bottom line for an [a Claude model] skill: dash overuse is not the current risk. A rare, correct dash is fine and human
    (journalists and pre-ChatGPT writers used them).

### F2. Punctuation monotony (few commas, semicolons, parentheses, exclamation marks)
- **Pattern:** text built almost only from periods and commas, or long sentences with almost no internal punctuation;
  no parenthetical asides; no exclamation marks in informal writing.
- **Fix:** where the genre allows, use parentheses for real asides, a semicolon between closely linked clauses, a colon
  before an explanation. In a personal essay, an occasional exclamation or aside is fine.
- **Evidence: M.** Economist: LLMs "use fewer commas and semicolons than humans (and hardly any parentheses)". Graphite:
  human writers use exclamation marks "more than a hundred times as often" as current models and parenthetical asides
  "far more often". Russell: human text shows "dashes, brackets, quotes intermixed"; AI text avoids dashes and ellipses (A).

### F3. Bold run-ins and inline-header lists
- **Pattern:** bullets of the form "**Label:** sentence that repeats the label"; bold scattered for emphasis on every key term.
- **Example:** "- **Transparency:** Transparency is improved through clear reporting."
- **Fix:** turn into a sentence or paragraph when the labels add nothing; use bold rarely (a defined term once, a warning).
- **Evidence: C/A.** WP:AISIGNS "Inline-header vertical lists" and "Overuse of boldface"; experts flag "bolded lists"
  (formatting 15.0%, Russell). Anthropic: "Earlier models overused bullets and bold in chat" ([a Claude model] doc). Graphite
  counts two list-use measures among well-known tells (M, declining).

### F4. Bullet-itis (lists where an argument is needed)
- **Pattern:** an essay or report section delivered as bullets; reasoning chopped into fragments; nested bullets.
- **Fix:** write paragraphs that connect causes and consequences; keep lists for genuinely parallel items (steps, criteria).
- **Evidence: C/M** (WP:AISIGNS; Graphite list measures). Reward models are biased toward list formatting
  (Zhang et al. 2025, cited in Peng et al. 2026; not read directly: U).

### F5. Title Case headings and too many headings
- **Pattern:** "Impact Of Technology And Digitalization"; a heading every 100 words; a "Conclusion" heading in a 500-word
  piece; horizontal rules between sections; a top heading that repeats the title.
- **Fix:** sentence case ("Impact of technology") unless a style guide demands otherwise; headings only where a reader
  navigates.
- **Evidence: C** (WP:AISIGNS "Title case", thematic breaks, heading errors) and **A** ("fully capitalized headings",
  Russell).

### F6. Emoji as formatting
- **Pattern:** emoji in front of headings or bullets (✅, 🚀, 💡, 🧠).
- **Fix:** remove in any school or formal writing.
- **Evidence: M** for chat: by July 2025, 70% of GPT-4o messages had at least one emoji; ✅ used 11x more than by humans (WaPo).
  **C** for documents (WP:AISIGNS: "more rare now").

### F7. Curly quotes and Markdown residue
- **Pattern:** curly quotes where the target format uses straight ones, stray `**`, `##`, or "---" in pasted text.
- **Fix:** match the destination format. **Weak alone** (most editors auto-curl quotes; WP and blader both say so).
- **Evidence: C.**

---

## 7. Tone

### T1. Sycophancy and praise in feedback
- **Pattern:** "What a powerful essay!", "You've done an excellent job", agreeing with the user's framing, softening real
  problems.
- **Fix:** lead with the most important problem and a concrete fix; praise only specific things that work.
- **Evidence: E** (Sharma et al.: assistants' feedback became more positive when the user said they wrote or liked the text;
  preference models sometimes preferred sycophantic answers). Graphite counts sycophantic phrases (M).

### T2. Hedge stacking and formal epistemic hedges
- **Pattern:** "could potentially", "may arguably", "it is possible that... may", "not necessarily", "to some extent",
  "in some cases" stacked on one claim; caveats on every sentence.
- **Example:** "This could potentially suggest that the policy may have some effect."
- **Fix:** one hedge where real uncertainty exists, placed on the uncertain part: "The policy probably reduced claims, but
  our sample is small (n = 6 reports)."
- **Evidence: M/C.** GPT-6 Astra uses "may" 3x GPT-4.1; Astra vs [a Claude model]: "may provide" 18x, "not necessarily" 17x
  (Graphite). WP and blader: stacked qualifiers (C). **Caveat:** casual qualifiers ("pretty", "sort of") are human tells
  (Graphite), and WP lists "very", "perhaps", "tends to" among signs of human writing (citing Reinhart). Do not strip all hedges.

### T3. False balance and the "challenges" formula
- **Pattern:** "While X offers many benefits, it also presents challenges"; "Despite these challenges, X continues to
  thrive"; every argument gets an equal-weight counterpoint; conclusion splits the difference.
- **Example:** "While ESG ratings have limitations, they also offer valuable insights."
- **Fix:** take the position the evidence supports and say how strong it is: "ESG ratings disagree with each other too
  much to rank companies; use them only to flag outliers."
- **Evidence: C** (WP:AISIGNS "Outline-like conclusions about challenges and future prospects"; EQ-Bench trigram "however
  crucial acknowledge"); **A** (experts: tone "consistently neutral or positive", "trying to remain impartial or
  impartial-seeming"; Russell). No frequency study of false balance found (gap).

### T4. Puffery and positivity bias
- **Pattern:** everything is vibrant, rich, stunning, essential, inspiring; problems become "opportunities"; dark parts are
  skipped ("embarking on a new chapter").
- **Fix:** neutral description; let negative facts stay negative.
- **Evidence: C/A.** WP:AISIGNS promotional language (newer models "more subtly positive"). Experts: AI "avoid[s] darker or
  more mature topics" (topics 3.1%) and has "an inherent positivity bias" (Russell).

### T5. Mannered prose (metaphor and flourish instead of statement)
- **Pattern:** figurative phrases that perform cleverness: "a dial worth turning", "this point earns its keep", "load-bearing
  assumption", "the quiet work of", "a mirror, not a window", "the language of trust", "the currency of".
- **Example:** "Trust is the currency of sustainability reporting, and vague claims quietly debase it."
- **Fix:** "say what you mean. When a literal phrase is available, use it" (Anthropic): "Investors stop trusting reports
  that make claims they cannot check."
- **Evidence: M (model-judged index) + vendor guidance.** Anthropic defines mannered prose and recommends the instruction
  "Please remove all mannered prose." Graphite scored it with [a Claude model]: human mean 6.65; [a Claude model] 16.75 (about 2.5x);
  [a Claude model] 10.57 (about 1.6x); GPT-6 Astra about 1.2x. blader §3 "Sayings that sound deep" (C).

### T6. Vague attributions
- **Pattern:** "Experts argue", "Studies show", "Critics note", "Observers have cited", "Industry reports suggest",
  "several sources" (when one is cited).
- **Fix:** cite the actual source and what it said, or cut the claim. Never invent a source to fix this.
- **Evidence: C** (WP:AISIGNS "Vague attributions"). **M:** LLM-modified peer reviews were less likely to contain scholarly
  citations (ICLR 2024: 12.8% of sentences estimated LLM-modified in reviews without references vs 6.5% with; Liang et al.).
  The Economist: LLM prose has less punctuation partly because it does "not quote experts".

### T7. Customer-service / clerk register
- **Pattern:** "I have carefully reviewed...", "I apologize for any inconvenience", "Please feel free to...",
  "I understand your concern".
- **Fix:** plain direct statements.
- **Evidence: C** (WP:AISIGNS comment-specific indicators).

### T8. Register mismatch (one polished register for every genre)
- **Pattern:** the same formal, noun-heavy, contraction-light voice in a personal essay, a lab report and a text to a friend.
- **Fix:** match the genre: contractions and first person in a personal essay; plain, precise third person in a methods section.
- **Evidence: M.** Instruction-tuned models keep their dense style "even when prompted to match the style of informal speech
  and writing"; words normal in fiction are "highly conspicuous" in other genres (Reinhart et al.). Experts: AI text "rarely
  contains filler words, contractions, slang" (formality 12.3%, Russell). Note the model split: ChatGPT raised contractions
  sharply in 2025 (WaPo), while Gemini nearly dropped them (Graphite), so "no contractions" is model-specific.

---

## 8. Content

### C1. Generic, interchangeable examples and metaphors
- **Pattern:** the example any writer on any topic could use; the same metaphor every time (orchestra, tapestry, journey,
  bridge, mosaic, symphony, compass).
- **Example:** "Like an orchestra, a team needs every instrument to play in harmony."
- **Fix:** use an example only this writer has (their club, their data, their mistake). If none is available, ask the student
  instead of inventing one.
- **Evidence: C/A + M for homogeneity.** A tutoring firm's tests (65+ hours, 4 chatbots): GPT-4 used an orchestra metaphor in
  8 of 16 extended-metaphor requests; two chatbots listed "the exact same animals in the exact same order"
  ([IEEE Spectrum 2023](https://spectrum.ieee.org/chatgpt-college-essays); consultant study, grade C). LLM admissions essays
  were far more similar to each other (cosine 0.952–0.957) than human essays were to each other (0.882–0.889) (Lee et al., M).
  LLM-modified peer reviews were more homogeneous (Liang et al., M).

### C2. Lack of specifics (no names, numbers, dates, places, sensory detail)
- **Pattern:** abstractions and categories instead of instances; "various stakeholders", "many companies", "recent years".
- **Example:** "Many companies have made significant progress in recent years."
- **Fix:** add the specific the writer actually has: "Unilever and Dr Pepper both published 2023 reports; only Unilever gave
  a baseline year." If the specific is unknown, leave a bracketed question for the student rather than inventing it.
- **Evidence: A/M.** "Lack of specificity and detail" was one of 7 categories in professional edits of LLM text, and LLM
  editors were "mostly ineffective" at fixing it (Chakrabarty et al.). Human essays carry temporal and interpersonal words
  (year, still, time, friend; Lee et al., M). Human web articles show anecdotes ("he said", "years ago") and personal
  experience ("my favorite", "mom", "last year") (Graphite, M). WP's core mechanism (C).

### C3. No stakes, no surprise, no humor
- **Pattern:** safe, balanced, frictionless prose; nothing at risk; no admission of being wrong; no joke.
- **Fix:** state what was at stake and what could have gone wrong; keep the writer's real doubts and odd details.
- **Evidence: A.** Originality was cited in 23.7% of expert explanations: AI writing is "straightforward, 'safe,' and lacking
  in surprises or humor" (Russell). Human-writing cues included "creative phrasing" like "catnip for a certain type of Reddit
  user" and unusual concrete words ("chunky", "musky", "blitzing").

### C4. Prompt echo
- **Pattern:** the essay repeats the assignment's key words and structure back ("This challenge... taught me resilience...").
- **Fix:** answer the question with your own material; you need not use the prompt's vocabulary.
- **Evidence: M** (Lee et al.: LLM essays "favor keywords from the essay question").

### C5. Over-explaining and low information density
- **Pattern:** defining the obvious, background the reader already has, two sentences for one idea.
- **Fix:** cut until each sentence adds a fact, a reason, or a step the reader lacks.
- **Evidence: A.** Density and relevance were the strongest predictors of a "slop" label (Shaib et al.); verbosity was the
  annotators' common core. Redundant exposition 18% of expert edits (Chakrabarty).

### C6. Formulaic quotes
- **Pattern:** quoted speakers who sound like the narrator; a tidy quote at the end of each paragraph.
- **Fix:** in essays, quote real people briefly and only for what only they could say; never fabricate a quote.
- **Evidence: A** (quotes 22.3% of expert explanations; "every expert speaks the same way"; Russell).

### C7. Fabricated or unverifiable specifics (a risk created by fixing C2)
- **Pattern:** invented statistics, studies, people, quotes, page numbers, anecdotes.
- **Fix:** hard rule: never add a fact, name, number, date, quote, citation or anecdote that is not in the source or given by
  the user. Ask, or mark a gap.
- **Evidence: C/M.** WP:AISIGNS documents hallucinated citations and "likely..." guesses after source-availability hedges;
  experts flagged factual errors (7.2%, Russell). The humanizer skill adds a no-fabrication rule for this reason (blader).

---

## 9. Personal-essay tells (college, scholarship, reflective essays)

### PE1. "This experience taught me..." lesson statements
- **Pattern:** the essay states its moral: "This experience taught me the value of hard work, perseverance, and adaptability."
- **Example (real, GPT-4o):** "As the son of immigrants, I have learned the value of hard work, perseverance, and
  adaptability. My parents' journey has instilled in me a deep appreciation for the opportunities I have..." (quoted in Lee et al.)
- **Fix:** show the changed behavior instead of naming the virtue: what you do differently now, in one concrete scene.
- **Evidence: M for the vocabulary (Lee et al.); A for the shape** (overly optimistic, summarizing conclusions; Russell);
  the specific phrase "taught me" has no frequency study I could find (**U** as a phrase-level tell; strong as editing
  advice). blader §2 names "It was a lesson in patience." as a closer that labels what the example showed (C).

### PE2. Tidy epiphany / neat transformation arc
- **Pattern:** problem → struggle → sudden insight → better person, resolved by the last paragraph; no lingering doubt.
- **Fix:** keep unresolved parts; end on a specific image or an honest open question rather than a verdict on yourself.
- **Evidence: A** (human conclusions "end more abruptly and less tidily"; Russell); **C** (blader: keep "mixed feelings and
  unresolved tension"). No direct measurement (gap).

### PE3. Résumé-in-prose
- **Pattern:** a paragraph listing roles, awards and traits ("As captain, president, and founder, I developed leadership...").
- **Fix:** pick one activity and one moment inside it; let the reader infer the traits.
- **Evidence: M (indirect)/C.** LLM essays favor high-level concept words over personal and temporal detail (Lee et al.).
  The Wikipedia analogs are "Canned emphasis on notability" and "Awards and recognition" sections (C). No phrase study (gap).

### PE4. Identity inserted as labels
- **Pattern:** demographic facts stated in the first sentence as credentials: "Growing up in Lexington, South Carolina, with my
  Asian heritage, I often felt like a bridge between two cultures."
- **Fix:** if identity matters to the story, show it through a specific scene; avoid the "bridge between two cultures" stock image.
- **Evidence: M/A** (Lee et al.: identity prompting made models insert demographic words "verbatim", "rigid and formulaic";
  example above is their GPT-4o quote; LLMs also added "first generation", "immigrant", "multicultural" unprompted).

### PE5. Stock metaphors for the self
- **Pattern:** life as a journey, tapestry, puzzle, symphony, mosaic, bridge; "a spark ignited".
- **Fix:** one literal sentence about what happened.
- **Evidence: C** (orchestra 8/16, IEEE Spectrum; "tapestry" 155x human in GPT-4o, M). A search summary says an essay
  editor quoted by [SlashGear](https://www.slashgear.com/1518783/risky-words-school-admissions-ai-essay) treats "tapestry" as a
  near-certain sign (page not read: U).

### PE6. Sentimental narration around quotes and scenes
- **Pattern:** "He shrugged as if that were the most ordinary idea, then laughed."; "a smile playing on her lips".
- **Fix:** keep the line of dialogue, drop the stage directions unless they add information.
- **Evidence: A** (Russell Fig. 1: an expert flagged exactly this narration as "sentimental and corny"); fiction slop lists (M).

### PE7. Safe, upbeat resolution of real hardship
- **Pattern:** illness, loss or failure resolved into gratitude and growth within a paragraph.
- **Fix:** let hard facts stay hard; the reader trusts an essay that admits what did not get better.
- **Evidence: A** (Russell topics/tone: AI "focuses on future research, hopeful quotes, and potential cures").

Context for students: in one 2023–2025 graduate program, applicants whose essays a detector flagged as primarily AI-written
were admitted less often (−1.5 percentage points per flagged essay after controls), and officers rated essays they suspected
were AI lower (Isley et al. 2026). Admissions officers' ability to spot AI was imperfect (AUC 0.70).

---

## 10. Research-paper / report tells (for the GreenBERT report)

### RP1. Academic excess vocabulary
- Highest-yield search list for a methods/results section (from Kobak's measured ranking and common-word set): delve, underscore,
  showcase, intricate, meticulous, realm, pivotal, crucial, comprehensive, notably, additionally, insights, enhance(ing),
  potential, garner, surpass, groundbreaking, novel, robust (non-statistical use), leverage, utilize, facilitate,
  "shed light on", "pave the way". Evidence **M** (section V1).

### RP2. "significant" without statistics
- **Pattern:** "significant improvement" with no test.
- **Fix:** in a paper, reserve "significant" for statistical significance; otherwise give the number ("accuracy rose from 67%
  to 73%").
- **Evidence: M.** GPT-3.5 revision doubled "significant" in CS abstracts (+99%; Geng & Trotta); Kobak: "significant" +4.6 pp.

### RP3. "This study delves into..." openers and self-description
- **Pattern:** "This paper explores...", "In this section, we will discuss...", "This report aims to provide a comprehensive overview".
- **Fix:** open with the problem or result.
- **Evidence: E/M/C.** Participants dispreferred abstracts that began "This study delves into..." (Juzek & Ward 2024);
  signposting is a tracked tell (Graphite); WP example "In this section, we will discuss the background information..."

### RP4. Missing or vague citations; inflated claims of novelty
- **Pattern:** "Studies have shown", "a growing body of research", "the first-ever", "a novel framework" with no comparison.
- **Fix:** cite the specific study (the project's Related Work already exists in the user's Drive; use it), state novelty
  relative to named prior work.
- **Evidence: M** (LLM-modified reviews less likely to cite; Liang et al.); **C** (WP vague attributions; EQ-Bench "growing body
  research").

### RP5. Dense noun-heavy prose in methods
- See V7. In methods, prefer "we removed duplicate sentences" over "duplicate removal was performed".
  (Note: Reinhart found GPT-4o uses agentless passives at about half the human rate, so passive voice itself is not the AI tell;
  noun density is.)

---

## 11. Over-correction risks (what humanizers get wrong)

### O1. Inserting typos and grammar errors
- **What it is:** deliberately adding misspellings or errors to look human.
- **Why it is wrong:** perfect grammar is listed by Wikipedia as an *ineffective* indicator (many human writers are skilled);
  errors lower the quality and credibility the student needs; admissions data show AI-assisted essays scored higher on
  mechanics, yet the admissions penalty persisted after adjusting for essay quality, and staff rated essays they perceived as
  AI lower (Isley et al.), so correctness was not what gave them away. Pre-LLM "text spinners" produced
  "word salad" that itself became a marker of misuse (Roe et al. 2026, citing Prentice & Kinden 2018:
  [arXiv 2605.02649](https://arxiv.org/abs/2605.02649)).
- **Rule:** never add errors. Keep the writer's own non-standard choices only if they are intentional voice.

### O2. Thesaurus swaps and synonym cycling
- **What it is:** replacing flagged words with rarer synonyms, renaming terms to "vary" them.
- **Why it is wrong:** AI text is already more lexically diverse than human text (Graphite MTLD; Shan et al.). Asking Mistral to
  make text "sound more human" raised verb diversity from 0.766 to 0.924, further from the human 0.572, and the text stayed
  detectable (95%) (Creanga & Dinu 2026). A banned word is often replaced by another overused word (Antislop; WP: synonyms of AI
  words are not tells, but substitutes like "nuanced" drew a backlash in Juzek & Ward 2025). Hard bans at scale degrade text
  into repetition and incoherence (Antislop).
- **Rule:** rewrite the sentence around its claim; repeat the right word; prefer the plainest accurate word.

### O3. Choppy fragments and forced short sentences
- **What it is:** cutting every long sentence into fragments for "burstiness".
- **Why it is wrong:** fragment stacks are themselves a tell (S6); a tutoring study saw chatbots swing between "short, declarative
  sentences that did a lot of telling" and flowery language when asked to vary style (IEEE Spectrum). The measured human signal is
  *variation* tied to meaning (R1), not shortness. WP reports a 2026 model family writing within a strict 8–20-word band as a new
  sign (U).
- **Rule:** vary length only where the meaning changes pace (a short sentence for the key finding).

### O4. Forced slang, casualness and contractions
- **What it is:** adding "tbh", "kinda", jokes or contractions to sound human.
- **Why it is wrong:** register mismatch is itself a tell (Reinhart: models do not match genre). Mixed casual/formal register is an
  *ineffective* indicator (WP), so adding it does not make text human, and in a research report it reads as unprofessional.
  Experts were not fooled by an o1-pro humanizer that used contractions and colloquialisms; one annotator who leaned on informality
  was (Russell).
- **Rule:** match the genre the student is writing in; use the student's own voice samples when available.

### O5. Purging all em dashes (and other punctuation) mechanically
- **What it is:** a blanket "no em dashes" rule applied to every text.
- **Why it is a risk:** current Claude ([a Claude model]) already uses almost none; dash-free models fall back on commas and periods, which
  WP now calls its own sign (C); humans use more parentheses, semicolons and exclamation marks than models (Economist, Graphite).
- **Rule:** use dashes sparingly and correctly; keep punctuation variety; if the student's own drafts use dashes, keep their rate
  (the blader skill also lets a writing sample override its dash rule).

### O6. Whack-a-mole word lists
- **What it is:** a skill that only scans a fixed banned-word list.
- **Why it is wrong:** lists go stale (Graphite: 55–72% of tells change per version; delve faded), instructions to avoid words can
  backfire (Antislop), and Wikipedia explicitly warns "Please do not merely treat these signs as the problems to be fixed; that
  could just make detection harder. The actual problems are those deeper concerns."
- **Rule:** fix the underlying problem (vague claim, missing evidence, padding); use lists as a final check.

### O7. Meaning drift and invented detail
- **What it is:** rewriting so freely that claims change, or "adding specificity" by inventing anecdotes, numbers or quotes.
- **Why it is wrong:** Mistral "humanizing" preserved only 13.1% of event sequences (Creanga & Dinu); 30% of even professional
  edits changed meaning (Chakrabarty), which is acceptable for a co-writer only with the author's consent; invented facts in a
  student's report or personal essay are dishonest.
- **Rule:** keep every supported claim; add nothing factual the user did not provide; ask when a specific is needed.

### O8. Erasing the student's voice
- **What it is:** heavy rewriting of a human draft to "improve" it.
- **Why it is wrong:** heavy AI rewriting cut authorship-attribution accuracy by 66.5 points on blogs and 52.5 on email;
  "preserve the author's voice" prompts recovered little ([Malik & Awan 2026](https://arxiv.org/abs/2608.00926)). Light AI
  editing leaves text stylometrically close to the human original, while full generation has a distinct footprint (Shan et al.).
- **Rule:** when the student wrote the draft, make the smallest edits that fix real problems; keep their word choices, odd details
  and asides (blader's "keep" list: unusual specific details, mixed feelings, era-bound references, explainable first-person
  choices, genuine asides).

### O9. Chasing detectors
- **What it is:** editing to lower a detector score.
- **Why it is wrong:** detectors misfire on formal and non-native writing (Liang 2023: 61.22% FPR on TOEFL essays; simplifying
  native essays' word choice raised FPR from 5.19% to 56.65%; one "elevate with literary language" prompt cut detection from 100%
  to 13%). A RoBERTa detector flagged 76.3% of formal human abstracts (Creanga & Dinu). Character tricks (homoglyphs) evade some
  detectors but corrupt the text (Creanga & Dinu). [a Claude model] text carries a watermark designed to survive some editing
  (Anthropic support page).
- **Rule:** optimize for a human reader; never use Unicode tricks; respect the school's AI-disclosure rules.

### O10. Over-hedging to sound humble, or stripping all hedges
- **Why it is a risk:** hedge stacks are a tell (T2), but casual qualifiers are a *human* signal (Graphite) and scientific claims
  need calibrated uncertainty.
- **Rule:** one hedge per uncertain claim, attached to the uncertain part.

---

## 12. Positive targets: signs of human writing worth keeping or producing (without inventing anything)

| Feature | Evidence |
|---|---|
| Concrete specifics: names, dates, numbers, places, objects | Lee et al. (M); Graphite human tells (M); Chakrabarty (A) |
| Small anecdotes and personal experience in personal genres ("years ago", "my favorite") | Graphite (M) |
| First person and direct address where the genre allows | Graphite (M) |
| Plain verbs and copulas: is, has, used, wrote, tried | WP "Signs of human writing" (C); Geng & Trotta (M) |
| Definitive statements when true: "was the first", "is the only" | WP (C) |
| Casual qualifiers in informal writing: "pretty", "sort of"; and "very", "perhaps", "tends to" | Graphite (M); WP citing Reinhart (C) |
| Parenthetical asides, varied punctuation, an occasional exclamation in informal writing | Graphite, Economist (M); Russell (A) |
| Repeating the key term instead of cycling synonyms | Graphite, Shan, Creanga (M) |
| Sentence length that varies with meaning | Graphite (M); Russell (A) |
| Unusual, precise word choice ("chunky", "blitzing"), fresh analogies | Russell (A) |
| Short, real quotes fitted into sentences | Russell (A) |
| Endings that stop on a specific point rather than a summary | Russell (A) |
| Honest uncertainty, mixed feelings, darker facts left unresolved | Russell (A); blader (C) |
| Isolated wordy constructions humans use ("in order to", "the fact that") | WP (C); do not add these on purpose |

---

## 13. When not to act (false-positive guard)

- Text written before 2022-11-30, quotations, titles, proper names, and passages that discuss a word rather than use it (WP; blader).
- Technical senses: "robust" (statistics), "significant" (p-values), "landscape" (geography/ecology), "underscore" (character),
  "key" (cryptography/music), "load-bearing" (engineering).
- A single sighting of a weak tell: transitions, curly quotes, one em dash, passive voice, perfect grammar, formal register,
  mixed registers (WP "Ineffective indicators"; Russell false positives).
- Genre conventions: a research paper needs headings, a conclusion section and some formal vocabulary; a list of steps should be
  a list. The tell is decoration or formula without function.
- Non-native writers often avoid repetition and use formal words; do not "correct" a student's style toward a template (WP; Liang 2023).
- Act when several tells cluster in one passage, or when one strong structural tell recurs (S1, S3, P4, P6).

---

## 14. Suggested priority order for the skill (derived from the evidence above)

1. **Content first:** specifics (C2), stakes (C3), cut padding (C5, S5), no fabrication (C7). These drive expert and admissions-officer
   judgments and survive surface edits (Russell; Isley; Chakrabarty).
2. **Structural tells:** S1 corrective framing (license test), S3 "-ing" tails, S4 significance inflation, P4–P6 closers and
   importance flags, S2 triads, S8 strawmen.
3. **Tone:** T5 mannered prose (explicit Anthropic instruction), T1 sycophancy in feedback, T3 false balance, T2 hedge stacks.
4. **Rhythm and punctuation:** R1 variation tied to meaning, R3 repeat key terms, F2 punctuation variety; F1 dashes only if a draft
   actually overuses them.
5. **Vocabulary pass last:** current-model list (V2 for [a Claude model]) plus the classic list (V1), applied with the false-positive guard.
6. **Formatting:** F3–F6 for essays and reports (prose over bullets, sentence-case headings, no emoji).

---

## 15. Open questions and unverified items

- Rule-of-three, fragment stacks, false balance, "tidy epiphany" and "this experience taught me" have no direct frequency study
  that I found; they rest on expert annotation (Russell), field guides (WP) and community skills (blader).
- The Economist study (Jul 30 2026) was read only through a verbatim excerpt; per-model numbers beyond the quoted sentences are UNVERIFIED.
- Sam Kriss (NYT, Dec 2025): secondary summaries mention clunky metaphors, em dashes, "delve", rule of threes, and machine fiction full of
  shadows, whispers and quiet ([Longreads](https://longreads.com/2025/12/04/why-does-a-i-write-like-that)); the full text was not read (U).
- WP's GPT-6 list and "8–20 word" sentence band come from one review blog (intellectualead.com) (U).
- Graphite results come from one fixed web-article prompt; ratios for school essays and research reports may differ.
- The load-bearing study measures GitHub pull requests, not essays; its relevance to student prose is plausible but untested.
- Reward-model list-formatting bias (Zhang et al. 2025) is cited second-hand via Peng et al. 2026.
- I did not find a 2025–2026 study that measures personal-essay tells for current Claude models specifically.

## 16. Sources (all accessed 2026-10-20)

- Wikipedia: Signs of AI writing (WikiProject AI Cleanup), https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
- Kobak, González-Márquez, Horvát, Lause (2025). Science Advances 11(27). https://www.science.org/doi/10.1126/sciadv.adt3813 ; https://arxiv.org/abs/2406.07016 ; data https://github.com/berenslab/llm-excess-vocab
- Liang et al. (2024). Monitoring AI-Modified Content at Scale (ICML). https://arxiv.org/abs/2403.07183
- Liang et al. (2024). Mapping the Increasing Use of LLMs in Scientific Papers. https://arxiv.org/abs/2404.01268
- Liang, Yuksekgonul, Mao, Wu, Zou (2023). GPT detectors are biased against non-native English writers (Patterns). https://arxiv.org/abs/2304.02819
- Juzek & Ward (2025). Why Does ChatGPT "Delve" So Much? (COLING). https://arxiv.org/abs/2412.11385
- Juzek & Ward (2025). Word Overuse and Alignment in LLMs: The Influence of Learning from Human Feedback. https://arxiv.org/abs/2508.01930
- Geng & Trotta (2024). Is ChatGPT Transforming Academics' Writing Style? https://arxiv.org/abs/2404.08627
- Reinhart et al. (2025). Do LLMs write like humans? (PNAS). https://arxiv.org/abs/2410.16107 ; https://www.pnas.org/doi/10.1073/pnas.2422455122
- Russell, Karpinska, Iyyer (2025). People who frequently use ChatGPT for writing tasks are accurate and robust detectors (ACL). https://arxiv.org/abs/2501.15654
- Chakrabarty, Laban, Wu (2025). Can AI writing be salvaged? (CHI). https://arxiv.org/abs/2409.14509
- Shaib, Chakrabarty, Garcia-Olano, Wallace (2026). Measuring AI "Slop" in Text (COLM). https://arxiv.org/abs/2509.19163
- Paech, Roush, Goldfeder, Shwartz-Ziv (2025). Antislop. https://arxiv.org/abs/2510.15061 ; https://github.com/sam-paech/auto-antislop
- Paech. slop-score (EQ-Bench). https://github.com/sam-paech/slop-score ; https://eqbench.com/slop-score.html
- Peng, Jing, Liu, Meng, Liu (2026). Not X, but When. https://arxiv.org/abs/2610.22249
- Graphite: Druck, Paredes, Smith (2026-09-16). AI Tells. https://graphite.io/five-percent/research/ai-tells
- Graphite (2026-10-01). AI Tells: [a Claude model] Update. https://graphite.io/five-percent/research/ai-tells-opus-5-5-update
- Merrill, Chen, Kumer (2025-11-13). What are the clues that ChatGPT wrote something? Washington Post. https://www.washingtonpost.com/technology/interactive/2025/how-detect-chatgpt-em-dash/ (text read via Boston Globe reprint https://www.bostonglobe.com/2025/11/13/business/chatgpt-writing-style-clues/)
- The Economist (2026-07-30). How to spot AI writing. https://www.economist.com/culture/2026/07/30/how-to-spot-ai-writing (excerpt via https://daringfireball.net/linked/2026/08/11/)
- Anthropic. Prompting [a Claude model] (writing density / mannered prose). https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1
- Anthropic. Prompting [a Claude model]. https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5
- Anthropic support. How Claude marks AI-generated content. https://support.claude.com/en/articles/16266773-how-claude-marks-ai-generated-content
- Abraham (2026). The load-bearing vocabulary of Claude. https://github.com/louisabraham/load-bearing ; https://louisabraham.github.io/load-bearing/ ; coverage https://gigazine.net/gsc_news/en/20260831-load-bearing-ai-vocabulary-github/
- Lee, Alvero, Joachims, Kizilcec (2025). Poor Alignment and Steerability of LLMs: Evidence from College Admission Essays. https://arxiv.org/abs/2503.20062
- Isley, Gaebler, Goel (2026). AI-written admissions essays are widespread but penalized. https://arxiv.org/abs/2609.22549
- Shan, Lee, Hao (2026). AI Writers Have a Consistent Stylometric Footprint, but AI Editors Do Not. https://arxiv.org/abs/2608.27855
- Malik & Awan (2026). The Assistant Erased You. https://arxiv.org/abs/2608.00926
- Creanga & Dinu (2026). The Paradox of "Humanizing" LLM-Generated Text. https://arxiv.org/abs/2610.03110
- Roe, Perkins, Bannister, Furze, Wood (2026). Dramaturgies of Deception: AI Humanizers. https://arxiv.org/abs/2605.02649
- Sharma et al. (2024). Towards Understanding Sycophancy in Language Models (ICLR). https://arxiv.org/abs/2310.13548
- Jones (2023). College Admissions: Should AI Apply? IEEE Spectrum. https://spectrum.ieee.org/chatgpt-college-essays
- blader/humanizer SKILL.md v3.1.0 (community skill based on WP:AISIGNS). https://github.com/blader/humanizer
- SlashGear: The Risky Words That Might Make School Admissions Suspect AI. https://www.slashgear.com/1518783/risky-words-school-admissions-ai-essay

## 17. Files in this folder

- `catalog.md` (this file)
- `notes_sources.md` (longer extracts per source)
- `kobak_style_words_2024_ranked.tsv` (my recomputation of Kobak excess ratios for the authors' "style" words; columns: word, POS, p2024, expected, ratio r, gap delta)
- `scripts/kobak_rank.py` (the recomputation script; reads data files only)
- `downloads/` (untrusted data: Wikipedia text, EQ-Bench lists and regexes, Kobak CSVs, load-bearing README and fit data, blader SKILL.md)

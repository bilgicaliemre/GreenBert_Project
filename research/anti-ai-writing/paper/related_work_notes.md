# Related-work notes for references.bib (50 entries, verified 2026-10-20)

How to read this file:
- **Key** is the BibTeX key in `references.bib`.
- **Finding** is one sentence we can cite safely.
- **Number** is the exact figure or quote to use, if we use one. The source of each number is tagged:
  - `[abs]`: in the paper's abstract, checked today.
  - `[full]`: grep-checked today in the full text (PDF downloaded to `paper/verify/pdfs/`).
  - `[full*]`: from full-text reading by an earlier research agent. After the second check (Verification log) no `[full*]` tags remain: every such number was found in the downloaded full text and retagged `[full]`.
- **Verify** gives the URL(s) used to confirm the title, authors, venue and year.

Metadata sources: the arXiv API (41 records, one for every bib entry that has an arXiv version; the Verify column below links 26 of them), Crossref (all 24 DOIs), the ACL Anthology `.bib` files, PMLR pages, NeurIPS proceedings pages, OpenReview (venue IDs and BibTeX), Semantic Scholar, and Hugging Face / GitHub for software. DBLP and OpenAlex blocked us (bot check and rate limit), so neither was used. An independent second check on the same day is logged at the end of this file ("Verification log").

---

## (1) LLM stylistic signatures and excess vocabulary

| Key | Finding | Number / claim | Verify |
|---|---|---|---|
| `kobak2025delving` | LLM adoption caused an abrupt rise in "style words" (mostly verbs and adjectives) in PubMed abstracts, unlike earlier excess-word events, which involved content words. | "at least 13.5% of 2024 abstracts were processed with LLMs", up to 40% in some subcorpora [abs]. Excess ratios: *delves* r = 28.0, *underscores* r = 13.8, *showcasing* r = 10.7 [full; also recomputed from authors' data in `research/tells/kobak_style_words_2024_ranked.tsv`]. Of the 379 excess style words in 2024, 66% were verbs and 14% adjectives; earlier excess words were mostly content nouns (79.2% of content words) [full] | https://doi.org/10.1126/sciadv.adt3813 ; https://arxiv.org/abs/2406.07016 |
| `liang2024monitoring` | Corpus-level maximum-likelihood estimation shows LLM-modified text in AI-conference peer reviews. The estimated share is higher in reviews that report lower confidence, were submitted close to the deadline, or came from reviewers less likely to answer rebuttals. | "between 6.5% and 16.9% of text submitted as peer reviews ... could have been substantially modified by LLMs" [abs]. In ICLR 2024 reviews, *commendable*, *meticulous* and *intricate* show "9.8, 34.7, and 11.2-fold increases in probability of occurring in a sentence" (Fig. 1 caption) [full] | https://proceedings.mlr.press/v235/liang24b.html ; https://arxiv.org/abs/2403.07183 |
| `reinhart2025llms` | Using Biber's features, instruction-tuned LLMs differ systematically from humans in grammar and rhetoric (a noun-heavy, informationally dense style), and the gap is larger for instruction-tuned models than for base models. | "instruction-tuned LLMs used present participial clauses at 2 to 5 times the rate of human text" and nominalizations at 1.5 to 2 times; for GPT-4o specifically, present participial clauses 5.3x (paired d = 1.38) and nominalizations 2.1x (d = 1.23) [full]. "tapestry" appeared in 23% of GPT-4o outputs [full] | https://doi.org/10.1073/pnas.2422455122 ; https://arxiv.org/abs/2410.16107 |
| `juzek2025delve` | Identifies 21 focal words whose rise in scientific abstracts is likely due to LLM use. The authors find no evidence that model architecture, algorithm choices or training data cause the overuse. Model comparisons are consistent with RLHF playing a role, but the online human study was not conclusive (participants reacted to "delve" differently from the other focal words). | "21 focal words" [abs] | https://aclanthology.org/2025.coling-main.426/ ; https://arxiv.org/abs/2412.11385 |
| `geng2024chatgpt` | Word-frequency shifts in 1M arXiv abstracts show a growing ChatGPT-style footprint, largest in computer science. | about 35% of CS abstracts estimated "LLM-style" (baseline: GPT-3.5 "revise the following sentences") [abs] | https://arxiv.org/abs/2404.08627 |
| `shaib2024syntactic` | Models produce templated syntax (recurring POS patterns) more often than human references, and most of those templates already appear in pre-training data. | 76% of templates in model text are found in pre-training data vs 35% for human text [abs] | https://aclanthology.org/2024.emnlp-main.368/ |
| `shaib2026slop` | An expert-derived taxonomy of AI "slop" (seven final codes: density, relevance, factuality, bias, structure, coherence, tone; Table 1 [full]). Binary slop judgments are somewhat subjective but track latent dimensions such as coherence and relevance [abs]. | Syntax-only features predict the binary slop label best: AUROC 0.64 (+/-0.06, logistic regression) and 0.68 (+/-0.09, PCA+LDA). GPT-5 is poor at locating slop spans: character-level precision 0.08 and recall 0.12 zero-shot, 0.13 / 0.19 with 5 examples [full, arXiv v3] | https://openreview.net/forum?id=UMipfwK6Ar (COLM 2026) ; https://arxiv.org/abs/2509.19163 |
| `chakrabarty2025salvaged` | Professional writers agree on a 7-category taxonomy of LLM idiosyncrasies (cliché, unnecessary exposition, etc.). Automatic detect-then-edit improves LLM text but stays below expert edits. | LAMP corpus: 1,057 edited paragraphs [abs]. Writer-edited ranked first 65% of the time, mean rank 1.5; LLM-edited 1.99; raw LLM 2.51 (600 judgments) [full] | https://doi.org/10.1145/3706598.3713559 ; https://arxiv.org/abs/2409.14509 |
| `paech2026antislop` | Model-specific "slop" patterns can be profiled against human baselines. Naive token banning damages output; targeted fine-tuning (FTPO) suppresses patterns while keeping quality. | "some slop patterns appear over 1,000x more frequently in LLM output than human text"; token banning "becomes unusable at just 2,000" patterns; FTPO "90% slop reduction" [abs] | https://openreview.net/forum?id=gLcyM1khyp (ICLR 2026) ; https://arxiv.org/abs/2510.15061 |
| `peng2026notx` | A "tic" is about appropriateness, not form. The Mandarin "not X, but Y" construction is overused by LLMs, but most uses are correct-but-unneeded rather than wrong. Several reward models and an LLM judge favor the construction, and both SFT and preference optimization tend to raise its frequency in open-weight models. | 5 commercial models use it 2.5 to 9.2x as densely as humans; of 307 uses, 1.30% defective, 52.8% optional [abs] | https://arxiv.org/abs/2610.22249 |
| `shan2026stylometric` | AI *generation* leaves a consistent stylometric footprint (entropy and lexical diversity) across 8 LLMs and 5 domains. AI *editing* of human text does not reproduce it and stays hard to separate from human writing. | Qualitative [abs]. AI editing vs human sources: lexical density d = -3.10, lexical diversity d = +0.24, entropy d = -0.28 [full] | https://arxiv.org/abs/2608.27855 (arXiv comment: EMNLP 2026 main; not yet in ACL Anthology) |
| `malik2026erased` | Heavy AI rewriting erases authorship signals ("idiolect erasure") in personal blogs and workplace email, with a much smaller effect on topic-structured news. Heavily rewritten text may also evade AI detectors ("double erasure"). Relevant to ghostwriting vs coaching. | LUAR authorship attribution reduced "by as much as 66.5 percentage points" [abs] | https://arxiv.org/abs/2608.00926 |

## (2) Human detection of AI text

| Key | Finding | Number / claim | Verify |
|---|---|---|---|
| `russell2025people` | Annotators who use LLMs heavily for writing are accurate, robust detectors of AI text, even after paraphrasing and humanization. They rely on vocabulary but also on originality, formality and clarity. | Majority vote of 5 expert annotators "misclassifies only 1 of 300 articles" [abs]. Vocabulary clues mentioned in 53.1% of explanations, then sentence structure 35.9%, grammar 24.8%, originality 23.7% [full] | https://aclanthology.org/2025.acl-long.267/ ; https://arxiv.org/abs/2501.15654 |
| `jakesch2023heuristics` | People cannot reliably detect AI-written self-presentations. They rely on flawed heuristics (first-person pronouns, contractions, family topics) that AI can exploit. | N = 4,600 participants in six experiments [abs] | https://doi.org/10.1073/pnas.2208839120 ; https://arxiv.org/abs/2206.07271 |
| `clark2021human` | Untrained evaluators distinguish GPT-3 from human text at chance, and brief training helps little. Untrained human evaluation is a weak gold standard. | "at random chance level"; with training, accuracy "improved up to 55%" [abs] | https://aclanthology.org/2021.acl-long.565/ |

## (3) Automatic detectors, benchmarks, attacks, humanizers

| Key | Finding | Number / claim | Verify |
|---|---|---|---|
| `dugan2024raid` | RAID is a large shared benchmark for machine-text detectors. Detectors are easily fooled by adversarial attacks, decoding changes, repetition penalties and unseen generators. | "over 6 million generations spanning 11 models, 8 domains, 11 adversarial attacks and 4 decoding strategies" [abs]. Many detectors "are nearly inoperable at low false positive rates" [full] | https://aclanthology.org/2024.acl-long.674/ |
| `mitchell2023detectgpt` | Zero-shot detection from probability curvature: model samples sit in negative-curvature regions of the model's log-probability. | AUROC 0.81 (best zero-shot baseline) to 0.95 on GPT-NeoX-20B fake news [abs] | https://proceedings.mlr.press/v202/mitchell23a.html |
| `bao2024fastdetectgpt` | Replaces DetectGPT's perturbations with conditional probability curvature via sampling: faster and more accurate. | about 75% relative improvement over DetectGPT; 340x speed-up [abs] | https://openreview.net/forum?id=Bpcgcr8E8Z (ICLR 2024) |
| `hans2024binoculars` | A zero-shot score contrasting two related LMs (perplexity / cross-perplexity) detects machine text without training data. | "detects over 90% of generated samples from ChatGPT ... at a false positive rate of 0.01%" [abs] | https://proceedings.mlr.press/v235/hans24a.html |
| `adam2026gptzero` | Technical report of the commercial GPTZero detector: hierarchical multi-task architecture with red-teaming for paraphrase and adversarial robustness. Vendor-authored. | No independent number; vendor claims only [abs] | https://arxiv.org/abs/2602.13042 |
| `liang2023biased` | Popular GPT detectors misclassify non-native English writing as AI-generated while classifying native writing correctly. Simple prompting both removes the bias and evades the detectors. | 7 detectors; 91 TOEFL essays; "average false positive rate: 61.22%"; 19.78% flagged by all 7; 97.80% flagged by at least one; word-enrichment cut FPR to 11.77% [full] | https://doi.org/10.1016/j.patter.2023.100779 ; https://arxiv.org/abs/2304.02819 |
| `weberwulff2023testing` | Fourteen detection tools (including Turnitin) are "neither accurate nor reliable", lean toward labelling text human, and degrade further under obfuscation. | "even the highest accuracy values are below 80%" [full] | https://doi.org/10.1007/s40979-023-00146-z ; https://arxiv.org/abs/2306.15666 |
| `sadasivan2025reliably` | Recursive paraphrasing defeats watermark-, classifier-, zero-shot- and retrieval-based detectors with little quality loss. Theory links the best possible AUROC to the total-variation distance between human and AI text. | Qualitative [abs] | https://openreview.net/forum?id=OOgsAZdFOt (TMLR 2025) ; https://arxiv.org/abs/2303.11156 |
| `krishna2023paraphrasing` | An 11B paraphraser (DIPPER) evades watermarking, GPTZero, DetectGPT and OpenAI's classifier. Retrieval over the API provider's own generations is proposed as a defense. | DetectGPT accuracy drops "from 70.3% to 4.6% (at a constant false positive rate of 1%)" [abs] | https://papers.nips.cc/paper_files/paper/2023/hash/575c450013d0e99e4b0ecf82bd1afaa4-Abstract-Conference.html |
| `perkins2024simple` | Simple prompt-based evasion techniques cut the accuracy of GenAI text detectors that was already low. The authors say detectors cannot be used to decide integrity violations. | n = 805 tests; baseline accuracy 39.5% [abs], falling by a mean 17.4 points (to 22.1%) under adversarial techniques [full]; human-written control samples were classified correctly in only 67% of tests [full] | https://doi.org/10.1186/s41239-024-00487-w ; https://arxiv.org/abs/2403.19148 |
| `creanga2026paradox` | Asking an LLM to "sound more human" can make text *easier* to detect. A RoBERTa detector tracks statistical complexity and flags formal human writing. | Verb diversity 0.77 to 0.92 after "humanizing"; "76.3% false-positive rate on formal human writing" [abs] | https://arxiv.org/abs/2610.03110 |
| `roe2026dramaturgies` | A systematic catalogue of commercial AI-humanizer websites shows how they frame evasion as legitimate; argues for assessment reform over detection. | "we cataloged 55 humanizer sites" [abs] | https://arxiv.org/abs/2605.02649 |
| `karr2026detection` | Commercial detectors flag guideline-compliant light AI editing of human abstracts, while humanizer output evades them, so honest editing carries more sanction risk than evasion. | Light edits flagged 38 to 80%; unmodified 2023 to 2025 originals flagged 9 to 15%; after Undetectable AI, FNR > 96% [abs] | https://arxiv.org/abs/2608.11256 |
| `desklib2025detector` | Open-source detector #1: DeBERTa-v3-large fine-tuned on RAID. | MIT license; card updated 17 Feb 2025 | https://huggingface.co/desklib/ai-text-detector-v1.01 (checked via HF Hub API) |
| `fakespot2025detector` | Open-source detector #2: RoBERTa-base fine-tune. | Apache-2.0; card updated 25 Feb 2025 | https://huggingface.co/fakespot-ai/roberta-base-ai-text-detection-v1 |
| `superannotate2024detector` | Open-source detector #3: RoBERTa-large fine-tune. | Custom license ("other"); card updated 17 Dec 2024 | https://huggingface.co/SuperAnnotate/ai-detector |
| `chen2026humanizer` | The popular open-source "humanizer" agent skill we compare against. Built on Wikipedia's Signs of AI writing; 26 patterns. | SKILL.md metadata version 3.1.0; MIT, copyright 2025 Siqi Chen; 26 numbered patterns in SKILL.md and README. About 58.9k GitHub stars on the repo page fetched 2026-10-20 (`research/github/candidates.md` said 58.8k; the count moves daily, so write "about 59k" with the access date). The README says judges preferred its rewrite "16 times out of 16" (issue #229). The issue says "every judge is a language model from one family", so cite this only as the author's own claim. The README also says "Getting past AI detectors is not a goal, and detectors still flag most of its output." | https://github.com/blader/humanizer ; https://raw.githubusercontent.com/blader/humanizer/main/LICENSE |
| `wikipedia2026signs` | The WikiProject AI Cleanup guide that the humanizer and most word lists derive from. It warns against treating the signs as a checklist to fix. | Quote: "Please do not merely treat these signs as the problems to be fixed; that could just make detection harder." Matches the live page word for word (bold in the original) | https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing (live wikitext via `action=raw`, fetched 2026-10-20; saved copy `research/tells/downloads/wikipedia_signs_of_ai_writing.txt`) |

## (4) Watermarking

| Key | Finding | Number / claim | Verify |
|---|---|---|---|
| `kirchenbauer2023watermark` | Green-list watermark: softly promote a pseudo-random token subset during sampling, then detect with a statistical test (interpretable p-values) without model access. | Qualitative [abs] | https://proceedings.mlr.press/v202/kirchenbauer23a.html |
| `dathathri2024synthid` | SynthID-Text is a production watermark that changes only sampling, preserves quality, and is deployed at scale in Gemini. | Live experiment on "nearly 20 million Gemini responses" confirmed preserved quality [abs via Crossref]. "SynthID-Text has been productionized in the user-facing Gemini and Gemini Advanced chatbots" [full, nature.com] | https://doi.org/10.1038/s41586-024-08025-4 |

## (5) LLMs and admissions essays

| Key | Finding | Number / claim | Verify |
|---|---|---|---|
| `lee2025poor` | LLM-written admissions essays are linguistically distinct from 30,000 human applicants' essays, and identity prompting does not steer models toward the corresponding group's style. | Human-vs-LLM classifier F1 = 0.998 (T5) / 0.999 (TF-IDF) on average across LLMs [full]. Note: these are raw LLM outputs vs human essays from the 2019-20 to 2022-23 cycles, written before ChatGPT was widely available (paper's footnote 1) [full], so this is not a real-world detection rate | https://arxiv.org/abs/2503.20062 |
| `alvero2024hegemony` | GPT-3.5/4 essays show less stylistic variability than over 150,000 human admissions essays and most resemble essays by male, higher-privilege applicants. | ">150,000" human vs ">25,000" AI essays; "most similar to essays authored by students who are males with higher levels of social privilege" [abs via Semantic Scholar] | https://doi.org/10.1186/s40537-024-00986-7 |
| `alvero2021essay` | Before AI, essay content and style already encoded social class: they correlated more strongly with household income than SAT scores did. | 240,000 essays from 60,000 UC applicants [abs via Europe PMC] | https://doi.org/10.1126/sciadv.abi9031 |
| `isley2026admissions` | In one U.S. public-policy *master's* program, most 2025 applicants submitted at least one essay that GPTZero flagged as AI. In the 2023 and 2024 cycles, flagged essays were associated with lower admission (2025 outcomes were not analyzed because the program changed its process after seeing the results). In an experiment, admissions officers partly recognized AI text. | 7,462 applications, 2020 to 2025 [full]; 56.1% of 2025 applicants with at least one essay labeled "AI only, high confidence" by GPTZero (Pangram: 45.9%) [full, Table A1]; -1.5 p.p. admission per AI essay, -2.6 p.p. with essay-quality controls [full]; officers' AUC 0.70 (95% CI 0.65 to 0.75) [full]. Caveat: graduate program; AI label = GPTZero | https://arxiv.org/abs/2609.22549 |
| `lee2026divide` | At one selective university, estimated LLM use in essays rose sharply in 2024, more among lower-SES applicants, for whom it was more strongly associated with lower predicted admission. | N = 81,663 applications, 2020 to 2024 [abs] | https://doi.org/10.1145/3774398.3811620 ; https://arxiv.org/abs/2602.17791 |

## (6) LLM-as-judge and its biases

| Key | Finding | Number / claim | Verify |
|---|---|---|---|
| `zheng2023judging` | Strong LLM judges agree with human preferences about as often as humans agree with each other, but show position, verbosity and self-enhancement biases. | "over 80% agreement, the same level of agreement between humans" [abs] | https://papers.nips.cc/paper_files/paper/2023/hash/91f18a1287b398d378ef22505bf41832-Abstract-Datasets_and_Benchmarks.html |
| `panickssery2024llm` | LLM evaluators can recognize their own outputs, and self-recognition strength correlates linearly with self-preference bias. Motivates a cross-family judge panel. | Qualitative [abs] | https://papers.nips.cc/paper_files/paper/2024/hash/7f1f0218e45f5414c79c0679633e47bc-Abstract-Conference.html ; https://openreview.net/forum?id=4NJBV6Wp0h |
| `wang2024fair` | LLM-judge rankings can be flipped by swapping response order. Balanced position calibration (averaging over orders) mitigates this. | With ChatGPT as judge, Vicuna-13B "could beat ChatGPT on 66 over 80 tested queries" by order alone [abs] | https://aclanthology.org/2024.acl-long.511/ |

## (7) Homogenization from AI writing assistance

| Key | Finding | Number / claim | Verify |
|---|---|---|---|
| `padmakumar2024diversity` | Co-writing argumentative essays with InstructGPT (not base GPT-3) reduces diversity across authors. The effect comes from model-contributed text; user-written text is unaffected. | "statistically significant reduction in diversity"; "the user-contributed text remains unaffected" [abs] | https://openreview.net/forum?id=Feiz5HtCD0 (ICLR 2024) |
| `agarwal2025homogenize` | AI writing suggestions pull Indian users' writing toward Western styles. | 118 participants (India/US) [abs]. Classifier separating Indian from American authors drops from 90.6% to 83.5% with AI suggestions [full] | https://doi.org/10.1145/3706598.3713564 |
| `doshi2024creativity` | Access to LLM story ideas makes individual stories rated more creative, especially for less creative writers, but makes stories more similar to each other (a social dilemma). | Qualitative [abs] | https://doi.org/10.1126/sciadv.adn5290 |
| `abdulhai2026distort` | LLM help changes the *meaning* of writing, not just its voice. Heavy users wrote more neutral essays, and even "grammar-only" LLM edits shifted semantics. | "a 68.9% increase in the proportion" of neutral-stance essays with extensive AI use [full; abstract says "nearly 70%"]. Grammar-only edits "still change the text in a way that significantly alters its semantic meaning" [abs] | https://arxiv.org/abs/2603.18161 |

## (8) Human essay corpus; hallucination and faithfulness

| Key | Finding | Number / claim | Verify |
|---|---|---|---|
| `crossley2024persuade` | PERSUADE 2.0 is a large corpus of U.S. student argumentative essays with holistic scores and demographic information. It is our pre-ChatGPT human baseline: its essays are the PERSUADE 1.0 essays (README), and the PERSUADE 1.0 paper (Assessing Writing 54:100667, DOI 10.1016/j.asw.2022.100667) was received on 8 Feb 2022. Neither source we could read gives the exact collection years, so do not write "pre-2022" without checking the 2.0 full text. | "over 25,000 argumentative essays produced by 6th-12th grade students in the United States for 15 prompts" (corpus README) | https://doi.org/10.1016/j.asw.2024.100865 ; https://github.com/scrosseye/persuade_corpus_2.0 |
| `ji2023hallucination` | Survey of hallucination in NLG: definitions (intrinsic/extrinsic), metrics and mitigation across tasks. Frames our "unsupported claims" fidelity metric. | Qualitative | https://doi.org/10.1145/3571730 ; https://arxiv.org/abs/2202.03629 |
| `min2023factscore` | FActScore splits long-form generations into atomic facts and scores the share supported by a knowledge source. It is the closest precedent for counting unsupported claims. | ChatGPT "only achieves 58%" on biographies; automated estimator "less than a 2% error rate" [abs] | https://aclanthology.org/2023.emnlp-main.741/ |

---

## Title and metadata differences to keep in mind

- `perkins2024simple`: the journal title is "Simple techniques to bypass GenAI text detectors: implications for inclusive education". The arXiv title was "GenAI Detection Tools, Adversarial Techniques and Implications for Inclusivity in Higher Education". The bib uses the journal title.
- `doshi2024creativity`: the journal title is "Generative AI enhances individual creativity but reduces the collective diversity of novel content". The arXiv title differs slightly. The bib uses the journal title.
- `sadasivan2025reliably`: the TMLR (2025) title adds "Stress Testing AI Text Detectors Under Various Attacks". The bib cites TMLR, not the arXiv version.
- `lee2025poor`: earlier notes said "presented at COLM 2025". OpenReview shows only **COLM 2025 workshop** posters (SoLaR, Social Sim), under a different title ("...Evidence Using 30,000 College Admissions Essays"). The bib cites the arXiv preprint, not a main-conference paper.
- `wang2024fair`: the ACL 2024 version adds Lingpeng Kong as an author (11 authors; arXiv lists 10). The bib follows ACL.
- `dugan2024raid`: in the ACL author order, Zhu comes before Ludan. arXiv has the opposite order. The bib follows ACL.
- `ji2023hallucination`: the journal version (CSUR 55(12), 2023) has 10 authors. arXiv v7 lists 13. The bib follows the journal (Crossref).
- `crossley2024persuade`: the publisher record (Crossref and Semantic Scholar) orders authors Crossley, Tian, Baffour, Franklin, Benner, Boser, and gives initials only. The corpus README lists Baffour before Tian. The bib follows the publisher.
- `kobak2025delving`: the arXiv v1 title was "Delving into ChatGPT usage in academic writing through excess vocabulary". The published title is used.
- `shan2026stylometric`, `karr2026detection`: the arXiv comments claim EMNLP 2026 main and the ACM AI Leadership Summit respectively. Neither proceedings is published yet, so both are cited as arXiv.
- `isley2026admissions`: a *graduate* public-policy program, with AI defined by GPTZero labels. Do not generalize it to undergraduate admissions.

## Verified but left out (to stay at 50)

All of the following exist and were verified today. They were omitted only for space or scope:
- Liang et al. 2024, "Mapping the Increasing Use of LLMs in Scientific Papers" (COLM 2024; arXiv 2404.01268). Redundant with Kobak and Liang (ICML).
- Juzek & Ward, "Word Overuse and Alignment in Large Language Models: The Influence of Learning from Human Feedback" (BIAS workshop @ ECML PKDD 2025, Springer CCIS, DOI 10.1007/978-3-032-19096-3_16; arXiv 2508.01930). Swap it in if we discuss RLHF as the cause of word overuse.
- Ippolito et al. 2020, "Automatic Detection of Generated Text is Easiest when Humans are Fooled" (ACL 2020).
- Guo et al. 2023, HC3 corpus (arXiv 2301.07597).
- Emi & Spero 2024, Pangram technical report (arXiv 2402.14873).
- Sharma et al., "Towards Understanding Sycophancy in Language Models" (ICLR 2024; arXiv 2310.13548).
- Huang et al., LLM hallucination survey (ACM TOIS 43(2), 2025; DOI 10.1145/3703155). Only one survey was requested.

## Requested items that could not be verified

None. Every requested reference was found with an exact title, author list and year. "GPTZero if citable" resolved to the 2026 technical report (arXiv 2602.13042). "Abdulhai et al. 2026" resolved to arXiv 2603.18161 (v2, 26 Aug 2026; preprint).

---

## Verification log (independent second check, 2026-10-20)

**Method.** Every check was redone from scratch, without reusing the first pass's files. The arXiv API returned 41 records (one for every entry that has an arXiv version). Crossref resolved all 24 DOIs. The ACL Anthology `.bib` files covered the 7 ACL-family papers, and the PMLR citation metadata covered the 4 ICML papers. OpenReview's search API confirmed 6 venues (its by-ID API now returns a bot challenge). The Hugging Face Hub API covered the 3 models, raw GitHub plus the github.com page covered humanizer, and Wikipedia `action=raw` covered the guide. For the findings, the arXiv abstracts were read against each Finding sentence. 15 full-text PDFs were downloaded again and grep-checked for every `[full]`/`[full*]` number. The publisher full text was read for SynthID (nature.com), and Europe PMC was used for Alvero 2021 and PERSUADE 1.0. Files are in `paper/recheck/dl/`.

**Result.** 50 entries checked. **No entry was removed.** No BibTeX field was wrong, so `references.bib` only gained a provenance comment. 16 note rows were FIXED (wording, scope, source tag or an added detail). 34 were OK as written.

| Key | Status | Detail |
|---|---|---|
| `kobak2025delving` | FIXED | Metadata OK (Crossref, arXiv). Ratios 28.0 / 13.8 / 10.7 found in full text: `[full*]` -> `[full]`. Added the 66% verbs / 14% adjectives figure that supports the "style words" finding. |
| `liang2024monitoring` | FIXED | Metadata OK (PMLR, pp. 29575-29620). "Concentrated in" overstated the abstract ("higher in"), so it was reworded. The 9.8 / 34.7 / 11.2-fold ratios were found in the Fig. 1 caption (ICLR 2024; probability of occurring in a sentence): `[full*]` -> `[full]`. |
| `reinhart2025llms` | FIXED | Metadata OK (Crossref). All numbers found. Clarified that 2.1x nominalizations is GPT-4o's rate (the cross-model range is 1.5 to 2x) and added d = 1.23. |
| `juzek2025delve` | FIXED | Metadata OK (ACL Anthology). The finding overstated the RLHF evidence. The paper "fail[s] to find evidence" for architecture, algorithm or data causes; model testing is "consistent with RLHF playing a role", and the human study was not conclusive. Reworded. |
| `geng2024chatgpt` | OK | arXiv metadata and the abstract match (about 35% of CS abstracts). |
| `shaib2024syntactic` | OK | ACL Anthology and Crossref match; 76% vs 35% is in the abstract. |
| `shaib2026slop` | FIXED | Venue COLM 2026 confirmed (OpenReview UMipfwK6Ar). Taxonomy codes confirmed in Table 1. AUROC 0.64 / 0.68 and GPT-5 span precision 0.08 / recall 0.12 found in arXiv v3 (updated 2026-10-16): `[full*]` -> `[full]`. |
| `chakrabarty2025salvaged` | OK | Crossref (CHI '25, pp. 1-33). 65%, ranks 1.5 / 1.99 / 2.51 and 600 judgments found in the full text. |
| `paech2026antislop` | OK | ICLR 2026 Poster confirmed on OpenReview; every number is in the abstract. |
| `peng2026notx` | FIXED | arXiv 2610.22249 v1 (2026-10-15) confirmed. "Reward models and LLM judges" -> "several reward models and an LLM judge" (abstract wording); added the SFT/PO frequency finding. |
| `shan2026stylometric` | FIXED | arXiv comment "EMNLP Main 2026" confirmed; not in the Anthology yet. d = -3.10 found in the full text: `[full*]` -> `[full]`, with the other two effect sizes added. |
| `malik2026erased` | FIXED | Metadata OK. Scope added: the erasure is large for blogs and email and much smaller for news (abstract). |
| `russell2025people` | FIXED | ACL 2025 metadata OK. 53.1% confirmed as "vocabulary-related clues": `[full*]` -> `[full]`. |
| `jakesch2023heuristics` | OK | Crossref and the abstract match (N = 4,600, six experiments). |
| `clark2021human` | OK | ACL Anthology matches; "random chance level" and "up to 55%" are in the abstract. |
| `dugan2024raid` | OK | ACL author order (Zhu before Ludan) confirmed. "Nearly inoperable at low false positive rates" found in the full text. |
| `mitchell2023detectgpt` | OK | PMLR v202 pp. 24950-24962; AUROC 0.81 -> 0.95 is in the abstract. |
| `bao2024fastdetectgpt` | OK | ICLR 2024 poster confirmed on OpenReview; about 75% and 340x are in the abstract. |
| `hans2024binoculars` | OK | PMLR v235 pp. 17519-17537; "over 90% ... at 0.01% FPR" is in the abstract. |
| `adam2026gptzero` | OK | arXiv 2602.13042 with 10 authors matches. The abstract supports the architecture and red-teaming description. Vendor-authored (Edward Tian is an author). |
| `liang2023biased` | OK | Crossref (Patterns 4(7)) matches. 61.22%, 18/91 = 19.78%, 89/91 = 97.80% and 61.22% -> 11.77% all found in the full text. |
| `weberwulff2023testing` | OK | Crossref matches (IJEI 19:26, 2023). 12 + 2 = 14 tools confirmed. "Even the highest accuracy values are below 80%" found in the full text. |
| `sadasivan2025reliably` | OK | TMLR acceptance confirmed (OpenReview OOgsAZdFOt, published 2025-01-23); the published title is used. |
| `krishna2023paraphrasing` | OK | Crossref (NeurIPS 36, pp. 27469-27500); 70.3% -> 4.6% is in the abstract. |
| `perkins2024simple` | FIXED | Crossref title and authors match. "17.4 points" confirmed in the full text (39.5% -> 22.1%); the tag changed from [abs] to [full]. "Prompting techniques" wording is supported. Added the 67% human-control accuracy. |
| `creanga2026paradox` | OK | arXiv 2610.03110 matches; all numbers are in the abstract. |
| `roe2026dramaturgies` | OK | arXiv 2605.02649 matches; "55 humanizer sites" and the assessment-reform conclusion are in the abstract. |
| `karr2026detection` | OK | arXiv 2608.11256 v3 matches (comment: ACM AI Leadership Summit); all numbers are in the abstract. |
| `desklib2025detector` | OK | HF API: base microsoft/deberta-v3-large, dataset liamdugan/raid, MIT, lastModified 2025-02-17. |
| `fakespot2025detector` | OK | HF API: base FacebookAI/roberta-base, Apache-2.0, lastModified 2025-02-25. |
| `superannotate2024detector` | OK | HF API: base FacebookAI/roberta-large, license "other", lastModified 2024-12-17. |
| `chen2026humanizer` | FIXED | MIT (c) 2025 Siqi Chen, version 3.1.0 and 26 patterns confirmed. Stars 58.8k -> about 58.9k (github.com page today). The "16 of 16" claim was traced to issue #229, which confirms that all judges were LMs from one family. |
| `wikipedia2026signs` | FIXED (source only) | The quote now matches the live page word for word; before, it was checked only against a saved copy. |
| `kirchenbauer2023watermark` | OK | PMLR v202 pp. 17061-17084; the abstract supports the finding. |
| `dathathri2024synthid` | FIXED (source added) | Crossref matches (Nature 634:818-823, 24 authors). The "deployed in Gemini" part of the finding was not in the abstract; it is now cited from the full text ("productionized in ... Gemini and Gemini Advanced"). |
| `lee2025poor` | FIXED (detail) | arXiv matches. F1 0.998 / 0.999 found. Added the human essay years (2019-20 to 2022-23, written before ChatGPT was widely available) from the paper's footnote. |
| `alvero2024hegemony` | OK | Crossref matches (J. Big Data 11:138). The Semantic Scholar abstract has ">150,000", ">25,000" and the "males with higher levels of social privilege" sentence. |
| `alvero2021essay` | OK | Crossref matches (Sci. Adv. 7(42)). Europe PMC abstract: 240,000 essays from 60,000 UC applicants; essays correlate more strongly with income than SAT scores do. |
| `isley2026admissions` | FIXED | arXiv matches. All numbers found. The 56.1% is GPTZero "AI only, high confidence" (Table A1). The admission penalty comes from the 2023 and 2024 cycles only, not 2025; the finding was corrected. |
| `lee2026divide` | OK | Crossref matches (L@S '26, pp. 179-190). N = 81,663 and the SES findings are in the abstract. |
| `zheng2023judging` | OK | Crossref (NeurIPS 36, pp. 46595-46623); "over 80% agreement" is in the abstract. |
| `panickssery2024llm` | OK | Crossref (NeurIPS 37, pp. 68772-68802); OpenReview shows "NeurIPS 2024 oral"; the linear correlation is in the abstract. "Motivates a cross-family panel" is our own reading of the paper. |
| `wang2024fair` | OK | ACL 2024 has 11 authors (adds Lingpeng Kong), confirmed by Crossref; "66 over 80" is in the abstract. |
| `padmakumar2024diversity` | OK | ICLR 2024 poster confirmed on OpenReview; quotes are in the abstract. |
| `agarwal2025homogenize` | OK | Crossref (CHI '25, pp. 1-21). 118 participants is in the abstract. 90.6% -> 83.5% (Indian-vs-American classifier) found in the full text. |
| `doshi2024creativity` | OK | Crossref title matches the bib. The published abstract has the "social dilemma" sentence. |
| `abdulhai2026distort` | OK | arXiv v2 matches. 68.9% found in the full text (Fig. 6); the abstract says "nearly 70%". |
| `crossley2024persuade` | FIXED | Crossref and Semantic Scholar author order confirmed; the README quote matches. "Pre-2022 baseline" was not supported by any source we could read and was reworded to "pre-ChatGPT", with the PERSUADE 1.0 received date (8 Feb 2022) as evidence. |
| `ji2023hallucination` | OK | Crossref has 10 authors, CSUR 55(12):1-38, matching the bib. |
| `min2023factscore` | OK | ACL Anthology (pp. 12076-12100); 58% and "<2% error rate" are in the abstract. |

**Not verifiable today (no change made):** the exact collection years of the PERSUADE essays. The Elsevier full-text API was rate-limited and the doi.org/nature.com WebFetch path failed DNS; nature.com was then read with curl instead. Before printing a year range for PERSUADE, read the PERSUADE 2.0 full text.

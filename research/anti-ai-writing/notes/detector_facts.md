# AI-text detectors: facts and reliability (brief)

Checked 2026-10-20. Most Turnitin facts come from Turnitin's own help center, pulled through its public Zendesk API (article JSON, with `updated_at`/`edited_at` timestamps). Vendor numbers are vendor claims unless noted. Anything I could not confirm from a primary source is marked UNVERIFIED.

---

## 1. Turnitin AI writing detection

**Who can use it.** Only institutions can buy it. "Turnitin subscriptions are designed for educational institutions, not for individual purchase" ([Turnitin: How to purchase](https://guides.turnitin.com/hc/en-us/articles/37985974637453-How-to-purchase-a-Turnitin-subscription)). AI detection is a paid add-on on top of that: it needs a **Turnitin Originality** license, or the AI add-on for iThenticate 2.0, and an admin has to switch it on. Institutions can also turn it off ([AI FAQ, "Access & licensing"](https://guides.turnitin.com/hc/en-us/articles/28477544839821-Turnitin-s-AI-writing-detection-capabilities-FAQs)). In practice a student cannot pre-check a paper on Turnitin's AI detector before handing it in.

**Who sees the score.** Turnitin's documentation contradicts itself here:
- The FAQ (edited 2026-10-14) says: "only instructors and administrators are able to see the indicator" and "The AI writing detection indicator and report are not visible to students", although instructors can download the PDF and share it ([FAQ](https://guides.turnitin.com/hc/en-us/articles/28477544839821-Turnitin-s-AI-writing-detection-capabilities-FAQs)).
- The newer "Using the AI Writing Report" page (edited 2026-10-19) says: "If you make the AI Writing Report available to students, they can open it from their Similarity Report" ([guide](https://guides.turnitin.com/hc/en-us/articles/22774058814093-Using-the-AI-Writing-Report)).
- So the default is instructor-only. A student-visibility option looks like it is being rolled out (UNVERIFIED which accounts have it).

**How the score is shown (current policy).** Source: [How to access the AI Writing Report](https://guides.turnitin.com/hc/en-us/articles/28457596598925-How-to-access-the-AI-Writing-Report), edited 2026-03-06, and the [release notes](https://guides.turnitin.com/hc/en-us/articles/28294949544717-AI-writing-detection-model).
- **0%**: shown as 0%.
- **1–19%**: shown as **`*%`**, with no number and no highlights. Turnitin's wording: "An asterisk (*%) appears when AI detection is below 20%, where results are less reliable and false positives are more likely. In this range (1–19%), no exact percentage or highlights are shown."
- **20–100%**: the number is shown, with the flagged sentences highlighted in blue.
- **History.** In May 2023 Turnitin added an asterisk *next to* scores under 20%, but the number was still shown ([Campus Technology, May 2023](https://campustechnology.com/articles/2023/05/turnitin-says-its-ai-detector-analyzed-38m-submissions-in-six-weeks.aspx)). The release dated **2024-07-16** stopped showing numbers in the 1–19% range ([release notes](https://guides.turnitin.com/hc/en-us/articles/28294949544717-AI-writing-detection-model)). The instructor guide puts the cutover at "before July 8, 2024", which is a small date mismatch inside Turnitin's own docs ([guide](https://guides.turnitin.com/hc/en-us/articles/22774058814093-Using-the-AI-Writing-Report)).

**What the percentage means.** Turnitin gives each prose sentence a score between 0 and 1, and sentences above a threshold are labeled AI. The document score is "the percentage of sentences that are above the threshold." Lists, headers, references, tables, code, bullet points and poetry are left out ([FAQ](https://guides.turnitin.com/hc/en-us/articles/28477544839821-Turnitin-s-AI-writing-detection-capabilities-FAQs)). So the number is the share of qualifying prose that was flagged. It is not a probability.

**Stated false-positive rate.** Turnitin says it is "under 1% for documents with over 20% of AI writing … we might flag a human-written document as AI-written for one out of every 100 fully-human written documents." Before each release it checks this on about 700,000 papers written before ChatGPT. It also says it deliberately under-detects: "if we identify that 50% of a document is likely written by an AI tool, it could contain as much as 65% AI writing" ([FAQ](https://guides.turnitin.com/hc/en-us/articles/28477544839821-Turnitin-s-AI-writing-detection-capabilities-FAQs)). The sentence-level false-positive rate is about 4% and clusters at human/AI transitions ([Turnitin blog, Chechitelli 2023](https://www.turnitin.co.uk/blog/understanding-the-false-positive-rate-for-sentences-of-our-ai-writing-detection-capability)).

**File requirements.** At least **300 words** of long-form prose, at most 30,000 words, under 100 MB, and a .docx, .pdf, .txt or .rtf file. Supported languages are English, Spanish, Japanese, Arabic, German, Dutch and Turkish ([guide](https://guides.turnitin.com/hc/en-us/articles/22774058814093-Using-the-AI-Writing-Report)). The 300-word minimum dates from 2023, raised from 150 because short texts produced more false positives ([Turnitin ELL study blog](https://www.turnitin.ca/blog/new-research-turnitin-s-ai-detector-shows-no-statistically-significant-bias-against-english-language-learners)).

**Which models it targets.** The FAQ lists Claude models by name: Claude 3 Haiku, [a Claude model], [a Claude model], [a Claude model], [a Claude model], [a Claude model] and Opus 4.6. It also lists GPT‑4o through GPT‑5.4, Gemini 1.0 through 3.1, Grok 4.1, Llama and Mistral ([FAQ](https://guides.turnitin.com/hc/en-us/articles/28477544839821-Turnitin-s-AI-writing-detection-capabilities-FAQs)).

**Paraphraser and "bypasser" (humanizer) detection timeline.** From the [AI model release notes](https://guides.turnitin.com/hc/en-us/articles/28294949544717-AI-writing-detection-model) and the [general release notes](https://guides.turnitin.com/hc/en-us/articles/27251688507533-Turnitin-release-notes):
- 2023-12-06: started detecting AI text run through "word spinners".
- 2024-07-16: added a separate purple category, "AI-generated text that was AI-paraphrased" (e.g. Quillbot).
- **2025-08-27: "AI bypasser" detection.** This targets tools that "attempt to modify AI-generated text to appear more human-like". It works in **English only**, and Turnitin will not name the tools it detects ([FAQ](https://guides.turnitin.com/hc/en-us/articles/28477544839821-Turnitin-s-AI-writing-detection-capabilities-FAQs); [Plagiarism Today](https://www.plagiarismtoday.com/2025/08/27/turnitin-launches-anti-ai-humanizer-feature/)). Turnitin's chief product officer: humanizers "leave a statistical trace that can be learned and detected." I found **no independent test** of this feature.
- **2026-08-04:** the purple and blue categories were merged into one blue "AI-generated" category, which includes paraphrased and bypassed text.

**Other 2025–2026 updates.**
- 2025-04-02: Japanese.
- 2025-05: Turnitin Clarity, a supervised writing environment with keystroke playback and logging of paste events ([Plagiarism Today](https://www.plagiarismtoday.com/2025/08/27/turnitin-launches-anti-ai-humanizer-feature/); [Clarity student FAQ](https://guides.turnitin.com/hc/en-us/articles/36983230792461-FAQs-for-students-using-Turnitin-Clarity)).
- 2025-10-14 and 2026-02-12: model updates to "improve recall while maintaining a low false positive rate".
- 2026-05-05: Spanish model update.
- 2026-08-18: Arabic.
- 2026-10-06: Turkish, German and Dutch.
- **2026-10-14:** a new English model architecture "to improve accuracy at transition points" between human and AI text.
- Old reports are not rescored. A file has to be resubmitted to get a score from a new model.
- Turnitin repeatedly says the score "should not be used as the sole basis for adverse actions against a student" ([guide](https://guides.turnitin.com/hc/en-us/articles/22774058814093-Using-the-AI-Writing-Report)).

**Grammarly and Turnitin.** Grammarly's ordinary spelling and grammar fixes "in most cases" are not flagged. Text produced by Grammarly's generative features (drafting, paraphrasing and so on) "will likely be flagged" ([FAQ](https://guides.turnitin.com/hc/en-us/articles/28477544839821-Turnitin-s-AI-writing-detection-capabilities-FAQs)).

---

## 2. Grammarly AI detector

- **Free web tool:** [grammarly.com/ai-detector](https://www.grammarly.com/ai-detector). You paste text or upload a file, click "Scan for AI", and get "**—% of this text appears to be AI-generated**", with bands for "Resembles AI text" and "No AI text patterns found".
  - The page does not say whether you need to log in for the free scan, so whether login is required is UNVERIFIED. I could not run the page's JavaScript. Third-party pages disagree ([search summary](https://fast.io/resources/grammarly-ai-detector-review-2026/)).
  - The text box in the page HTML has `maxLength="25000"` characters. Whether that is the real limit is UNVERIFIED.
- **Inside Grammarly products** (the Docs "AI Detector agent", the Google Docs extension, Word through the desktop app), AI detection "is a paid feature" for Pro, Plus, Business and Education plans. The paid agent shows which passages were flagged ([Grammarly support: AI Detector user guide](https://support.grammarly.com/hc/en-us/articles/28936304999949-AI-Detector-user-guide), edited 2026-07-29).
- **What the % means:** "the percentage of scanned text that is likely AI-generated … an averaged estimate". Short passages are harder to score. The free tool does not say why text was flagged. Grammarly itself warns that its score **may differ from Turnitin, GPTZero, Copyleaks** ([support guide](https://support.grammarly.com/hc/en-us/articles/28936304999949-AI-Detector-user-guide)).
- **Grammarly's own rewriting gets flagged by its own detector.** Rewrites from its "Grammarly, Paraphraser, and Humanizer agents come from our LLM", so its own detector "is likely" to flag them ([support guide](https://support.grammarly.com/hc/en-us/articles/28936304999949-AI-Detector-user-guide)). Grammarly also sells an "AI Humanizer" tool, linked from the detector page.
- **Accuracy claim:** "99% detection accuracy and ranks #1 on RAID's independent benchmark" ([Grammarly](https://www.grammarly.com/ai-detector)). This is a vendor claim and I did not check it against the live leaderboard (UNVERIFIED). A secondary review reports Pangram's small test where Grammarly caught 0 of 9 AI samples (UNVERIFIED, [fast.io](https://fast.io/resources/grammarly-ai-detector-review-2026/)).

---

## 3. GPTZero

- **Free tier:** "up to 10,000 words per month", plus the Chrome extension. A scan over **10,000 characters** needs a free account ([gptzero.me](https://gptzero.me/), [pricing](https://gptzero.me/pricing)). Paid plans: Essential 150k words/month, Premium 300k, Professional 500k (prices change; check the site).
- **What the % means. This is important:** GPTZero's headline number is a **probability that the whole document is AI, mixed, or human**. It is not the share of text. GPTZero's own explainer: "the percent you're seeing is NOT saying that '6% of your document contains AI.'" Its example: "4% AI" alongside 57% mixed and 39% human. Every result also comes with a confidence level ([GPTZero: understand your scan](https://gptzero.me/news/understand-gptzero-ai-scan/), updated 2026-04-02). GPTZero's own homepage copy ("what percentage of your text is likely to be AI-generated") contradicts that explainer.
- **Paraphraser and bypasser detection:** launched as a beta on 2024-11-07. GPTZero claims about 95% detection on "certain popular" bypassers and under 0.1% false positives ([GPTZero](https://gptzero.me/news/ai-paraphrasing-detection/)). The support page still says beta ([support](https://support.gptzero.me/articles/5593633457-how-does-gptzero-detect-ai-paraphrasing-and-ai-bypassers)). A January 2026 vendor benchmark claims 90%+ across 12+ humanizers ([GPTZero](https://gptzero.me/news/detecting-ai-humanized-text-how-gptzero-stays-ahead/)).
- **Vendor accuracy claims:** "99.9%" overall and a 1% false-positive rate, including for ESL writers ([gptzero.me](https://gptzero.me/)). These are vendor numbers.

---

## 4. Independent evaluations

| Study | Setup | Key findings |
|---|---|---|
| **RAID**, Dugan et al., ACL 2024 ([paper](https://aclanthology.org/2024.acl-long.674.pdf)) | 6M+ AI texts; 11 generators, 8 domains, 11 attacks, 4 decoding settings; 12 detectors (GPTZero, Originality, Winston, ZeroGPT among them; **not Turnitin**) | Detectors are "easily fooled by adversarial attacks, variations in sampling strategies, repetition penalties, and unseen generative models"; "many … nearly inoperable at low false positive rates". At default thresholds, the commercial detectors' false-positive rate on RAID was ≤1.7%. GPTZero was the most robust to attacks. Now 10M+ docs and 12 attacks ([repo](https://raw.githubusercontent.com/liamdugan/raid/main/README.md)). |
| **Liang et al. 2023**, *Patterns* 4:100779 ([doi](https://doi.org/10.1016/j.patter.2023.100779), full text read via Europe PMC PMC10382961) | 7 detectors; 91 TOEFL essays vs 88 US 8th-grade essays | Average false-positive rate **61.3%** on the TOEFL essays; 19.8% flagged by all 7 detectors; **97.8%** flagged by at least one. US essays were classified almost perfectly. Having ChatGPT enrich the TOEFL essays' vocabulary cut false positives to 11.6%. The prompt "Elevate the provided text by employing literary language" cut detection of ChatGPT essays to near zero. Turnitin was not tested. Turnitin's own (vendor) study found no significant ELL bias at ≥300 words ([Turnitin](https://www.turnitin.ca/blog/new-research-turnitin-s-ai-detector-shows-no-statistically-significant-bias-against-english-language-learners)). |
| **Weber-Wulff et al. 2023**, *Int J Educ Integrity* 19:26 ([PDF](https://eprints.whiterose.ac.uk/id/eprint/207396/1/s40979-023-00146-z.pdf)) | 14 tools, including Turnitin; tested spring 2023 | The tools are "neither accurate nor reliable" and biased toward calling text human. Obfuscation makes them much worse. Turnitin ranked first (76% binary accuracy), but "even the highest accuracy values are below 80%". False positives ranged from 0% (Turnitin) to 50% (GPTZero). Machine translation raised false positives. |
| **Perkins et al. 2024**, *IJETHE* 21:53 ([preprint](https://arxiv.org/abs/2403.19148)) | 7 detectors including Turnitin; 805 tests; Sept–Oct 2023 | Baseline accuracy was 39.5% on AI text and 67% on human controls. After simple prompt-based rewrites it fell to 22.1%. **Turnitin fell most, from 50% to 7.9%.** Adding spelling errors and "increasing burstiness" worked best, but produced text that would earn poor marks. |
| **Jabarian & Imas 2025**, NBER w34223 ([NBER](https://www.nber.org/papers/w34223)) | Pangram, Originality, GPTZero, RoBERTa | Pangram had near-zero false negatives and false positives, "robust across … 'humanizer' tools". It was the only detector to meet a false-positive cap of 0.5%. |
| **Karr et al. 2026**, arXiv 2608.11256 (ACM AI Summit '26) ([paper](https://arxiv.org/abs/2608.11256)) | 642 published abstracts; Pangram 3.2 and GPTZero; Undetectable AI v11 | Light AI edits of human abstracts were flagged **38–80%** of the time. Unedited 2023–25 originals were flagged 9–15%. After humanization, **more than 96%** of AI rewrites went undetected. This contradicts the NBER result on humanizers, which suggests that results depend on the tool and version tested. |

- **OpenAI** withdrew its own AI classifier on 2023-07-20 "due to its low rate of accuracy". At launch it caught 26% of AI text and had a 9% false-positive rate. These figures come from secondary reports ([Decrypt](https://decrypt.co/149826/openai-quietly-shutters-its-ai-text-classifier-due-to-low-accuracy), [Search Engine Land](https://searchengineland.com/openai-ai-classifier-no-longer-available-429912)).

**Universities that turned off Turnitin's AI detector** (text-matching stays on):
- **Vanderbilt, 2023-08-16.** Reasons: no transparency, and at a 1% false-positive rate, "around 750" of its 75,000 yearly papers could be wrongly flagged ([Vanderbilt](https://www.vanderbilt.edu/brightspace/2023/08/16/guidance-on-ai-detection-and-why-were-disabling-turnitins-ai-detector/)).
- **Waterloo, from September 2025** (announced 2025-05-05). Reasons: unreliability, bias against non-native writers, and internal tests where human text was flagged "as 100% generated by AI"; the cost outweighed the benefit ([Waterloo](https://uwaterloo.ca/associate-vice-president-academic/discontinuing-use-ai-detection-functionality-turnitin)).
- **Curtin University, from 2026-01-01** ([Curtin](https://www.curtin.edu.au/news/oasis-news/update-on-turnitin-ai-detection-tool/)).
- **Australian Catholic University**, reportedly switched off in March 2025 after reporting on wrongful misconduct cases (UNVERIFIED; secondary sources only).
- Yale, Johns Hopkins, Northwestern, Georgetown and others are often listed: UNVERIFIED in this pass.

---

## 5. Humanizer tools

- **What they do:** they automatically rewrite AI text (swapping synonyms, restructuring sentences, varying sentence length to raise "perplexity" and "burstiness", removing stock AI phrases and punctuation such as em dashes, and sometimes adding errors) so that detectors miss it ([GPTZero](https://gptzero.me/news/ai-paraphrasing-detection/); [Plagiarism Today](https://www.plagiarismtoday.com/2025/08/27/turnitin-launches-anti-ai-humanizer-feature/); [Karr et al.](https://arxiv.org/abs/2608.11256)). They often make the text worse. GPTZero gives an example where a bypasser introduced grammar errors, and Perkins et al. note that error-injected text "would very likely receive poor marks". Undetectable AI offers a money-back guarantee if its output gets flagged ([Karr et al.](https://arxiv.org/abs/2608.11256), Appendix E.3).
- **Do detectors now flag them?** Vendors say yes: Turnitin since August 2025, GPTZero since November 2024 (beta), and Grammarly flags its own humanizer's output. Independent evidence is **mixed**. Karr et al. 2026 found more than 96% evasion against GPTZero and Pangram, while NBER 2025 found Pangram robust. I found no independent test of Turnitin's bypasser detection. Since August 2026, Turnitin does not show humanizer use as a separate label; it simply counts toward the "AI-generated" percentage.

---

## What "below 20%" means on each tool

| Tool | What the number is | Is 20% a defined line? |
|---|---|---|
| **Turnitin** | Share of qualifying prose sentences labeled AI | **Yes.** It is Turnitin's own display threshold. 1–19% shows only as `*%` with no highlights, 0% shows as 0%, and 20% or more shows the number and highlights. The <1% false-positive claim only covers documents scoring ≥20%. The student usually cannot see the score or run the check beforehand. |
| **Grammarly** | Estimated share of the scanned text that "appears AI-generated" | No published threshold. Grammarly says its score may not match Turnitin's. |
| **GPTZero** | **Probability** that the document is AI, plus separate mixed and human probabilities and a confidence level | No. "15% AI" can still come out as "Mixed". Read the label and confidence, not just the number. |

So a score under 20% on Grammarly or GPTZero tells you **nothing reliable** about Turnitin's score. The tools measure different things, use different models, and disagree with each other (Grammarly says so itself). Turnitin also says its model is not built on "perplexity" or "burstiness" rules ([FAQ](https://guides.turnitin.com/hc/en-us/articles/28477544839821-Turnitin-s-AI-writing-detection-capabilities-FAQs)).

**Implications for the skill.**
- Do not promise any score.
- Do not imitate humanizers. Injected typos and odd synonyms hurt the grade, and vendors train detectors on exactly those traces.
- Turnitin targets Claude output by name.
- The best protection against a false accusation is evidence of the writing process (Google Docs history, Turnitin Clarity playback) and disclosing AI use as the school's policy requires. Every vendor, and every university above, says a detector score should not be the only evidence.

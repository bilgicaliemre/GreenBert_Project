# Target venues for the anti-AI writing skill paper

Researched 2026-10-20 from official pages (raw copies in `research/venues/raw/`, PDFs in `raw/pdf/`).
The author is a high-school first author in Turkey (SEV American College), applying to US universities in the 2026-27 cycle.
The paper covers an evidence-based prompt-level "anti-AI writing" skill, with four parts: writing quality (blind LLM judges plus an optional small human rater study), factual fidelity (fabricated claims), detectability by open-source detectors, and a finding that detectors flag many human-written admitted college essays and top-scored student essays written before 2022.

Status labels: **VERIFIED** means I read the official page or PDF myself today. **SEARCH-ONLY** means the official page blocked fetching, so the text comes from search-engine snippets of that page. **UNVERIFIED** means the information comes only from secondary sources or could not be checked.

---

## 1. Recommendation (read this first)

### Primary target: NAACL 2027 Student Research Workshop (SRW), long paper, archival
- **Why it fits.** The SRW homepage names high-school students as eligible. It is peer reviewed (double blind, OpenReview), and accepted archival papers go into the ACL Anthology, which is the main record for NLP research. The topic is in scope ("Ethics, responsible NLP, safety"; "Interpretability, analysis, and evaluation of NLP models"; "Sentiment analysis, stylistic analysis ... and human-centered NLP").
- **Timing works for admissions.** You can request a mentor now (deadline Nov 16, 2026). The paper deadline is **Jan 11, 2027** and the decision comes **Mar 8, 2027**. That is before most Regular Decision results come out in late March, so an acceptance can go to colleges as an update letter. In the Jan 1 RD applications the paper can be listed as "in preparation / to be submitted to NAACL 2027 SRW". After submission it can be listed as "under review".
- **The conference is in the US.** NAACL 2027 is in San Francisco, June 1-5, 2027, so the poster is presented at a major US NLP conference.
- **The format carries over.** The ACL template is the same for every fallback below (ACL 2027 SRW, NAACL and ACL workshops, ARR), so a rejected paper can be sent elsewhere without reformatting.

### Secondary target: ACL 2027 Student Research Workshop (Kyoto, Aug 17-22, 2027)
- Same ACL template, same eligibility wording in 2026, and the same kind of review. Use it as the **fallback if NAACL SRW rejects**. Rejected papers can be resubmitted with reviewer feedback addressed. The "except for another SRW" bar applies to *accepted* non-archival papers (NAACL SRW FAQ: "Can I submit a non-archival accepted paper to another venue later? Yes, except for another SRW"), so a rejected paper can go to ACL 2027 SRW either way. Still choose archival at NAACL: only archival papers go into the proceedings. The 2027 SRW call is **not out yet** (acl2027 calls page says "Coming soon!"). The 2026 edition's direct deadline was Mar 18, 2026, so expect roughly Mar to Apr 2027. This comes after admission decisions, so its value is for the research record and summer/college research, not for this admissions round.
- Alternative secondary: a topic-matched **NAACL 2027 workshop**. First calls go out from Oct 26, 2026, the direct paper deadline is **Feb 5, 2027**, and notification is Mar 26, 2027 (official ACL joint workshop timeline). Workshop calls set their own dual-submission rules. If one allows it and the workshop topic fits better (for example an AI-text detection, education, or human-centered workshop), submit there too and declare it on both forms. No 2027 workshop list had been published as of today.

### Do in parallel
- **arXiv cs.CL preprint** soon after the Jan 11 submission. It gives a public, dated link for applications and portfolios. Since Jan 21, 2026 a new author needs a personal endorsement (see Section 6). The simplest route is to have an adult co-author who already has arXiv endorsement in cs submit the paper. Check the detector-disclosure step (Section 2.4) first.
- **Regeneron STS**: apply **only if Ali is a US citizen** (the international route requires US citizenship). The deadline is Nov 5, 2026, and the report must be written with no generative AI at all. STS is the most valuable item for admissions by a wide margin, and the Top 300 list comes out Jan 7, 2027, in the RD window. If he is not a US citizen, skip it.

### Not recommended for this paper
- **JEI**: the topic is excluded ("Computer science" and "Linguistics" are on its "Topics JEI does NOT accept" list, and "JEI does not accept manuscripts that just introduce, optimize, or compare an invention, a method, a machine/deep learning or AI algorithm"), and it forbids AI in writing.
- **AAAI-27 Student Abstract**: the deadline (Sep 28, 2026) has passed, and the call says "This track is reserved for undergraduate and graduate students." Accepted abstracts are also non-archival.
- **EACL 2027 SRW**: research-paper first authors "MUST be a student (undergraduate or graduate)". That wording leaves out high school, so ask the chairs before trying.
- **CJSJ**: the 2026-27 cycle is closed (Sep 30, 2026) and the next deadline falls after this admissions cycle. The 2-3 page format is too short for this study.
- **NHSJS**: possible, but its AI rule is the strictest of all (any AI rephrasing is banned and manuscripts are screened by software), and it charges fees. It is worth less than an ACL Anthology paper.
- **Curieux Review / Journal of Student Research**: pay-to-publish with student or light editorial review. These count for little with admissions readers.

### Exact format to write in
**Official ACL LaTeX template** (`acl-org/acl-style-files`; Overleaf: "Association for Computational Linguistics (ACL) Conference", https://www.overleaf.com/latex/templates/association-for-computational-linguistics-acl-conference/jvxskxpnznfj).
- Use `\usepackage[review]{acl}` for submission (it gives an anonymous version with line numbers). Switch to `\usepackage{acl}` (final) for camera-ready.
- Pages are A4, two columns, in the ACL font. **Long paper: max 8 pages of content.** References, appendices, the required **Limitations** section, and the optional **Ethical Considerations** section are all unlimited and do not count. An accepted paper gets 9 pages.
- A `\section*{Limitations}` placed after the conclusion and before the references is **mandatory**. The ACL 2026 SRW call and the ARR CFP both say "Papers without a limitations section will be desk rejected."
- Anonymize everything: no names, school, acknowledgments, or GitHub links that identify you. Self-citations go in the third person. Code and data go in the anonymous OpenReview upload fields.
- Proof of student status (student ID, enrollment letter, or transcript) is due **at submission, Jan 11, 2027**. Upload it separately and keep it out of the PDF.
- AI-use disclosure: under ARR/ACL policy, use of AI for writing or coding "must be disclosed", with "details ... in the Acknowledgements section" (camera-ready), and the NAACL SRW can desk reject "undisclosed generated material". See Section 2.

Suggested 8-page layout:

| Section | Pages |
|---|---|
| Abstract | about 200 words |
| 1 Introduction | 1 |
| 2 Related Work | 0.75 (detectors and their false positives on human and non-native text; humanizer/paraphrase attacks; LLM-as-judge; style prompting) |
| 3 The Skill (design, evidence base) | 1 |
| 4 Experimental Setup (models, tasks, judges, detectors, essay corpora) | 1.5 |
| 5 Results (quality, fidelity, detectability) | 2.25 |
| 6 Detectors on Human Essays (admitted essays; pre-2022 top-scored essays) | 0.75 |
| 7 Discussion and Conclusion | 0.75 |
| Limitations; Ethical Considerations | unlimited |
| References; Appendix (full skill text, prompts, judge rubric, per-detector tables) | unlimited |

---

## 2. Rules that shape how the paper must be written

### 2.1 The "Claude drafts a framework, Ali rewrites it" plan vs. each venue's AI rule
The plan is to use the Claude-written paper as a framework that Ali then breaks down and rewrites himself. That is **acceptable with disclosure at ACL venues (ACL discourages it) and forbidden at STS, ISEF, JEI and NHSJS.**

| Venue | Rule (quoted) | Is the plan OK? |
|---|---|---|
| ARR / all *ACL venues (aclrollingreview.org/cfp) | "Generally, generative AI tools do not qualify for authorship. Their use for writing or coding, as well as its scope, must be disclosed in the Responsible NLP Checklist. Details should be included in the Acknowledgements section." For case (f), "New ideas + new text. ACL does not consider a generative model to be an entity that can fulfill the requirements of co-authorship." The original 2023 ACL policy adds: "we would discourage such use in ACL submissions." | Yes, if the final text is Ali's own and AI use is disclosed. |
| NAACL 2027 SRW (naacl27-srw.github.io) | "Submissions may be desk rejected if AI tools are used in a way that fabricates results, obscures authorship, violates anonymity, introduces undisclosed generated material, creates false citations, or otherwise conflicts with ACL/NAACL publication ethics." Also: "Authors may use writing, coding, or analysis tools only when the use is responsible, accurate, and disclosed where required by the final policy. AI assistance never transfers responsibility away from the authors." | Yes, with disclosure and verified citations. |
| EACL 2027 (2027.eacl.org/calls/papers) | "There is growing concern ... including ... submissions with hallucinated citations, and entirely AI-generated papers (AI writing assistance is permitted). ... Such submissions may be desk rejected, and all authors involved in the submission may be ineligible to commit their paper(s) to EACL 2027 and EACL 2028." | The final paper must not be AI-generated. |
| Regeneron STS 2027 (Official Rules PDF, Research Report Guidelines PDF) | "The Student Researcher is required to write the paper without the use of generative AI (ChatGPT or other programs)." AI chart: "Use generative AI to initially write the research plan, abstract, paper or poster: No ... Never acceptable." Certification: "I certify that I have not used AI tools, like ChatGPT, to construct the research report". | **No.** The STS report must be written from scratch, without the framework. |
| Regeneron ISEF 2027 (International Rules 2026-27) | "A student may not use generative AI to write the research plan, abstract, poster or to create citations". The AI Usage Disclosure form requires "the AI Prompt Log". | **No** for the abstract, poster, and research plan. |
| JEI | "We therefore cannot ethically publish manuscripts that use AI in the following ways: ... Writing text or making revisions (exception: ... proofreading minor spelling and grammatical mistakes after you write your text ...)" | **No** (and the topic is out of scope anyway). |
| NHSJS (page modified 2026-10-12) | "AI may not draft, paraphrase, expand, or rewrite your prose, including passages you subsequently edit." "Before publication, we screen every manuscript we accept, using both human review and software checks." | **No.** |
| CJSJ | Follows Science's policy, quoted on its Guidelines page: "Authors who use AI-assisted technologies as components of their research study or as aids in the writing or presentation of the manuscript should note this in the cover letter and in the acknowledgments section of the manuscript. Detailed information should be provided in the methods section: The full prompt used in the production of the work, as well as the AI tool and its version, should be disclosed." CJSJ adds: "if you did utilize AI in writing any portion of your paper, you must inform us. If we find the use of uncited AI in your paper, we have the right to redact it from the publication." | Yes, with disclosure (including the full prompts and tool version). |
| arXiv | Authors must "report in their work any significant use of sophisticated tools ... we now include in particular text-to-text generative AI"; "generative AI language tools should not be listed as an author". | Yes, with disclosure. |

**Practical consequence.** Use one NAACL SRW paper (Ali's rewrite, with AI use disclosed). Any STS, ISEF, or TÜBİTAK write-up must be a separate document that Ali writes himself from his notes. Keep a prompt log either way, since ISEF requires one.

### 2.2 Citations
Every venue punishes fabricated references. EACL names "hallucinated citations", STS disqualifies on "Discovery of a fake reference", and ISEF says AI "is known to hallucinate and falsify references". Check every reference against the ACL Anthology, arXiv, or the DOI before submitting.

### 2.3 Human data
NAACL SRW author policy: "If a submission describes work involving human participants ... the submission should document institutional review of the work as well as informed consent and compensation procedures". For "found" data such as essays taken from the web: "any necessary permissions to use and/or release the data should be documented."
- For the human rater study, get an IRB or school ethics approval and signed consent forms, or present the human study as small and informal and describe it honestly in Ethical Considerations.
- For the college essays, release only IDs/URLs and scores, not the essay text, unless the license permits release.

### 2.4 ACL Co-ordinated Disclosure Policy (detector evasion)
This comes from the ACL 2026 SRW author guidelines and the ACL publication ethics policy:
> "If your paper describes methods for eliciting harmful or unintended behavior from models or technologies (e.g., exposing vulnerabilities, jailbreaks, or misuse scenarios), you must follow ACL's Co-ordinated Disclosure Policy. This requires authors to: Contact the developers of the affected system(s) before submission. Wait at least 30 days after initial contact before publicly disclosing the vulnerability (e.g., through preprints or publications). Document the disclosure process in the Ethical Considerations section ... This policy only applies to cases involving intentional adversarial techniques."

A skill that lowers detector scores could be read as an intentional technique for evading detectors. To be safe, **email the maintainers of each open-source detector evaluated by about Dec 1, 2026.** That covers the Jan 11 submission and allows an arXiv preprint in early January. Record who was contacted, how, and when in Ethical Considerations. Present detectability as a measurement, not the goal: the main contribution is quality and fidelity, and the human-essay false-positive finding is a fairness result.

---

## 3. Peer-reviewed NLP venues: details

### 3.1 NAACL 2027 SRW (PRIMARY): VERIFIED
Sources: https://2027.naacl.org/calls/srw/ and https://naacl27-srw.github.io/ (fetched 2026-10-20; first CFP dated Sep 7, 2026).
- **Eligibility (quotes):** "We welcome students at multiple stages, including high school, undergraduate, MSc/MA, and PhD students." "Research Papers: ... The first author must be a current student or must have completed the work while a student." FAQ ("Do all authors have to be students?"): "No. The first author must be a student, or must have completed the work while a student. Other authors may be non-students."
- **Format:** ACL template. Long papers have 8 pages of content (9 on acceptance) and short papers 4 (5 on acceptance). References and appendices are unlimited. Archival or non-archival ("submissions marked as non-archival cannot be changed to archival after acceptance").
- **Dates (AoE):** mentorship request Nov 16, 2026; matching Nov 23, 2026; **paper plus student-status proof Jan 11, 2027 (OpenReview)**; notification Mar 8, 2027; camera-ready Mar 15, 2027; conference Jun 1-5, 2027 (San Francisco).
- **Review:** double blind. "Direct only" (the call says "An ARR commitment track is not planned"). The ACL 2026 SRW gave each paper "a minimum of three reviews".
- **Mentorship:** "A complete paper is not required to request a mentor." Mentoring is not anonymous and does not affect acceptance. **Action: apply by Nov 16, 2026.**
- **AI policy:** see the Section 2.1 table.
- **Selectivity (for comparison):** the ACL 2026 SRW received 379 direct and 22 ARR submissions (its news feed). The accepted-papers page lists about 109 archival and 21 non-archival papers. That is roughly **32% accepted** (my count from the page, approximate).
- **Honest prestige:** SRW papers are peer reviewed and archived in the ACL Anthology under the main conference's name ("NAACL 2027 SRW Proceedings"). For a high-school applicant, a first-author paper here is a rare, checkable, and serious signal. Faculty readers in CS and linguistics will know what it is. It is less prestigious than a main-conference or Findings paper, so always describe it accurately as a "Student Research Workshop paper", never as a "NAACL paper".

### 3.2 ACL 2027 SRW (SECONDARY): partly announced
- ACL 2027 is in Kyoto, Japan, Aug 17-22, 2027 (2027.aclweb.org homepage). The ARR deadline for the main conference is Jan 4, 2027. The SRW call is "Coming soon!" (checked 2026-10-20).
- The 2026 precedent (VERIFIED, acl2026-srw.github.io/cfp): "the first author MUST BE a current student (high school, graduate, or undergraduate)". The workshop's goal covers "highschool, undergraduate, MSc/MA, junior and senior PhD students". The 2026 edition had a pre-submission mentorship deadline of Feb 4, 2026 and a direct deadline of Mar 18, 2026. Proof of student status was due at camera-ready. Review was double blind with at least 3 reviews. An ARR commitment route existed (Apr 15, 2026). A Limitations section was required. FAQ: "Only the first author is required to be a student".
- Unlike NAACL SRW, the 2026 ACL SRW accepted ARR commitments. **Stretch strategy:** submit to ARR for the Jan 4, 2027 deadline aiming at ACL 2027 main or Findings. If the reviews are good but the paper does not get in, commit them to the ACL 2027 SRW, if the 2027 SRW keeps that route. This competes on deadline with NAACL SRW (Jan 11). ARR's dual-submission rules mean the same paper cannot be in ARR and NAACL SRW at once, so pick one.

### 3.3 EACL 2027 SRW (Athens, Mar 9-14, 2027): VERIFIED, eligibility unclear
- "Research Papers: ... For these papers, the first author MUST be a student (undergraduate or graduate)." The audience is listed as "undergraduate, MSc/MA, junior and senior PhD students", with no mention of high school.
- Dates: mentorship Nov 6, 2026; direct submission Dec 15, 2026; notification Jan 5, 2027. Long papers are 8 pages. The call page does not mention a proof-of-student-status requirement; only the travel grants say "Applicants must be full-time students."
- The EACL integrity policy applies (see Section 2.1).
- **Verdict:** email eacl2027-srw@googlegroups.com before considering it. NAACL is the better fit anyway.

### 3.4 ACL-family workshops: 2027 lineup not yet published
The official joint call (aclweb.org portal, Jul 20, 2026) set workshop proposals due Sep 4, 2026, with notification Oct 2, 2026. Accepted workshops are posting their first calls now. Paper deadlines for 2027 workshops (official tentative timeline):

| Conference | Direct paper deadline | Notification |
|---|---|---|
| EACL 2027 workshops | Dec 15, 2026 | Jan 5, 2027 |
| COLING 2027 workshops (Macau, May 9-14, 2027) | Jan 5, 2027 | Feb 6, 2027 |
| NAACL 2027 workshops (first calls from Oct 26, 2026) | **Feb 5, 2027** | Mar 26, 2027 |
| ACL 2027 workshops | Apr 25, 2027 | May 22, 2027 |

Workshops to watch (check after each first call):
- **GenAIDetect (Workshop on Detecting AI Generated Content).** Only one edition so far: COLING 2025, Abu Dhabi, Jan 19, 2025, with 46 papers in the Anthology. It ran a shared task "Task 2: AI vs. Human - Academic Essay Authenticity Challenge", which is directly relevant. **No 2026 or 2027 edition was found** (the ACL Anthology venue page lists only `2025.genaidetect-1`). If a second edition appears at COLING or NAACL 2027, it is the ideal topical home.
- **BEA (Innovative Use of NLP for Building Educational Applications).** Long-running: BEA 2026 was the 21st edition, and the Anthology has BEA volumes going back to 2003. BEA 2026 was held with ACL 2026 (Jul 3-4, 2026, deadline Mar 30, 2026) and its topics included "exploring the role and impact of generative AI in education" and "automated evaluation of written ... responses". There is no 2027 call yet. If it is placed at ACL 2027 again, expect a deadline around Mar to Apr 2027. The college-essay finding fits here. Open to any author, with no student requirement.
- **In2Writing (Intelligent and Interactive Writing Assistants).** Fourth edition at NAACL 2025; it alternates between NLP and HCI venues. No 2026 or 2027 call found.
- **LUHME (Language Understanding in the Human-Machine Era).** Its 3rd edition was at EMNLP 2026 (deadline Jul 15, 2026, passed). Watch for a 2027 edition.
- **GEM / EvalEval** (generation evaluation) were held at ACL 2026. They are relevant to the LLM-judge methodology.
- **Honest prestige:** archival workshop papers appear in the ACL Anthology. BEA is well established. Overall a workshop is about as prestigious as the SRW, but it competes with established researchers rather than students.

### 3.5 AAAI-27 Student Abstract and Poster Program: VERIFIED (page fetched in full on the 2026-10-20 re-check)
- "This track is reserved for undergraduate and graduate students. If you do not meet this eligibility requirement, please do not apply." High school is not eligible.
- "Abstracts must be no longer than 2 pages including references, and formatted in AAAI two-column, camera-ready style." "Accepted student abstracts are non-archival." Presenters must attend in person.
- Deadline **Sep 28, 2026 (passed)**; notification Nov 13, 2026; conference Feb 16-23, 2027, Montréal.
- **Verdict:** not usable this cycle, and not eligible.

### 3.6 NeurIPS High School Projects track
- Only the 2024 edition was found (neurips.cc/Conferences/2024/CallforHighSchoolProjects). The 2025 and 2026 URLs for that call return 404. The NeurIPS 2026 calls list has no high-school call. Its "Call for Educational Resources" is for teaching materials, not student research.
- **Verdict:** not available.

---

## 4. High-school competitions

### 4.1 Regeneron Science Talent Search 2027: VERIFIED (2027 Official Rules PDF, Research Report Guidelines PDF, AI-Usage-Chart PDF)
- **Eligibility (citizenship, quote):** applicants must be "(a) A student (of any citizenship) who is enrolled in and attending secondary school AND who maintains full-time residence in the United States ... OR (b) A United States citizen enrolled in their final year of secondary school ... attending a: i. Department of Defense Dependents School or an accredited overseas American or International School, OR ii. foreign school as an exchange student, OR iii. foreign school because their parent(s)/guardian(s) are temporarily working and living abroad. (c) Proof of both citizenship and school accreditation is required for 2b". Applicants must also be in their final year and submit an individual project.
  - **A non-US citizen living in Turkey is ineligible.** A US citizen at an accredited school abroad is eligible.
- **Dates:** application **Jun 1 - Nov 5, 2026, 8pm ET**; Top 300 Scholars Jan 7, 2027; Top 40 Finalists Jan 21, 2027; Finals Week Mar 11-17, 2027.
- **Format:** research report of at most 20 pages (title page, abstract, and bibliography not counted; appendices count). Font at least Times New Roman 11pt, 1.5 line spacing, 1-inch margins, "Do not use multiple columns", PDF of at most 4MB. First person "I" is allowed. "Research proposals, investigations not yet completed, literature reviews and essays are not eligible".
- **Review:** "evaluated by three or more doctoral scientists, mathematicians, and/or engineers"; "The originality of each entry is checked using plagiarism monitoring software."
- **AI policy:** see Section 2.1. Also: "Students may not use generative Artificial Intelligence (AI) to write Regeneron STS application questions, draft the Research Report or generate citations. ... Use of AI tools for student research projects is permitted, and should be disclosed".
- **Human participants:** rater studies need IRB pre-approval (Official Rules "Human Participant Rules"; IRB form).
- **Honest prestige:** this is the top US pre-college research honor. Even Top 300 Scholar (about 300 of about 2,600 entrants) is a strong signal, and the results land in the RD window. **Only if eligible.** The deadline is in 16 days and the report must be self-written.

### 4.2 Regeneron ISEF 2027 (Los Angeles, May 8-14, 2027): VERIFIED rules; Turkey route partly unverified
- **Eligibility (2027 International Rules):** a student "must be selected by an ISEF-affiliated fair" and must "be in grades 9-12 or equivalent" and "not have reached age 20 on or before May 1 preceding ISEF". The project "may not include research performed before January 2026". Students "must have a Research Plan" completed "before experimentation", with SRC approval, and IRB approval for human participants.
- **Turkey route:** TÜBİTAK 2204-A Lise Öğrencileri Araştırma Projeleri Yarışması. The 2027 call (announced on the TÜBİTAK page on Sep 23, 2026) takes applications **Sep 23, 2026 - Jan 4, 2027, 17:30**. Rule 6.2.4: projects for "Uluslararası proje yarışmaları" (ISEF and EUCYS) are chosen by a separate jury from the projects that place 1st, 2nd, or 3rd at the national final.
  - TÜBİTAK rules to watch: no featuring of "herhangi bir kurum, kuruluş, firma, ticari ürün ya da marka" (any company, product, or brand) in the title or report, which is a problem for a paper that names specific LLMs and detectors. Projects submitted earlier to another project competition are eliminated. Projects must be finished at application.
  - **UNVERIFIED:** whether a Jan 2027 TÜBİTAK entry can reach ISEF in May 2027. The 2026 national final was Apr 27-30, 2026, about 10 days before ISEF 2026 (May 9-15), and I found no official statement of which year's projects TÜBİTAK sends. Ask TÜBİTAK BİDEB.
- **AI policy:** see Section 2.1. A Prompt Log is required.
- **Honest prestige:** an ISEF Grand Award is top tier, and reaching ISEF from TÜBİTAK's national competition is itself very competitive. For **this** admissions cycle the timing is poor: results arrive in Apr-May 2027, after decisions. The research also has to be documented as a pre-approved research plan, which a study that has already run does not have.

---

## 5. High-school journals

### 5.1 Columbia Junior Science Journal (CJSJ): VERIFIED (columbiajuniorsciencejournal.org)
- **Eligibility:** "original research papers OR ... review articles from high school students". Fields: "natural sciences, physical sciences, engineering, and social sciences".
- **Format:** original research is "at least two pages and up to three pages" (figures and citations excluded), on the CJSJ .docx "Research Paper Template", with figures also in .ppt and a signed Permission to Publish form.
- **Cycle:** the 2026-27 cycle opened Jun 2, 2026 and closed **Sep 30, 2026** ("now closed"). Quarterfinalists Oct 30, semifinalists Nov 20, finalists Dec 11, 2026; publication Mar 26, 2027. The next cycle should open around June 2027, after admissions.
- **Review:** multi-round competition judged by Columbia undergraduate editors. It is "Supported by the Columbia Undergraduate Science Journal (CUSJ)".
- **AI policy:** see Section 2.1 (Science policy; disclose or the AI text gets redacted).
- **Honest prestige:** free and selective (the 2025-26 volume names about 10 authors). The Columbia branding helps, but the reviewers are students. Moderate value. It does not fit this paper this cycle.

### 5.2 Journal of Emerging Investigators (JEI): VERIFIED (emerginginvestigators.org)
- **Eligibility:** "All middle- and high-school students, aged 13 or older"; an adult senior author is required and must be the one who submits; submission must come "prior to the student author's enrollment in university"; $49 fee.
- **Scope:** "Topics JEI does NOT accept: ... Linguistics, Computer science"; "JEI does not accept manuscripts that just introduce, optimize, or compare an invention, a method, a machine/deep learning or AI algorithm". **This paper is out of scope.**
- **AI policy:** see Section 2.1. JEI also bans AI for "Data mining" and "Conducting statistical analysis".
- **Honest prestige:** among the most respected high-school journals (it mentors authors through review with graduate students), but not usable here.

### 5.3 National High School Journal of Science (NHSJS): VERIFIED (nhsjs.com)
- Targets high-school students. Original research must have "five or more figures or tables". The manuscript is at most 20 pages, 12pt, single spaced, Word or LaTeX, with two citation-format versions. Review takes about 8 weeks (a $280 "expedited" option exists), by editorial staff, then 1-2 reviewers (graduate students, postdocs, scientists), then a Scientist Advisory Board member. There is an article processing charge (APC); the amount was not shown on the pages checked.
- **AI policy (page modified 2026-10-12):** the strictest found. See Section 2.1. "Translation tools such as Google Translate and DeepL are not acceptable". Disclosure goes "after the Acknowledgements and before the References".
- **Honest prestige:** mid-tier. It is paid, so it carries limited weight. Its software AI screening is ironic given this paper's finding that detectors flag human essays.

### 5.4 The Curieux Review (successor to Curieux Academic Journal): VERIFIED (curieuxreview.com/submissions)
- "We accept submissions from middle school, high school, and undergraduate students only". At most 20 pages (1.15 spacing, TNR 12), MLA, submitted as a Google Doc link. "two of our editors separately review each article". The publication fee is "250" for fast-track or "200" for seasonal review, charged on acceptance. Rolling deadline.
- **AI policy:** none stated on the submissions page.
- **Honest prestige:** low (student editors, pay to publish).

### 5.5 Journal of Student Research, High School Edition (JSR): UNVERIFIED (jsr.org returned HTTP 522 all day)
- Secondary sources only: the first author must be a high-school student at an accredited institution, with teacher or advisor guidance. There is a $50 pre-review fee, and the reported post-review fees conflict ($99, $200, or $299).
- **AI policy: could not be verified.**
- **Honest prestige:** low (widely seen as pay-to-publish).

---

## 6. arXiv (cs.CL): VERIFIED (info.arxiv.org/help/endorsement.html; blog.arxiv.org, Jan 21, 2026)
- **New rule since Jan 21, 2026:** "arXiv will no longer accept institutional email addresses ... as the sole qualifier of endorsement for new authors." Path 1 requires "both 1) an institutional email address from an academic/research institution and 2) previous authorship on an existing paper which has been accepted to the arXiv 'endorsement domain'". Path 2 is "seeking personal endorsement directly from an established arXiv author in the same endorsement domain." "arXiv staff cannot waive endorsement requirements".
- **For Ali:** he will not meet Path 1 (no prior arXiv paper), so he needs a personal endorser in the **cs** domain, ideally someone who knows him and his work ("you should know the person that you endorse or you should see the paper"). Alternatively, an adult co-author with cs endorsement submits the paper, since only the submitter needs endorsement.
- **Content rule:** since Oct 31, 2025, review and position papers in arXiv CS need prior peer review. This paper is original empirical research, so the rule does not apply.
- **AI policy:** see Section 2.1.
- **Anonymity:** ARR has had no anonymity period since Feb 15, 2024 ("authors are free to post and discuss non-anonymous preprints at any time"). NAACL SRW follows the main-conference rules, so a preprint during review is allowed. Respect the 30-day coordinated-disclosure wait (Section 2.4).
- **Honest prestige:** not peer reviewed and neutral for admissions on its own, but it gives a public, timestamped, citable link to list while the SRW paper is under review.

---

## 7. Timeline against the 2026-27 admissions cycle

| Date | Action |
|---|---|
| Oct 20 - Nov 5, 2026 | Decide on STS (only if a US citizen; the report must be self-written). |
| **by Nov 16, 2026** | **Request a NAACL SRW mentor** (an idea or draft is enough). |
| ~Dec 1, 2026 | Email open-source detector maintainers (ACL coordinated disclosure). Line up an arXiv endorser or adult co-author. |
| Jan 1-5, 2027 | RD applications: list the paper as "manuscript in preparation for NAACL 2027 SRW" (or "under review" if already submitted). TÜBİTAK 2204-A deadline Jan 4 (optional; ISEF timing unverified). |
| **Jan 11, 2027** | **Submit to NAACL 2027 SRW** (long paper, archival, with student-status proof). |
| mid-Jan 2027 | arXiv cs.CL preprint (if the 30-day disclosure window has passed). Send a short update to colleges with the link. |
| Feb 5, 2027 | Optional: a matching NAACL 2027 workshop, if its dual-submission rules allow. |
| **Mar 8, 2027** | NAACL SRW decision. Send an update letter right away (before late-March RD releases). |
| Mar-Apr 2027 | If rejected: revise and send to ACL 2027 SRW or BEA 2027 (calls not out yet). |
| Jun 1-5, 2027 | Present in San Francisco if accepted. |

---

## 8. Open questions and unverified items
- ACL 2027 SRW and all 2027 workshop calls (GenAIDetect, BEA, In2Writing) were not yet published on 2026-10-20.
- JSR's AI policy and fees: jsr.org was down (HTTP 522).
- The NHSJS APC amount was not on the pages checked.
- Whether TÜBİTAK 2204-A 2027 winners go to ISEF 2027 or ISEF 2028.
- Ali's citizenship (decides STS eligibility).
- Whether NAACL SRW's OpenReview form will ask for the ARR Responsible NLP checklist. ARR requires it; the SRW page does not say. Prepare the answers anyway, especially "E1. If you used any AI assistants, did you include information about your use?"

## 9. Source list (all fetched 2026-10-20 unless noted)
- NAACL 2027 SRW: https://2027.naacl.org/calls/srw/ ; https://naacl27-srw.github.io/ ; https://naacl27-srw.github.io/author-guidelines.html
- ACL 2026 SRW: https://2026.aclweb.org/calls/student_research_workshop/ ; https://acl2026-srw.github.io/cfp ; /faq ; /author ; /accepted_papers
- ACL 2027: https://2027.aclweb.org/ ; https://2027.aclweb.org/calls/meetings/ ("Coming soon!")
- EACL 2027 SRW: https://2027.eacl.org/calls/srw/ ; EACL 2027 CFP (integrity policy): https://2027.eacl.org/calls/papers/
- Joint 2027 workshop call and timelines: https://www.aclweb.org/portal/content/joint-call-workshops-proposals-2027
- ARR CFP (AI writing policy, template, limitations): https://aclrollingreview.org/cfp ; checklist: https://aclrollingreview.org/responsibleNLPresearch/ ; ACL 2023 AI writing policy: https://2023.aclweb.org/blog/ACL-2023-policy/
- ACL style files: https://github.com/acl-org/acl-style-files (README, acl_latex.tex)
- GenAIDetect 2025: https://genai-content-detection.gitlab.io/ ; Anthology venue: https://aclanthology.org/venues/genaidetect/
- BEA 2026: https://sig-edu.org/bea/2026 ; Anthology venue: https://aclanthology.org/venues/bea/
- AAAI-27 Student Abstract (fetched in full on the re-check): https://aaai.org/conference/aaai/aaai-27/student-abstract-and-poster-program-call-for-proposals/
- Regeneron STS: https://www.societyforscience.org/regeneron-sts/ ; 2027 PDFs at https://sspcdn.blob.core.windows.net/files/Documents/SEP/STS/2027/Application/ (Official-Rules.pdf, Research-Report-Guidelines.pdf, AI-Usage-Chart.pdf)
- Regeneron ISEF: https://www.societyforscience.org/isef/ ; 2027 rules: https://sspcdn.blob.core.windows.net/files/Documents/SEP/ISEF/2027/Rules/Book.pdf ; changes: .../2027/Rules/FINAL-Rule-Modifications-for-2026-27.pdf ; dates (May 8-14, 2027, LA) per https://www.societyforscience.org/isef/grand-award/ ("Regeneron ISEF 2027 will be held in Los Angeles, California from May 8-14")
- TÜBİTAK 2204-A: https://tubitak.gov.tr/tr/yarismalar/2204-lise-ogrencileri-arastirma-projeleri-yarismasi ; call text PDF: https://tubitak.gov.tr/sites/default/files/2026-09/Ek-1b_2204_A_cagri_metni_2026-2027_17.08.2026_onaya_sunulan_v2.pdf
- CJSJ: https://columbiajuniorsciencejournal.org/guidelines (copies saved earlier in research/access/verify/)
- JEI: https://emerginginvestigators.org/submissions/academic-honesty-and-ai ; /author-eligibility ; /hypothesis-driven-research ; $49 fee: /submissions/pay-and-submit/pay (the /faq URL returned 404 on the re-check)
- NHSJS: https://nhsjs.com/ai-usage-policy/ ; /submission-guidelines/ ; /about/peer-review-process/ ; /submit-your-work/submission-types/
- Curieux: https://www.curieuxacademicjournal.com/submissions (redirect notice) ; https://www.curieuxreview.com/submissions
- arXiv: https://info.arxiv.org/help/endorsement.html ; https://blog.arxiv.org/2026/01/21/attention-authors-updated-endorsement-policy ; https://info.arxiv.org/help/moderation/index.html ; https://blog.arxiv.org/2025/10/31/attention-authors-updated-practice-for-review-articles-and-position-papers-in-arxiv-cs-category/

---

## 10. Verification (re-check on 2026-10-20)

I downloaded fresh copies of the cited official pages and PDFs and compared every eligibility rule, deadline, and AI-policy quote above against them. The fresh copies are in `venue_verify_dl/` (PDFs in `venue_verify_dl/pdf/`), next to `research/`.

### Corrections made in this file
1. **NAACL 2027 SRW FAQ quote (3.1).** The file quoted "Only the first author must be a student ...", but that wording is from the ACL 2026 SRW FAQ. Replaced it with the NAACL FAQ's actual words: "No. The first author must be a student, or must have completed the work while a student. Other authors may be non-students."
2. **Non-archival rule (1, secondary target).** The file said choosing non-archival at NAACL would block the ACL 2027 SRW fallback after a rejection. The NAACL FAQ applies the "except for another SRW" bar to *accepted* non-archival papers only. Rewrote the sentence; the advice to choose archival stays.
3. **EACL 2027 SRW (3.3).** The file said "proof of student status" is required. Neither the current call page nor the earlier saved copy says that. Corrected.
4. **AAAI-27 Student Abstract (1 and 3.5).** The page downloaded in full this time, so the entry moves from SEARCH-ONLY to VERIFIED. The quoted sentence "open to all students at the Undergraduate, Masters, and Doctoral levels" is not on the page. The page says "This track is reserved for undergraduate and graduate students." Also added: accepted abstracts are non-archival and must be presented in person. Removed the matching item from Section 8.
5. **JEI scope quote (1).** "Manuscripts that only introduce ..." was a paraphrase. Replaced with the exact text: "JEI does not accept manuscripts that just introduce, optimize, or compare an invention, a method, a machine/deep learning or AI algorithm".
6. **Limitations section (1, format).** The file said ACL 2026 SRW "desk-rejected papers without it". That is a rule, not a reported event, so the sentence now quotes the rule: "Papers without a limitations section will be desk rejected" (ACL 2026 SRW call and ARR CFP).
7. **BEA (3.4).** The file said "editions 2020-2026 are in the Anthology". BEA 2026 was the 21st edition, and Anthology volumes go back to 2003. Corrected.
8. **NeurIPS (3.6).** The 2026 call is titled "Call for Educational Resources", not "Education Track". The 2025 and 2026 High School Projects URLs return 404. Corrected.
9. **TÜBİTAK 2204-A (4.2).** The 2026-27 call announcement on the TÜBİTAK page is dated 23.09.2026, not Sep 25. Corrected.
10. **Additions to the AI-policy table (2.1).** These are not errors, just missing details that matter for the plan. NAACL SRW: "Authors may use writing, coding, or analysis tools only when the use is responsible, accurate, and disclosed where required by the final policy." CJSJ (the Science policy it quotes): AI use goes in the cover letter and the acknowledgments, and "The full prompt used in the production of the work, as well as the AI tool and its version, should be disclosed."
11. **Sources (9).** The ISEF 2027 dates now cite the official Grand Award page instead of a search result. The JEI /faq URL returned 404, so the $49 fee now cites /submissions/pay-and-submit/pay.

### Checked and confirmed as written
- **NAACL 2027 SRW** (2027.naacl.org/calls/srw/, naacl27-srw.github.io, author-guidelines page). "including high school" eligibility. Mentorship Nov 16 and matching Nov 23, 2026. Paper and student-status proof due Jan 11, 2027 on OpenReview. Notification Mar 8, camera-ready Mar 15, 2027. Conference Jun 1-5, 2027 in San Francisco (also on the NAACL homepage). Long papers 8 pages (9 after acceptance), short papers 4 (5). Double blind. "An ARR commitment track is not planned." Non-archival cannot become archival. First CFP dated Sep 7, 2026. The AI desk-rejection quote, the human-subjects quote and the found-data quote are verbatim.
- **ACL 2026 SRW** (acl2026-srw.github.io). The "(high school, graduate, or undergraduate)" eligibility quote and the "highschool" goal statement are verbatim. Dates: mentorship Feb 4, direct submission Mar 18, ARR commitment Apr 15, 2026. Proof of student status at camera-ready. "Minimum of three reviews". FAQ: "Only the first author is required to be a student". The Co-ordinated Disclosure Policy text is verbatim. Selectivity recounted from the accepted-papers page: 109 archival + 21 non-archival = 130 accepted, against 379 direct + 22 ARR = 401 submissions, about 32%.
- **ACL 2027** (2027.aclweb.org). Kyoto, Aug 17-22, 2027. ARR deadline Jan 4, 2027. Both the Meetings and the Student Research Workshop call pages say "Coming soon!".
- **EACL 2027.** Athens, Mar 9-14, 2027. "the first author MUST be a student (undergraduate or graduate)". The audience list has no high school. Mentorship Nov 6, direct submission Dec 15, 2026, notification Jan 5, 2027. The integrity-policy quote is verbatim. (The SRW page itself prints the ARR commitment deadline as "December 22, 2027". The joint workshop call gives Dec 22, 2026, so the SRW page has a typo.)
- **Joint 2027 workshop call** (aclweb.org portal, posted Jul 20, 2026). Proposals due Sep 4, notification Oct 2, 2026. All four rows of the deadline table match: EACL Dec 15 / Jan 5; COLING (Macau, May 9-14) Jan 5 / Feb 6; NAACL first call Oct 26, direct deadline Feb 5, notification Mar 26, 2027; ACL Apr 25 / May 22, 2027.
- **ARR / ACL AI-writing policy** (aclrollingreview.org/cfp). The authorship and disclosure sentences and case (f) are verbatim. The ACL 2023 policy's "we would discourage such use in ACL submissions" is verbatim. "Beginning February 15, 2024, there is no anonymity period". Checklist item "E1. If you used any AI assistants, did you include information about your use?" exists.
- **Workshops.** GenAIDetect: only the 2025 volume (46 papers) is in the Anthology. It ran at COLING 2025 in Abu Dhabi on Jan 19, 2025, with "Task 2: AI vs. Human – Academic Essay Authenticity Challenge". BEA 2026: ACL 2026, Jul 3-4, deadline Mar 30, 2026; both topic quotes are present. In2Writing: 4th edition at NAACL 2025. LUHME: on the EMNLP 2026 workshop list, after the 2024 and 2025 editions. GEM and EvalEval: on the ACL 2026 workshop list.
- **Regeneron STS 2027** (Official Rules, Research Report Guidelines and AI Usage Chart PDFs). The citizenship clause (2a/2b/2c) is verbatim, so the conclusion that a non-US citizen living in Turkey is ineligible stands. Applications Jun 1 - Nov 5, 2026, 8:00 pm ET. Top 300 on Jan 7 and Top 40 on Jan 21, 2027. Finals Mar 11-17, 2027. 20-page limit with appendices counted. Times New Roman 11pt, 1.5 spacing, 1" margins, no multiple columns, PDF of at most 4MB. All the AI quotes ("without the use of generative AI", "Never acceptable", the certification) and "Discovery of a fake reference will result in disqualification" are verbatim. The "around 2,600" entrant figure is on the STS homepage.
- **Regeneron ISEF 2027** (2027 rules Book.pdf). Selection by an affiliated fair, grades 9-12, the age-20 rule, "may not include research performed before January 2026", and the AI clause "(it is known to hallucinate and falsify references)" are all verbatim. The AI Usage Disclosure asks for "the AI Prompt Log". LA, May 8-14, 2027. ISEF 2026 was May 9-15, 2026 in Phoenix (Society for Science attendee page, via search).
- **TÜBİTAK 2204-A.** Applications 23 Eylül 2026 - 4 Ocak 2027, closing at 17:30. Rule 6.2.4 (projects for ISEF/EUCYS are picked by a separate jury from national 1st-3rd place winners), the brand rule and the prior-competition rule are in the 2026-27 call PDF. The 2026 national final was 27-30 Nisan 2026, confirmed in the official ek4 PDF. Whether a Jan 2027 entry can reach ISEF 2027 is still UNVERIFIED.
- **CJSJ.** High-school only. Research papers of 2-3 pages. Due Sep 30, 2026, and the homepage says the cycle is "now closed". The homepage timeline is in the page HTML: opened Jun 2, 2026; quarterfinalists Oct 30, semifinalists Nov 20, finalists Dec 11, 2026; publication Mar 26, 2027. Fields are from the FAQ. "Supported by the Columbia Undergraduate Science Journal (CUSJ)". The 2025-26 volume lists 9 entries (10 authors). (The FAQ still says "early November (semifinalists) and late December (finalists)", which does not match the homepage timeline. Trust the homepage.)
- **JEI.** Ages 13+, middle and high school. An adult senior author must submit. Initial submission must come before university enrollment. $49 fee. Linguistics and computer science are excluded. AI may not be used for writing, statistical analysis or data mining.
- **NHSJS.** The AI policy page was modified 2026-10-12 (page metadata). All AI quotes are verbatim, including the Google Translate/DeepL ban and where the disclosure goes. The same page mentions a non-refundable "APC", but no amount was shown on any page checked. "five or more figures or tables". 20 pages, 12pt, single spaced. 8-week median review. $280 expedited option. Reviewers are graduate students, postdocs and scientists, followed by a Scientist Advisory Board member.
- **The Curieux Review.** Middle school, high school and undergraduate authors only. 20 pages, TNR 12, 1.15 spacing, MLA, submitted as a Google Doc link. Two editors review. Fees of 250 (fast track) or 200 (seasonal), charged on acceptance. No AI policy on the submissions page.
- **arXiv.** Endorsement change effective Jan 21, 2026, with both endorsement paths quoted verbatim. "arXiv staff cannot waive endorsement requirements". "you should know the person that you endorse or you should see the paper". The CS review/position-paper rule is from Oct 31, 2025. The generative-AI reporting and authorship quotes are verbatim.
- **ACL template.** acl_latex.tex uses `\usepackage[review]{acl}` and drops the `review` option for the final version.

### Could not verify
- **Journal of Student Research.** jsr.org still returns HTTP 522 (and its DNS fails from the fetch tool), so its fees and AI policy remain UNVERIFIED.
- **LUHME's Jul 15, 2026 deadline.** I did not re-check it. It has passed, so it does not change any recommendation.

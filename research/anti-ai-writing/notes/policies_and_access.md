# Fact-check of the two researchers' findings (2026-10-20)

All URLs were re-fetched on 2026-10-20 unless marked otherwise. Fresh copies are in
/tmp/claude-0/-home-user-GreenBert-Project/c9e6db40-731a-54da-a22b-93c87a1090bf/scratchpad/research/access/verify/

## Bottom line on access
- Primary sources say nothing about whether Yale/YYGS or Columbia/CJSJ has, has applied for, or lacks
  Claude Watermark Detector access. This is UNKNOWN. Anthropic publishes no list of approved organizations.
- Searches of yale.edu and columbia.edu found no official page about Claude watermark detection. The only
  Columbia-affiliated item is Prof. Tian Zheng's personal blog post (Aug 13, 2026). It does not mention
  Columbia having access, and it argues "A watermark does not detect cheating." That is a personal view,
  not institutional policy:
  https://sites.stat.columbia.edu/tzheng/post/2026-08-13-claude-watermark/
- No primary statement from Turnitin, GPTZero, Copyleaks or Pangram says they read Claude's watermark.
  Anthropic says these vendors "don't have our key". Not finding an announcement does not prove none exists.

## Researcher A (watermark / detection)
| # | Claim | Verdict |
|---|---|---|
| A1 | Support article: detection is in private preview; eligible groups include "educational organizations"; there is an interest form | CONFIRMED, exact quote (page dateModified 2026-10-08) |
| A2 | Form requires a Claude Platform account with the Admin role, the Console org ID, country, organization name and description, and intended use | CONFIRMED. Addition: the country list includes "United States", so a US organization can register interest. Whether US organizations get approved is UNKNOWN. |
| A3 | News page: "We are releasing a detection API in private preview..." and "Updated Sep 1, 2026" | CONFIRMED. The page metadata dateModified is 2026-10-14; the visible update note says Sep 1. |
| A4 | Detector vendors "don't have our key"; Pangram is named | CONFIRMED |
| A5 | Cloud partners AWS, Google Cloud and Microsoft Foundry are named; no detection partners or universities are named | CONFIRMED |
| A6 | arXiv 2609.09604: "no public tool can test the deployed systems" | CONFIRMED (submitted 9 Sep 2026; Nemecek, Chaudhary, Ayday) |
| A7 | Google SynthID Detector opened Oct 7, 2026; covers image, video and audio; Anthropic not named | CONFIRMED |
| A8 | JRA consulting quote "Detection requires Anthropic's key... has not released it..." | CONFIRMED. Correction: the top-20 review was done on **Aug 19, 2026** (article published Sep 7, modified Sep 14). The article says none of the top 20 "publicly claims to run AI detectors on essays". Its "not released" conflicts with Anthropic's private preview. |
| A9-A11 | YYGS 2027 sample: AI NOTICE, PLAGIARISM NOTICE, certification, limits (300-400 words, 280 characters, 150-200 words, 100-word items) | CONFIRMED (PDF created 2026-09-15; pp. 12 and 16) |
| A12 | YYGS residential rules point scholars to AI at Yale | CONFIRMED. The how-to-apply, required-components and common-questions pages have 0 AI mentions. |
| A13 | Yale undergraduate admissions AI policy | CONFIRMED. It also says AI-composed responses "may result in admission revocation or expulsion". |
| A14 | Poorvu quote combining "currently disabled" and "doesn't endorse" | WRONG CITATION. The two sentences are on different pages. "The AI detection feature of Turnitin is currently disabled." is at https://poorvucenter.yale.edu/teaching/canvas-yale/instructional-tools/turnitin . The "doesn't endorse the use of AI detection software or enable such features in Canvas" sentence is at the .../ai-course-assignment-design/academic URL. Both apply to Yale courses, not YYGS admissions. |
| A15 | CJSJ disclose-or-redact AI rule | CONFIRMED |
| A16 | CJSJ is a CUSJ spin-off; 2026-27 cycle closed | CONFIRMED |
| A17 | Columbia CTL: detectors "should not be the primary mechanism" | CONFIRMED |
| A18 | Anthropic: detection "doesn't work well on small samples" | CONFIRMED |
| A19 | Support limitations list, including "The passage is very short..." | CONFIRMED |
| A20 | "A detected mark shows only that Claude processed the text, not that it wrote it" | PARTLY WRONG (overstated). Anthropic: "A watermark can only determine that Claude was likely involved with the content at some point. It cannot distinguish 'Claude wrote this' from 'Claude heavily edited this.'" A mark does not rule out that Claude wrote the text. The proofreading and light-editing quotes are CONFIRMED. |
| A21 | Nature 2024 SynthID-Text length quote | CONFIRMED (published 23 Oct 2024) |

### Correction to Researcher A's unknown on older models
The support page's model table (as of 2026-10-08) does show which models carry text watermarks today.
**No text watermark** (C2PA file credentials only): [a Claude model], [a Claude model], [a Claude model], [a Claude model],
[a Claude model], [a Claude model] and Haiku 4.5. **Text watermark on first-party surfaces**: [a Claude model]/5, [a Claude model],
[a Claude model]/5/4.8, [a Claude model]/5 and Haiku 5.5. The rollout to Amazon Bedrock for the asterisked models was due
to complete by October 17. The page gives no start date for each model's watermarking.
Also, Anthropic offers a free "Claude Content Checker", but it checks file Content Credentials (C2PA)
only. It does not check text watermarks.

## Researcher B (policies)
| # | Claim | Verdict |
|---|---|---|
| B1-B3 | YYGS AI NOTICE, PLAGIARISM NOTICE, Page 16 certification | CONFIRMED |
| B4 | The same AI NOTICE appears in the 2026 sample | CONFIRMED (PDF created 2025-09-15) |
| B5 | Residential rules quote | CONFIRMED (links ai.yale.edu/guidance) |
| B6 | No AI text on the YYGS admissions pages; Required Components quote | CONFIRMED (8 pages checked; 0 hits) |
| B7 | Early Action Oct 15, 2026; Regular Decision Jan 6, 2027 | CONFIRMED |
| B8-B9 | CJSJ Science-policy paragraph and redaction rule | CONFIRMED, exact |
| B10 | Permission to Publish Form: "original creation", CUSJ as parent, guardian if under 18, no AI text | CONFIRMED (Squarespace timestamp = 2025-05-27) |
| B11 | FAQ, Submit page and templates have no AI text; Google form is closed | CONFIRMED (form "created inside of LionMail", Columbia's Google Workspace) |
| B12 | CJSJ timeline Sep 30 / Oct 30, 2026 | CONFIRMED |
| B13-B14 | CUSJ OJS pages and Author Agreement 3.2 | UNCHECKABLE live: an Anubis bot challenge appeared on curl and a DNS failure on WebFetch. The researcher's saved copies from 20:02 UTC (Apache server, 2018 PDF) contain the quoted text and 0 AI mentions. Note: Researcher A reported this site as blocked, and B's saved files show B got through. |
| B15 | Columbia Scientist has the same AI paragraph and is open to high schoolers | CONFIRMED. The high-school eligibility is on its FAQ and home page, not the guidelines URL. |
| B16-B17 | Common App fraud policy (Aug 2023) and penalties; Terms of Use Oct 24, 2025 with no AI text | CONFIRMED |

## Still unknown (not public)
- Whether YYGS or CJSJ readers run any AI detector, or any approved Claude watermark detector.
- Anthropic's approval criteria, approved organizations, minimum text length, and false-positive and false-negative rates.
- Whether the user's own answers carry a mark. That depends on the model and the date, and it cannot be tested from here because there is no detector access.
- The "private-reviewer" wording in the request is ambiguous. If it means Anthropic's private-preview detector, YYGS or CJSJ access is unknown. If it means a private document or artifact, no public source covers who can view it.

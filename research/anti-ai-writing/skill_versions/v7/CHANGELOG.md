# anti-ai-writing v7 (release candidate): changelog

Base: v4, the version that ranked first in the held-out evaluation (DEVLOG section 15). Three changes:

1. **Rebuild mode added** (from v6, adapted). For drafts the user says an AI wrote. Check every fact, quote and
   reading first; then, if the draft was built from the user's material, keep the checked evidence and write
   fresh sentences, and if it was built from the topic alone, write from step 1 with your own plan. Evidence:
   on the 16 held-out briefs, v6's Rebuild of the plain draft ranked above the humanizer skill's edit in 42 of
   48 judgments (Wilcoxon p = 0.0008) and had the fewest unsupported claims of any condition (0.79 per text).
   Adapted because v4 has no separate "reading check" bullet: the check is now spelled out inside the mode.
2. **Example hygiene** (from v6). Six examples in v4 came from development briefs (a fictional student's notes
   and the phone-ban argument). Models copy skill examples word for word, so they were replaced with neutral
   ones. A script found no 5-word sequence shared between the skill's quoted examples and any brief.
3. **Watermark sentence corrected.** v4 said schools "can check" Claude's watermark. Detection is currently
   limited to approved organizations, so the sentence now says that.

Not carried over from v6: the argument-essay rules, the student register pass, the literary-analysis and
explanation sections, the beat outline and the Logic audit row. v6 as a whole did not beat v4 on held-out briefs
(27 of 48 judgments, p = 0.35), and judges called its arguments "arithmetic-heavy for an English class".

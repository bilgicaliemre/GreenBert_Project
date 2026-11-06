# Appeals benchmark scripts

Methods for DEVLOG section 22 and LEDGER case 2. The appeals themselves are not in this repository: they are real
runners' texts from public campaign pages, kept private (the writers are real people). The reconstructed notes and
the model-written versions are derived from them and stay private too. Set `WF_DIR` to the folder that holds the
workflow run directories (each with a `journal.jsonl`).

1. `collect.py TARGET MAXREQ`: samples campaign pages by random code, one request per second, keeps events up to
   2022 with at least 70 words in "Neden Koşuyorum"; stores no runner names. `screen.py` cleans (links, the
   platform's default template sentences, sign-off names) and screens (60 to 300 words, not shared across pages,
   some first-person voice).
2. `ap_notes.js` (workflow): reconstructs the runner's notes, four appeals per agent. `ap_write.js`: writes each
   appeal from the notes as plain Claude (P) or with a skill version (S8, S9, ...); one agent per text.
   `wf_out.py` writes outputs from a workflow journal to files.
3. `ap_pile.py`: normalizes and anonymizes every version and builds reading piles of 12 appeals by 12 different
   runners, fresh random piles per judge lens. `ap_judge.js`: one blind judge per pile (donor, editor).
   `ap_analyze.py`: judged-human share, mean p(human), AUC against the real appeals, would-give and quality,
   paired differences by runner with bootstrap CIs.
4. `fid_build.py` + `ap_fidb.js` + `fid_analyze.py`: blind count of claims the notes do not support.
   `ap_features.py`: surface features (sentence length, punctuation, greetings) per version.
   `cue_build.py` + `ap_cues.js` + `cue_analyze.py`: optional blind coding of judge rationales into cues.

"""Build v15 from v14: the seven changes that survived the rule-by-rule audit of five GitHub humanizer skills
(research workflow 2026-11-23/24). Each replacement must match exactly once. usage: python3 build_v15.py SRC DST"""
import os, shutil, sys
SRC, DST = sys.argv[1], sys.argv[2]
if os.path.exists(DST): shutil.rmtree(DST)
shutil.copytree(SRC, DST)
def rep(rel, old, new, tag):
    p = f'{DST}/{rel}'; s = open(p).read()
    assert s.count(old) == 1, (tag, rel, s.count(old))
    open(p, 'w').write(s.replace(old, new)); print('ok', tag)
# A3 scope: prose inside files with code, markup or data
rep('SKILL.md', "Skip it for code, data tables and one-line chat answers.",
    "Skip it for code, data tables and one-line chat answers. When prose sits in a file with code, commands,\n"
    "paths, URLs, YAML front matter, LaTeX markup, citation keys or data, edit only the prose and leave the rest exactly\n"
    "as it is, dashes and hyphens included.", 'A3-scope')
# A1 edit diff (both directions), after the fact diff bullet
rep('SKILL.md', "  user or the source. Remove or bracket anything that does not.\n",
    "  user or the source. Remove or bracket anything that does not.\n"
    "- Edit diff (only when you edit a draft the user gave you: Edit, Rebuild, Coach corrections): check the other\n"
    "  direction too. Every claim, hedge, number, name, date and quote in their version must still be in yours or be\n"
    "  named in your note as a cut, and a sentence you join must not add an order, a ranking, a cause or a \"same time\"\n"
    "  the original did not state. In Edit and Coach, compare your version with theirs at each place they differ: each\n"
    "  difference must fix an outright error, clear up something that blocks the meaning, remove a clear AI tell or meet\n"
    "  something the user asked for (such as a word limit). Put anything else back in the writer's words, and mention\n"
    "  in the notes after the text only changes that are actually in it.\n", 'A1-edit-diff')
# A3 output: file edits
rep('SKILL.md', "Never wrap the text in \"Here's your revised version!\" or end with offers.",
    "Never wrap the text in \"Here's your revised version!\" or end with offers. When you edit a file, write only the\n"
    "finished text into it and give Edit's list, any number flag and any note about cuts in your reply.", 'A3-output')
# A2 writing sample: full rule in Write, pointer in Edit
rep('SKILL.md', "(a personal story, a report on their data), ask two or three targeted questions first.\n",
    "(a personal story, a report on their data), ask two or three targeted questions first.\n"
    "If the user gives a sample of their own writing, read it before drafting and match the habits you can count in it:\n"
    "sentence length and spread, contractions, dashes, colons and semicolons, how sentences open and connect, and how\n"
    "formal the words are. These habits override the default style rules, the dash rule included. Do not copy the\n"
    "sample's facts, exact phrases or errors. Use only writing the user says is theirs (a sample an AI polished brings its\n"
    "tells with it). In Coach a sample changes nothing, since the student still writes.\n", 'A2-sample-write')
rep('SKILL.md', "then the list, never a rewrite. If the user also gave a writing sample, it overrides the default style rules\nhere, including the dash rule.",
    "then the list, never a rewrite. A sample of the user's own writing works here as described under Write.", 'A2-sample-edit')
# A5 pointer in Edit
rep('SKILL.md', "  Cut clear AI tells if the text has them.\n",
    "  Cut clear AI tells if the text has them. In informal text, check `references/tells.md` section 9 before treating\n"
    "  lowercase or fragments as errors.\n", 'A5-edit-pointer')
# A7 watermark sentence
rep('SKILL.md', "AI detectors are unreliable\nin both directions (they flag many human essays and miss some AI ones), and recent Claude models add an\n"
    "invisible watermark to their text that approved organizations can check.",
    "AI detectors are unreliable\nin both directions (they flag many human essays and miss some AI ones). Recent Claude models also mark their\n"
    "text through word choice, a statistical watermark with no hidden characters, which organizations Anthropic approves\n"
    "can check. Stripping characters does not remove it, and this skill does not try.", 'A7-watermark')
# credits
rep('SKILL.md', "\"Never inject\" guardrails adapted from\nconorbronsdon/avoid-ai-writing (MIT).",
    "\"Never inject\" guardrails and the idea\nthat every difference in an edit needs a reason adapted from conorbronsdon/avoid-ai-writing (MIT).", 'credits')
# tells.md: A4, A5 in section 9; A6 in T8
rep('references/tells.md', "- Quotations, titles, names, and text written before late 2022.\n",
    "- Quotations, titles, names, and text written before late 2022.\n"
    "- Text that talks about a pattern instead of using it, such as a paper, log or guide that names \"delve\" or \"It's\n"
    "  not X, it's Y\" as an example of an AI tell.\n"
    "- The user's own informal text (a chat message, a comment, a review, a casual post). Lowercase, short forms such as\n"
    "  \"lmk\", fragments and emphatic stops such as \"Worst. Service. Ever.\" belong to the register, so leave them and fix\n"
    "  only what blocks the meaning. Never add them to text you write.\n", 'A4-A5-tells9')
rep('references/tells.md', "**T8 Chatbot residue.** \"Great question\", \"I hope this helps\", \"Let me know if…\", \"Certainly!\". Delete.",
    "**T8 Chatbot residue.** \"Great question\", \"I hope this helps\", \"Let me know if…\", \"Certainly!\". Delete.\n"
    "This covers an assistant talking to its user (\"Let me know if you'd like me to expand this\"). In the user's own\n"
    "message, a greeting, a sign-off or a \"let me know\" that asks the reader for something (\"let me know by Friday if\n"
    "you can drive\") is ordinary correspondence. Keep it.", 'A6-T8')

"""Build v14.1 from v14: the subset of the v15 changes that does not touch Write mode (A3, A4, A5, A6, A7); v15 = this plus A1 and A2.
Original note: the seven changes that survived the rule-by-rule audit of five GitHub humanizer skills
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
# A3 output: file edits
rep('SKILL.md', "Never wrap the text in \"Here's your revised version!\" or end with offers.",
    "Never wrap the text in \"Here's your revised version!\" or end with offers. When you edit a file, write only the\n"
    "finished text into it and give Edit's list, any number flag and any note about cuts in your reply.", 'A3-output')
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

"""EB3 generation. usage: python3 eb3/build_edit3.py GENRE TASK CONDS OUTNAME [model]
TASK E = edit a real text ("Can you improve it?"); TASK R = humanize the plain model's rewrite of a real text (source eb3/<g>/PI).
CONDS (E): C copyedit, PI plain, BI plain+one sentence, S14 our v14, S15 our v15 candidate, HB HT HN HA third-party skills.
CONDS (R): RP plain, R14, R15, RB RT RN RA.  Codes: B=blader/humanizer, T=hardikpandya/stop-slop, N=petergyang/no-ai-slop,
A=conorbronsdon/avoid-ai-writing. Jobs interleaved by item pair so a cut-off splits items, not conditions."""
import json, sys, os, glob
sys.path.insert(0, 'tools'); import bench
G, TASK, conds, outname = sys.argv[1], sys.argv[2], sys.argv[3].split(','), sys.argv[4]
model = sys.argv[5] if len(sys.argv) > 5 else os.environ.get('BENCH_MODEL')
B = f'eb3/{G}'
GEN = G.rstrip('0123456789')  # isef2 = clean rerun of isef, same texts
items = json.load(open(f'{B}/items.json'))
V14 = '/home/user/GreenBert_Project/.claude/skills/anti-ai-writing'
V15 = '/tmp/claude-0/-home-user-GreenBert-Project/c9e6db40-731a-54da-a22b-93c87a1090bf/scratchpad/v15/anti-ai-writing'
REF = {'ell': ['tells.md'], 'isef': ['research.md', 'tells.md']}[GEN]
def files_text(root, rels):
    return '\n\n'.join(f'===== FILE: {r} =====\n' + open(f'{root}/{r}').read() for r in rels)
THIRD = {  # the files each installed skill gives the model (SKILL.md first); scripts cannot run here, as for every condition
    'B': ('/home/user/blader/humanizer', ['SKILL.md']),
    'T': ('/home/user/hardikpandya/stop-slop', ['SKILL.md', 'references/phrases.md', 'references/structures.md', 'references/examples.md']),
    'N': ('/home/user/petergyang/no-ai-slop/skills/no-ai-slop', ['SKILL.md', 'eval.md']),
    'A': ('/home/user/conorbronsdon/avoid-ai-writing/skills/avoid-ai-writing', ['SKILL.md', 'references/patterns.md']),
}
def skill_for(c):
    if c in ('S14', 'R14', 'S14r'): return ('SK_V14', bench.skill_text(V14, REF))
    if c in ('S15', 'R15'): return ('SK_V15', bench.skill_text(V15, REF))
    k = c[1]
    root, rels = THIRD[k]
    return (f'SK_{k}', files_text(root, rels))
NOTOOLS = (' All the text you need is in this message: do not use Bash, Read, Skill or any other tool except the final '
           'structured output.')
ONE = ' Make the smallest edits you can and keep my wording.'
def request(it, c):
    if TASK == 'E':
        q = ('I wrote this essay to practice for my English class. Can you improve it?' if GEN == 'ell' else
             f'Here is the abstract for my science fair project "{it["title"]}". Can you improve it? It has to stay under 250 words.')
        src = open(f'{B}/real/{it["rid"]}.txt').read().strip()
        return q + (ONE if c == 'BI' else '') + '\n\n' + src
    q = ('I wrote this essay to practice for my English class and had AI help me improve it, but now it sounds like AI wrote it. '
         'Can you make it sound more human?' if GEN == 'ell' else
         f'Here is the abstract for my research project "{it["title"]}". I had AI help me polish it, but now it sounds like AI wrote it. '
         'Can you make it sound more human? Keep it under 250 words.')
    return q + '\n\n' + open(f'{B}/PI/{it["rid"]}.txt').read().strip()
CE = ('Copyediting task for a writing study. For each text below, fix OUTRIGHT ERRORS ONLY: misspellings, typos, grammatical errors '
      '(agreement, articles, verb forms, broken sentences), punctuation errors. Do NOT change anything else: keep awkward but '
      'grammatical phrasing, word choice, sentence order, paragraphing, length and every fact. If a text has no errors, return it unchanged.' + NOTOOLS)
RET = "Return every request's revised text only (no notes, explanations, lists of changes or comments) as texts: [{id, text}], one entry per request id."
jobs, shared = [], {}
for bi in range(0, len(items), 2):
    b = items[bi:bi + 2]
    for c in conds:
        lab = f'{c}:{bi // 2}'
        if c == 'C':
            body = '\n\n'.join(f'########## id={it["rid"]} ##########\n' + open(f'{B}/real/{it["rid"]}.txt').read().strip() for it in b)
            jobs.append({'label': lab, 'schema': 'texts', 'prompt': CE + '\n\n' + body + '\n\nReturn texts: [{id, text}] with each full corrected text.'})
            continue
        reqs = '\n\n'.join(f'########## REQUEST id={it["rid"]} ##########\n{request(it, c)}' for it in b)
        multi = ('Below are 2 separate requests from 2 different people. Handle each one independently, exactly as if it were the only '
                 'request you received; do not compare them or make them differ from each other on purpose.')
        if c in ('PI', 'BI', 'RP'):
            head = multi + ' Answer each request the way you normally would as a helpful assistant. Do not use any skills or style guides.' + NOTOOLS
        else:
            key, txt = skill_for(c); shared[key] = txt
            head = (f'You have a writing skill. Its files are below. Follow SKILL.md, including the reference files it points to for this kind '
                    f'of text, for every request.{NOTOOLS}\n\n{{{{{key}}}}}\n\n===== END OF SKILL FILES =====\n\n' + multi)
        jobs.append({'label': lab, 'schema': 'texts', 'prompt': f'{head}\n\n{reqs}\n\n{RET}'})
schema = {'texts': {'type': 'object', 'properties': {'texts': {'type': 'array', 'items': {'type': 'object', 'properties': {'id': {'type': 'string'}, 'text': {'type': 'string'}}, 'required': ['id', 'text']}}}, 'required': ['texts']}}
bench.run_mkwf({'name': f'eb3-{G}-{TASK}-{outname}', 'description': f'EB3 {TASK} ({G}): {",".join(conds)}', 'phase': 'Edit', 'model': model,
                'effort': 'high', 'schemas': schema, 'shared': shared, 'jobs': jobs}, f'{B}/{outname}.js')
print(G, TASK, outname, len(jobs), 'jobs', os.path.getsize(f'{B}/{outname}.js') // 1000, 'kB', {k: len(v) // 1000 for k, v in shared.items()})

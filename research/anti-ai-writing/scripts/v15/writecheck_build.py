"""Writing-from-notes check: skill version X against v14 on the 16 phase-3 briefs, blind paired judging.
usage: BENCH_MODEL=<alias> python3 writecheck_build.py SKILL_DIR_X OUT.js
Each brief: one text per version (v14, X), then two judgments, one in each slot order (exactly balanced).
The 2026-11-24 runs drew the order as (o == 0) XOR random() with a fixed seed, which put v14 in the second slot in
19 of 32 judgments in every run; judges preferred the second text about 64 percent of the time (DEVLOG 26)."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'modes_benchmark', 'tools')); import bench
R = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
V14 = os.path.abspath(os.path.join(R, '..', '..', '.claude', 'skills', 'anti-ai-writing'))
VX, OUT = sys.argv[1], sys.argv[2]
MODEL = os.environ.get('BENCH_MODEL')
B = json.load(open(f'{R}/eval/briefs3/briefs3.json'))
REFS = ['tells.md', 'personal-essay.md', 'short-answers.md', 'messages.md', 'research.md']
def refs(t):
    return {'ps': ['personal-essay.md', 'tells.md'], 'supp': ['short-answers.md', 'tells.md'], 'email': ['messages.md', 'tells.md'],
            'lab': ['research.md', 'tells.md']}.get(t, ['tells.md'])
def facts(b):
    if not b.get('facts'): return 'No facts file: do not invent statistics, studies, quotes or named sources.'
    return 'Facts (the only permitted source of specifics):\n' + open(os.path.join(R, b['facts'])).read().strip()
def brief(b):
    fic = ' The people in the facts are FICTIONAL test material, so write the full piece yourself.' if b.get('facts') and not b['task'].startswith('lit') else ''
    return f'Writing task. Genre: {b["genre"]}. Target length: {b["words"]} words.\n{b["brief"]}{fic}\n\n{facts(b)}'
F = {}
for tag, d in [('V14', V14), ('VX', VX)]:
    F[f'{tag}/SKILL.md'] = open(f'{d}/SKILL.md').read()
    for r in REFS: F[f'{tag}/{r}'] = open(f'{d}/references/{r}').read()
jobs = [{'label': f'{v}:{b["id"]}', 'bid': b['id'], 'sk': f'{v}|{"+".join(refs(b["task"]))}', 'brief': brief(b)} for b in B for v in ['V14', 'VX']]
judges = [{'bid': b['id'], 'order': order, 'brief': brief(b), 'label': f'judge:{b["id"]}:{k}'}
          for b in B for k, order in enumerate([['V14', 'VX'], ['VX', 'V14']])]
NOT = ' All the text you need is in this message: do not use any tool except the final structured output.'
opt = (f", model: {json.dumps(MODEL)}" if MODEL else '') + ", effort: 'high', agentType: 'Explore'"
js = f'''export const meta = {{ name: 'writing-check', description: 'v14 vs a candidate, writing from notes on 16 briefs; blind paired judging, both slot orders per brief', phases: [{{title:'Write'}},{{title:'Judge'}}] }}
const J = {json.dumps(jobs)}
const F = {json.dumps(F)}
const JS = {json.dumps(judges)}
const sk = (key) => {{ const [v, rs] = key.split('|'); return '===== FILE: SKILL.md =====\\n' + F[v + '/SKILL.md'] + rs.split('+').map(r => '\\n\\n===== FILE: references/' + r + ' =====\\n' + F[v + '/' + r]).join('') }}
const TS = {{type:'object', properties:{{text:{{type:'string'}}}}, required:['text']}}
const texts = {{}}
await parallel(J.map(j => () => agent('You have a writing skill. Its files are below. Follow SKILL.md, including the reference files it points to for this kind of text. Use Write mode: this is a writing task for a fictional person or a class example.{NOT}\\n\\n' + sk(j.sk) + '\\n\\n===== END OF SKILL FILES =====\\n\\n' + j.brief + '\\n\\nReturn only the finished text as text.', {{label: j.label, phase: 'Write', schema: TS{opt}}}).then(r => {{ texts[j.label] = r ? r.text : '' }})))
const ONE = {{type:'object', properties:{{p_human:{{type:'integer'}}, quality:{{type:'integer'}}, unsupported:{{type:'array', items:{{type:'string'}}}}}}, required:['p_human','quality','unsupported']}}
const VS = {{type:'object', properties:{{A: ONE, B: ONE, prefer:{{type:'string', enum:['A','B','tie']}}, reason:{{type:'string'}}}}, required:['A','B','prefer','reason']}}
const res = await parallel(JS.map(s => () => agent('You are an experienced writing teacher and editor. Two texts below were written for the same task by two different writers; one or both may be AI-written. For each, give p_human (0-100, chance a skilled human wrote it with no AI), quality (1-10, how well it does the task for its reader) and unsupported: every fact, number, quote, event or claim in it that the facts below do not support (general knowledge only counts if the task is an explanation). Then say which you would rather hand to the reader.{NOT}\\n\\nTASK AND FACTS:\\n' + s.brief + '\\n\\n===== TEXT A =====\\n' + texts[s.order[0] + ':' + s.bid] + '\\n\\n===== TEXT B =====\\n' + texts[s.order[1] + ':' + s.bid] + '\\n\\n===== END =====', {{label: s.label, phase: 'Judge', schema: VS{opt}}}).then(r => ({{bid: s.bid, order: s.order, r}}))))
return {{res, lens: Object.fromEntries(Object.entries(texts).map(([k, v]) => [k, v.split(/\\s+/).length]))}}
'''
open(OUT, 'w').write(js); print(OUT, len(js) // 1000, 'kB', len(jobs), 'writes', len(judges), 'judgments')

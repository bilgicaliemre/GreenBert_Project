"""Regression check 2: 20 phase-2 development briefs; plain vs v9 vs v11 vs v12, each skill given only the references
its router points to for the genre (as in real use)."""
import json, sys, os
sys.path.insert(0, 'tools'); import bench
SK = '/home/user/GreenBert_Project/research/anti-ai-writing/skill_versions'
DIRS = {'V9': f'{SK}/v9/anti-ai-writing', 'V11': f'{SK}/v11/anti-ai-writing', 'V12': 'skills/v12'}
briefs = json.load(open('rg2/briefs2.json')) if os.path.exists('rg2/briefs2.json') else json.load(open('rg/briefs2.json'))
def refs(cond, kind):
    if kind == 'ps': return ['personal-essay.md', 'tells.md']
    if kind == 'supp': return ['personal-essay.md', 'tells.md'] if cond == 'V9' else ['short-answers.md', 'tells.md']
    return ['tells.md']
def facts(b):
    if not b.get('facts'): return 'No facts file: do not invent statistics, studies, quotes or named sources.'
    p = b['facts']
    if not os.path.exists(p):
        for cand in [f'/home/user/GreenBert_Project/research/anti-ai-writing/{p}', f'/home/user/GreenBert_Project/research/anti-ai-writing/eval/briefs/{os.path.basename(p)}']:
            if os.path.exists(cand): p = cand; break
    return 'Facts (the only permitted source of specifics):\n' + open(p).read().strip()
def brief(b):
    fic = ' The people in the facts are FICTIONAL test material, so write the full piece yourself.' if b.get('facts') and not b['task'].startswith('lit') else ''
    return f'Writing task. Genre: {b["genre"]}. Target length: {b["words"]} words.\n{b["brief"]}{fic}\n\n{facts(b)}'
items = [{'rid': b['id'], **b} for b in briefs]
json.dump([{'rid': b['id'], 'genre': b['genre'], 'split': 'test'} for b in briefs], open('rg2/items.json', 'w'), indent=1)
jobs, shared = [], {}
spec = bench.write_spec('rg2', 'x', 'x', items, ['P'], brief, {}, batch=2, plain_note='Do not use any skills or style guides.')
jobs += spec['jobs']
for cond, d in DIRS.items():
    groups = {}
    for it in items: groups.setdefault(tuple(refs(cond, it['rid'].split('_')[0])), []).append(it)
    for gi, (rs, its) in enumerate(sorted(groups.items())):
        key = f'SKILL_{cond}_{gi}'
        sp = bench.write_spec('rg2', 'x', 'x', its, [cond], brief, {cond: (key, bench.skill_text(d, list(rs)))}, batch=2)
        for j in sp['jobs']:
            j['label'] = f'{cond}:{gi}{j["label"].split(":")[1]}'
            j['prompt'] = j['prompt'].replace('for every request.', 'for every request. Use Write mode: these are writing tasks for fictional people or for class examples.', 1)
        jobs += sp['jobs']; shared.update(sp['shared'])
out = {'name': 'rg2-write', 'description': 'Regression check 2: plain, v9, v11, v12 on 20 development briefs', 'phase': 'Write', 'model': 'opus',
       'schemas': spec['schemas'], 'shared': shared, 'jobs': jobs}
bench.run_mkwf(out, 'rg2/write.js'); print(len(jobs), 'jobs', os.path.getsize('rg2/write.js') // 1000, 'kB')

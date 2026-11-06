"""Regression check: 16 phase-3 briefs (ten genres), plain vs v9 vs v10.1, single-turn writers; then panel judges."""
import json, sys, os, random
sys.path.insert(0, 'tools'); import bench
R = '/home/user/GreenBert_Project/research/anti-ai-writing'
SK = f'{R}/skill_versions'
briefs = json.load(open(f'{R}/eval/briefs3/briefs3.json'))
def allrefs(d):
    return bench.skill_text(d, sorted(os.listdir(f'{d}/references')))
SKILLS = {'V9': ('SKILL_V9', allrefs(f'{SK}/v9/anti-ai-writing')), 'V101': ('SKILL_V101', allrefs(f'{SK}/v10.1/anti-ai-writing'))}
def facts(b):
    if not b.get('facts'): return 'No facts file: do not invent statistics, studies, quotes or named sources.'
    p = b['facts'] if os.path.isabs(b['facts']) else f'{R}/{b["facts"]}' if os.path.exists(f'{R}/{b["facts"]}') else f'{R}/eval/briefs3/{os.path.basename(b["facts"])}'
    return 'Facts (the only permitted source of specifics):\n' + open(p).read().strip()
def brief(b):
    fic = ' The people in the facts are FICTIONAL test material, so write the full piece yourself.' if b.get('facts') and not b['task'].startswith('lit') else ''
    return f'Writing task. Genre: {b["genre"]}. Target length: {b["words"]} words.\n{b["brief"]}{fic}\n\n{facts(b)}'
items = [{'rid': b['id'], **b} for b in briefs]
os.makedirs('rg', exist_ok=True)
json.dump([{'rid': b['id'], 'genre': b['genre'], 'task': b['task'], 'words': b['words'], 'split': 'test'} for b in briefs], open('rg/items.json', 'w'), indent=1)
spec = bench.write_spec('rg', 'rg-write', 'Regression check on 16 held-out briefs: plain, v9, v10.1', items, ['P', 'V9', 'V101'], brief, SKILLS, batch=2,
                        plain_note='Do not use any skills or style guides.')
for j in spec['jobs']:
    if not j['label'].startswith('P:'):
        j['prompt'] = j['prompt'].replace('for every request.', 'for every request. Use Write mode: these are writing tasks for fictional people or for class examples.', 1)
spec['model'] = 'opus'
bench.run_mkwf(spec, 'rg/write.js'); print(len(spec['jobs']), 'jobs')

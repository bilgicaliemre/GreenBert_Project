"""Analyze the find-the-human panels.

usage: python3 hc_analyze.py HC_DIR OUT.json workflow_output.json [...] [--split dev|test] [--lens editor,reader,reader2]
Maps each label to its condition through the judge args (label -> file) and anon_map.json (file -> condition).
H = the admitted student's essay; P plain; L word list; F skill v7; G skill v8 (later).
"""
import glob
import json
import sys
from collections import defaultdict

import numpy as np

hc, out = sys.argv[1], sys.argv[2]
rest = sys.argv[3:]
split = lenses = None
if '--split' in rest:
    i = rest.index('--split'); split = rest[i + 1]; rest = rest[:i] + rest[i + 2:]
if '--lens' in rest:
    i = rest.index('--lens'); lenses = set(rest[i + 1].split(',')); rest = rest[:i] + rest[i + 2:]
amap = json.load(open(f'{hc}/anon_map.json'))
label_cond = {}
for f in glob.glob(f'{hc}/judge_args_*.json'):
    for it in json.load(open(f))['items']:
        label_cond[it['id']] = {t['label']: amap[t['path'].split('/')[-1][:-4]]['cond'] for t in it['texts']}
ids_split = None
if split:
    ids_split = {e['id'] for e in json.load(open(f'{hc}/split_{split}.json'))}
types = {e['id']: e['type'] for e in json.load(open(f'{hc}/selected.json'))}

rows, fid = [], defaultdict(list)
for p in rest:
    d = json.load(open(p)); d = d.get('result', d)
    for r in d['results']:
        if ids_split and r['id'] not in ids_split:
            continue
        lc = label_cond[r['id']]
        for j in r['judged']:
            if lenses and j['lens'] not in lenses:
                continue
            rank = {lc[l]: k + 1 for k, l in enumerate(j['ranking']) if l in lc}
            per = {t['label']: t for t in j['texts']}
            rows.append({'id': r['id'], 'type': types[r['id']], 'lens': j['lens'], 'pick': lc.get(j['human_pick'].strip()[:2], '?'),
                         'conf': j['confidence'], 'rank': rank,
                         'scores': {lc[l]: per[l] for l in per if l in lc}})
        if r.get('fidelity'):
            for t in r['fidelity']['texts']:
                c = lc.get(t['label'].strip()[:2])
                if c:
                    fid[c].append(len(t['unsupported']))
conds = sorted({c for r in rows for c in r['rank']}, key=lambda c: 'HFPLG'.index(c) if c in 'HFPLG' else 9)
n = len(rows)
summ = {'n_judgments': n, 'n_essays': len({r['id'] for r in rows}),
        'human_found': sum(r['pick'] == 'H' for r in rows) / n if n else None, 'conds': {}}
for c in conds:
    rk = [r['rank'][c] for r in rows if c in r['rank']]
    sc = [r['scores'][c] for r in rows if c in r['scores']]
    above_h = [r['rank'][c] < r['rank']['H'] for r in rows if c in r['rank'] and 'H' in r['rank']]
    summ['conds'][c] = {
        'picked_as_human': sum(r['pick'] == c for r in rows), 'picked_as_human_rate': sum(r['pick'] == c for r in rows) / n,
        'mean_rank': float(np.mean(rk)), 'ranked_above_human': (int(sum(above_h)), len(above_h)) if c != 'H' else None,
        'quality': float(np.mean([s['quality'] for s in sc])), 'human_likeness': float(np.mean([s['human_likeness'] for s in sc])),
        'ai_suspicion': float(np.mean([s['ai_suspicion'] for s in sc])),
        'unsupported_mean': float(np.mean(fid[c])) if fid.get(c) else None}
json.dump({'summary': summ, 'rows': rows}, open(out, 'w'), indent=1)
NAME = {'H': 'Admitted student', 'P': 'Plain Claude', 'L': 'Word list', 'F': 'Skill v7', 'G': 'Skill v8'}
print(f"{summ['n_essays']} essays, {n} judgments; judges found the real essay in {summ['human_found']:.0%} (chance 25%)")
for c, v in summ['conds'].items():
    ah = f"above human {v['ranked_above_human'][0]}/{v['ranked_above_human'][1]}" if v['ranked_above_human'] else ''
    un = f"unsup {v['unsupported_mean']:.2f}" if v['unsupported_mean'] is not None else ''
    print(f"{NAME[c]:17s} picked-as-human {v['picked_as_human']:3d} ({v['picked_as_human_rate']:.0%})  rank {v['mean_rank']:.2f}  "
          f"qual {v['quality']:.2f}  human {v['human_likeness']:.2f}  susp {v['ai_suspicion']:.2f}  {ah}  {un}")

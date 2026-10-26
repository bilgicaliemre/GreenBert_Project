"""Score the single-text piles.

usage: python3 pile_analyze.py HC_DIR OUT.json result.json [...] [--split dev|test] [--lens editor,reader]
result.json: workflow output ({results: [...]}) or a list of pile results.
Reports per condition: mean p_human, share judged human (p_human >= 50), AUC against the real essays
(chance that a random real essay gets a higher p_human; 0.5 = indistinguishable), mean quality,
and per-essay paired differences against the real essay (version minus real, same judge lens).
"""
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
amap = json.load(open(f'{hc}/anon2_map.json'))
ids = {e['id'] for e in json.load(open(f'{hc}/split_{split}.json'))} if split else None
rows = []
for p in rest:
    d = json.load(open(p))
    d = d.get('result', d) if isinstance(d, dict) else d
    d = d['results'] if isinstance(d, dict) else d
    for r in d:
        if lenses and r['lens'] not in lenses:
            continue
        path = {t['label']: t['path'] for t in r['texts']}
        for j in r['judged']:
            lab = j['label'].strip()[:3].rstrip(':. ')
            if lab not in path:
                continue
            m = amap[path[lab].split('/')[-1][:-4]]
            if ids and m['id'] not in ids:
                continue
            rows.append({'id': m['id'], 'cond': m['cond'], 'lens': r['lens'], 'p_human': j['p_human'],
                         'quality': j['quality'], 'evidence': j['evidence']})


def auc(h, x):
    """P(random real essay scores more human than random version x); ties count half."""
    h, x = np.array(h), np.array(x)
    return float(((h[:, None] > x[None, :]).sum() + 0.5 * (h[:, None] == x[None, :]).sum()) / (len(h) * len(x)))


def boot_ci(f, a, n=4000, seed=0):
    rng = np.random.default_rng(seed)
    a = np.array(a)
    v = [f(a[rng.integers(0, len(a), len(a))]) for _ in range(n)]
    return [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))]


by = defaultdict(list)
for r in rows:
    by[r['cond']].append(r)
key = {(r['id'], r['cond'], r['lens']): r for r in rows}
conds = sorted(by, key=lambda c: 'HPLFG'.index(c) if c in 'HPLFG' else 9)
summ = {'n_ratings': len(rows), 'n_essays': len({r['id'] for r in rows}), 'conds': {}}
H = [r['p_human'] for r in by.get('H', [])]
for c in conds:
    ph = [r['p_human'] for r in by[c]]
    q = [r['quality'] for r in by[c]]
    s = {'n': len(ph), 'p_human': float(np.mean(ph)), 'p_human_ci': boot_ci(np.mean, ph),
         'judged_human': float(np.mean([x >= 50 for x in ph])), 'quality': float(np.mean(q)), 'quality_ci': boot_ci(np.mean, q)}
    if c != 'H' and H:
        s['auc_vs_real'] = auc(H, ph)
        dp = [key[(i, c, l)]['p_human'] - key[(i, 'H', l)]['p_human'] for (i, cc, l) in key if cc == c and (i, 'H', l) in key]
        dq = [key[(i, c, l)]['quality'] - key[(i, 'H', l)]['quality'] for (i, cc, l) in key if cc == c and (i, 'H', l) in key]
        s['paired_p_human_minus_real'] = float(np.mean(dp)) if dp else None
        s['paired_quality_minus_real'] = float(np.mean(dq)) if dq else None
        s['quality_ge_real'] = float(np.mean([x >= 0 for x in dq])) if dq else None
    summ['conds'][c] = s
json.dump({'summary': summ, 'rows': rows}, open(out, 'w'), indent=1)
NAME = {'H': 'Admitted student', 'P': 'Plain Claude', 'L': 'Word list', 'F': 'Skill v7', 'G': 'Skill v8'}
print(f"{summ['n_essays']} essays, {summ['n_ratings']} ratings" + (f" (lenses {','.join(sorted(lenses))})" if lenses else ''))
print(f"{'':17s} {'p_human':>8s} {'judged human':>13s} {'AUC vs real':>12s} {'quality':>8s} {'qual>=real':>11s}")
for c, s in summ['conds'].items():
    a = f"{s['auc_vs_real']:.2f}" if 'auc_vs_real' in s else '-'
    g = f"{s['quality_ge_real']:.0%}" if s.get('quality_ge_real') is not None else '-'
    print(f"{NAME.get(c, c):17s} {s['p_human']:8.1f} {s['judged_human']:13.0%} {a:>12s} {s['quality']:8.2f} {g:>11s}")

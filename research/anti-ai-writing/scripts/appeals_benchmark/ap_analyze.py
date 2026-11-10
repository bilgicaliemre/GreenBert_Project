"""Analyze appeals piles straight from workflow journals.

usage: python3 ap_analyze.py DIR OUT.json ARGS.json:WF_DIR [...] [--ids IDS_JSON] [--pairs A-B,C-D]
R = the runner's own text. Prints per version: share judged human (p >= 50), mean p_human, AUC against R,
would_give, quality; then paired differences by runner (bootstrap 95% CI over runners).
"""
import json, sys
from collections import defaultdict
import numpy as np

d, out = sys.argv[1], sys.argv[2]
rest = sys.argv[3:]
ids = pairs = None
if '--ids' in rest:
    i = rest.index('--ids'); ids = set(json.load(open(rest[i + 1]))); rest = rest[:i] + rest[i + 2:]
if '--pairs' in rest:
    i = rest.index('--pairs'); pairs = [p.split('-') for p in rest[i + 1].split(',')]; rest = rest[:i] + rest[i + 2:]
amap = json.load(open(f'{d}/anon_map.json'))
rows = []
for pair in rest:
    a, wf = pair.split(':', 1)
    args = json.load(open(a)); piles = {p['pile']: p for p in args['piles']}
    lab = {}
    for line in open(f'{wf}/journal.jsonl'):
        e = json.loads(line)
        if e['type'] == 'started':
            lab[e['key']] = e['label']
        elif e['type'] == 'result' and e.get('result') and lab.get(e['key']) in piles:
            p = piles[lab[e['key']]]; f = {t['label']: t['f'] for t in p['texts']}
            for j in e['result']['texts']:
                l = j['label'].strip().rstrip(':.')
                if l not in f:
                    continue
                m = amap[f[l]]
                if ids and m['id'] not in ids:
                    continue
                rows.append({'id': m['id'], 'cond': m['cond'], 'lens': args['lens'], 'p': j['p_human'], 'give': j['would_give'],
                             'q': j['quality'], 'ev': j['evidence']})
seen = {}
for r in rows:
    seen[(r['id'], r['cond'], r['lens'])] = r
rows = list(seen.values())
by = defaultdict(list)
for r in rows:
    by[r['cond']].append(r)
def auc(h, x):
    h, x = np.array(h)[:, None], np.array(x)[None, :]
    return float(((h > x).sum() + 0.5 * (h == x).sum()) / (h.size * x.size))
summ = {}
order = sorted(by, key=lambda c: 'RPLSTUVWXYZ'.index(c) if c in 'RPLSTUVWXYZ' else 99)
lenses = sorted({r['lens'] for r in rows})
print(f"{len({r['id'] for r in rows})} runners, {len(rows)} ratings, lenses {lenses}")
print(f"{'':6s}{'judged human':>13s}{'mean p':>8s}{'AUC vs R':>10s}{'give':>7s}{'quality':>9s}")
for c in order:
    v = by[c]; ph = [r['p'] for r in v]
    s = {'n': len(v), 'judged_human': float(np.mean([x >= 50 for x in ph])), 'p': float(np.mean(ph)),
         'give': float(np.mean([r['give'] for r in v])), 'q': float(np.mean([r['q'] for r in v])),
         'by_lens': {l: {'judged_human': float(np.mean([r['p'] >= 50 for r in v if r['lens'] == l] or [np.nan])),
                         'p': float(np.mean([r['p'] for r in v if r['lens'] == l] or [np.nan]))} for l in lenses}}
    if c != 'R' and 'R' in by:
        s['auc'] = auc([r['p'] for r in by['R']], ph)
    summ[c] = s
    print(f"{c:6s}{s['judged_human']:13.0%}{s['p']:8.1f}{s.get('auc', float('nan')):10.2f}{s['give']:7.2f}{s['q']:9.2f}   " +
          '  '.join(f"{l}: {s['by_lens'][l]['judged_human']:.0%}" for l in lenses))
key = {(r['id'], r['cond'], r['lens']): r for r in rows}
idl = sorted({r['id'] for r in rows})
res_pairs = {}
for a, b in (pairs or []):
    for fld in ['p', 'give', 'q']:
        rng = np.random.default_rng(7)
        def stat(sample):
            v = [key[(i, a, l)][fld] - key[(i, b, l)][fld] for i in sample for l in lenses if (i, a, l) in key and (i, b, l) in key]
            return float(np.mean(v)) if v else float('nan')
        m = stat(idl); bs = [stat(rng.choice(idl, len(idl))) for _ in range(3000)]
        res_pairs[f'{a}-{b}:{fld}'] = [round(m, 2), round(float(np.nanpercentile(bs, 2.5)), 2), round(float(np.nanpercentile(bs, 97.5)), 2)]
        print(f'{a}-{b} {fld:5s} {m:+6.2f} [{np.nanpercentile(bs, 2.5):+.2f}, {np.nanpercentile(bs, 97.5):+.2f}]')
json.dump({'summary': summ, 'pairs': res_pairs, 'rows': rows}, open(out, 'w'), indent=1, ensure_ascii=False)

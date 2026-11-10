"""Analyze rg2 panel judgments: 4 versions per brief, two lenses. usage: python3 rg2/analyze.py RUN... > rg2/res.txt"""
import json, sys, statistics as st, random
sys.path.insert(0, 'tools'); from wfread import results
m = json.load(open('rg2/panel_map.json'))
C = ['P', 'V9', 'V11', 'V12']
rows = []
for r in sys.argv[1:]:
    for lab, res in results(r).items():
        lens, bid = lab.split(':', 1)
        rank = {l.strip(): i + 1 for i, l in enumerate(res.get('ranking', []))}
        for t in res.get('texts', []):
            x = m.get(t['label'].strip())
            if not x: continue
            rows.append((bid, lens, x['cond'], rank.get(t['label'].strip()), t['quality'], t['human_likeness'], len(t['unsupported'])))
J = {(r[0], r[1]) for r in rows}
print('judgments', len(J))
out = {'n_judgments': len(J), 'conds': {}, 'pairs': {}, 'by_genre': {}}
for c in C:
    R = [r for r in rows if r[2] == c and r[3]]
    d = {'mean_rank': round(st.mean(r[3] for r in R), 2), 'first': sum(r[3] == 1 for r in R), 'n': len(R),
         'quality': round(st.mean(r[4] for r in R), 2), 'human': round(st.mean(r[5] for r in R), 2), 'unsupported': round(st.mean(r[6] for r in R), 2)}
    out['conds'][c] = d
    print(f"{c:4s} mean rank {d['mean_rank']:.2f}  first {d['first']}/{d['n']}  quality {d['quality']:.2f}  human {d['human']:.2f}  unsupported {d['unsupported']:.2f}")
def get(bid, lens, c, k):
    v = [r[k] for r in rows if r[0] == bid and r[1] == lens and r[2] == c]
    return v[0] if v else None
def pair(a, b):
    w = l = 0; diffs = []
    for bid, lens in J:
        ra, rb = get(bid, lens, a, 3), get(bid, lens, b, 3)
        if ra and rb: w += ra < rb; l += ra > rb
    # bootstrap over briefs of mean rank difference (b - a; positive = a better)
    B = sorted({j[0] for j in J}); rng = random.Random(7)
    def md(bs):
        v = [get(x, ln, b, 3) - get(x, ln, a, 3) for x in bs for ln in ('reader', 'editor') if get(x, ln, a, 3) and get(x, ln, b, 3)]
        return st.mean(v) if v else 0
    boots = sorted(md([rng.choice(B) for _ in B]) for _ in range(4000))
    return w, l, round(md(B), 2), [round(boots[100], 2), round(boots[3899], 2)]
for a, b in (('V12', 'V9'), ('V12', 'P'), ('V12', 'V11'), ('V11', 'V9'), ('V11', 'P'), ('V9', 'P')):
    w, l, d, ci = pair(a, b)
    out['pairs'][f'{a}>{b}'] = {'wins': w, 'losses': l, 'rank_gain': d, 'ci95': ci}
    print(f'{a} ranked above {b} in {w} of {w + l}; mean rank advantage {d:+.2f} {ci} (bootstrap over briefs)')
by = {}
for r in rows:
    if r[3]: by.setdefault(r[0].split('_')[0], {}).setdefault(r[2], []).append(r[3])
out['by_genre'] = {g: {c: round(st.mean(v), 2) for c, v in d.items()} for g, d in sorted(by.items())}
print('mean rank by genre:', json.dumps(out['by_genre']))
json.dump(out, open('rg2/res.json', 'w'), indent=1)

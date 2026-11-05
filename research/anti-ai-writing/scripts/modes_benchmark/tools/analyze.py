"""Aggregate pile judgments. usage: python3 analyze.py B RUN:TAG [RUN:TAG ...] [--pairs A-B,C-D] [--out f.json] [--split dev]
Prints only aggregates (no texts, no evidence)."""
import json, sys, random, statistics as st, os
sys.path.insert(0, os.path.dirname(__file__))
from wfread import results

B = sys.argv[1]
args = sys.argv[2:]
pairs, out, split = [], None, None
runs = []
i = 0
while i < len(args):
    a = args[i]
    if a == '--pairs': pairs = [p.split('-') for p in args[i + 1].split(',')]; i += 2; continue
    if a == '--out': out = args[i + 1]; i += 2; continue
    if a == '--split': split = args[i + 1]; i += 2; continue
    runs.append(a.split(':')); i += 1
items = {it['rid']: it for it in json.load(open(f'{B}/items.json'))}
rows = []  # (rid, cond, lens, p, quality, extra)
for run, tag in runs:
    P = json.load(open(f'{B}/piles_{tag}.json'))
    for pile, r in results(run).items():
        lens = pile.split(':')[0]
        for t in r.get('texts', []):
            m = P['map'].get(t['label'].strip())
            if not m: continue
            if split and items[m['rid']]['split'] != split: continue
            rows.append({'rid': m['rid'], 'cond': m['cond'], 'lens': lens, 'p': t.get('p_human'), 'q': t.get('quality'),
                         **{k: v for k, v in t.items() if isinstance(v, (int, float)) and k not in ('p_human', 'quality')}})
conds = sorted({r['cond'] for r in rows}, key=lambda c: (c != 'H', c))
lenses = sorted({r['lens'] for r in rows})
def auc(h, x):
    if not h or not x: return None
    s = sum((a > b) + 0.5 * (a == b) for a in h for b in x)
    return s / (len(h) * len(x))
summary = {}
print(f'{"cond":6s} {"n":>4s} {"human%":>7s} {"mean_p":>7s} {"quality":>7s}  AUC vs H by lens  ' + ' '.join(lenses))
for c in conds:
    R = [r for r in rows if r['cond'] == c]
    s = {'n': len(R), 'human_share': sum(r['p'] >= 50 for r in R) / len(R), 'mean_p': st.mean(r['p'] for r in R),
         'quality': st.mean(r['q'] for r in R)}
    extra = sorted({k for r in R for k in r if k not in ('rid', 'cond', 'lens', 'p', 'q')})
    for k in extra: s[k] = st.mean(r[k] for r in R if k in r)
    s['auc_by_lens'] = {L: auc([r['p'] for r in rows if r['cond'] == 'H' and r['lens'] == L], [r['p'] for r in R if r['lens'] == L]) for L in lenses} if c != 'H' else {}
    s['human_share_by_lens'] = {L: (lambda RL: sum(r['p'] >= 50 for r in RL) / len(RL) if RL else None)([r for r in R if r['lens'] == L]) for L in lenses}
    summary[c] = s
    print(f'{c:6s} {s["n"]:4d} {100 * s["human_share"]:6.0f}% {s["mean_p"]:7.1f} {s["quality"]:7.2f}  ' +
          ' '.join(f'{(s["auc_by_lens"].get(L) or 0):.2f}' for L in lenses) + '   ' + ' '.join(f'{k}={s[k]:.2f}' for k in extra) +
          '   human% by lens ' + ' '.join(f'{100 * (s["human_share_by_lens"][L] or 0):.0f}' for L in lenses))
def per_item(c, key):
    d = {}
    for r in rows:
        if r['cond'] == c: d.setdefault(r['rid'], []).append(r[key])
    return {k: st.mean(v) for k, v in d.items()}
res_pairs = {}
for a, b in pairs:
    for key in ('p', 'q'):
        A, Bm = per_item(a, key), per_item(b, key)
        common = sorted(set(A) & set(Bm))
        if not common: continue
        diffs = [A[k] - Bm[k] for k in common]
        rng = random.Random(7); boots = []
        for _ in range(4000):
            smp = [diffs[rng.randrange(len(diffs))] for _ in diffs]; boots.append(st.mean(smp))
        boots.sort()
        res_pairs[f'{a}-{b}:{key}'] = (st.mean(diffs), boots[100], boots[3899], len(common))
        print(f'{a} vs {b} {key}: {st.mean(diffs):+.2f} [{boots[100]:+.2f}, {boots[3899]:+.2f}] n={len(common)}')
if out:
    json.dump({'summary': summary, 'pairs': res_pairs}, open(out, 'w'), indent=1)

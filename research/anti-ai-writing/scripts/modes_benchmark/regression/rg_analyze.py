import json, sys, statistics as st, random
sys.path.insert(0, 'tools'); from wfread import results
m = json.load(open('rg/panel_map.json'))
rows = []  # (brief, lens, cond, rank, quality, human, unsupported)
for r in sys.argv[1:]:
    for lab, res in results(r).items():
        lens, bid = lab.split(':', 1)
        rank = {l.strip(): i + 1 for i, l in enumerate(res.get('ranking', []))}
        for t in res.get('texts', []):
            x = m.get(t['label'].strip())
            if not x: continue
            rows.append((bid, lens, x['cond'], rank.get(t['label'].strip()), t['quality'], t['human_likeness'], len(t['unsupported'])))
print('judgments', len(rows) // 3)
for c in ['P', 'V9', 'V101']:
    R = [r for r in rows if r[2] == c and r[3]]
    print(f"{c:5s} mean rank {st.mean(r[3] for r in R):.2f}  first {sum(r[3]==1 for r in R)}/{len(R)}  quality {st.mean(r[4] for r in R):.2f}  human {st.mean(r[5] for r in R):.2f}  unsupported {st.mean(r[6] for r in R):.2f}")
def wins(a, b):
    w = l = 0
    for bid in {r[0] for r in rows}:
        for lens in ('reader', 'editor'):
            ra = [r[3] for r in rows if r[0] == bid and r[1] == lens and r[2] == a]
            rb = [r[3] for r in rows if r[0] == bid and r[1] == lens and r[2] == b]
            if ra and rb and ra[0] and rb[0]: w += ra[0] < rb[0]; l += ra[0] > rb[0]
    return w, l
for a, b in (('V101', 'P'), ('V101', 'V9'), ('V9', 'P')):
    print(a, 'ranked above', b, '%d of %d' % (wins(a, b)[0], sum(wins(a, b))))
by = {}
for r in rows:
    if r[3]: by.setdefault((r[0].split('_')[0], r[2]), []).append(r[3])
print('mean rank by genre:', {k: round(st.mean(v), 2) for k, v in sorted(by.items())})

"""Analyze phase-2 panel judgments and detector scores.

usage: python3 analyze.py OUT_JSON workflow_output.json [more.json ...] [--scores scores.json]
Writes a JSON summary with per-condition and per-genre statistics.
"""
import json
import sys
from collections import defaultdict
from itertools import combinations

import numpy as np
from scipy import stats

ORDER = ['P', 'L', 'H', 'E', 'O', 'V', 'R']  # display order; the conditions actually used come from the data
NAMES = {'P': 'Plain', 'L': 'Word-list prompt', 'H': 'Humanizer edit', 'E': 'Our edit', 'O': 'Our write',
         'V': 'v5 write', 'R': 'v5 rebuild'}
CONDS = ORDER
SCORE_KEYS = ['quality', 'human_likeness', 'specificity', 'voice', 'structure_and_insight', 'ai_suspicion']
rng = np.random.default_rng(0)


def load(paths):
    out = []
    for p in paths:
        d = json.load(open(p))
        d = d.get('result', d)
        out += d['results']
    return out


def boot_ci(x, n=5000):
    x = np.asarray(x, float)
    if len(x) == 0:
        return (float('nan'), float('nan'))
    m = rng.choice(x, size=(n, len(x)), replace=True).mean(1)
    return (float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5)))


def main(argv):
    out_path = argv[0]
    rest = argv[1:]
    scores_path = None
    if '--scores' in rest:
        i = rest.index('--scores'); scores_path = rest[i + 1]; rest = rest[:i] + rest[i + 2:]
    results = load(rest)
    rows = []  # one row per (brief, judge, condition)
    for r in results:
        for j in r['judged']:
            rank = {j['map'][lab]: k + 1 for k, lab in enumerate(j['ranking']) if lab in j['map']}
            per = {t['label']: t for t in j['texts']}
            for lab, cond in j['map'].items():
                t = per.get(lab)
                if t is None or cond not in rank:
                    continue
                rows.append({'brief': r['brief'], 'task': r.get('task', r['brief'].split('_')[0]), 'lens': j['lens'],
                             'cond': cond, 'rank': rank[cond], 'unsupported': len(t['unsupported']),
                             **{k: t[k] for k in SCORE_KEYS}})
    global CONDS
    CONDS = [c for c in ORDER if any(r['cond'] == c for r in rows)]
    summary = {'conds': CONDS, 'n_briefs': len({r['brief'] for r in rows}), 'n_judgments': len(rows) // len(CONDS), 'conditions': {}, 'pairwise': {}, 'by_task': {}}
    for c in CONDS:
        rc = [r for r in rows if r['cond'] == c]
        if not rc:
            continue
        d = {'n': len(rc), 'mean_rank': float(np.mean([r['rank'] for r in rc])), 'mean_rank_ci': boot_ci([r['rank'] for r in rc]),
             'first_place': sum(r['rank'] == 1 for r in rc), 'unsupported_mean': float(np.mean([r['unsupported'] for r in rc])),
             'unsupported_ci': boot_ci([r['unsupported'] for r in rc])}
        for k in SCORE_KEYS:
            d[k] = float(np.mean([r[k] for r in rc])); d[k + '_ci'] = boot_ci([r[k] for r in rc])
        summary['conditions'][c] = d
    # Friedman test on per-brief mean ranks
    briefs = sorted({r['brief'] for r in rows})
    mat = []
    for b in briefs:
        vals = []
        for c in CONDS:
            x = [r['rank'] for r in rows if r['brief'] == b and r['cond'] == c]
            vals.append(np.mean(x) if x else np.nan)
        if not any(np.isnan(vals)):
            mat.append(vals)
    mat = np.array(mat)
    if len(mat) >= 3:
        fr = stats.friedmanchisquare(*[mat[:, i] for i in range(len(CONDS))])
        summary['friedman'] = {'statistic': float(fr.statistic), 'p': float(fr.pvalue), 'n_briefs': int(len(mat))}
    # pairwise: per judgment, did a rank above b; Wilcoxon on per-brief mean rank differences
    for a, b in combinations(CONDS, 2):
        wins = ties = n = 0
        for (br, lens) in {(r['brief'], r['lens']) for r in rows}:
            ra = [r['rank'] for r in rows if r['brief'] == br and r['lens'] == lens and r['cond'] == a]
            rb = [r['rank'] for r in rows if r['brief'] == br and r['lens'] == lens and r['cond'] == b]
            if ra and rb:
                n += 1; wins += ra[0] < rb[0]
        diffs = []
        if len(mat):
            ia, ib = CONDS.index(a), CONDS.index(b)
            diffs = mat[:, ia] - mat[:, ib]
        p = None
        if len(diffs) >= 5 and np.any(diffs != 0):
            p = float(stats.wilcoxon(diffs, zero_method='zsplit').pvalue)
        summary['pairwise'][f'{a}>{b}'] = {'wins': wins, 'n': n, 'win_rate': wins / n if n else None, 'wilcoxon_p': p}
    for task in sorted({r['task'] for r in rows}):
        rt = [r for r in rows if r['task'] == task]
        summary['by_task'][task] = {c: {'mean_rank': float(np.mean([r['rank'] for r in rt if r['cond'] == c])),
                                        'unsupported_mean': float(np.mean([r['unsupported'] for r in rt if r['cond'] == c])),
                                        'human_likeness': float(np.mean([r['human_likeness'] for r in rt if r['cond'] == c])),
                                        'n': len([r for r in rt if r['cond'] == c])}
                                    for c in CONDS if any(r['cond'] == c for r in rt)}
    if scores_path:
        sc = json.load(open(scores_path))
        det = defaultdict(list)
        for path, s in sc.items():
            c = path.split('/')[-2]  # condition = folder that holds the text
            det[c].append(s)
        summary['detectors'] = {}
        for c in CONDS:
            v = det.get(c, [])
            if not v:
                continue
            under = sum(1 for s in v if s['desklib'] < 20 and s['fakespot'] < 20 and s.get('superannotate', 0) < 20)
            summary['detectors'][c] = {'n': len(v), 'under20_all': under,
                                       **{k: float(np.mean([s[k] for s in v])) for k in ('desklib', 'fakespot', 'superannotate') if k in v[0]}}
    json.dump(summary, open(out_path, 'w'), indent=1)
    c = summary['conditions']
    print(f"briefs={summary['n_briefs']} judgments={summary['n_judgments']}")
    for k in CONDS:
        if k in c:
            x = c[k]
            print(f"{NAMES[k]:18s} rank {x['mean_rank']:.2f} [{x['mean_rank_ci'][0]:.2f},{x['mean_rank_ci'][1]:.2f}] 1st {x['first_place']:3d} "
                  f"human {x['human_likeness']:.2f} qual {x['quality']:.2f} susp {x['ai_suspicion']:.2f} unsup {x['unsupported_mean']:.2f}")
    if 'friedman' in summary:
        print('Friedman', summary['friedman'])
    for k, v in summary['pairwise'].items():
        print(k, v)
    if 'detectors' in summary:
        for k, v in summary['detectors'].items():
            print('DET', NAMES[k], v)


if __name__ == '__main__':
    main(sys.argv[1:])

"""Paper figures.

usage: python3 figures.py OUTDIR --rank NAME=summary.json [NAME=summary.json ...]
                          --det LABEL=ROLE=scores.json[:substr,substr] [...]   (ROLE: skill|plain|human|other)
Writes fig_rank.pdf (mean rank with 95% CI per condition, one panel per study) and
fig_detectors.pdf (per-text scores on the three detectors, one row per group).
"""
import json
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402

INK, INK2, GRID = '#0b0b0b', '#52514e', '#e4e3df'
SKILL, PLAIN, HUMAN, OTHER = '#2a78d6', '#eb6834', '#1baf7a', '#8f8d86'
plt.rcParams.update({'font.family': 'serif', 'font.serif': ['Nimbus Roman', 'Times New Roman', 'DejaVu Serif'],
                     'font.size': 8, 'axes.edgecolor': INK2, 'axes.labelcolor': INK, 'xtick.color': INK2,
                     'ytick.color': INK, 'axes.spines.top': False, 'axes.spines.right': False})

NAMES = {'P': 'Plain', 'L': 'Word list', 'H': 'Humanizer edit', 'E': 'Skill edit (v4)', 'O': 'Skill write (v4)',
         'V': 'Skill write (v5)', 'R': 'Skill rebuild (v5)', 'F': 'Skill write (v4)', 'S': 'Skill write (v6)', 'B': 'Skill revise (v6)'}
ROLE = {'P': PLAIN, 'L': OTHER, 'H': OTHER, 'E': SKILL, 'O': SKILL, 'V': SKILL, 'R': SKILL, 'F': SKILL, 'S': SKILL, 'B': SKILL}


def kv(items):
    return [tuple(x.split('=', 1)) for x in items]


def fig_rank(out, studies):
    fig, axes = plt.subplots(1, len(studies), figsize=(3.2 * len(studies), 1.9), sharex=True, squeeze=False)
    for ax, (title, path) in zip(axes[0], studies):
        s = json.load(open(path))
        conds = [c for c in s.get('conds', list(s['conditions'])) if c in s['conditions']]
        conds = sorted(conds, key=lambda c: -s['conditions'][c]['mean_rank'])
        for y, c in enumerate(conds):
            d = s['conditions'][c]
            lo, hi = d['mean_rank_ci']
            ax.plot([lo, hi], [y, y], color=ROLE[c], lw=2, solid_capstyle='round')
            ax.plot(d['mean_rank'], y, 'o', ms=6, color=ROLE[c], mec='white', mew=1.5)
            ax.text(hi + 0.08, y, f"{d['mean_rank']:.2f}", va='center', fontsize=7, color=INK2)
        ax.set_yticks(range(len(conds)), [NAMES[c] for c in conds])
        n = len(conds)
        ax.set_xlim(0.8, n + 0.4)
        ax.set_xticks(range(1, n + 1))
        ax.grid(axis='x', color=GRID, lw=0.6)
        ax.set_axisbelow(True)
        ax.set_title(f"{title} ({s['n_briefs']} briefs, {s['n_judgments']} judgments)", fontsize=8, color=INK, loc='left')
        ax.set_xlabel('Mean rank (1 = best)', color=INK2)
    fig.tight_layout()
    fig.savefig(out, bbox_inches='tight')


def fig_det(out, groups):
    dets = [('desklib', 'D1 (DeBERTa, RAID)'), ('fakespot', 'D2 (RoBERTa-base)'), ('superannotate', 'D3 (RoBERTa-large)')]
    fig, axes = plt.subplots(1, 3, figsize=(6.6, 0.32 * len(groups) + 0.7), sharey=True)
    for ax, (k, title) in zip(axes, dets):
        for y, (label, color, vals) in enumerate(groups):
            xs = [v[k] for v in vals]
            jit = [((i * 0.37) % 1 - 0.5) * 0.35 for i in range(len(xs))]
            ax.scatter(xs, [y + j for j in jit], s=9, color=color, edgecolor='white', linewidth=0.4, zorder=3)
        ax.axvline(20, color=INK2, lw=0.8, ls=(0, (3, 2)))
        ax.set_xlim(-3, 103)
        ax.set_xticks([0, 20, 50, 100])
        ax.grid(axis='x', color=GRID, lw=0.6)
        ax.set_axisbelow(True)
        ax.set_title(title, fontsize=8, color=INK, loc='left')
        ax.set_xlabel('AI score (%)', color=INK2)
    axes[0].set_yticks(range(len(groups)), [f"{g[0]} (n={len(g[2])})" for g in groups])
    axes[0].invert_yaxis()
    fig.tight_layout()
    fig.savefig(out, bbox_inches='tight')


if __name__ == '__main__':
    a = sys.argv[1:]
    outdir = a[0]
    i_r, i_d = a.index('--rank'), a.index('--det')
    rank = kv(a[i_r + 1:i_d] if i_d > i_r else a[i_r + 1:])
    det = a[i_d + 1:] if i_d > i_r else a[i_d + 1:i_r]
    fig_rank(f'{outdir}/fig_rank.pdf', rank)
    groups = []
    for spec in det:  # label=color=path[:prefix]
        label, color, rest = spec.split('=', 2)
        path, _, prefix = rest.partition(':')
        d = json.load(open(path))
        keys = prefix.split(',') if prefix else ['']
        vals = [v for p, v in d.items() if any(k in p for k in keys)]
        groups.append((label, {'skill': SKILL, 'plain': PLAIN, 'human': HUMAN, 'other': OTHER}[color], vals))
    fig_det(f'{outdir}/fig_detectors.pdf', groups)

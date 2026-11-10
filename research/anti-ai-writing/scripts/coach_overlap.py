"""Ghostwriting leakage in the coaching experiment.

For each student, how much of each revision was copied from the feedback it got? We count the revision's word
6-grams that occur in the feedback but in neither the student's first draft nor their notes (so quoting the
student's own words back does not count), and the longest such span.

usage: python3 coach_overlap.py OUT_DIR NOTES_JSON [--json out.json]
NOTES_JSON maps student id -> path of their notes file.
"""
import json
import re
import sys

N = 6


def words(path):
    return re.findall(r"[a-z0-9']+", open(path, encoding='utf-8').read().lower().replace('’', "'"))


def grams(ws, n=N):
    return {tuple(ws[i:i + n]) for i in range(len(ws) - n + 1)}


def longest_copied_span(rev, fb, own):
    """Longest run of consecutive revision words whose every 6-gram is in the feedback and not the student's own."""
    best = run = 0
    for i in range(len(rev) - N + 1):
        g = tuple(rev[i:i + N])
        if g in fb and g not in own:
            run = run + 1 if run else N
            best = max(best, run)
        else:
            run = 0
    return best


def main(argv):
    out, notes = argv[0], json.load(open(argv[1]))
    res = {}
    for sid, npath in notes.items():
        own = grams(words(f'{out}/D0/{sid}.txt')) | grams(words(npath))
        row = {}
        for rev, fb in (('RS', 'FS'), ('RP', 'FP')):
            r, f = words(f'{out}/{rev}/{sid}.txt'), grams(words(f'{out}/{fb}/{sid}.txt'))
            rg = grams(r)
            copied = {g for g in rg if g in f and g not in own}
            row[rev] = {'words': len(r), 'copied_6grams': len(copied), 'share': round(len(copied) / max(1, len(rg)), 3),
                        'longest_span_words': longest_copied_span(r, f, own)}
        res[sid] = row
        print(sid, row)
    for rev in ('RS', 'RP'):
        print(rev, 'mean share copied from feedback:', round(sum(v[rev]['share'] for v in res.values()) / len(res), 3))
    if '--json' in argv:
        json.dump(res, open(argv[argv.index('--json') + 1], 'w'), indent=1)


if __name__ == '__main__':
    main(sys.argv[1:])

"""Decode answer codes from the reading-study page and tally them.

Each rater sends a code that starts with RR1-. Paste the codes into a text file, one per line, then run:
    python3 decode_survey.py codes.txt ../eval/results/survey_pool_key.json

The key maps each pair id to the brief and to which side (x or y) holds which condition
(F = skill write, P = plain, L = word-list prompt). The page never contains the key.
"""
import base64
import json
import sys
from collections import Counter, defaultdict


def decode(code):
    raw = code.strip()
    if not raw.startswith('RR1-'):
        raise ValueError(f'not a reading-study code: {raw[:20]}...')
    return json.loads(base64.b64decode(raw[4:]).decode('utf-8'))


def main(codes_path, key_path):
    key = json.load(open(key_path))
    raters, seen = [], set()
    for line in open(codes_path):
        if not line.strip():
            continue
        r = decode(line)
        if r['id'] in seen:  # the same rater pasted twice
            continue
        seen.add(r['id'])
        raters.append(r)
    better = defaultdict(Counter)   # opponent -> who was judged better
    ai_like = defaultdict(Counter)  # opponent -> which read more like AI
    for r in raters:
        for pair_id, b, ai, conf in r['a']:
            k = key[pair_id]
            other = k['x'] if k['y'] == 'F' else k['y']
            side = {'x': k['x'], 'y': k['y']}
            better[other][side.get(b, 'same')] += 1
            ai_like[other][side.get(ai, 'cannot tell')] += 1
    print(f'{len(raters)} raters: ' + ', '.join(f'{v} {k}' for k, v in Counter(r["role"] for r in raters).items()))
    names = {'P': 'plain', 'L': 'word list'}
    for other in ('P', 'L'):
        b, a = better[other], ai_like[other]
        n = sum(b.values())
        if not n:
            continue
        print(f'\nSkill vs {names[other]} ({n} judgments)')
        print(f'  better writing: skill {b["F"]}, {names[other]} {b[other]}, about the same {b["same"]}')
        print(f'  reads more like AI: skill {a["F"]}, {names[other]} {a[other]}, cannot tell {a["cannot tell"]}')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])

"""Surface features by condition (aggregates only). usage: python3 features.py B COND[,COND..] [--split dev] [--out f.json]"""
import json, re, sys, os, statistics as st
B = sys.argv[1]; conds = sys.argv[2].split(',')
split = sys.argv[sys.argv.index('--split') + 1] if '--split' in sys.argv else None
out = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else None
items = [it for it in json.load(open(f'{B}/items.json')) if not split or it['split'] == split]
HYPE = r'\b(novel|innovative|groundbreaking|crucial|pivotal|significant(ly)?|promising|potential|paves?|comprehensive|robust|leverag\w*|utiliz\w*|facilitat\w*|enhanc\w*|delve\w*|underscore\w*|showcas\w*|intricate|notably|furthermore|moreover|additionally)\b'
TAIL = r',\s+(demonstrating|highlighting|showing|suggesting|indicating|underscoring|revealing|making|allowing|enabling|providing)\b'
WORLD = r'^(In recent years|In today|Over the (past|last)|With the (rise|growth|increasing)|.{0,60}\b(is|are|remains|has become) (one of the|a (major|growing|critical|significant|serious|pressing)))'
FIRST = r'\b(I|my|me|we|our|us)\b'
PASSIVE = r'\b(was|were|is|are|been|being)\s+\w+ed\b'
def sents(t):
    return [s for s in re.split(r'(?<=[.!?])\s+(?=[A-Z0-9"(])', t.strip()) if s.strip()]
def feats(t):
    w = t.split(); n = max(1, len(w)); S = sents(t); L = [len(s.split()) for s in S]
    return {
        'words': len(w), 'sent_len': st.mean(L) if L else 0, 'sent_sd': st.pstdev(L) if len(L) > 1 else 0,
        'long30': sum(l >= 30 for l in L) / max(1, len(L)),
        'hype_per100': 100 * len(re.findall(HYPE, t, re.I)) / n, 'ing_tails': len(re.findall(TAIL, t)),
        'world_open': int(bool(re.search(WORLD, S[0] if S else '', re.I))), 'first_person_per100': 100 * len(re.findall(FIRST, t)) / n,
        'passive_per100': 100 * len(re.findall(PASSIVE, t, re.I)) / n, 'numbers_per100': 100 * len(re.findall(r'\d+(?:[.,]\d+)?', t)) / n,
        'semicolons': t.count(';'), 'colons': t.count(':'), 'dashes': len(re.findall(r'—|–| - |--', t)), 'parens': t.count('('),
        'this_study_starts': sum(bool(re.match(r'(This|The present|Our) (study|project|research|work|paper)', s)) for s in S),
        'contractions_per100': 100 * len(re.findall(r"\b\w+'(s|t|re|ve|ll|d|m)\b", t)) / n,
        'paras': len([p for p in t.split('\n\n') if p.strip()]),
        'exclam': t.count('!'), 'questions': t.count('?'),
    }
res = {}
for c in conds:
    F = []
    for it in items:
        p = f'{B}/real/{it["rid"]}.txt' if c == 'H' else f'{B}/{c}/{it["rid"]}.txt'
        if os.path.exists(p): F.append(feats(open(p).read()))
    if not F: continue
    res[c] = {k: st.mean(f[k] for f in F) for k in F[0]}; res[c]['n'] = len(F)
keys = list(next(iter(res.values())).keys())
print('feature'.ljust(22) + ''.join(c.rjust(9) for c in res))
for k in keys:
    print(k.ljust(22) + ''.join(f'{res[c][k]:9.2f}' for c in res))
if out: json.dump(res, open(out, 'w'), indent=1)

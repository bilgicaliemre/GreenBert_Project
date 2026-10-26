"""Surface style features of essays, for comparing admitted students' essays with model-written ones.

usage: python3 style_features.py OUT.json GROUP=glob [GROUP=glob ...]
Each glob matches .txt files; a header block ending in a line '---' (corpus files) is skipped.
Prints the mean of each feature per group and writes per-file values to OUT.json.
"""
import glob
import json
import re
import statistics as st
import sys

ABSTRACT = re.compile(r"\b\w+(?:tion|ness|ment|ity|ance|ence|ship|ism)s?\b", re.I)
LESSON = re.compile(r"\b(I (?:learned|realized|discovered|understood|came to (?:see|understand|realize))|taught me|showed me that|made me realize)\b", re.I)


def body(path):
    t = open(path, encoding='utf-8').read().replace('\r', '')
    if '\n---\n' in t[:1500]:
        t = t.split('\n---\n', 1)[1]
    return t.strip()


def sentences(t):
    t = re.sub(r'\s+', ' ', t)
    return [s for s in re.split(r'(?<=[.!?])["”’)]?\s+(?=[A-Z"“‘(])', t) if s.strip()]


def features(t):
    words = re.findall(r"[A-Za-z0-9'’-]+", t)
    n = max(1, len(words))
    sents = sentences(t)
    sl = [len(re.findall(r"[A-Za-z0-9'’-]+", s)) for s in sents] or [0]
    paras = [p for p in re.split(r'\n\s*\n', t) if p.strip()] or [t]
    last = [sentences(p)[-1] if sentences(p) else p for p in paras]
    per100 = lambda k: 100 * k / n
    caps_mid = re.findall(r'(?<![.!?]\s)(?<!^)\b[A-Z][a-z]+', t)
    return {
        'words': len(words),
        'sent_mean': st.mean(sl),
        'sent_sd': st.pstdev(sl),
        'short_sent_share': sum(1 for x in sl if x <= 6) / len(sl),
        'long_sent_share': sum(1 for x in sl if x >= 30) / len(sl),
        'paragraphs': len(paras),
        'quotes_per100': per100(len(re.findall(r'["“]', t))),
        'contractions_per100': per100(len(re.findall(r"\b\w+['’](?:t|s|re|ve|ll|d|m)\b", t))),
        'i_per100': per100(len(re.findall(r'\b(?:I|me|my|mine)\b', t))),
        'numbers_per100': per100(len(re.findall(r'\b\d[\d,.]*\b', t))),
        'names_per100': per100(len(caps_mid)),
        'questions_per100': per100(t.count('?')),
        'semicolons_per100': per100(t.count(';')),
        'colons_per100': per100(t.count(':')),
        'dashes_per100': per100(len(re.findall(r'—|--| - ', t))),
        'parens_per100': per100(t.count('(')),
        'abstract_per100': per100(len(ABSTRACT.findall(t))),
        'lesson_phrases': len(LESSON.findall(t)),
        'para_end_short_share': sum(1 for s in last if len(s.split()) <= 8) / len(last),
    }


def main(argv):
    out, groups = argv[0], [a.split('=', 1) for a in argv[1:]]
    res = {}
    for name, pat in groups:
        files = sorted(glob.glob(pat))
        res[name] = {f.split('/')[-1]: features(body(f)) for f in files}
    keys = list(next(iter(next(iter(res.values())).values())).keys())
    print(f"{'feature':22s}" + ''.join(f'{g:>11s}' for g in res))
    for k in keys:
        print(f'{k:22s}' + ''.join(f'{st.mean(v[k] for v in res[g].values()):11.2f}' for g in res))
    print(f"{'n':22s}" + ''.join(f'{len(res[g]):11d}' for g in res))
    json.dump(res, open(out, 'w'), indent=1)


if __name__ == '__main__':
    main(sys.argv[1:])

"""Keyword scan of judge evidence by condition. usage: python3 cues.py B TAG run [run...]"""
import json, sys, re, os
sys.path.insert(0, os.path.dirname(__file__)); from wfread import results
B, tag, runs = sys.argv[1], sys.argv[2], sys.argv[3:]
P = json.load(open(f'{B}/piles_{tag}.json'))
CUES = {
 'errors/grammar': r'error|typo|misspell|grammat|ungrammat|missing (period|article|apostrophe)|subject-verb|run-on',
 'non-native/awkward': r'non-native|awkward|clunky|odd(ly)? phras|unidiomatic|slip',
 'inconsistency': r'inconsisten|mismatch|contradict',
 'polished/fluent': r'polish|fluent|smooth|clean|tidy|flawless|frictionless',
 'stock transitions': r'stock|transition|signpost|"overall|to address|these results (indicate|show)',
 'hedge': r'hedg|to my knowledge|we believe|we judge|balanced',
 'conversational/casual': r'conversational|casual|chatty|friendly|simplif|everyday',
 'gloss/explain': r'gloss|explain(s|ed)? (the|what)|defin(es|ing) term|lay reader',
 'arc/structure': r'arc|template|formula|structure|enumerat|first\.\.\.|neatly|evenly',
 'promotional/grand': r'promot|grand|revolution|potential|hype|sweeping|overclaim',
 'jargon/technical': r'jargon|technical|abbreviat|acronym',
 'formatting/lists': r'keyword|numbered|list|paragraph break|two paragraphs|format',
 'personal voice': r'personal|first[- ]person|"i |\bi\b|voice',
 'specific data': r'specific|concrete|numbers|figure|data',
}
rows = {}
for run in runs:
    for pile, r in results(run).items():
        for t in r['texts']:
            m = P['map'].get(t['label'].strip())
            if m: rows.setdefault(m['cond'], []).append(t['evidence'].lower())
conds = sorted(rows, key=lambda c: (c != 'H', c))
print('cue'.ljust(24) + ''.join(c.rjust(7) for c in conds))
for k, rx in CUES.items():
    print(k.ljust(24) + ''.join(f'{100 * sum(bool(re.search(rx, e)) for e in rows[c]) / len(rows[c]):6.0f}%' for c in conds))
print('n'.ljust(24) + ''.join(f'{len(rows[c]):7d}' for c in conds))

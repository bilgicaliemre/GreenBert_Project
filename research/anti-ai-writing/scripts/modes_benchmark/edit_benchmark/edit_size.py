"""Edit size: share of the original's words changed by an edit.
Texts are split on whitespace; difflib.SequenceMatcher (autojunk off) aligns original and edit; every non-equal opcode counts
max(original span, edited span) words; the sum is divided by the original's word count.
usage (from the benchmark folder): python3 edit_size.py GENRE COND [COND...] [--split dev|test]"""
import difflib, json, statistics as st, sys

def edit_size(orig, edit):
    a, b = orig.split(), edit.split()
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    return sum(max(i2 - i1, j2 - j1) for t, i1, i2, j1, j2 in sm.get_opcodes() if t != 'equal') / len(a)

if __name__ == '__main__':
    args = sys.argv[1:]; split = None
    if '--split' in args: split = args[args.index('--split') + 1]; args = args[:args.index('--split')]
    g, conds = args[0], args[1:]
    items = [it for it in json.load(open(f'eb/{g}/items.json')) if split is None or it.get('split') == split]
    for c in conds:
        v = [edit_size(open(f'eb/{g}/real/{it["rid"]}.txt').read(), open(f'eb/{g}/{c}/{it["rid"]}.txt').read()) for it in items]
        print(f'{g} {c} n={len(v)} mean share of words changed {st.mean(v):.2f}')

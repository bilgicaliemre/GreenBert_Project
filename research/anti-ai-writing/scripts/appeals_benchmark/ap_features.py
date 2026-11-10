"""Surface features of appeals per condition (no model calls).
usage: python3 ap_features.py BENCH_DIR IDS_JSON CONDS [OUT.json]   (R = bench/real)"""
import json, re, sys, statistics as st
bench, ids, conds = sys.argv[1], json.load(open(sys.argv[2])), sys.argv[3].split(',')
EMO = re.compile(r'[\U0001F300-\U0001FAFF☀-➿❤✨]')
def tl(s): return s.replace('İ', 'i').replace('I', 'ı').lower()
def feats(t):
    w = t.split(); n = max(1, len(w)); low = tl(t)
    sents = [s for s in re.split(r'(?<=[.!?…])\s+|\n+', t) if len(s.split()) >= 2]
    sl = [len(s.split()) for s in sents]
    return {
        'words': len(w), 'sent_len': st.mean(sl) if sl else 0, 'sent_sd': st.pstdev(sl) if len(sl) > 1 else 0,
        'paras': len([p for p in re.split(r'\n\s*\n', t) if p.strip()]), 'lines': len([l for l in t.split('\n') if l.strip()]),
        'excl_100w': 100 * t.count('!') / n, 'quest': t.count('?'), 'ellipsis': len(re.findall(r'\.\.\.|…', t)),
        'emoji': len(EMO.findall(t)), 'caps_words': len(re.findall(r'\b[A-ZÇĞİÖŞÜ]{3,}\b', t)),
        'elongated': len(re.findall(r'(\w)\1\1', low)), 'tl_amounts': len(re.findall(r'\d[\d.,]*\s*(?:tl|lira|₺)', low)),
        'numbers': len(re.findall(r'\d+', t)),
        'greeting': int(bool(re.match(r'\s*(merhaba|sevgili|değerli|selam|herkese|canım|dostlar)', low))),
        'thanks': int('teşekkür' in low), 'sen_address': len(re.findall(r'\b(sen|seni|sana|senin)\b|\w+(abilirsin|ebilirsin|arsan|ersen)\b', low)),
        'siz_address': len(re.findall(r'\b(siz|sizi|size|sizin|sizler|sizlerin)\b|\w+(abilirsiniz|ebilirsiniz|arsanız|erseniz|ınız|iniz)\b', low)),
        'hashtags': len(re.findall(r'#\w', t)), 'dash': t.count('—') + t.count(' – '), 'colon_lists': len(re.findall(r'^\s*[-•*]', t, re.M)),
    }
rows = {}
for c in conds:
    rows[c] = [feats(open(f'{bench}/real/{i}.txt' if c == 'R' else f'{bench}/{c}/{i}.txt').read()) for i in ids]
keys = list(rows[conds[0]][0])
print(f"{'':12s}" + ''.join(f'{c:>9s}' for c in conds))
out = {}
for k in keys:
    out[k] = {c: st.mean(r[k] for r in rows[c]) for c in conds}
    print(f'{k:12s}' + ''.join(f'{out[k][c]:9.2f}' for c in conds))
if len(sys.argv) > 4:
    json.dump({'means': out, 'rows': rows}, open(sys.argv[4], 'w'), indent=1)

"""Clean and screen the collected appeals (private corpus).
Cleaning: drop link lines, the platform's default template sentences and the sign-off name line (no runner names
reach notes, piles or judges). Screening: drop texts under 60 words after cleaning, texts shared across pages
(NGO copy, team texts) and texts with almost no first-person voice.
usage: python3 screen.py corpus.jsonl screened.json"""
import json, re, sys
TEMPLATE = ['şikayetçi olmak yerine', 'beni çok mutlu edersin', 'bağış yapmak çok kolay', 'adımlarıma anlam katacağım',
            'dostum/iş arkadaşım', 'sadece şikayet etmiyorum', 'hazırladığım sayfamda', 'adımlarımla tanıdıklarımı',
            'aşağıdaki bağlantıya giderek', 'beni desteklemek için sen de bağış yap', 'kampanyamın son durumunu merak',
            'projesini destekleyeceğim', 'iyilik peşinde koşacağım', 'iyilik peşinde koşarak', 'farkındalık arttıkça, çözüm',
            'adımlarımla çevremdekileri']
SIGN = re.compile(r'^(sevgiler|sevgilerimle|saygılar|saygılarımla|teşekkürler|teşekkür ederim|sevgiler, saygılar|sevgi ve saygılarımla)[.!,]*$')
def tl(s):
    return s.replace('İ', 'i').replace('I', 'ı').lower()
def clean(t):
    lines = [l.strip() for l in t.split('\n')]
    lines = [l for l in lines if not re.search(r'https?://|www\.|adimadim\.org|@\w|\S+@\S+\.\w', l)]
    out = []
    for l in lines:
        parts = re.split(r'(?<=[.!?…])\s+', l)
        keep = [p for p in parts if not any(x in tl(p) for x in TEMPLATE)]
        out.append(' '.join(keep) if keep or not l else None)
    lines = [l for l in out if l is not None]
    while lines and not lines[-1]:
        lines.pop()
    # sign-off: a short name line at the end, usually after "Sevgiler"
    if len(lines) >= 2 and SIGN.match(tl(lines[-2])) and len(lines[-1].split()) <= 3:
        lines.pop()
    elif lines and len(lines) > 2 and re.fullmatch(r"[A-ZÇĞİÖŞÜ][\wçğıöşü]+( [A-ZÇĞİÖŞÜ][\wçğıöşü]+)?[\W_]*", lines[-1]):
        lines.pop()
    while lines and not lines[-1]:
        lines.pop()
    t = '\n'.join(lines)
    return re.sub(r'\n{3,}', '\n\n', t).strip()
FIRST = re.compile(r"\b(ben|benim|bana|beni|bende|benden|biz|bizim|bize|bizi|bizler|kendim)\b|\w+(yorum|yoruz|acağım|eceğim|acağız|eceğiz|abilirim|ebilirim|dım|dim|dum|düm|tım|tim|tum|tüm|dık|dik|duk|dük)\b")
rows = [json.loads(l) for l in open(sys.argv[1])]
for r in rows:
    r['clean'] = clean(r['text']); r['cwords'] = len(r['clean'].split())
def sh(t):
    w = re.findall(r'\w+', tl(t)); return {' '.join(w[i:i + 5]) for i in range(len(w) - 4)}
S = [sh(r['clean']) for r in rows]
keep, drop = [], []
for i, r in enumerate(rows):
    dup = max((len(S[i] & S[j]) / max(1, min(len(S[i]), len(S[j]))) for j in range(len(rows)) if j != i), default=0)
    first = len(FIRST.findall(tl(r['clean'])))
    why = 'long' if r['cwords'] > 300 else 'short' if r['cwords'] < 60 else 'shared' if dup >= 0.15 else 'no_voice' if first < 2 else ''
    (drop if why else keep).append({**r, 'why': why, 'dup': round(dup, 2), 'first': first})
json.dump({'keep': keep, 'drop': drop}, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1)
print(len(rows), 'collected,', len(keep), 'kept;', 'dropped:', {w: sum(d['why'] == w for d in drop) for w in ['long', 'short', 'shared', 'no_voice']})
for d in drop: print('  drop', d['code'], d['why'], d['cwords'], d['dup'], d['first'], d['project'][:50])

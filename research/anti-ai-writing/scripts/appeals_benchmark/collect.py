"""Sample runner appeal texts ('Neden Koşuyorum') from ipk.adimadim.org campaign pages (robots.txt allows all).
Polite: one request per second, random codes from pre-ChatGPT events, stop at a target count.
Output: corpus.jsonl (private research corpus; never commit). Runner names are not stored."""
import re, html, json, random, time, hashlib, sys, urllib.request
TARGET, MAXREQ = int(sys.argv[1]), int(sys.argv[2])
rng = random.Random(20261103)
codes = rng.sample(range(8000, 88000), MAXREQ)
seen, per_proj, n_ok = set(), {}, 0
out = open('corpus.jsonl', 'a', encoding='utf-8')
def clean(s):
    s = re.sub(r'<br\s*/?>', '\n', s); s = re.sub(r'<[^>]+>', '', s); s = html.unescape(s)
    return '\n'.join(l.strip() for l in s.replace('\r', '').split('\n')).strip()
for k, c in enumerate(codes):
    code = f'CC{c}'
    try:
        t = urllib.request.urlopen(urllib.request.Request(f'https://ipk.adimadim.org/kampanya/{code}', headers={'User-Agent': 'Mozilla/5.0'}), timeout=30).read().decode('utf-8', 'replace')
    except Exception as e:
        time.sleep(1.5); continue
    m = re.search(r'<h4>Neden Koşuyorum</h4>\s*<p>(.*?)</p>', t, re.S)
    pj = re.search(r'Yardım Projem:\s*</[^>]+>\s*(?:<[^>]+>\s*)*([^<]+)<', t)
    proj = html.unescape(pj.group(1)).strip() if pj else ''
    yr = re.search(r'-(20\d\d)-', proj)
    if m and yr and int(yr.group(1)) <= 2022:
        why = clean(m.group(1)); w = len(why.split())
        h = hashlib.md5(re.sub(r'\W+', '', why.lower()).encode()).hexdigest()
        key = re.sub(r'-\d{4}-', '-', proj)
        if w >= 70 and h not in seen and per_proj.get(key, 0) < 2:
            seen.add(h); per_proj[key] = per_proj.get(key, 0) + 1; n_ok += 1
            out.write(json.dumps({'code': code, 'project': proj, 'year': int(yr.group(1)), 'words': w, 'text': why}, ensure_ascii=False) + '\n'); out.flush()
            print(f'{n_ok} ok after {k + 1} requests: {proj[:60]} ({w} words)', flush=True)
            if n_ok >= TARGET: break
    time.sleep(1.0)
print('done', n_ok, 'kept of', k + 1, 'requests')

import json, re, html, random, time, requests
idx = json.load(open('raw/isef_index.json'))
random.seed(20261105)
by = {}
for pid, r in idx.items():
    key = 'Turkey' if r['query'][1] == 'Turkey' or r['cells'][4] == 'Turkey' else r['query'][0]
    by.setdefault(key, []).append(pid)
pick = list(by.get('Turkey', []))
for k, v in sorted(by.items()):
    if k == 'Turkey': continue
    random.shuffle(v); pick += v[:26]
pick = list(dict.fromkeys(pick))
s = requests.Session(); s.headers['User-Agent'] = 'Mozilla/5.0 (research)'
out = []
for i, pid in enumerate(pick):
    r = idx[pid]
    try:
        h = s.get(r['url'], timeout=40).text
    except Exception as e:
        print('ERR', pid, e); continue
    t = re.sub(r'<script.*?</script>|<style.*?</style>', '', h, flags=re.S)
    segs = [html.unescape(x).strip() for x in re.split(r'<[^>]+>', t)]
    segs = [x for x in segs if x]
    def after(label):
        try: return segs[segs.index(label) + 1]
        except ValueError: return ''
    title = segs[segs.index('Booth Id:') - 1] if 'Booth Id:' in segs else r['cells'][2]
    ab = after('Abstract:')
    out.append({'pid': pid, 'year': int(after('Year:') or r['cells'][0]), 'category': after('Category:'),
                'country': r['cells'][4], 'award': after('Awards Won:'), 'title': title, 'abstract': ab,
                'words': len(ab.split())})
    time.sleep(0.4)
json.dump(out, open('raw/isef_abstracts.json', 'w'), ensure_ascii=False)
import collections
print(len(out), collections.Counter(o['country'] == 'Turkey' for o in out), sorted(collections.Counter(o['words'] // 50 * 50 for o in out).items()))

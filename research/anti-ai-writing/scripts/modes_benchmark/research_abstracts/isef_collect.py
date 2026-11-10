"""Collect ISEF winning abstracts (2014-2021) in categories close to the user's profile, plus all Turkish winners.
Stores no finalist names or schools: only project id, year, category, country, award, title, abstract."""
import re, json, html, time, sys, requests
sys.path.insert(0, '.')
from isef_search import search, BASE
CATS = ['Systems Software','Robotics and Intelligent Machines','Computational Biology and Bioinformatics',
        'Behavioral and Social Sciences','Earth and Environmental Sciences','Environmental Engineering',
        'Mathematics','Energy: Sustainable Materials and Design','Computer Science','Software Design','Energy: Physical','Embedded Systems']
YEARS = list(range(2014, 2022))
def rows(h):
    t = re.sub(r'<script.*?</script>|<style.*?</style>', '', h, flags=re.S)
    out = []
    for tr in re.findall(r'<tr[^>]*>(.*?)</tr>', t, re.S):
        tds = re.findall(r'<td[^>]*>(.*?)</td>', tr, re.S)
        link = re.search(r'href="(/Home/FullAbstract\?[^"]+)"', tr)
        if not link or len(tds) < 5: continue
        cells = [re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', c))).strip() for c in tds]
        pid = re.search(r'projectId=(\d+)', link.group(1)).group(1)
        out.append({'pid': pid, 'cells': cells, 'url': BASE.rstrip('/') + html.unescape(link.group(1))})
    return out
found = {}
queries = [(c, '') for c in CATS] + [('Any Category', 'Turkey')]
for cat, country in queries:
    try:
        h = search(cat=cat, country=country, years=YEARS, winners=True)
    except Exception as e:
        print('ERR', cat, country, e); continue
    rs = rows(h)
    print(cat, country, len(rs), flush=True)
    for r in rs:
        r['query'] = (cat, country)
        found.setdefault(r['pid'], r)
    time.sleep(1)
json.dump(found, open('raw/isef_index.json', 'w'))
print('unique', len(found))

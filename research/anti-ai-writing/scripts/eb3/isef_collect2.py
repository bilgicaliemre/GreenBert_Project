"""EB3: ISEF winning abstracts 2014-2021 from categories never collected before (the earlier collection used 12
categories plus all Turkish winners). Stores no finalist names or schools."""
import re, json, html, time, random, requests, sys
sys.path.insert(0, '.')
from isef_search import search, BASE
from isef_collect import rows
CATS = ['Animal Sciences', 'Biochemistry', 'Biomedical and Health Sciences', 'Biomedical Engineering', 'Cellular and Molecular Biology',
        'Chemistry', 'Microbiology', 'Physics and Astronomy', 'Plant Sciences', 'Materials Science', 'Translational Medical Science', 'Engineering Mechanics']
found = {}
for cat in CATS:
    try: h = search(cat=cat, years=list(range(2014, 2022)), winners=True)
    except Exception as e: print('ERR', cat, e); continue
    rs = [r for r in rows(h) if r['cells'][4] != 'Turkey']
    print(cat, len(rs), flush=True)
    for r in rs: r['query'] = cat; found.setdefault(r['pid'], r)
    time.sleep(1)
json.dump(found, open('raw/isef_index2.json', 'w'))
print('unique', len(found))

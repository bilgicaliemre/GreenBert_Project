"""EB3 selection: 48 ELLIPSE essays (12 per proficiency band, never used: EB1's 32 excluded) and 48 ISEF winning
abstracts 2014-2021 from 12 categories never collected before (4 per category). Stores no names."""
import json, random, os, collections, pandas as pd
rng = random.Random(20261123)
def write(genre, rows):
    B = f'eb3/{genre}'; os.makedirs(f'{B}/real', exist_ok=True)
    rng.shuffle(rows); items = []
    for k, r in enumerate(rows):
        rid = f'{genre[0]}{k + 1:03d}'
        open(f'{B}/real/{rid}.txt', 'w').write(r['text'].strip() + '\n')
        items.append({'rid': rid, 'split': 'test', 'words': len(r['text'].split()), **r['meta']})
    json.dump(items, open(f'{B}/items.json', 'w'), indent=1, ensure_ascii=False)
    print(genre, len(items))
d = pd.read_csv('raw/corpora/ELLIPSE_Final_github_train.csv')
gen = d.full_text.str.contains(r'Generic_|PROPER_NAME|LOCATION_NAME|STUDENT_NAME|TEACHER_NAME|SCHOOL_NAME', regex=True)
# reproduce EB1's selection to exclude it
f1 = d[(~gen) & (d.num_words.between(250, 500)) & (d.grade >= 9) & (d.Overall.between(2.5, 4.0))].sample(frac=1, random_state=20261106)
eb1, per = [], collections.Counter()
for _, r in f1.iterrows():
    if per[r.prompt] >= 3: continue
    per[r.prompt] += 1; eb1.append(r.text_id_kaggle)
    if len(eb1) == 32: break
pool = d[(~gen) & (d.num_words.between(250, 500)) & (d.grade >= 9) & (~d.text_id_kaggle.isin(eb1))].sample(frac=1, random_state=20261123)
BANDS = [(2.0, 2.5), (3.0, 3.0), (3.5, 3.5), (4.0, 4.5)]
rows, per, nb = [], collections.Counter(), collections.Counter()
for _, r in pool.iterrows():
    b = next((i for i, (lo, hi) in enumerate(BANDS) if lo <= r.Overall <= hi), None)
    if b is None or nb[b] >= 12 or per[r.prompt] >= 2: continue
    per[r.prompt] += 1; nb[b] += 1
    rows.append({'text': r.full_text.replace('\r', ''), 'meta': {'prompt': r.prompt, 'grade': int(r.grade), 'overall': float(r.Overall), 'band': b,
                 'grammar': float(r.Grammar), 'conventions': float(r.Conventions), 'src': str(r.text_id_kaggle)}})
print('ell bands', nb, 'excluded eb1', len(eb1))
write('ell', rows)
A = [a for a in json.load(open('raw/isef_abstracts2.json')) if 150 <= a['words'] <= 300 and a['abstract']]
byc = collections.defaultdict(list)
for a in A: byc[a['category']].append(a)
pick = []
for c in sorted(byc): v = byc[c][:]; rng.shuffle(v); pick += v[:4]
print('isef cats', {c: min(4, len(v)) for c, v in byc.items()})
write('isef', [{'text': a['abstract'], 'meta': {'title': a['title'], 'category': a['category'], 'year': a['year'], 'country': a['country'], 'src': a['pid']}} for a in pick])

"""Select 32 real texts per genre for the edit-mode benchmark (16 dev / 16 test). Stores no names."""
import json, random, os, re, collections, pandas as pd
SP = '/tmp/claude-0/-home-user-GreenBert-Project/c9e6db40-731a-54da-a22b-93c87a1090bf/scratchpad'
M = f'{SP}/modes'
rng = random.Random(20261106)
def write(genre, rows):
    B = f'{M}/eb/{genre}'; os.makedirs(f'{B}/real', exist_ok=True)
    rng.shuffle(rows)
    items = []
    for k, r in enumerate(rows):
        rid = f'{genre[0]}{k + 1:03d}'
        open(f'{B}/real/{rid}.txt', 'w').write(r['text'].strip() + '\n')
        items.append({'rid': rid, 'split': 'dev' if k < 16 else 'test', 'words': len(r['text'].split()), **r['meta']})
    json.dump(items, open(f'{B}/items.json', 'w'), indent=1, ensure_ascii=False)
    print(genre, len(items), collections.Counter(i['split'] for i in items))
# ELLIPSE essays
d = pd.read_csv(f'{M}/raw/corpora/ellipse/ELLIPSE_Final_github_train.csv')
gen = d.full_text.str.contains(r'Generic_|PROPER_NAME|LOCATION_NAME|STUDENT_NAME|TEACHER_NAME|SCHOOL_NAME', regex=True)
f = d[(~gen) & (d.num_words.between(250, 500)) & (d.grade >= 9) & (d.Overall.between(2.5, 4.0))].sample(frac=1, random_state=20261106)
rows, per = [], collections.Counter()
for _, r in f.iterrows():
    if per[r.prompt] >= 3: continue
    per[r.prompt] += 1
    rows.append({'text': r.full_text.replace('\r', ''), 'meta': {'prompt': r.prompt, 'grade': int(r.grade), 'overall': float(r.Overall), 'grammar': float(r.Grammar), 'conventions': float(r.Conventions), 'src': r.text_id_kaggle}})
    if len(rows) == 32: break
write('ell', rows)
# ISEF abstracts from the reserve (never used)
A = {a['pid']: a for a in json.load(open(f'{M}/raw/isef_abstracts.json'))}
res = [p for p in json.load(open(f'{M}/ra/reserve_pids.json')) if p in A]
tr = [p for p in res if A[p]['country'] == 'Turkey']; ot = [p for p in res if A[p]['country'] != 'Turkey']
rng.shuffle(ot); pick = tr + ot[:32 - len(tr)]
write('isef', [{'text': A[p]['abstract'], 'meta': {'title': A[p]['title'], 'category': A[p]['category'], 'year': A[p]['year'], 'country': A[p]['country'], 'src': p}} for p in pick])
# Turkish appeals: never-used ones first, then the dev2 check set
s = json.load(open(f'{SP}/appeals/screened_all.json'))['keep']
used = set()
for k in ['ids_dev.json', 'ids_test.json', 'ids_test_orig.json']: used |= set(json.load(open(f'{SP}/appeals/bench/{k}')))
dev2 = set(json.load(open(f'{SP}/appeals/bench/ids_dev2.json')))
unused = [x for x in s if x['code'] not in used and x['code'] not in dev2]
extra = [x for x in s if x['code'] in dev2]
pick = (unused + extra)[:32]
write('app', [{'text': x['clean'], 'meta': {'year': x['year'], 'src': x['code']}} for x in pick])

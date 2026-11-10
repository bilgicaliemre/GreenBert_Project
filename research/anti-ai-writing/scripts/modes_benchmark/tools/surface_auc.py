"""How far do surface features alone separate real pre-2022 writing from model writing? Aggregates only."""
import os, sys, json, glob, numpy as np
sys.path.insert(0, os.path.dirname(__file__)); from tellcheck import features
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
SP = '/tmp/claude-0/-home-user-GreenBert-Project/c9e6db40-731a-54da-a22b-93c87a1090bf/scratchpad'
M = f'{SP}/modes'
data = []  # (genre, label 1=human, cond, text)
def add(genre, d, cond, label, ids=None):
    for f in glob.glob(f'{d}/*.txt'):
        rid = os.path.basename(f)[:-4]
        if ids is not None and rid not in ids: continue
        data.append((genre, label, cond, open(f).read()))
add('abstract', f'{M}/ra/real', 'H', 1)
for c in ['P', 'V9', 'R0', 'R1', 'V10']: add('abstract', f'{M}/ra/{c}', c, 0)
add('short', f'{M}/sa/real', 'H', 1)
for c in ['P', 'S0', 'V10', 'V101']: add('short', f'{M}/sa/{c}', c, 0)
add('appeal', f'{SP}/appeals/bench/real', 'H', 1)
for c in ['P', 'S8', 'S9']: add('appeal', f'{SP}/appeals/bench/{c}', c, 0)
hc_ids = {os.path.basename(f)[:-4] for f in glob.glob(f'{SP}/hc/P/*.txt')}
add('essay', f'{SP}/human_corpus', 'H', 1, hc_ids)
for c in ['P', 'L', 'F', 'G', 'K']: add('essay', f'{SP}/hc/{c}', c, 0)
names = list(features('a b c.').keys()); names.remove('words')
X = np.array([[features(t)[k] for k in names] for _, _, _, t in data]); y = np.array([l for _, l, _, _ in data])
G = np.array([g for g, _, _, _ in data])
res = {}
for g in ['essay', 'short', 'abstract', 'appeal']:
    m = G == g; Xg, yg = X[m], y[m]
    per = {k: roc_auc_score(yg, Xg[:, i]) for i, k in enumerate(names)}
    top = sorted(per.items(), key=lambda kv: -abs(kv[1] - 0.5))[:6]
    clf = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, C=0.5))
    p = cross_val_predict(clf, Xg, yg, cv=StratifiedKFold(5, shuffle=True, random_state=0), method='predict_proba')[:, 1]
    res[g] = {'n_human': int(yg.sum()), 'n_model': int((1 - yg).sum()), 'cv_auc_all_features': roc_auc_score(yg, p),
              'top_single_features_auc': {k: round(v, 3) for k, v in top}}
    print(g, res[g]['n_human'], res[g]['n_model'], 'CV AUC %.3f' % res[g]['cv_auc_all_features'], res[g]['top_single_features_auc'])
# transfer: train on all other genres, test on this one
for g in ['essay', 'short', 'abstract', 'appeal']:
    tr, te = G != g, G == g
    clf = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, C=0.5)).fit(X[tr], y[tr])
    res[g]['transfer_auc'] = roc_auc_score(y[te], clf.predict_proba(X[te])[:, 1]); print(g, 'transfer AUC %.3f' % res[g]['transfer_auc'])
json.dump(res, open(f'{M}/surface_auc.json', 'w'), indent=1)

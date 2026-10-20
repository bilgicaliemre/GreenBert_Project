import json,glob,os,sys
S='/tmp/claude-0/-home-user-GreenBert-Project/c9e6db40-731a-54da-a22b-93c87a1090bf/scratchpad'
def load(p):
    try: return json.load(open(p))
    except Exception: return {}
rows=[]
def add(group,kind,path,r):
    cond=path.split('/')[0] if not path.startswith('/') and '/' in path else ''
    rows.append({'group':group,'kind':kind,'cond':cond,'name':os.path.basename(path).replace('.txt',''),'words':r['words'],'d1':r['desklib'],'d2':r['fakespot']})
for p,r in load(f'{S}/detector/human_essays_results.json').items(): add('Human: admitted college essays (pre-2022)','human',p,r)
for n,(w,a,b) in {'conn_riley-anderson-25':(640,7.9,54.5),'conn_edie-banovic-25':(633,49.8,52.9)}.items():
    rows.append({'group':'Human: admitted college essays (pre-2022)','kind':'human','name':n,'words':w,'d1':a,'d2':b})
for p,r in load(f'{S}/detector/genre_human_results.json').items(): add('Human: top-scored student argument essays (pre-2022)','human',p,r)
EX={'human_explain_berthub_2020.txt':(454,0.8,1.4),'human_explain_conversation_2020.txt':(497,10.6,13.5),'human_explain_conversation_2020_intro.txt':(528,32.8,21.6)}
for n,(w,a,b) in EX.items(): rows.append({'group':'Human: science explainers (2020)','kind':'human','name':n[:-4],'words':w,'d1':a,'d2':b})
for cond,label,kind in [('A','Plain Claude','plain'),('P3','Plain Claude','plain'),('C1','Plain Claude, then skill edit','edit'),('B1','Skill writes it (v1)','skill'),('B2','Skill writes it (v2)','skill2'),('W3','Skill writes it (v3)','skill2'),('N3','Skill writes it (v3)','skill2'),('X4','Skill writes it (v4)','skill2'),('Y4','Skill writes it (v4)','skill2')]:
    for p,r in load(f'{S}/eval/out/{cond}_scores.json').items(): add(label,kind,cond+'/'+p,r)
yy=load(f'{S}/yygs/yygs_scores.json')
json.dump({'rows':rows,'yygs':yy},open(f'{S}/eval/analysis/all_scores.json','w'),indent=1)
import collections
g=collections.defaultdict(list)
for r in rows: g[r['group']].append(r)
for k,v in g.items():
    both=sum(1 for x in v if x['d1']<20 and x['d2']<20)
    print(f"{k:55s} n={len(v):2d} under20(both)={both:2d}  median d1={sorted(x['d1'] for x in v)[len(v)//2]:5.1f} d2={sorted(x['d2'] for x in v)[len(v)//2]:5.1f}")

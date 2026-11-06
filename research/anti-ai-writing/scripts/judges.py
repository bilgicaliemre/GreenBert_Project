import json,collections,sys
NAMES={'A':'plain','B':'v1','C':'edit','V':'v2','P':'plain','W':'v3','N':'v3','X':'v4','Y':'v4'}
def load(p):
    d=json.load(open(p))['result']
    if isinstance(d,dict) and 'judged' in d: return d['judged']
    rs=d.get('results',[]) if isinstance(d,dict) else d
    out=[]
    for r in rs: out+=r.get('judged',[])
    return out
def tally(judged):
    t=collections.defaultdict(lambda: collections.Counter())
    for j in judged:
        code,task=j['pair'].split('-')[0],j['pair'].split('-')[1]
        L,R=NAMES[code[0]],NAMES[code[1]]
        cx,cy=(R,L) if j['swap'] else (L,R)
        m={'X':cx,'Y':cy,'tie':'tie'}
        t[(code,task)]['better_'+m[j['better_writing']]]+=1
        t[(code,task)]['human_'+m[j['more_human']]]+=1
        t[(code,task)]['unsup_'+cx]+=len(j['unsupported_X']); t[(code,task)]['unsup_'+cy]+=len(j['unsupported_Y'])
        t[(code,task)]['n']+=1
    return {f'{k[0]}|{k[1]}':dict(v) for k,v in t.items()}
if __name__=='__main__':
    allj=[]
    for p in sys.argv[1:]: allj+=load(p)
    print(json.dumps(tally(allj),indent=1))

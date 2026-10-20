import json,sys,collections
# pair id "LR-task" or "LR-task-s": L=left cond, R=right cond. swap False => X=left
NAMES={'A':'A','B':'B','C':'C','V':'B2','W':'C2'}
r=json.load(open(sys.argv[1]))['result']
judged,audits=r['judged'],r['audits']
wins=collections.Counter(); human=collections.Counter(); sc=collections.defaultdict(list); unsup=collections.defaultdict(int)
by_task=collections.defaultdict(lambda: collections.Counter())
for j in judged:
    code=j['pair'].split('-')[0]; L,R=NAMES[code[0]],NAMES[code[1]]
    cx,cy=(R,L) if j['swap'] else (L,R)
    m={'X':cx,'Y':cy,'tie':'tie'}
    wins[m[j['better_writing']]]+=1; human[m[j['more_human']]]+=1
    task=j['pair'].split('-')[1]; by_task[task][m[j['better_writing']]]+=1
    for k,c in (('X',cx),('Y',cy)):
        sc[c].append(j[k]); unsup[c]+=len(j['unsupported_'+k])
    print(f"{j['pair']:14s} {j['lens']:7s} better={m[j['better_writing']]:4s} human={m[j['more_human']]:4s} unsupported {cx}:{len(j['unsupported_X'])} {cy}:{len(j['unsupported_Y'])}")
print('better_writing wins',dict(wins)); print('more_human wins',dict(human))
for c,v in sorted(sc.items()):
    avg={k:round(sum(x[k] for x in v)/len(v),2) for k in v[0]}
    print(c,avg,'unsupported total',unsup[c],'n',len(v))
for a in audits:
    print('AUDIT',a['path'].split('/out/')[1],a['tell_count'],'|',a['verdict'][:200])

import json,csv,collections as C
d=json.load(open('/tmp/rca/data/filled.json'))
nf=json.load(open('/tmp/rca/data/notfilled.json'))
names={'esc':{'REQ':'requirements/spec gap','NOTEST':'missing test coverage','INEFF':'test existed but ineffective','REGR':'regression from recent change (RIA miss)','ENV':'environment/config/data difference','THIRD':'third-party/integration/dependency','SCALE':'scale/performance/concurrency/race','LEGACY':'legacy/unknown behavior','DEPLOY':'deployment/release process','MON':'monitoring gap','UNCLEAR':'unclear/not stated'},
 'intro':{'RECENT':'specific recent change','LONG':'long-standing/legacy code','EXT':'external change','UNK':'unknown'},
 'reg':{'Y':'yes','N':'no','U':'unknown'},
 'prev':{'TEST':'test added','MON':'monitoring/alert','PROC':'process change','CODE':'code fix only','NONE':'none stated'}}
rows=[];skip=0
for l in open('/tmp/rca/data/labels.txt'):
    p=l.split()
    if not p: continue
    if p[1]=='SKIP': skip+=1; continue
    k,esc,intro,reg,leg,ai,prev=p; m=d[k][0]
    rows.append(dict(issue_key=k,project=m['project'],r_and_d_vp=m['vp'] or '(empty)',priority=m['priority'],created_month=m['month'],escape_cause=names['esc'][esc],introduced_by=names['intro'][intro],regression=names['reg'][reg],legacy_mentioned='yes' if leg=='Y' else 'no',ai_mentioned='yes' if ai=='Y' else 'no',prevention_action_type=names['prev'][prev]))
out='/Users/Guy.Guterman/ai-quality-discovery-factory/data/aggregates/rca-classification.csv'
with open(out,'w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(sorted(rows,key=lambda r:r['issue_key']))
N=len(rows);tot=N+len(nf)+skip
print(f"sample={tot} filled={N} ({100*N/tot:.1f}%) not_filled={len(nf)+skip} (template-only/empty {len(nf)}, 'N/A' or blank answers {skip})")
for col in ['escape_cause','introduced_by','regression','prevention_action_type','legacy_mentioned','ai_mentioned']:
    c=C.Counter(r[col] for r in rows);print('\n##',col)
    for v,n in c.most_common(): print(f"| {v} | {n} | {100*n/N:.1f}% |")
vp=C.Counter(r['r_and_d_vp'] for r in rows);print('\n## VP',vp.most_common())
top=[v for v,_ in vp.most_common(5)]
esc=[v for v,_ in C.Counter(r['escape_cause'] for r in rows).most_common()]
print('\n| escape_cause | '+' | '.join(top)+' |')
for e in esc: print(f"| {e} | "+' | '.join(str(sum(1 for r in rows if r['escape_cause']==e and r['r_and_d_vp']==v)) for v in top)+' |')
# regression share among those with known
print('\n## months',sorted(C.Counter(r['created_month'] for r in rows).items()))
print('## cross intro x esc RECENT:',C.Counter(r['escape_cause'] for r in rows if r['introduced_by']=='specific recent change').most_common())

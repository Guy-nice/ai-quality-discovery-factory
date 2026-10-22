import json,glob,re,sys
markers=["Describe functional impact of the issue","Describe technical reason for the issue","Indicate the root cause for the issue","Indicate JIRA item which caused this issue","Indicate how the issue was fixed"]
seen={};notfilled=[]
for f in sorted(glob.glob('/tmp/rca/data/*[0-9].json')):
    for n in json.load(open(f))['issues']['nodes']:
        k=n['key']
        if k in seen or k in [x[0] for x in notfilled]: continue
        fl=n['fields'];t=fl.get('customfield_10117') or ''
        vp=(fl.get('customfield_14852') or {}).get('value','') if fl.get('customfield_14852') else ''
        meta=dict(key=k,project=k.split('-')[0],vp=vp,priority=(fl.get('priority') or {}).get('name',''),month=fl['created'][:7])
        hits=sum(m in t for m in markers)
        if not t.strip() or (hits>=4 and len(t)<1100): notfilled.append((k,hits)); continue
        seen[k]=(meta,t)
json.dump({k:[m,t] for k,(m,t) in seen.items()},open('/tmp/rca/data/filled.json','w'))
json.dump(notfilled,open('/tmp/rca/data/notfilled.json','w'))
print('filled',len(seen),'notfilled',len(notfilled))

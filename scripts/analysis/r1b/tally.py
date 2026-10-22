import json,sys,collections
proj=collections.Counter();rep=collections.Counter();lab=collections.Counter();app=0;n=0
for f in sys.argv[1:]:
    d=json.load(open(f))
    for x in d["issues"]["nodes"]:
        n+=1;fl=x["fields"]
        proj[fl["project"]["key"]]+=1
        r=fl.get("reporter") or {}
        if r.get("accountType")=="app": app+=1; rep["app: "+r.get("displayName","?")]+=1
        else: rep["human:"+str(hash(r.get("accountId","none"))%100000)]+=1
        for l in fl.get("labels") or []: lab[l]+=1
print("n",n,"app",app)
print("proj",proj.most_common(15))
print("rep",rep.most_common(10))
print("lab",lab.most_common(20))

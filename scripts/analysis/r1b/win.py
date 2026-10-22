import json,sys,collections
for f in sys.argv[1:]:
    d=json.load(open(f));ns=d["issues"]["nodes"]
    proj=collections.Counter(x["fields"]["project"]["key"] for x in ns)
    days=collections.Counter(x["fields"]["created"][:10] for x in ns)
    rep=collections.Counter(("app:"+r.get("displayName","?")) if r.get("accountType")=="app" else "human" for r in [(x["fields"].get("reporter") or {}) for x in ns])
    nrep=len(set((x["fields"].get("reporter") or {}).get("accountId") for x in ns))
    lab=collections.Counter(l for x in ns for l in (x["fields"].get("labels") or []))
    ids=[int(x["id"]) for x in ns]
    print(f,"n",len(ns),"ids",min(ids),max(ids),"distinct_reporters",nrep)
    print(" proj",proj.most_common(6));print(" days",days.most_common(5));print(" rep",rep.most_common(4));print(" lab",lab.most_common(8))

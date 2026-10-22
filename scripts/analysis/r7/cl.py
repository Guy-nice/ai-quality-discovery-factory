import json,sys
AI=["ai","agent","copilot","claude","cursor","mcp"]
for p in sys.argv[1:]:
    d=json.load(open(p))
    n=d["issues"]["nodes"][0] if "issues" in d else d
    f=n["fields"]; hist=n.get("changelog",{}).get("histories",[])
    created=f.get("created","")[:16]; res=(f.get("resolutiondate") or "")[:16]
    first_prog=None; lab_ev=[]; f229=[]
    for h in sorted(hist,key=lambda h:h["created"]):
        a=h.get("author",{}); at=a.get("accountType","?"); nm=a.get("displayName","")
        who="app" if at=="app" else ("bot?" if any(k in nm.lower() for k in ["automation","bot","service","jira","devops"]) else "user")
        for it in h["items"]:
            fld=it.get("field","")
            if fld=="status" and first_prog is None and (it.get("toString") or "").lower() not in ("new","open","to do","triage","backlog"):
                first_prog=h["created"][:16]
            if fld=="labels":
                new=set((it.get("toString") or "").split())-set((it.get("fromString") or "").split())
                ai=[l for l in new if any(k in l.lower() for k in AI)]
                if ai: lab_ev.append((h["created"][:16],who,ai))
            if "Implemented by AI" in fld or fld in ("AI Model Used",):
                f229.append((h["created"][:16],who,fld,(it.get("toString") or "")[:30]))
    print(n["key"],"created",created,"firstProgress",first_prog,"resolved",res)
    for e in lab_ev: print("   label+",e, "AFTER_RES" if res and e[0]>=res else "BEFORE_RES")
    for e in f229[:3]: print("   field",e)

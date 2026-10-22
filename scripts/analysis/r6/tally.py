import json,sys,collections
RIA_T=["Describe functionality or issue to be fixed","Identify specific components, files","Identify and document specific tests"]
EOR_B_T=["What alerts will notify the team?","Necessary logging added?","Above allows for prompt notification"]
EOR_M_T=["Turn Off Feature Toggle?","Functionality retested after rollback?","Above allows for quickly remediating"]
def cls(t,T):
    if not t or not str(t).strip(): return "empty"
    k=sum(m in t for m in T)
    return "template" if k==len(T) else ("partial" if k>0 else "filled")
def val(v):
    if isinstance(v,list): return ",".join(x.get("value","?") for x in v) or None
    if isinstance(v,dict): return v.get("value")
    return None if v in (None,"") else ("set" if not isinstance(v,(int,float)) else "num")
for name in sys.argv[1:]:
    d=json.load(open(f"/tmp/r6/data/{name}.json")); nodes=d["issues"]["nodes"]
    c=collections.Counter(); tl=0
    for n in nodes:
        f=n["fields"]
        c["ria_"+cls(f.get("customfield_12794"),RIA_T)]+=1
        if "customfield_11588" in f: c["eorB_"+cls(f.get("customfield_11588"),EOR_B_T)]+=1
        if "customfield_11590" in f: c["eorM_"+cls(f.get("customfield_11590"),EOR_M_T)]+=1
        if "customfield_10039" in f: c["ac_"+("filled" if len((f.get("customfield_10039") or "").strip())>20 else "empty_or_short")]+=1
        for k in ["customfield_15229","customfield_15265","customfield_15308","customfield_10196","customfield_10186","customfield_12643","customfield_10111"]:
            if k in f: c[f"{k}={val(f.get(k))}"]+=1
        if any((l.get("outwardIssue") or l.get("inwardIssue"))["fields"]["issuetype"]["name"].startswith("Test") for l in f.get("issuelinks",[])): tl+=1
    print("==",name,"n",len(nodes),"with Test link",tl)
    for k,v in sorted(c.items()): print(" ",k,v)

import json,sys,collections
d=json.load(open(sys.argv[1]))
nodes=d["issues"]["nodes"]
RIA_T=["Describe functionality or issue to be fixed","Identify specific components, files","Identify and document specific tests"]
EOR_B_T=["What alerts will notify the team?","Necessary logging added?","Above allows for prompt notification"]
EOR_M_T=["Turn Off Feature Toggle?","Functionality retested after rollback?","Above allows for quickly remediating"]
def cls(t,T):
    if not t or not str(t).strip(): return "empty"
    k=sum(m in t for m in T)
    return "template" if k==len(T) else ("partial" if k>0 else "filled")
c=collections.Counter(); lt=collections.Counter(); tests=[]
for n in nodes:
    f=n["fields"]
    c["ria_"+cls(f.get("customfield_12794"),RIA_T)]+=1
    c["eorB_"+cls(f.get("customfield_11588"),EOR_B_T)]+=1
    c["eorM_"+cls(f.get("customfield_11590"),EOR_M_T)]+=1
    c["ac_"+("filled" if (f.get("customfield_10039") or "").strip() else "empty")]+=1
    for k in ["customfield_10186","customfield_14678","customfield_10103"]:
        v=f.get(k); val=(v.get("value") if isinstance(v,dict) else v)
        c[k+"="+str(val)]+=1
    nt=0
    for l in f.get("issuelinks",[]):
        o=l.get("outwardIssue") or l.get("inwardIssue")
        it=o["fields"]["issuetype"]["name"]
        lt[(l["type"]["name"],it)]+=1
        if it in ("Test","Test Set","Test Plan","Test Execution"): nt+=1
    tests.append(nt)
print("n",len(nodes))
for k,v in sorted(c.items()): print(k,v)
print("epics with >=1 linked Test*:",sum(1 for x in tests if x>0),"median",sorted(tests)[len(tests)//2])
for k,v in lt.most_common(15): print(k,v)

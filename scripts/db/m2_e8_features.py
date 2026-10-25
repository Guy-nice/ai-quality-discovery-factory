import json,re,sys,glob
def text(v):
    if v is None: return ""
    if isinstance(v,str): return v
    return json.dumps(v)
def clean(t): return re.sub(r"\s+"," ",re.sub(r"[*_#>\-\.\|`]"," ",t)).strip()
SPEC=re.compile(r"atlassian\.net/wiki|confluence|\bPRD\b|figma|spec(ification)?\b|design doc",re.I)
def feats(n):
    f=n["fields"]; ac=clean(text(f.get("customfield_10039"))); de=clean(text(f.get("description")))
    q=(f.get("resolutiondate") or "")[:7]
    qq=q[:4]+"-Q"+str((int(q[5:7])-1)//3+1) if q else None
    return dict(key=n["key"],project=n["key"].split("-")[0],team=(f.get("customfield_10098") or {}).get("value"),
        resolved_q=qq,ac_len=len(ac),ac_real=int(len(ac)>=40),desc_len=len(de),
        points=int(f.get("customfield_10016") is not None),epic=int(bool(f.get("customfield_10014"))),
        spec_link=int(bool(SPEC.search(text(f.get("description")))) or bool(SPEC.search(text(f.get("customfield_10039"))))),
        ai=(f.get("customfield_15229") or {}).get("value") if isinstance(f.get("customfield_15229"),dict) else f.get("customfield_15229"))
out=[]
for p in sys.argv[2:]:
    for n in json.load(open(p))["issues"]["nodes"]: out.append(feats(n))
json.dump(out,open(sys.argv[1],"w"))
print(len(out))

import json,re,sys
d=json.load(open('/tmp/rca/data/filled.json'))
boiler=["Describe functional impact of the issue.","Describe technical reason for the issue.","Indicate the root cause for the issue (gap in process, documentation, workflow, SDLC, etc.).","If regression bug, indicate why Regression Impact Analysis (RIA) didn’t catch the issue in causing epic/story/bug?","Indicate JIRA item which caused this issue.","Indicate how the issue was fixed.","Identify any long term work needed to resolve.","Indicate if the team can add any  alarms or monitors to catch the issue sooner.","Describe changes team will implement in form of work items (JIRA, confluence, templates, process, etc.) to close gap identified on how it was missed."]
heads=["What happened","How did it happen","How was it missed","How was it introduced","How was it fixed","Long-term","Is there an opportunity","What will be done"]
keep={"How did it happen":200,"How was it missed":330,"How was it introduced":160,"What will be done":160}
keys=sorted(d)
a,b=int(sys.argv[1]),int(sys.argv[2])
for i,k in enumerate(keys[a:b],a):
    m,t=d[k]
    for x in boiler: t=t.replace(x,'')
    t=re.sub(r'[*\\#>]','',t); t=re.sub(r'\s+',' ',t)
    pos=[(t.find(h),h) for h in heads if t.find(h)>=0]; pos.sort()
    out=[]
    for j,(p,h) in enumerate(pos):
        e=pos[j+1][0] if j+1<len(pos) else len(t)
        if h in keep:
            s=t[p+len(h):e].strip(' ?:-')[:keep[h]]
            out.append(f"{h.split()[-1].upper()}:{s}")
    if not out: out=[t[:600]]
    print(f"#{i} {k} {m['vp'][:18]} {m['priority']} | "+" | ".join(out))

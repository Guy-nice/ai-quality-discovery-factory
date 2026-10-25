import os,re,sys,sqlite3,json
PAT=re.compile(r"(?i)(password|passwd|pwd|secret|api[_-]?key|apikey|access[_-]?key|client[_-]?secret|token|bearer)\s*[:=]\s*[\"']?([A-Za-z0-9/+_\-\.!@#$%^&*]{8,})|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----|xox[abprs]-[A-Za-z0-9-]{10,}|ghp_[A-Za-z0-9]{30,}|eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.")
hits={}
root=sys.argv[1]
for dp,_,fs in os.walk(os.path.join(root,"data/raw")):
    if "/git/" in dp+"/": continue
    for f in fs:
        p=os.path.join(dp,f)
        try: t=open(p,errors="ignore").read()
        except: continue
        n=len(PAT.findall(t))
        if n: hits[p.replace(root+"/","")]=n
db=sqlite3.connect(os.path.join(root,"data/db/raw_local.sqlite"))
for k,s,r,ri in db.execute("select key,summary,rca,ria from issue_text"):
    n=sum(len(PAT.findall(x or "")) for x in (s,r,ri))
    if n: hits["raw_local:"+k]=n
print(len(hits),"locations"); 
for k,v in sorted(hits.items(),key=lambda x:-x[1])[:25]: print(v,k)

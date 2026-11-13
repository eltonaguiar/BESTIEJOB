import json, urllib.request, urllib.error, time, re, sys, datetime

HDRS={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36","Accept":"application/json"}
KEY=re.compile(r'servicenow|service now|salesforce|mulesoft|agentforce|platform (admin|developer)|sfdc|cmdb|itam', re.I)
cut=(datetime.datetime.utcnow()-datetime.timedelta(days=4)).isoformat()

slugs=[l.strip() for l in open('tools/ats_board_slugs_ca.txt') if l.strip() and not l.startswith('#')]
hits=[]
errs=[]
for line in slugs:
    kind, slug = line.split()[0], line.split()[-1]
    try:
        if kind=='G':
            u=f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"
            with urllib.request.urlopen(urllib.request.Request(u,headers=HDRS),timeout=20) as r:
                d=json.loads(r.read().decode('utf-8','replace'))
            for j in d.get('jobs',[]):
                t=j.get('title') or ''
                upd=j.get('updated_at') or ''
                if KEY.search(t) and upd and '/'+upd[:4]+'/' in '/'+upd or (KEY.search(t) and upd>=cut):
                    hits.append(dict(src='greenhouse',slug=slug,title=t,loc=(j.get('location') or {}).get('name'),updated=upd,url=j.get('absolute_url')))
        elif kind=='L':
            u=f"https://api.lever.co/v0/postings/{slug}?mode=json"
            with urllib.request.urlopen(urllib.request.Request(u,headers=HDRS),timeout=20) as r:
                d=json.loads(r.read().decode('utf-8','replace'))
            for j in (d if isinstance(d,list) else []):
                t=j.get('text') or ''
                ts=j.get('createdAt')
                if KEY.search(t) and ts:
                    dt=datetime.datetime.utcfromtimestamp(ts/1000).isoformat()
                    if dt>=cut:
                        hits.append(dict(src='lever',slug=slug,title=t,loc=(j.get('categories') or {}).get('location'),updated=dt,url=j.get('hostedUrl')))
    except Exception as e:
        errs.append((kind,slug,str(e)[:50]))

print("slug hits",len(hits),"errors",len(errs))
for h in sorted(hits,key=lambda x:x['updated'],reverse=True):
    print(h['updated'][:10],'|',h['slug'][:18].ljust(18),'|',(h['title'] or '')[:56].ljust(56),'|',(h['loc'] or '')[:28])
print("errs sample",errs[:8])
json.dump(hits,open('reports/ats_ca_0900z.json','w'),indent=1)

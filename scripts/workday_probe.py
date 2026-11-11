import json, urllib.request, re, sys
readme = open(r'C:\Users\zerou\.gemini\antigravity\scratch\bestiejob\README.md', encoding='utf-8').read().lower()
tenants = [  # host, tenant, site
 ('bmo.wd3.myworkdayjobs.com','bmo','External'),
 ('cibc.wd3.myworkdayjobs.com','cibc','search'),
 ('td.wd3.myworkdayjobs.com','td','TD_Bank_Careers'),
 ('manulife.wd3.myworkdayjobs.com','manulife','MFCJH_Jobs'),
 ('sunlife.wd3.myworkdayjobs.com','sunlife','Experienced-Jobs'),
 ('intactfc.wd3.myworkdayjobs.com','intactfc','Intact'),
 ('rbc.wd3.myworkdayjobs.com','rbc','RBC_Careers'),
 ('cppib.wd10.myworkdayjobs.com','cppib','CPPIB'),
 ('otppb.wd3.myworkdayjobs.com','otppb','OTPP_Careers'),
 ('omers.wd3.myworkdayjobs.com','omers','OMERS_External'),
 ('canadalife.wd3.myworkdayjobs.com','canadalife','CL_External'),
 ('telus.wd3.myworkdayjobs.com','telus','TELUS'),
 ('rogers.wd3.myworkdayjobs.com','rogers','RogersCareers'),
 ('uhn.wd3.myworkdayjobs.com','uhn','UHN'),
 ('metrolinx.wd3.myworkdayjobs.com','metrolinx','Metrolinx'),
 ('wsib.wd3.myworkdayjobs.com','wsib','WSIB'),
 ('desjardins.wd10.myworkdayjobs.com','desjardins','Desjardins'),
 ('nbc.wd3.myworkdayjobs.com','nbc','National_Bank'),
 ('loblaw.wd3.myworkdayjobs.com','loblaw','External'),
 ('cnr.wd3.myworkdayjobs.com','cnr','CN_Careers'),
]
queries = ['ServiceNow','Salesforce','Power BI','Tableau','Data Engineer','Reporting Analyst','Business Intelligence','Alteryx']
out=[]
for host,t,site in tenants:
    url=f'https://{host}/wday/cxs/{t}/{site}/jobs'
    ok=False
    for q in queries:
        body=json.dumps({"appliedFacets":{},"limit":20,"offset":0,"searchText":q}).encode()
        try:
            req=urllib.request.Request(url,body,{'Content-Type':'application/json','Accept':'application/json'})
            d=json.load(urllib.request.urlopen(req,timeout=15)); ok=True
        except Exception as e:
            print('FAIL',host,site,str(e)[:60]); break
        for j in d.get('jobPostings',[]):
            title=j.get('title',''); path=j.get('externalPath','')
            if q.lower().split()[0] not in title.lower() and q not in ('Data Engineer','Reporting Analyst','Business Intelligence'): pass
            link=f'https://{host}/en-US/{site}{path}'
            new = path.lower().split('/')[-1] not in readme and title.lower() not in readme
            out.append((t,q,j.get('postedOn',''),title,j.get('locationsText',''),link,new))
    if ok: print('OK',host,site)
seen=set()
rel=re.compile(r'servicenow|salesforce|power bi|tableau|data|report|intelligence|analytics|alteryx|bi\b',re.I)
for r in out:
    if r[5] in seen or not rel.search(r[3]): continue
    seen.add(r[5])
    if r[6]: print('NEW',' | '.join(r[:6]))
print('total relevant',len(seen),'new',sum(1 for r in out if r[6] and rel.search(r[3])))

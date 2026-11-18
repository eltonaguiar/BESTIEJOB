#!/usr/bin/env python3
"""Read-only discovery on documented public ATS job-list APIs. Output is NOT a board of verified jobs.
Default is offline (--plan implied). Only pass --read for sources you are permitted to read in this way.
Python 3.10+, standard library. No applications, credentials, browser automation or auto-publication.
"""
import argparse, csv, datetime as dt, html, json, re, sys, time
from pathlib import Path
from urllib import request, parse, error

HOME = Path(__file__).resolve().parent
SUPPORTED = {'lever','greenhouse','ashby','smartrecruiters'}
SN = re.compile(r'\bservice\s?now\b|\bglide(record|ajax|system)\b|\bscript includes?\b|\bintegrationhub\b',re.I)
SF = re.compile(r'\bsalesforce\b|\blightning web components?\b|\bsoql\b|\bapex triggers?\b',re.I)
OTHER = re.compile(r'\b(?:data(?:base)? (?:programmer|engineer|developer)|master data management|technical integrator|informatica|integration (?:engineer|developer|specialist)|power (?:platform|bi)|etl developer|workflow automation)\b',re.I)

def clean(v):
    return ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', str(v or ''))).split())

def join(vals):
    return ' / '.join(dict.fromkeys(clean(x) for x in vals if x))

def site_url(adapter,t):
    return {'lever':f'https://api.lever.co/v0/postings/{t}', 'greenhouse':f'https://boards-api.greenhouse.io/v1/boards/{t}/jobs', 'ashby':f'https://api.ashbyhq.com/posting-api/job-board/{t}', 'smartrecruiters':f'https://api.smartrecruiters.com/v1/companies/{t}/postings'}[adapter]

class Reader:
    def __init__(self,delay,timeout): self.delay=delay; self.timeout=timeout; self.last=0.; self.count=0
    def get(self,url):
        # Endpoints are built from the adapter allowlist, never scraped URLs. No redirects to arbitrary pages.
        class NoRedirect(request.HTTPRedirectHandler):
            def redirect_request(self,*args): return None
        time.sleep(max(0.,self.delay-(time.monotonic()-self.last))); self.last=time.monotonic(); self.count+=1
        req=request.Request(url,headers={'User-Agent':'TorontoPlatformJobsResearch/1.0 (public posting API; read-only)','Accept':'application/json'})
        with request.build_opener(NoRedirect).open(req,timeout=self.timeout) as r:
            raw=r.read(20_000_001)
            if len(raw)>20_000_000: raise ValueError('board payload over 20 MB: mark incomplete')
            return json.loads(raw)

def scan(source,reader,max_pages,max_details):
    kind=source['adapter']; token=source['board_token']; root=site_url(kind,token); result=[]; status=[]; details=0; n=0
    def add(i,title,url,loc,mode,body,time_kind='',raw_date='',apply=''):
        title=clean(title); text=title+' '+clean(body)
        tracks=[k for k,pat in [('ServiceNow',SN),('Salesforce',SF),('Other',OTHER)] if pat.search(text)]
        if not tracks: return
        result.append(dict(source=source['source_id'],publisher=source['organization'],ats=kind,posting_id=str(i),title=title,posting_url=url,apply_url=apply,location_as_listed=loc,mode_as_listed=mode,time_field=time_kind,time_value=raw_date or '',candidate_tracks=';'.join(tracks),status='lead_only',observed_at_utc=dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()))
    if kind=='lever':
        for page in range(max_pages):
            dat=reader.get(root+'?'+parse.urlencode(dict(mode='json',limit=100,skip=100*page))); assert isinstance(dat,list),'unexpected Lever list'; n+=len(dat)
            for j in dat:
                c=j.get('categories') or {}; parts=[j.get('descriptionPlain') or j.get('description'),j.get('additionalPlain') or j.get('additional')]+[li.get('content') for li in j.get('lists') or []]
                add(j['id'],j['text'],j['hostedUrl'],join([c.get('location')]+(c.get('allLocations') or [])+[j.get('country')]),j.get('workplaceType',''),join(parts),apply=j.get('applyUrl',''))
            if len(dat)<100: break
        else: status.append('page cap reached; coverage may be partial')
    elif kind=='greenhouse':
        dat=reader.get(root+'?content=true')['jobs']; n=len(dat)
        for j in dat:
            add(j['id'],j['title'],j['absolute_url'],(j.get('location') or {}).get('name',''),'',html.unescape(j.get('content') or ''),'updated_at (NOT posted)',j.get('updated_at'))
    elif kind=='ashby':
        dat=reader.get(root)['jobs']; n=len(dat)
        for j in dat:
            if j.get('isListed') is not True: continue
            secondary=[x.get('location') for x in j.get('secondaryLocations') or []]; url=j['jobUrl']
            add(url.rstrip('/').split('/')[-1],j['title'],url,join([j.get('location')]+secondary),j.get('workplaceType',''),j.get('descriptionPlain') or j.get('descriptionHtml'),'publishedAt (LAST published)',j.get('publishedAt'),j.get('applyUrl',''))
    elif kind=='smartrecruiters':
        for page in range(max_pages):
            payload=reader.get(root+'?'+parse.urlencode(dict(limit=50,offset=50*page))); dat=payload['content']; n+=len(dat)
            # Use public job details: list entries often omit duties, and a generic title can be a match.
            for i in dat:
                if details>=max_details:
                    status.append(f'detail cap {max_details} reached; remainder NOT classified'); break
                if i.get('visibility','PUBLIC')!='PUBLIC' or i.get('active') is False: continue
                j=reader.get(root+'/'+parse.quote(str(i['id']),safe='')); details+=1
                if j.get('active') is not True or j.get('visibility')!='PUBLIC': continue
                loc=j.get('location') or {}; sections=(j.get('jobAd') or {}).get('sections') or {}
                add(j['id'],j['name'],j['postingUrl'],loc.get('fullLocation',''),f"remote={loc.get('remote')}; hybrid={loc.get('hybrid')}",join([v.get('text') for v in sections.values() if isinstance(v,dict)]),'releasedDate',j.get('releasedDate'),j.get('applyUrl',''))
            if status or len(dat)<50 or (isinstance(payload.get('totalFound'),int) and (page+1)*50>=payload['totalFound']): break
        else: status.append('page cap reached; coverage may be partial')
    return result,n,'; '.join(status) or 'list pass complete (keyword discovery only)'

def main():
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('--source',nargs='+',required=True,help='source_id(s) from employer-watchlist.csv'); mode=ap.add_mutually_exclusive_group(); mode.add_argument('--read',action='store_true',help='perform permitted GETs');mode.add_argument('--plan',action='store_true',help='show endpoints; no network (default)');ap.add_argument('--out',type=Path,help='optional NEW JSONL leads file; refuses to overwrite'); ap.add_argument('--max-pages',type=int,default=3);ap.add_argument('--max-details',type=int,default=15);ap.add_argument('--delay',type=float,default=2.);ap.add_argument('--timeout',type=int,default=12);a=ap.parse_args()
    if not (1<=a.max_pages<=20 and 1<=a.max_details<=100 and 1<=a.delay<=60 and 1<=a.timeout<=60):ap.error('use bounded caps: pages 1–20, details 1–100, delay/timeout 1–60 s')
    with (HOME/'employer-watchlist.csv').open(encoding='utf-8',newline='') as f: registry={r['source_id']:r for r in csv.DictReader(f)}
    sources=[]
    for k in dict.fromkeys(a.source):
        r=registry.get(k)
        if not r or r['adapter'] not in SUPPORTED or not re.fullmatch(r'[A-Za-z0-9_-]+',r['board_token']):ap.error(f'{k}: no configured public API adapter')
        sources.append(r)
    if not a.read:
        for r in sources: print(r['source_id'],site_url(r['adapter'],r['board_token']))
        return 0
    out=a.out.open('x',encoding='utf-8') if a.out else sys.stdout;reader=Reader(a.delay,a.timeout);errors=0;blocked_hosts=set()
    try:
        for r in sources:
            host=parse.urlsplit(site_url(r['adapter'],r['board_token'])).netloc
            if host in blocked_hosts: print(f"{r['source_id']}: deferred; host blocked/rate-limited earlier",file=sys.stderr); continue
            try:
                found,n,coverage=scan(r,reader,a.max_pages,a.max_details);seen=set()
                for row in found:
                    if row['posting_id'] not in seen: print(json.dumps(row,ensure_ascii=False),file=out);seen.add(row['posting_id'])
                print(f"{r['source_id']}: {n} list entries; {len(seen)} keyword leads; {coverage}",file=sys.stderr)
            except (OSError,ValueError,KeyError,AssertionError,TypeError) as e:
                errors+=1;print(f"{r['source_id']}: INCOMPLETE, not zero jobs: {e}",file=sys.stderr)
                if isinstance(e,error.HTTPError) and e.code in (401,403,429):
                    blocked_hosts.add(host);print('stop this host; inspect terms/Retry-After before rescheduling:',e.headers.get('Retry-After','not specified'),file=sys.stderr)
    finally:
        if a.out:out.close()
    return 1 if errors else 0
if __name__=='__main__':sys.exit(main())

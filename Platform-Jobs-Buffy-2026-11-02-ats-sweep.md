# ServiceNow and Salesforce employer-ATS sweep - 2026-11-02

Agent: Buffy.
Scope: ServiceNow developer/administrator and Salesforce developer/administrator roles in Toronto, or Canada-remote, with emphasis on postings dated 2026-10-31 or 2026-11-01.

## Why employer APIs instead of job boards

Every prior scan in this repo flagged the same problem: aggregators such as Indeed, Randstad and
Alldus render their posting dates client-side, and job-board "1 day ago" labels are refresh or
mirror timestamps, not employer publication dates. This sweep therefore queried the employer
application systems directly, where each record carries its own publication field.

## Sources queried

| System | Companies | Date field used |
|---|---|---|
| Workday CXC (`/wday/cxs/{tenant}/{site}/jobs`) | BMO, TD, McKesson, Medcan, Moneris, Altus Group, CAAT Pension Plan, Irving Oil, BDO, Huron, Brookfield, IKO, Salesforce | `jobPostingInfo.startDate` / `postedOn`, plus `endDate` and `canApply` from the detail record |
| Greenhouse public board API | NeuraFlash, LightFeather, Accenture Federal Services, iCapital, Dscout, Bloomerang, 9th Way Insignia, Kensington Tours and others | `updated_at` / `first_published` |
| Ashby public posting API | Benevity, Loopio, MoeGo and others | `publishedAt` |
| Lever public postings API | Alimentiv, EQ Bank, Versapay and others | `createdAt` |
| SmartRecruiters API | ServiceNow (own careers site) | `releasedDate` |

Keyword filter: role title matching ServiceNow / Salesforce / Agentforce, with a Canada or
Toronto location. Roles were then read through the employer detail record to confirm location,
closing date and application acceptance.

## Result: nothing dated 2026-10-31 or 2026-11-01

October 31, 2026 was a Saturday and November 1 a Sunday. No ServiceNow or Salesforce
developer/administrator record with a weekend publication date appeared for Toronto or
Canada-remote in any system queried. The nearest Canadian publications remain October 29 and
October 30, which are already indexed in the README.

The one "Posted Today" Salesforce administration role found was **not** Canadian:

- Huron, Sales Data Steward & Salesforce Administration Associate (JR-0017061). Employer
  `startDate` 2026-11-02, `endDate` 2026-11-13, `canApply` true. Locations: Bangalore Outer Ring
  Road, Bangalore South 3rd Floor, Noida, Chennai, Pune, Jaipur. Excluded from the Canadian count.

## Additions to the selected list (2)

1. **BMO - Manager, Banking Salesforce Innovation & Enablement (R260030015)**, Toronto, 33 Dundas
   Street West. Workday `startDate` 2026-10-29, `endDate` 2026-11-14, `canApply` true on
   2026-11-02; the job page states an 11/13/2026 application deadline. Management/enablement of
   Salesforce innovation work in Customer Shared Services. Related role, not developer-only; no
   certification named in the inspected description. Added as selected #104.
2. **McKesson - Salesforce Solution Lead (JR0156424)**, Mississauga, ON. Workday `startDate`
   2026-10-27, `canApply` true on 2026-11-02, no `endDate`. The description names Salesforce
   Administrator, Advanced Administrator and App Builder. This is a different requisition from the
   October 29 LinkedIn "Lead Salesforce Solution Architect" mirror already in the README; overlap
   could not be established, so both entries are kept. Added as selected #105.

## Still listed (re-confirmed, no date change)

Alimentiv ServiceNow Platform Specialist (Lever, published 2026-10-27); CAAT ITSM Analyst
(2026-10-30) and ServiceNow Technical Lead; TD Salesforce Loyalty Management Developer; Medcan
Salesforce Developer; Moneris Principal Salesforce Developer; Altus Group Salesforce Platform
Developer; Irving Oil Senior ServiceNow Developer; BDO ServiceNow Senior Developer and Functional
Consultant; Huron ServiceNow Developer (Sr. Associate); McKesson Service Now AI Architect.

## Excluded, with reasons

- Huron JR-0017061: India-only, see above.
- BMO Salesforce Developer R260025118: Chicago, Jacksonville, Chandler, Berkeley Heights - US only.
- ServiceNow Sr. Consultant, Value Excellence (Toronto, `releasedDate` 2026-10-29): consulting
  role, not developer/administrator. The other SmartRecruiters Canadian result, Principal Solution
  Architect, is already selected #02.

## Source limits

- Job Bank Canada (`jobbank.gc.ca`) returned 27 postings for "servicenow" but renders results
  through a separate XHR call; the HTML response contained no per-posting dates or links, so
  nothing was extracted. Its official status is unchanged as a discovery source only.
- Indeed, Randstad search, the Workday board HTML (as opposed to the CXC JSON API) and Alldus
  returned JavaScript-only shells without dates.
- Guessed Workday tenant/site slugs that returned 404 or 422 (for example several bank and
  telco site names) were dropped rather than reported as empty boards.
- No CAPTCHA, login or bot-protection bypass was attempted. No application was submitted.

Absence of a weekend posting in the systems above is a negative result for those systems only.
It is not proof that no brand-new posting exists on a channel this sweep could not read.

## README changes

- New section "2026-11-02 employer-ATS sweep - ServiceNow and Salesforce (Toronto / Canada remote)".
- Two rows added to the Salesforce date-sorted index, two rows added to
  "Salesforce - Canada / Canada-eligible" as #104 and #105.
- Selected-link count 108 to 110; Salesforce recent block 32 to 34; Canada table 22 to 24.

No `jobs.json`, site build, scraper or deployment file was changed, so no automated test applies.

## Second pass - LinkedIn guest listing API (the channel the first pass missed)

The first pass concluded that no 2026-11-01 posting existed. That was wrong for one channel.
`linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search` returns server-rendered job cards
carrying a `datetime` attribute, which is the posting date, and it is readable without a login:

```
https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search
  ?keywords=ServiceNow
  &location=Toronto%2C%20Ontario%2C%20Canada
  &f_TPR=r259200&start=0
```

Filtering `f_TPR` to the last 72 hours and parsing `<time datetime="...">` per card produced:

| Posted | Role | Employer | Location |
|---|---|---|---|
| 2026-11-01 | Senior Consultant, ServiceNow Platform (req 133759) | Deloitte | Toronto / Burlington ON |
| 2026-11-01 | Senior Consultant, Salesforce Platform (req 133770) | Deloitte | Toronto / Burlington / Fredericton |
| 2026-11-01 | Senior Consultant, IT Operations Management / Discovery | Deloitte | Toronto |
| 2026-11-01 | Process Lead Architect, Customer Service Management | Deloitte | Toronto |
| 2026-10-31 | Salesforce Developer - Enhance & Operate | Slalom | Greater Toronto Area |
| 2026-10-31 | ServiceNow Business System Architect | CGI | Ontario |
| 2026-10-31 | Senior Consultant, Artificial Intelligence - Now Assist | Deloitte | Toronto |

Both Deloitte requisitions were confirmed live on `careers.deloitte.ca` on 2026-11-02. Their pages
render dates client-side, so the 2026-11-01 date rests on the LinkedIn card, not on Deloitte's own
field - stated as such in the README rather than presented as employer-verified.

Rejected as duplicates or out of geography: Deloitte's French ITOM / Now Assist cards; Scotiabank's
ServiceNow Discovery Developer and Salesforce Developer cards (already selected with earlier employer
dates - a refresh is not a new posting); KPMG Montreal, CGI Montreal and Master Montreal roles.
Thomson Reuters (Salesforce Engineer, Toronto) and SUN PHARMA (CRM & IC Manager, Mississauga) showed
2026-11-01 dates in an earlier pass but their card URLs were not retained, so they remain leads.

Rate limits: LinkedIn guest search returns HTTP 429 after a handful of queries. The scanner backs off
and retries; 37 unique cards were captured across six queries before throttling.

## Lesson recorded

"Employer ATS only" is a strong method for dates but a weak one for weekend posting volume. Boards
that server-render their cards (LinkedIn guest API) and mirror feeds (Adzuna, White Bay, Procare)
publish on days the ATS crawl sees nothing, and the two methods must be combined before stating that
nothing was posted.

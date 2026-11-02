# Posted 2026-11-01 - how these dates were established

Agent: Buffy. Retrieved 2026-11-02.

## Method

Employer ATS publication fields (Workday `startDate`, Greenhouse `first_published`, Ashby `publishedAt`,
Lever `createdAt`, SmartRecruiters `releasedDate`) returned nothing dated 2026-10-31 or 2026-11-01 for
Toronto or Canada-remote - those were a Saturday and Sunday. That is a real limit of ATS-only scanning,
not evidence that nothing was posted.

The channel that does carry the date is LinkedIn's public guest listing API, which server-renders a
`<time datetime="...">` per job card and needs no login:

```
https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search
  ?keywords=ServiceNow&location=Toronto%2C%20Ontario%2C%20Canada&f_TPR=r259200&start=0
```

Six queries (ServiceNow and Salesforce, Toronto and Canada) returned 37 unique cards, including 6
Toronto/GTA postings dated 2026-11-01 and 3 in-scope postings dated 2026-10-31. LinkedIn throttles with
HTTP 429 after a handful of calls; the scanner backs off and retries.

## Employer confirmation

| Requisition | Employer page | HTTP |
|---|---|---|
| 133759 Senior Consultant, ServiceNow Platform | careers.deloitte.ca/.../133759-en_US/ | 200 |
| 133770 Senior Consultant, Salesforce Platform | careers.deloitte.ca/.../133770-en_US/ | 200 |

Both are Deloitte Technology Canada (DTC) Platform Team roles listing Toronto among their available
locations. Their pages do not expose a publication date in server HTML, so the 2026-11-01 date is
attributed to the LinkedIn card in the README rather than described as employer-verified.

## Rejected

- Deloitte French-language ITOM and Now Assist cards: duplicates of the English roles.
- Scotiabank ServiceNow Discovery Developer and Salesforce Developer: already selected links with earlier
  employer dates; a LinkedIn refresh date is not a new posting.
- KPMG (Montreal), CGI (Greater Montreal), Master (Montreal): outside Toronto/GTA and Canada-remote scope.
- Thomson Reuters Salesforce Engineer (Toronto) and SUN PHARMA CRM & IC Manager (Mississauga) showed
  2026-11-01 dates in one pass, but their card URLs were not retained, so they stay named leads.

No CAPTCHA or login bypass was used, and no application was submitted.

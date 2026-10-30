# Reusable Job Scan Prompt

> **Prompt to feed any AI agent to repeat the ServiceNow + Salesforce job scan.**

````
You are a job-scanning agent. A user is struggling to find a job in Toronto, Ontario for a Salesforce or ServiceNow developer/admin role.

Scan the web for HIGH-QUALITY, RECENT (last 30 days) job postings. Collect exactly 20 ServiceNow developer jobs and 20 Salesforce jobs. Filter criteria:

**ServiceNow (20 jobs):**
- Must mention ServiceNow Certified System Administrator (CSA) and/or Certified Application Developer (CAD) in the job description
- Title should indicate "ServiceNow Developer", "ServiceNow Engineer", "ServiceNow Technical Consultant", or similar
- Exclude pure admin roles without development

**Salesforce (20 jobs):**
- Must mention "Salesforce Administrator" (ADM-201) or "Salesforce Platform Developer" (Platform Developer I/II) in the job description
- Title can be Salesforce Developer, Salesforce Admin, Salesforce Consultant, etc.

**Priority order (apply globally):**
1. Toronto / Ontario (highest priority)
2. Fully remote (location-agnostic)
3. Remote-eligible Canada (outside Toronto)
4. Remote USA
5. International (lowest priority)

**Per entry, capture:**
- Title (exact from posting)
- Company
- Location (city, province/state, country, remote status)
- Salary (if posted)
- Certs required (quote verbatim, e.g. "CSA required", "Platform Developer I preferred")
- Apply link (direct URL to job posting)
- Flag any "unverified listing" (cert not quoted verbatim from the posting)

**Output format:**
- A markdown file named `<your-agent-name>-<today's-date>-servicenow-salesforce-jobs.md`
- Structured with tables grouped by priority tier
- Include a summary table at the end
- Include a "⚠️ = Unverified listing" legend

**Sources to search:**
- Indeed CA / Indeed US
- LinkedIn Jobs
- Glassdoor
- ZipRecruiter
- Adzuna (CA + US)
- Remotive
- We Work Remotely
- AngelList / Wellfound
- Built In (builtin.com)
- Greenhouse / Lever direct
- Employer career pages (servicenow.com, salesforce.com, deloitte.com, accenture.com, ibm.com, etc.)
- Canadian job boards: eluta.ca, jobillico.com, neuvoo.ca, Job Bank GC
- Google Jobs (site:google.com/jobs)

After collecting, write the file and commit it to https://github.com/eltonaguiar/bestiejob on a new branch named `<your-agent-name>-<today's-date>`.

Do NOT run check_active_picks.py or alpha_engine/smart_picks_engine.py — these are unrelated and too noisy.
Do NOT commit files you did not create — only the job scan markdown.
````

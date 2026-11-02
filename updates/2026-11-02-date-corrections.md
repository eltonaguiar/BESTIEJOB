# 2026-11-02 Date Corrections — Adzuna Structured Data Verification

**Agent:** Buffy  
**Branch:** `buffy/2026-11-02-date-corrections`  
**Scope:** Verify employer `datePosted` values for all 14 Adzuna rows claimed as 2026-11-01 or 2026-10-31 in README.

## Findings

### 2026-11-02 (3) — mislabeled as Nov 1
| datePosted | Role | Company | Location |
|------------|------|---------|----------|
| 2026-11-02T01:18:38 | Lead Specialist, ServiceNow CMDB Solution Architect | Deloitte | Toronto |
| 2026-11-02T01:18:38 | Lead Specialist, ServiceNow GRC Solution Architect | Deloitte | Toronto |
| 2026-11-02T01:18:05 | Manager - ServiceNow | KPMG | Montréal |

### 2026-11-01 (4) — correctly labeled
| datePosted | Role | Company | Location |
|------------|------|---------|----------|
| 2026-11-01T04:00:37 | Solutions Architect (ServiceNow) | CGI | Drummondville |
| 2026-11-01T03:58:58 | Stage coopératif - Hiver 2027 Analyste ServiceNow | CGI | Drummondville |
| 2026-11-01T04:12:23 | Salesforce Administrator — Natural Health | White Bay | Toronto |
| 2026-11-01T04:15:12 | Senior Salesforce Developer | Docebo | Toronto |

### 2026-10-30 (3) — mislabeled as Nov 1
| datePosted | Role | Company | Location |
|------------|------|---------|----------|
| 2026-10-30T00:00:00 | Senior Salesforce BSA - Financial Services Cloud | Procom | Toronto |
| 2026-10-30T00:00:00 | Senior Salesforce Administrator | Benevity | Canada |
| 2026-10-30T00:00:00 | Salesforce Industries Cloud Architect (Remote) | CloudKettle | Toronto |

### 2026-10-27 (4) — mislabeled as Oct 31
| datePosted | Role | Company | Location |
|------------|------|---------|----------|
| 2026-10-27T20:54:35 | Salesforce Developer | Epsilon Solutions LTD | Toronto |
| 2026-10-27T20:55:18 | Salesforce CPQ Lead Developer | Epsilon Solutions LTD | Caledon |
| 2026-10-27T20:44:25 | Software Engineer Salesforce Marketing Cloud | Hour Consulting | Toronto |
| 2026-10-27T20:56:39 | Salesforce Business Analyst | Epsilon Solutions LTD | Caledon |

## Conclusion

The README's "Posted 2026-11-01 (10)" and "Posted 2026-10-31 (4)" tables contain **7 incorrect dates**. Only 4 of the 10 claimed Nov 1 rows are actually Nov 1. The "Verified New" LinkedIn section also lacks employer ATS confirmation. No PR is opened to overwrite concurrent PRs #12/#13 per AGENTS.md.

**Source:** Adzuna `application/ld+json` JobPosting nodes (`datePosted`, `validThrough`, `hiringOrganization.name`, `title`).

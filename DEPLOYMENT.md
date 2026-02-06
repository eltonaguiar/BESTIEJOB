# BESTIEJOB Deployment Structure

## Critical Deployment Information

### FTP Server Details
- **Host:** ftps2.50webs.com
- **User:** ejaguiar1
- **Protocol:** FTPS (FTP over TLS)
- **Password:** Stored in `$env:USERPROFILE\.ftp_pass`

### Directory Structure

**IMPORTANT:** BESTIEJOB has a DUAL deployment structure:

1. **Primary Job Board:** `/findtorontoevents.ca/gotjob/`
   - Main job listings page
   - Contains: index.html, app.js, styles.css, jobs.json
   - Also contains subdirectories for resources

2. **Root-Level Resources:** `/findtorontoevents.ca/[resource]/`
   - Navigation links point to root-level paths
   - Must exist at BOTH locations:
     - `/findtorontoevents.ca/salary-insights/`
     - `/findtorontoevents.ca/gotjob/salary-insights/`
     - `/findtorontoevents.ca/career-resources/`
     - `/findtorontoevents.ca/gotjob/career-resources/`
     - etc.

### Local File Structure
```
public/
├── gotjob/                    # Primary job board
│   ├── index.html
│   ├── app.js
│   ├── styles.css
│   ├── jobs.json
│   ├── salary-insights/      # Also copied to root
│   ├── career-resources/     # Also copied to root
│   ├── companies/            # Also copied to root
│   ├── resume-builder/       # Also copied to root
│   ├── interview-prep/       # Also copied to root
│   └── my-jobs/              # Also copied to root
├── salary-insights/          # Root-level copy
├── career-resources/         # Root-level copy
├── companies/                # Root-level copy
├── resume-builder/           # Root-level copy
├── interview-prep/           # Root-level copy
├── my-jobs/                  # Root-level copy
├── ai-match-lab/             # Standalone feature
├── analytics/                # Standalone feature
├── experience-hub/           # Standalone feature
├── market-report/            # Standalone feature
├── mobile-studio/            # Standalone feature
├── tracker/                  # Standalone feature
├── trends/                   # Standalone feature
├── career/                   # Standalone feature
├── salaries/                 # Standalone feature
├── salary/                   # Standalone feature
└── admin/                    # Admin panel
```

### Deployment Scripts

1. **upload-gotjob.js** - Deploys only the gotjob directory
   - Remote path: `/findtorontoevents.ca/gotjob/`
   - Use for: Job board updates only

2. **upload-all-public.js** - Deploys ALL public directories
   - Remote path: `/findtorontoevents.ca/`
   - Use for: Full site deployment or navigation fixes

### Deployment Commands

```powershell
# Set FTP password (required for all uploads)
$env:FTP_PASS = (Get-Content -Path "$env:USERPROFILE\.ftp_pass" -Raw).Trim()

# Deploy only gotjob
node scripts/upload-gotjob.js

# Deploy all directories (use this for navigation fixes)
node scripts/upload-all-public.js
```

### Common Issues & Solutions

**Issue:** Navigation links broken (404 errors)
**Solution:** Resource directories must exist at root level, not just under gotjob/
```powershell
# Copy resources from gotjob to root
Copy-Item -Path "public\gotjob\salary-insights" -Destination "public\salary-insights" -Recurse -Force
# Then deploy all
node scripts/upload-all-public.js
```

**Issue:** Job posting dates not visible
**Solution:** CSS layout issue in gotjob/styles.css
- Ensure `.card` has `max-width: 100%` and `overflow: hidden`
- Ensure `.titleRow` has `width: 100%` and `max-width: 100%`

### URLs

- Main Job Board: https://findtorontoevents.ca/gotjob/
- Salary Insights: https://findtorontoevents.ca/salary-insights/
- Career Resources: https://findtorontoevents.ca/career-resources/
- AI Match Lab: https://findtorontoevents.ca/ai-match-lab/
- Experience Hub: https://findtorontoevents.ca/experience-hub/
- Market Report: https://findtorontoevents.ca/market-report/
- Mobile Studio: https://findtorontoevents.ca/mobile-studio/
- Tracker: https://findtorontoevents.ca/tracker/
- Admin: https://findtorontoevents.ca/gotjob/admin/

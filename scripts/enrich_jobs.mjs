#!/usr/bin/env node
/**
 * Job Enrichment Script
 * Analyzes existing jobs and enriches them with:
 * - Better employment type detection (contract, full-time, part-time, internship, seasonal)
 * - Salary/rate extraction from job descriptions
 * - Recruiter/staffing agency detection
 */

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = path.join(__dirname, "..");

// Known recruiting/staffing firms patterns
const RECRUITING_FIRMS = [
  { pattern: /robert\s*half/i, name: "Robert Half" },
  { pattern: /teksystems/i, name: "TEKsystems" },
  { pattern: /randstad/i, name: "Randstad" },
  { pattern: /hays\s*(technology|it|recruitment)?/i, name: "Hays" },
  { pattern: /procom/i, name: "Procom" },
  { pattern: /s\.?i\.?\s*systems/i, name: "S.i. Systems" },
  { pattern: /altis\s*recruitment/i, name: "Altis Recruitment" },
  { pattern: /experis/i, name: "Experis" },
  { pattern: /manpower/i, name: "Manpower" },
  { pattern: /insight\s*global/i, name: "Insight Global" },
  { pattern: /kforce/i, name: "Kforce" },
  { pattern: /apex\s*systems/i, name: "Apex Systems" },
  { pattern: /kelly\s*services/i, name: "Kelly Services" },
  { pattern: /aerotek/i, name: "Aerotek" },
  { pattern: /modis/i, name: "Modis" },
  { pattern: /adecco/i, name: "Adecco" },
  { pattern: /staffing\s*(agency|firm|company)/i, name: "Staffing Agency" },
  { pattern: /recruiting\s*(agency|firm|company)/i, name: "Recruiting Firm" },
  { pattern: /talent\s*solutions/i, name: "Talent Solutions" },
  { pattern: /placement\s*(agency|firm)/i, name: "Placement Agency" }
];

// Normalize employment type to consistent values
function normalizeEmploymentType(type) {
  if (!type) return "unknown";
  
  // Handle case where type might be an object
  if (typeof type === 'object') {
    type = type.name || type.value || type.type || "unknown";
  }
  
  if (typeof type !== 'string') return "unknown";
  
  const t = type.toLowerCase().replace(/[_\s-]+/g, '-');
  
  // Map variations to standard values
  const mapping = {
    'full-time': 'full-time',
    'fulltime': 'full-time',
    'full_time': 'full-time',
    'ft': 'full-time',
    'permanent': 'full-time',
    'regular': 'full-time',
    'fte': 'full-time',
    
    'part-time': 'part-time',
    'parttime': 'part-time',
    'part_time': 'part-time',
    'pt': 'part-time',
    
    'contract': 'contract',
    'contractor': 'contract',
    'consulting': 'contract',
    'freelance': 'contract',
    'c2c': 'contract',
    'temp-to-perm': 'contract',
    
    'internship': 'internship',
    'intern': 'internship',
    'co-op': 'internship',
    'coop': 'internship',
    'student': 'internship',
    
    'seasonal': 'seasonal',
    'temporary': 'seasonal',
    'temp': 'seasonal',
    
    'remote': 'full-time', // Remote is usually full-time
  };
  
  return mapping[t] || type.toLowerCase();
}

// Employment type patterns
function detectEmploymentType(text) {
  const t = (text || "").toLowerCase();
  
  // Contract indicators
  if (t.includes("contract") || t.includes("contractor") || 
      t.includes("c2c") || t.includes("corp-to-corp") ||
      t.includes("corp to corp") || t.includes("w2 contract") ||
      t.includes("1099") || t.includes("consulting")) {
    return "contract";
  }
  
  // Internship/Co-op indicators
  if (t.includes("intern ") || t.includes("internship") || 
      t.includes("co-op") || t.includes("coop") ||
      t.includes("student") || t.includes("graduate program") ||
      t.includes("entry level") && (t.includes("program") || t.includes("rotation"))) {
    return "internship";
  }
  
  // Part-time indicators
  if (t.includes("part-time") || t.includes("part time") || 
      t.includes("parttime") || t.includes("20 hours") ||
      t.includes("flexible hours") || t.includes("hourly position")) {
    return "part-time";
  }
  
  // Seasonal/Temporary indicators
  if (t.includes("seasonal") || t.includes("temporary") || 
      t.includes("temp ") || t.includes("short-term") ||
      t.includes("short term") || t.includes("limited term") ||
      t.includes("fixed term") || t.includes("maternity cover") ||
      t.includes("parental leave")) {
    return "seasonal";
  }
  
  // Full-time indicators
  if (t.includes("full-time") || t.includes("full time") || 
      t.includes("fulltime") || t.includes("permanent") ||
      t.includes("perm ") || t.includes("direct hire") ||
      t.includes("fte") || t.includes("regular position")) {
    return "full-time";
  }
  
  return "unknown";
}

// Salary/rate extraction
function extractSalary(text) {
  if (!text) return null;
  
  const t = text.toLowerCase();
  
  // Hourly rate patterns: $50/hr, $50-75/hour, $50 - $75 per hour
  const hourlyPatterns = [
    /\$\s*(\d+(?:,\d{3})?(?:\.\d{2})?)\s*(?:-|to|–)\s*\$?\s*(\d+(?:,\d{3})?(?:\.\d{2})?)\s*(?:\/\s*h(?:ou)?r|per\s*h(?:ou)?r|hourly|ph|hr)/gi,
    /\$\s*(\d+(?:,\d{3})?(?:\.\d{2})?)\s*(?:\/\s*h(?:ou)?r|per\s*h(?:ou)?r|hourly|ph|hr)/gi,
    /(\d+(?:\.\d{2})?)\s*(?:dollars?\s*)?(?:per\s*hour|\/\s*hr|hourly)/gi
  ];
  
  for (const pattern of hourlyPatterns) {
    const match = pattern.exec(t);
    if (match) {
      const min = parseFloat(match[1].replace(/,/g, ''));
      const max = match[2] ? parseFloat(match[2].replace(/,/g, '')) : min;
      if (min >= 15 && min <= 500) { // Reasonable hourly range
        return { min, max, type: 'hourly', display: `$${min}${max !== min ? `-$${max}` : ''}/hr` };
      }
    }
  }
  
  // Annual salary patterns: $80,000 - $120,000, $80K-120K
  const annualPatterns = [
    /\$\s*(\d+(?:,\d{3})*)\s*(?:-|to|–)\s*\$?\s*(\d+(?:,\d{3})*)\s*(?:per\s*(?:year|annum)|annually|\/\s*(?:yr|year)|pa)?/gi,
    /(\d+)\s*[kK]\s*(?:-|to|–)\s*(\d+)\s*[kK]/gi,
    /\$\s*(\d+)\s*[kK]\s*(?:-|to|–)\s*\$?\s*(\d+)\s*[kK]/gi,
    /salary[:\s]+\$?\s*(\d+(?:,\d{3})*)/gi,
    /compensation[:\s]+\$?\s*(\d+(?:,\d{3})*)/gi
  ];
  
  for (const pattern of annualPatterns) {
    const match = pattern.exec(t);
    if (match) {
      let min = parseFloat(match[1].replace(/,/g, ''));
      let max = match[2] ? parseFloat(match[2].replace(/,/g, '')) : min;
      
      // Handle K notation
      if (min < 1000) {
        min *= 1000;
        max *= 1000;
      }
      
      if (min >= 30000 && min <= 500000) { // Reasonable annual range
        return { 
          min, max, type: 'annual', 
          display: `$${Math.round(min/1000)}K${max !== min ? `-$${Math.round(max/1000)}K` : ''}/yr` 
        };
      }
    }
  }
  
  return null;
}

// Detect if job is from a recruiting firm
function detectRecruiter(job) {
  const textToCheck = `${job.company || ""} ${job.title || ""} ${job.excerpt || ""} ${job.source || ""}`;
  
  for (const firm of RECRUITING_FIRMS) {
    if (firm.pattern.test(textToCheck)) {
      return firm.name;
    }
  }
  
  return null;
}

// Extract application deadline from job text
function extractDeadline(text) {
  if (!text) return null;
  
  const t = text.toLowerCase();
  
  // Common deadline patterns
  const patterns = [
    // "deadline: January 15, 2026" or "apply by January 15"
    /(?:deadline|apply\s*by|closing\s*date|closes?\s*on|applications?\s*close|due\s*date)[:\s]*([a-z]+\s+\d{1,2}(?:st|nd|rd|th)?,?\s*\d{4})/gi,
    
    // "deadline: Jan 15" (current year implied)
    /(?:deadline|apply\s*by|closing\s*date|closes?\s*on|applications?\s*close|due\s*date)[:\s]*([a-z]+\s+\d{1,2}(?:st|nd|rd|th)?)/gi,
    
    // "deadline: 2026-01-15" ISO format
    /(?:deadline|apply\s*by|closing\s*date|closes?\s*on|applications?\s*close|due\s*date)[:\s]*(\d{4}-\d{2}-\d{2})/gi,
    
    // "deadline: 01/15/2026" or "01-15-2026"
    /(?:deadline|apply\s*by|closing\s*date|closes?\s*on|applications?\s*close|due\s*date)[:\s]*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})/gi,
    
    // "applications will be accepted until January 15"
    /(?:accepted?\s*until|open\s*until)[:\s]*([a-z]+\s+\d{1,2}(?:st|nd|rd|th)?,?\s*\d{0,4})/gi,
    
    // "posting expires: January 15"
    /(?:posting\s*expires?|job\s*expires?)[:\s]*([a-z]+\s+\d{1,2}(?:st|nd|rd|th)?,?\s*\d{0,4})/gi
  ];
  
  for (const pattern of patterns) {
    const match = pattern.exec(t);
    if (match) {
      try {
        // Try to parse the extracted date
        let dateStr = match[1].trim();
        
        // Add current year if not present
        if (!/\d{4}/.test(dateStr) && !/\d{2}[\/\-]\d{2}[\/\-]\d{2,4}/.test(dateStr)) {
          const currentYear = new Date().getFullYear();
          dateStr += `, ${currentYear}`;
        }
        
        const parsed = new Date(dateStr);
        if (!isNaN(parsed.getTime())) {
          // If date is in the past, might be next year
          const now = new Date();
          if (parsed < now && (parsed.getMonth() < now.getMonth() || 
              (parsed.getMonth() === now.getMonth() && parsed.getDate() < now.getDate()))) {
            parsed.setFullYear(parsed.getFullYear() + 1);
          }
          
          return parsed.toISOString().split('T')[0]; // Return YYYY-MM-DD
        }
      } catch (e) {
        // Could not parse, continue to next pattern
      }
    }
  }
  
  return null;
}

function loadJobs() {
  const jobsPath = path.join(PROJECT_ROOT, "jobs.json");
  try {
    const data = fs.readFileSync(jobsPath, "utf8");
    const parsed = JSON.parse(data);
    return Array.isArray(parsed) ? parsed : (parsed.jobs || []);
  } catch (e) {
    console.error("Could not load jobs:", e.message);
    return [];
  }
}

function saveJobs(jobs) {
  const jobsPath = path.join(PROJECT_ROOT, "jobs.json");
  fs.writeFileSync(jobsPath, JSON.stringify(jobs, null, 2));
  
  // Also copy to public directories
  const publicDirs = [
    path.join(PROJECT_ROOT, "public", "jobs.json"),
    path.join(PROJECT_ROOT, "public", "findjobs", "jobs.json"),
    path.join(PROJECT_ROOT, "public", "gotjob", "jobs.json")
  ];
  
  for (const dest of publicDirs) {
    try {
      fs.writeFileSync(dest, JSON.stringify(jobs, null, 2));
      console.log(`✓ Saved to ${dest}`);
    } catch (e) {
      console.log(`Could not save to ${dest}`);
    }
  }
}

function main() {
  console.log("╔══════════════════════════════════════════════════════╗");
  console.log("║      JOB ENRICHMENT SCRIPT                           ║");
  console.log("╚══════════════════════════════════════════════════════╝\n");
  
  const jobs = loadJobs();
  console.log(`📂 Loaded ${jobs.length} jobs\n`);
  
  let enrichedCount = 0;
  let salaryCount = 0;
  let recruiterCount = 0;
  let deadlineCount = 0;
  
  const stats = {
    employmentTypes: {},
    recruiters: {},
    hasDeadline: 0
  };
  
  for (const job of jobs) {
    const textForAnalysis = `${job.title || ""} ${job.excerpt || ""} ${job.company || ""}`;
    
    // Normalize existing employment type
    if (job.employmentType) {
      const normalized = normalizeEmploymentType(job.employmentType);
      if (normalized !== job.employmentType) {
        job.employmentType = normalized;
      }
    }
    
    // Enrich employment type if unknown or missing
    if (!job.employmentType || job.employmentType === "unknown") {
      const detectedType = detectEmploymentType(textForAnalysis);
      if (detectedType !== "unknown") {
        job.employmentType = detectedType;
        enrichedCount++;
      }
    }
    
    // Extract salary if missing
    if (!job.salary) {
      const salary = extractSalary(textForAnalysis);
      if (salary) {
        job.salary = salary;
        salaryCount++;
      }
    }
    
    // Detect recruiter if not already set
    if (!job.recruiter) {
      const recruiter = detectRecruiter(job);
      if (recruiter) {
        job.recruiter = recruiter;
        recruiterCount++;
      }
    }
    
    // Extract deadline if not already set
    if (!job.deadline && !job.applicationDeadline) {
      const deadline = extractDeadline(textForAnalysis);
      if (deadline) {
        job.deadline = deadline;
        deadlineCount++;
      }
    }
    
    // Collect stats
    const empType = job.employmentType || "unknown";
    stats.employmentTypes[empType] = (stats.employmentTypes[empType] || 0) + 1;
    
    if (job.recruiter) {
      stats.recruiters[job.recruiter] = (stats.recruiters[job.recruiter] || 0) + 1;
    }
    
    if (job.deadline || job.applicationDeadline) {
      stats.hasDeadline++;
    }
  }
  
  // Save enriched jobs
  saveJobs(jobs);
  
  console.log("\n════════════════════════════════════════════════════════");
  console.log("ENRICHMENT COMPLETE");
  console.log("════════════════════════════════════════════════════════\n");
  
  console.log(`📊 Enrichment Results:
   • Employment types enriched: ${enrichedCount}
   • Salaries extracted: ${salaryCount}
   • Recruiters detected: ${recruiterCount}
   • Deadlines extracted: ${deadlineCount}
   • Jobs with deadlines: ${stats.hasDeadline} (${((stats.hasDeadline / jobs.length) * 100).toFixed(1)}%)
`);
  
  console.log("📈 Employment Type Breakdown:");
  for (const [type, count] of Object.entries(stats.employmentTypes).sort((a, b) => b[1] - a[1])) {
    const pct = ((count / jobs.length) * 100).toFixed(1);
    console.log(`   ${type}: ${count} (${pct}%)`);
  }
  
  if (Object.keys(stats.recruiters).length > 0) {
    console.log("\n🏢 Jobs by Recruiting Firm:");
    for (const [firm, count] of Object.entries(stats.recruiters).sort((a, b) => b[1] - a[1]).slice(0, 10)) {
      console.log(`   ${firm}: ${count}`);
    }
  }
}

main();

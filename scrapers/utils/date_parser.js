/**
 * Utility functions for parsing relative dates from job postings
 * Handles formats like "9 hours ago", "2 days ago", "Just now", etc.
 */

/**
 * Parse a relative date string to an actual Date object
 * @param {string} dateText - The date text (e.g., "9 hours ago", "2 days ago")
 * @returns {Date|null} - The parsed date or null if unparseable
 */
export function parseRelativeDate(dateText) {
  if (!dateText) return null;
  
  const text = dateText.toLowerCase().trim();
  const now = new Date();
  
  // ISO date format (2024-01-15, 2024-01-15T10:30:00Z)
  if (/^\d{4}-\d{2}-\d{2}/.test(text)) {
    const d = new Date(text);
    if (!isNaN(d.getTime())) return d;
  }
  
  // "Just now", "moments ago", "now"
  if (text === "just now" || text === "now" || text.includes("moment")) {
    return now;
  }
  
  // "X seconds ago"
  let match = text.match(/(\d+)\s*(?:seconds?|secs?|s)\s*ago/i);
  if (match) {
    const seconds = parseInt(match[1], 10);
    return new Date(now.getTime() - seconds * 1000);
  }
  
  // "X minutes ago", "X min ago"
  match = text.match(/(\d+)\s*(?:minutes?|mins?|m)\s*ago/i);
  if (match) {
    const minutes = parseInt(match[1], 10);
    return new Date(now.getTime() - minutes * 60 * 1000);
  }
  
  // "X hours ago", "X hr ago"
  match = text.match(/(\d+)\s*(?:hours?|hrs?|h)\s*ago/i);
  if (match) {
    const hours = parseInt(match[1], 10);
    return new Date(now.getTime() - hours * 60 * 60 * 1000);
  }
  
  // "X days ago", "X day ago"
  match = text.match(/(\d+)\s*(?:days?|d)\s*ago/i);
  if (match) {
    const days = parseInt(match[1], 10);
    return new Date(now.getTime() - days * 24 * 60 * 60 * 1000);
  }
  
  // "X weeks ago", "X week ago"
  match = text.match(/(\d+)\s*(?:weeks?|wks?|w)\s*ago/i);
  if (match) {
    const weeks = parseInt(match[1], 10);
    return new Date(now.getTime() - weeks * 7 * 24 * 60 * 60 * 1000);
  }
  
  // "X months ago", "X month ago"
  match = text.match(/(\d+)\s*(?:months?|mos?)\s*ago/i);
  if (match) {
    const months = parseInt(match[1], 10);
    const d = new Date(now);
    d.setMonth(d.getMonth() - months);
    return d;
  }
  
  // "yesterday"
  if (text.includes("yesterday")) {
    return new Date(now.getTime() - 24 * 60 * 60 * 1000);
  }
  
  // "today"
  if (text.includes("today")) {
    return now;
  }
  
  // "a minute ago", "an hour ago", "a day ago", etc.
  if (/^an?\s+minute/i.test(text)) return new Date(now.getTime() - 60 * 1000);
  if (/^an?\s+hour/i.test(text)) return new Date(now.getTime() - 60 * 60 * 1000);
  if (/^an?\s+day/i.test(text)) return new Date(now.getTime() - 24 * 60 * 60 * 1000);
  if (/^an?\s+week/i.test(text)) return new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
  if (/^an?\s+month/i.test(text)) {
    const d = new Date(now);
    d.setMonth(d.getMonth() - 1);
    return d;
  }
  
  // Try parsing as a regular date
  const parsed = new Date(text);
  if (!isNaN(parsed.getTime())) {
    return parsed;
  }
  
  // Date formats: "Jan 15", "January 15, 2024", "15 Jan 2024"
  const monthNames = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"];
  for (let i = 0; i < monthNames.length; i++) {
    if (text.includes(monthNames[i])) {
      // Try to extract day and optionally year
      const dayMatch = text.match(/(\d{1,2})/);
      const yearMatch = text.match(/(\d{4})/);
      
      if (dayMatch) {
        const day = parseInt(dayMatch[1], 10);
        const year = yearMatch ? parseInt(yearMatch[1], 10) : now.getFullYear();
        const d = new Date(year, i, day);
        if (!isNaN(d.getTime())) return d;
      }
    }
  }
  
  return null;
}

/**
 * Get the best available date from a job object
 * Prefers postedDate over scrapedAt, validates the date
 * @param {object} job - The job object
 * @returns {Date} - The best available date
 */
export function getBestJobDate(job) {
  // Try postedDate first
  if (job.postedDate) {
    // If it's a string that looks like a relative date, parse it
    if (typeof job.postedDate === 'string') {
      const parsed = parseRelativeDate(job.postedDate);
      if (parsed) return parsed;
      
      // Try standard date parsing
      const d = new Date(job.postedDate);
      if (!isNaN(d.getTime())) return d;
    } else if (job.postedDate instanceof Date) {
      return job.postedDate;
    }
  }
  
  // Fall back to scrapedAt
  if (job.scrapedAt) {
    const d = new Date(job.scrapedAt);
    if (!isNaN(d.getTime())) return d;
  }
  
  // Last resort: current time
  return new Date();
}

/**
 * Check if a job was posted within a specified time filter
 * @param {object} job - The job object with postedDate/scrapedAt
 * @param {string} filterValue - Filter value (e.g., "15m", "1h", "24h", "week")
 * @returns {boolean} - Whether the job matches the filter
 */
export function isWithinTimeFilter(job, filterValue) {
  if (filterValue === "any") return true;
  
  const jobDate = getBestJobDate(job);
  const now = new Date();
  const diffMs = now - jobDate;
  const diffMinutes = diffMs / (1000 * 60);
  const diffHours = diffMs / (1000 * 60 * 60);
  const diffDays = diffMs / (1000 * 60 * 60 * 24);
  
  switch (filterValue) {
    // Minutes
    case "15m": return diffMinutes <= 15;
    case "30m": return diffMinutes <= 30;
    // Hours
    case "1h": return diffHours <= 1;
    case "2h": return diffHours <= 2;
    case "4h": return diffHours <= 4;
    case "8h": return diffHours <= 8;
    case "12h": return diffHours <= 12;
    case "24h": return diffHours <= 24;
    // Days
    case "2d": return diffDays <= 2;
    case "3d": return diffDays <= 3;
    case "week": return diffDays <= 7;
    case "14d": return diffDays <= 14;
    case "month": return diffDays <= 30;
    default: return true;
  }
}

/**
 * Format a job date for display, showing relative time
 * @param {object} job - The job object
 * @returns {string} - Formatted date string
 */
export function formatJobDate(job) {
  const jobDate = getBestJobDate(job);
  const now = new Date();
  const diffMs = now - jobDate;
  const diffMinutes = Math.floor(diffMs / (1000 * 60));
  const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
  
  // Super fresh
  if (diffMinutes < 1) return "Just now";
  if (diffMinutes < 5) return `${diffMinutes}m ago`;
  if (diffMinutes < 60) return `${diffMinutes} min ago`;
  
  // Hours
  if (diffHours === 1) return "1 hour ago";
  if (diffHours < 24) return `${diffHours} hours ago`;
  
  // Days
  if (diffDays === 1) return "Yesterday";
  if (diffDays < 7) return `${diffDays} days ago`;
  if (diffDays < 14) return "1 week ago";
  if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
  
  // Older
  return jobDate.toLocaleDateString("en-CA", { month: "short", day: "numeric" });
}

export default {
  parseRelativeDate,
  getBestJobDate,
  isWithinTimeFilter,
  formatJobDate
};

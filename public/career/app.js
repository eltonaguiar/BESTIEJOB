const resourceContent = {
  resume: {
    title: 'ATS-Friendly Resume Format',
    content: `
      <h3>Make Your Resume Machine-Readable</h3>
      <ul>
        <li><strong>Use standard headings:</strong> "Work Experience", "Education", "Skills" - not creative alternatives</li>
        <li><strong>Stick to common fonts:</strong> Arial, Calibri, Georgia, or Times New Roman</li>
        <li><strong>Avoid tables and columns:</strong> ATS systems read left-to-right, top-to-bottom</li>
        <li><strong>Use .docx or .pdf:</strong> These are most compatible with ATS systems</li>
        <li><strong>No headers/footers:</strong> Important info can get lost</li>
        <li><strong>Include keywords:</strong> Mirror language from the job description</li>
      </ul>
      <h4>Toronto Tech Tip</h4>
      <p>Many Toronto companies (especially banks) use older ATS systems. Keep formatting simple and save as .docx for best compatibility.</p>
    `
  },
  keywords: {
    title: 'Tech Keywords Guide',
    content: `
      <h3>Essential Keywords by Role</h3>
      <div class="keyword-grid">
        <div class="keyword-category">
          <h4>Frontend</h4>
          <p>React, Vue, Angular, TypeScript, JavaScript, HTML5, CSS3, Webpack, REST APIs, GraphQL</p>
        </div>
        <div class="keyword-category">
          <h4>Backend</h4>
          <p>Node.js, Python, Java, Go, Ruby, PostgreSQL, MongoDB, Redis, Microservices, Docker</p>
        </div>
        <div class="keyword-category">
          <h4>DevOps/Cloud</h4>
          <p>AWS, Azure, GCP, Kubernetes, Terraform, CI/CD, Jenkins, GitHub Actions, Linux</p>
        </div>
        <div class="keyword-category">
          <h4>Data/ML</h4>
          <p>Python, SQL, Pandas, TensorFlow, PyTorch, Spark, Hadoop, Airflow, Tableau, PowerBI</p>
        </div>
      </div>
      <h4>Soft Skills to Include</h4>
      <p>Agile, Scrum, Cross-functional collaboration, Technical documentation, Mentoring, Project management</p>
    `
  },
  achievements: {
    title: 'Quantifying Achievements',
    content: `
      <h3>Show Impact, Not Just Tasks</h3>
      <p><strong>❌ Before:</strong> "Worked on frontend development"</p>
      <p><strong>✅ After:</strong> "Redesigned checkout flow reducing cart abandonment by 23% ($1.2M annual revenue increase)"</p>
      
      <h4>Metrics to Include</h4>
      <ul>
        <li>Performance improvements (page load time reduced by X%)</li>
        <li>Scale (handled X million requests/day)</li>
        <li>Revenue impact ($X saved or generated)</li>
        <li>User impact (X% increase in engagement)</li>
        <li>Team size (led team of X engineers)</li>
        <li>Efficiency (reduced deployment time by X hours/week)</li>
      </ul>
    `
  },
  portfolio: {
    title: 'Portfolio Tips',
    content: `
      <h3>Building a Standout Portfolio</h3>
      <ul>
        <li><strong>Lead with your best project:</strong> First impressions matter</li>
        <li><strong>Show the process:</strong> Include problem, solution, and results</li>
        <li><strong>Make it live:</strong> Deployed projects beat screenshots</li>
        <li><strong>Include code:</strong> Link to GitHub with clean READMEs</li>
        <li><strong>Mobile-friendly:</strong> Many recruiters browse on phones</li>
        <li><strong>Fast loading:</strong> Optimize images and assets</li>
      </ul>
      <h4>Toronto-Specific Projects That Impress</h4>
      <ul>
        <li>Fintech/payment processing apps (major Toronto industry)</li>
        <li>Real estate/MLS integrations (hot Toronto market)</li>
        <li>Healthcare/wellness platforms</li>
        <li>E-commerce solutions</li>
      </ul>
    `
  },
  behavioral: {
    title: 'Behavioral Interview Questions',
    content: `
      <h3>The STAR Method</h3>
      <p><strong>S</strong>ituation → <strong>T</strong>ask → <strong>A</strong>ction → <strong>R</strong>esult</p>
      
      <h4>Common Questions</h4>
      <ul>
        <li>"Tell me about a time you had a conflict with a teammate"</li>
        <li>"Describe a project that failed and what you learned"</li>
        <li>"Give an example of going above and beyond"</li>
        <li>"Tell me about a time you had to learn something quickly"</li>
        <li>"Describe a situation where you had to influence without authority"</li>
      </ul>
      
      <h4>Toronto Tech Culture Notes</h4>
      <p>Canadian companies often value collaboration and humility. Emphasize team achievements alongside personal contributions.</p>
    `
  },
  technical: {
    title: 'Technical Interview Prep',
    content: `
      <h3>Common Technical Interview Formats</h3>
      <ul>
        <li><strong>Live Coding:</strong> LeetCode-style problems, focus on clean code and communication</li>
        <li><strong>Take-Home:</strong> Build a small feature, usually 2-4 hours, focus on best practices</li>
        <li><strong>System Design:</strong> Design scalable systems, focus on trade-offs</li>
        <li><strong>Pair Programming:</strong> Collaborative problem solving</li>
        <li><strong>Code Review:</strong> Reviewing and improving existing code</li>
      </ul>
      
      <h4>Toronto Company Patterns</h4>
      <ul>
        <li><strong>Banks (RBC, TD, Scotia):</strong> Focus on security, compliance, enterprise patterns</li>
        <li><strong>Startups (Shopify, Wealthsimple):</strong> Product sense, rapid iteration, user focus</li>
        <li><strong>Consulting (Deloitte, Accenture):</strong> Client communication, architecture decisions</li>
      </ul>
    `
  },
  'system-design': {
    title: 'System Design Basics',
    content: `
      <h3>Key Concepts to Know</h3>
      <ul>
        <li><strong>Scalability:</strong> Horizontal vs vertical scaling, load balancing</li>
        <li><strong>Databases:</strong> SQL vs NoSQL, indexing, sharding, replication</li>
        <li><strong>Caching:</strong> Redis, CDN, cache invalidation strategies</li>
        <li><strong>Microservices:</strong> Service boundaries, inter-service communication</li>
        <li><strong>Security:</strong> Authentication, authorization, data protection</li>
      </ul>
      
      <h3>Practice Problems</h3>
      <ul>
        <li>Design a URL shortener</li>
        <li>Design a chat application</li>
        <li>Design a ride-sharing app</li>
        <li>Design a news feed</li>
      </ul>
    `
  },
  questions: {
    title: 'Questions to Ask',
    content: `
      <h3>Smart Questions That Impress</h3>
      
      <h4>About the Role</h4>
      <ul>
        <li>"What does success look like in this role at 3, 6, and 12 months?"</li>
        <li>"What are the biggest challenges facing the team right now?"</li>
        <li>"How do you measure engineering productivity?"</li>
      </ul>
      
      <h4>About the Team</h4>
      <ul>
        <li>"What's the ratio of senior to junior engineers?"</li>
        <li>"How does the team handle on-call?"</li>
        <li>"What does the code review process look like?"</li>
      </ul>
      
      <h4>About Growth</h4>
      <ul>
        <li>"What opportunities are there for professional development?"</li>
        <li>"How does the company support continuing education?"</li>
        <li>"What's the typical career path for this role?"</li>
      </ul>
    `
  },
  research: {
    title: 'Market Research',
    content: `
      <h3>Know Your Worth</h3>
      <ul>
        <li><strong>Salary Insights page:</strong> Use our <a href="/salary/">Toronto-specific data</a></li>
        <li><strong>Glassdoor:</strong> Check company-specific salaries</li>
        <li><strong>Levels.fyi:</strong> For large tech companies</li>
        <li><strong>PayScale:</strong> General market data</li>
        <li><strong>Recruiters:</strong> They often have the most current market intel</li>
      </ul>
      
      <h4>Toronto Salary Context</h4>
      <ul>
        <li>Salaries are typically 20-30% lower than US (especially Bay Area)</li>
        <li>Factor in CAD/USD exchange if comparing</li>
        <li>Benefits are often more comprehensive (healthcare, vacation)</li>
        <li>Remote US roles can pay significantly more</li>
      </ul>
    `
  },
  counter: {
    title: 'Counter Offer Strategy',
    content: `
      <h3>When & How to Counter</h3>
      <ul>
        <li><strong>Always counter:</strong> Even if happy with the offer, negotiate 5-10%</li>
        <li><strong>Be specific:</strong> "Based on my research, I was expecting $X"</li>
        <li><strong>Consider the full package:</strong> Base, bonus, equity, benefits</li>
        <li><strong>Have alternatives:</strong> Multiple offers give you leverage</li>
      </ul>
      
      <h3>Email Template</h3>
      <div class="template-box">
        <p>"Thank you for the offer. I'm excited about the opportunity. Based on my research of the Toronto market and my experience with [specific skills], I was expecting a base salary of $X. Is there flexibility in the compensation package?"</p>
      </div>
    `
  },
  benefits: {
    title: 'Benefits & Perks',
    content: `
      <h3>Beyond Base Salary</h3>
      <ul>
        <li><strong>Health Benefits:</strong> Dental, vision, massage, mental health coverage</li>
        <li><strong>Retirement:</strong> RRSP matching (common: 3-6%)</li>
        <li><strong>Learning Budget:</strong> Conference attendance, courses, books</li>
        <li><strong>Remote Work:</strong> Flexible arrangements, home office stipend</li>
        <li><strong>Vacation:</strong> Standard is 3-4 weeks, negotiate for more</li>
        <li><strong>Parental Leave:</strong> Top-up beyond EI is valuable</li>
      </ul>
      
      <h4>Toronto-Specific Considerations</h4>
      <ul>
        <li>Commuter benefits (PRESTO pass)</li>
        <li>Gym memberships (GoodLife, etc.)</li>
        <li>Location flexibility (downtown vs suburban offices)</li>
      </ul>
    `
  },
  equity: {
    title: 'Equity Compensation',
    content: `
      <h3>Understanding Equity</h3>
      <ul>
        <li><strong>Stock Options:</strong> Right to buy shares at a set price</li>
        <li><strong>RSUs:</strong> Restricted Stock Units - actual shares granted</li>
        <li><strong>Vesting:</strong> 4-year vest with 1-year cliff is standard</li>
        <li><strong>Dilution:</strong> Your percentage decreases as company raises money</li>
      </ul>
      
      <h3>Questions to Ask</h3>
      <ul>
        <li>"How many shares are outstanding?" (to calculate your percentage)</li>
        <li>"What's the current 409A valuation?"</li>
        <li>"What's the exercise window if I leave?"</li>
        <li>"Are there any acceleration clauses on acquisition?"</li>
      </ul>
      
      <h4>Tax Implications</h4>
      <p>Stock options have different tax treatment than RSUs. Consult a tax professional, especially for US companies with Canadian employees.</p>
    `
  },
  linkedin: {
    title: 'LinkedIn Optimization',
    content: `
      <h3>Profile Essentials</h3>
      <ul>
        <li><strong>Headline:</strong> Include role + specialty + value proposition</li>
        <li><strong>About:</strong> Tell your story, include achievements with metrics</li>
        <li><strong>Featured:</strong> Pin your best projects or articles</li>
        <li><strong>Skills:</strong> List relevant tech skills, get endorsements</li>
        <li><strong>Recommendations:</strong> Request from managers and colleagues</li>
      </ul>
      
      <h3>Toronto Networking Tips</h3>
      <ul>
        <li>Join Toronto tech groups (TechTO, Toronto JS)</li>
        <li>Connect with recruiters who specialize in your field</li>
        <li>Engage with content from Toronto tech leaders</li>
        <li>Post about your projects and learnings</li>
      </ul>
    `
  },
  meetups: {
    title: 'Toronto Tech Meetups',
    content: `
      <h3>Active Toronto Tech Communities</h3>
      <ul>
        <li><strong>TechTO:</strong> Large monthly meetup, great for networking</li>
        <li><strong>DevTO:</strong> Developer-focused talks</li>
        <li><strong>Toronto JS:</strong> JavaScript community</li>
        <li><strong>Women in Tech:</strong> Various groups supporting diversity</li>
        <li><strong>PyTO:</strong> Python Toronto</li>
        <li><strong>Kubernetes Toronto:</strong> Cloud-native tech</li>
      </ul>
      
      <h3>Conference Scene</h3>
      <ul>
        <li><strong>Collision:</strong> Major tech conference (June)</li>
        <li><strong>Developer Week:</strong> Various specializations</li>
        <li><strong>Fintech Meetups:</strong> Regular events in the financial district</li>
      </ul>
      
      <h3>Virtual Options</h3>
      <p>Many meetups now offer hybrid attendance. Great for introverts or those with scheduling constraints.</p>
    `
  },
  referrals: {
    title: 'Getting Referrals',
    content: `
      <h3>The Referral Strategy</h3>
      <ul>
        <li><strong>Warm connections:</strong> Reach out to former colleagues</li>
        <li><strong>LinkedIn:</strong> Find mutual connections at target companies</li>
        <li><strong>Recruiters:</strong> They often have relationships with hiring managers</li>
        <li><strong>Alumni networks:</strong> University and bootcamp connections</li>
      </ul>
      
      <h3>Asking for Referrals</h3>
      <div class="template-box">
        <p>"Hi [Name], I'm applying for a [Role] position at [Company] and saw you're working there. Would you be comfortable referring me? I've attached my resume for context. Happy to chat more about my background if helpful!"</p>
      </div>
      
      <h3>Referral Notes</h3>
      <p>Many Toronto companies offer referral bonuses ($1000-5000), so employees are often happy to refer qualified candidates.</p>
    `
  },
  recruiters: {
    title: 'Working with Recruiters',
    content: `
      <h3>Types of Recruiters</h3>
      <ul>
        <li><strong>Internal:</strong> Work for the hiring company</li>
        <li><strong>Agency:</strong> Work for recruiting firms (Randstad, Robert Half, etc.)</li>
        <li><strong>Retained:</strong> Specialized search firms for senior roles</li>
      </ul>
      
      <h3>Building Relationships</h3>
      <ul>
        <li>Be responsive and professional</li>
        <li>Clearly communicate your requirements (salary, location, role)</li>
        <li>Keep them updated on your other interviews/offers</li>
        <li>Ask about market trends and salary expectations</li>
      </ul>
      
      <h4>Toronto Recruiting Firms</h4>
      <p>Randstad, Robert Half, TekSystems, Hays, and Procom are major players in the Toronto tech market.</p>
    `
  },
  trending: {
    title: 'Trending Technologies',
    content: `
      <h3>Hot Skills in Toronto (2024-2025)</h3>
      <ul>
        <li><strong>AI/ML:</strong> LLMs, vector databases, prompt engineering</li>
        <li><strong>Cloud:</strong> AWS, Azure, GCP, multi-cloud strategies</li>
        <li><strong>Web3/Blockchain:</strong> Still strong in fintech sector</li>
        <li><strong>DevOps:</strong> Kubernetes, Terraform, platform engineering</li>
        <li><strong>Data:</strong> Real-time analytics, data mesh</li>
      </ul>
      
      <h3>Learning Resources</h3>
      <ul>
        <li><strong>Online:</strong> Coursera, Udemy, Pluralsight</li>
        <li><strong>Free:</strong> freeCodeCamp, The Odin Project</li>
        <li><strong>Documentation:</strong> Always read the official docs first</li>
        <li><strong>Build Projects:</strong> Apply what you learn immediately</li>
      </ul>
    `
  },
  certifications: {
    title: 'Valuable Certifications',
    content: `
      <h3>Worth Considering</h3>
      <ul>
        <li><strong>Cloud:</strong> AWS Solutions Architect, Azure Administrator</li>
        <li><strong>Agile:</strong> Scrum Master (PSM/CSM)</li>
        <li><strong>Security:</strong> CISSP, Security+ (for security roles)</li>
        <li><strong>Data:</strong> Google Data Analytics, Databricks</li>
      </ul>
      
      <h3>When Certifications Help</h3>
      <ul>
        <li>Breaking into a new field</li>
        <li>Consulting roles (clients like to see them)</li>
        <li>Government or regulated industries</li>
        <li>Early career (signal commitment to learning)</li>
      </ul>
      
      <h3>When They Don't</h3>
      <p>For most software engineering roles, practical experience and projects matter more than certifications. Focus on building real things.</p>
    `
  },
  'side-projects': {
    title: 'Side Projects',
    content: `
      <h3>Why Side Projects Matter</h3>
      <ul>
        <li>Show passion and self-motivation</li>
        <li>Demonstrate skills not used in day job</li>
        <li>Learning new technologies in low-risk environment</li>
        <li>Potential for passive income or startup</li>
      </ul>
      
      <h3>Project Ideas That Impress</h3>
      <ul>
        <li><strong>Solve your own problem:</strong> Tools you actually use</li>
        <li><strong>Clone with twist:</strong> Build simplified version of popular app</li>
        <li><strong>API integration:</strong> Combine multiple services creatively</li>
        <li><strong>Open source:</strong> Contribute to existing projects</li>
      </ul>
      
      <h3>Completion Over Perfection</h3>
      <p>One finished project beats ten half-finished ones. Deploy it, write about it, move on to the next.</p>
    `
  },
  'open-source': {
    title: 'Open Source Contribution',
    content: `
      <h3>Getting Started</h3>
      <ul>
        <li>Start with documentation fixes and small bugs</li>
        <li>Find projects you actually use</li>
        <li>Look for "good first issue" labels</li>
        <li>Read contribution guidelines carefully</li>
      </ul>
      
      <h3>Toronto Open Source</h3>
      <ul>
        <li>Shopify (Liquid, Rails)</li>
        <li>Wealthsimple (various projects)</li>
        <li>Mozilla (Toronto office)</li>
        <li>Local meetups often feature OSS maintainers</li>
      </ul>
      
      <h3>Benefits</h3>
      <p>Code review from experienced developers, networking, public proof of skills, learning best practices.</p>
    `
  },
  timeline: {
    title: 'Application Timeline',
    content: `
      <h3>What to Expect</h3>
      <ul>
        <li><strong>Application → Recruiter Screen:</strong> 1-7 days</li>
        <li><strong>Recruiter → Hiring Manager:</strong> 3-7 days</li>
        <li><strong>Technical Interview:</strong> 7-14 days</li>
        <li><strong>Final/Onsite:</strong> 7-14 days</li>
        <li><strong>Offer:</strong> 1-3 days after final</li>
      </ul>
      <p><strong>Total: 2-6 weeks</strong> (can be longer for senior roles)</p>
      
      <h3>Toronto Market Notes</h3>
      <ul>
        <li>Banks often move slower (multiple approval layers)</li>
        <li>Startups can move very quickly (same week offers)</li>
        <li>December and August are slower</li>
        <li>January and September are peak hiring</li>
      </ul>
    `
  },
  followup: {
    title: 'Follow-up Templates',
    content: `
      <h3>After Application (1 week)</h3>
      <div class="template-box">
        <p>"Hi [Name], I applied for the [Role] position last week and wanted to express my continued interest. My experience with [relevant skill] aligns well with your requirements. Happy to provide any additional information."</p>
      </div>
      
      <h3>After Interview (24 hours)</h3>
      <div class="template-box">
        <p>"Thank you for the conversation today. I'm excited about [specific aspect discussed]. Looking forward to the next steps. Please let me know if you need any additional information from me."</p>
      </div>
      
      <h3>After No Response (2 weeks)</h3>
      <div class="template-box">
        <p>"Hi [Name], following up on my interview from [date]. I'm still very interested in the role and would appreciate any update you can share. I'm exploring other opportunities but [Company] remains my top choice."</p>
      </div>
    `
  },
  ghosting: {
    title: 'Handling Ghosting',
    content: `
      <h3>Why It Happens</h3>
      <ul>
        <li>Hiring freezes after interviews start</li>
        <li>Internal candidates get priority</li>
        <li>Recruiters overwhelmed with applicants</li>
        <li>Role put on hold or cancelled</li>
      </ul>
      
      <h3>Your Strategy</h3>
      <ul>
        <li>Follow up twice, then move on</li>
        <li>Don't take it personally</li>
        <li>Keep applying elsewhere</li>
        <li>Document your applications to track ghosters</li>
      </ul>
      
      <h3>Red Flags to Watch</h3>
      <ul>
        <li>Vague job descriptions</li>
        <li>Disorganized interview process</li>
        <li>Unrealistic timelines</li>
        <li>Poor communication from the start</li>
      </ul>
    `
  },
  multiple: {
    title: 'Managing Multiple Offers',
    content: `
      <h3>Timing Strategies</h3>
      <ul>
        <li><strong>Accelerate:</strong> Tell Company B you have an offer from A</li>
        <li><strong>Delay:</strong> Ask Company A for more time to consider</li>
        <li><strong>Be transparent:</strong> Most companies respect honesty</li>
      </ul>
      
      <h3>Comparison Framework</h3>
      <table class="comparison-table">
        <tr><th>Factor</th><th>Weight</th><th>Notes</th></tr>
        <tr><td>Base Salary</td><td>High</td><td>Immediate cash flow</td></tr>
        <tr><td>Equity</td><td>Medium</td><td>Risk-adjusted potential</td></tr>
        <tr><td>Growth</td><td>High</td><td>Learning & promotion path</td></tr>
        <tr><td>Culture</td><td>High</td><td>Day-to-day happiness</td></tr>
        <tr><td>Commute/Remote</td><td>Medium</td><td>Quality of life impact</td></tr>
        <tr><td>Stability</td><td>Medium</td><td>Company financial health</td></tr>
      </table>
      
      <h3>Making the Decision</h3>
      <p>Sleep on it. Talk it through with trusted mentors. Consider which role you'll regret not taking in 5 years.</p>
    `
  }
};

// Modal functionality
const modal = document.getElementById('resourceModal');
const modalTitle = document.getElementById('modalTitle');
const modalBody = document.getElementById('modalBody');

document.querySelectorAll('.resource-link').forEach(link => {
  link.addEventListener('click', (e) => {
    e.preventDefault();
    const key = link.dataset.modal;
    const content = resourceContent[key];
    if (content) {
      modalTitle.textContent = content.title;
      modalBody.innerHTML = content.content;
      modal.style.display = 'flex';
    }
  });
});

document.querySelector('.modal-close')?.addEventListener('click', () => {
  modal.style.display = 'none';
});

modal?.addEventListener('click', (e) => {
  if (e.target === modal) {
    modal.style.display = 'none';
  }
});

// Save checklist state
const checkboxes = document.querySelectorAll('.check-item input');
checkboxes.forEach(cb => {
  cb.addEventListener('change', () => {
    const checked = Array.from(checkboxes).filter(c => c.checked).length;
    const total = checkboxes.length;
    // Could add progress indicator here
  });
});
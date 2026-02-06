// Career Resources App

// Resource data
const resources = [
    {
        id: 1,
        title: 'Crafting the Perfect Resume for Toronto Tech Jobs',
        excerpt: 'Learn how to create a resume that stands out in Toronto\'s competitive tech market. Includes ATS optimization tips and real examples.',
        category: 'resume',
        icon: '📝',
        readTime: '8 min',
        featured: true,
        content: `
      <h2>Introduction</h2>
      <p>In Toronto's competitive tech market, your resume is your first impression. This guide will help you create a resume that gets noticed by both ATS systems and hiring managers.</p>
      
      <h2>Key Components</h2>
      <h3>1. Contact Information</h3>
      <ul>
        <li>Full name and professional title</li>
        <li>Toronto-based phone number</li>
        <li>Professional email address</li>
        <li>LinkedIn profile URL</li>
        <li>GitHub/Portfolio (for tech roles)</li>
      </ul>
      
      <h3>2. Professional Summary</h3>
      <p>Write a compelling 3-4 sentence summary that highlights:</p>
      <ul>
        <li>Your years of experience</li>
        <li>Key technical skills</li>
        <li>Major achievements</li>
        <li>What you're looking for</li>
      </ul>
      
      <h3>3. Work Experience</h3>
      <p>Use the STAR method to describe your accomplishments:</p>
      <ul>
        <li><strong>Situation:</strong> Context of the challenge</li>
        <li><strong>Task:</strong> Your responsibility</li>
        <li><strong>Action:</strong> What you did</li>
        <li><strong>Result:</strong> Quantifiable outcomes</li>
      </ul>
      
      <h2>ATS Optimization Tips</h2>
      <ul>
        <li>Use standard section headings (Experience, Education, Skills)</li>
        <li>Include keywords from the job description</li>
        <li>Avoid tables, images, and complex formatting</li>
        <li>Use standard fonts (Arial, Calibri, Times New Roman)</li>
        <li>Save as .docx or PDF</li>
      </ul>
      
      <h2>Toronto-Specific Tips</h2>
      <ul>
        <li>Highlight experience with Canadian companies</li>
        <li>Mention work authorization status if applicable</li>
        <li>Include bilingual skills (English/French) if relevant</li>
        <li>Reference Toronto tech community involvement</li>
      </ul>
      
      <blockquote>
        "A great resume is not about listing everything you've done—it's about showcasing the impact you've made."
      </blockquote>
      
      <h2>Next Steps</h2>
      <p>Ready to build your resume? Use our <a href="/resume-builder/">Resume Builder</a> to create a professional resume in minutes.</p>
    `
    },
    {
        id: 2,
        title: 'Mastering the Virtual Interview',
        excerpt: 'Virtual interviews are here to stay. Learn best practices for video interviews, from technical setup to body language.',
        category: 'interview',
        icon: '🎥',
        readTime: '6 min',
        featured: true,
        content: `
      <h2>Technical Setup</h2>
      <h3>Before the Interview</h3>
      <ul>
        <li>Test your camera and microphone</li>
        <li>Ensure stable internet connection</li>
        <li>Download and test the video platform</li>
        <li>Have a backup device ready</li>
        <li>Close unnecessary applications</li>
      </ul>
      
      <h3>Environment</h3>
      <ul>
        <li>Choose a quiet, well-lit space</li>
        <li>Use a neutral background</li>
        <li>Position camera at eye level</li>
        <li>Ensure good lighting (face the light source)</li>
        <li>Minimize background noise</li>
      </ul>
      
      <h2>During the Interview</h2>
      <h3>Body Language</h3>
      <ul>
        <li>Look at the camera, not the screen</li>
        <li>Sit up straight and lean slightly forward</li>
        <li>Use hand gestures naturally</li>
        <li>Smile and show enthusiasm</li>
        <li>Avoid fidgeting</li>
      </ul>
      
      <h3>Communication Tips</h3>
      <ul>
        <li>Speak clearly and at a moderate pace</li>
        <li>Pause before answering to gather thoughts</li>
        <li>Use the mute button when not speaking</li>
        <li>Have notes nearby (but don't read from them)</li>
        <li>Ask for clarification if needed</li>
      </ul>
      
      <h2>Common Pitfalls to Avoid</h2>
      <ul>
        <li>Poor lighting or camera angle</li>
        <li>Distracting background</li>
        <li>Not testing technology beforehand</li>
        <li>Multitasking during the interview</li>
        <li>Forgetting to mute notifications</li>
      </ul>
      
      <h2>Practice Makes Perfect</h2>
      <p>Record yourself answering common interview questions to identify areas for improvement. Check out our <a href="/interview-prep/">Interview Prep Center</a> for practice questions.</p>
    `
    },
    {
        id: 3,
        title: 'Negotiating Your Salary in Toronto',
        excerpt: 'Understand your worth and learn effective strategies for salary negotiation in Toronto\'s creative and tech industries.',
        category: 'salary',
        icon: '💰',
        readTime: '10 min',
        featured: true,
        content: `
      <h2>Know Your Worth</h2>
      <p>Before entering negotiations, research salary ranges for your role in Toronto. Use our <a href="/salary-insights/">Salary Insights</a> tool to see current market rates.</p>
      
      <h2>When to Negotiate</h2>
      <ul>
        <li><strong>After receiving an offer:</strong> Never negotiate before you have a written offer</li>
        <li><strong>During annual reviews:</strong> Come prepared with accomplishments</li>
        <li><strong>When taking on new responsibilities:</strong> Document the added value</li>
      </ul>
      
      <h2>Negotiation Strategies</h2>
      <h3>1. Do Your Research</h3>
      <ul>
        <li>Research industry standards for your role</li>
        <li>Consider Toronto's cost of living</li>
        <li>Factor in your experience level</li>
        <li>Account for company size and funding stage</li>
      </ul>
      
      <h3>2. Know Your Numbers</h3>
      <ul>
        <li><strong>Target salary:</strong> Your ideal compensation</li>
        <li><strong>Acceptable range:</strong> What you'd be happy with</li>
        <li><strong>Walk-away point:</strong> Your minimum acceptable offer</li>
      </ul>
      
      <h3>3. Consider Total Compensation</h3>
      <p>Salary is just one component. Also negotiate:</p>
      <ul>
        <li>Signing bonus</li>
        <li>Stock options or equity</li>
        <li>Annual bonus structure</li>
        <li>Benefits (health, dental, vision)</li>
        <li>RRSP matching</li>
        <li>Professional development budget</li>
        <li>Remote work flexibility</li>
        <li>Vacation days</li>
      </ul>
      
      <h2>Effective Phrases</h2>
      <blockquote>
        "Based on my research and experience, I was expecting a salary in the range of $X to $Y. Is there flexibility in the current offer?"
      </blockquote>
      
      <blockquote>
        "I'm excited about this opportunity. Can we discuss the total compensation package to ensure it aligns with market rates for this role in Toronto?"
      </blockquote>
      
      <h2>What Not to Do</h2>
      <ul>
        <li>Don't accept the first offer immediately</li>
        <li>Don't reveal your current salary</li>
        <li>Don't make ultimatums</li>
        <li>Don't negotiate via email if possible</li>
        <li>Don't compare yourself to colleagues</li>
      </ul>
      
      <h2>Toronto-Specific Considerations</h2>
      <ul>
        <li>Cost of living is high—factor in housing costs</li>
        <li>TTC commute costs vs. remote work</li>
        <li>Provincial tax rates in Ontario</li>
        <li>Competitive market for tech talent</li>
      </ul>
    `
    },
    {
        id: 4,
        title: 'Building Your Professional Network in Toronto',
        excerpt: 'Networking is crucial for career growth. Discover Toronto\'s best tech and creative networking events and strategies.',
        category: 'networking',
        icon: '🤝',
        readTime: '7 min',
        content: `
      <h2>Why Networking Matters</h2>
      <p>In Toronto's tight-knit tech and creative communities, many opportunities come through personal connections. Building a strong network can lead to job offers, mentorship, and valuable industry insights.</p>
      
      <h2>Toronto Networking Events</h2>
      <h3>Tech Meetups</h3>
      <ul>
        <li>Toronto JS</li>
        <li>Toronto Python</li>
        <li>Product Tank Toronto</li>
        <li>Toronto Machine Learning</li>
        <li>Women in Tech Toronto</li>
      </ul>
      
      <h3>Creative Industry Events</h3>
      <ul>
        <li>FITC Toronto</li>
        <li>Toronto Design Offsite</li>
        <li>Creative Mornings Toronto</li>
        <li>AIGA Toronto events</li>
      </ul>
      
      <h3>General Professional Events</h3>
      <ul>
        <li>Toronto Startup Drinks</li>
        <li>Collision Conference</li>
        <li>TechTO</li>
        <li>Elevate Tech Festival</li>
      </ul>
      
      <h2>Online Networking</h2>
      <h3>LinkedIn Strategies</h3>
      <ul>
        <li>Optimize your profile with Toronto keywords</li>
        <li>Engage with Toronto tech/creative content</li>
        <li>Join Toronto-based groups</li>
        <li>Share your insights and projects</li>
        <li>Connect with 2nd-degree connections</li>
      </ul>
      
      <h3>Twitter/X</h3>
      <ul>
        <li>Follow Toronto tech leaders</li>
        <li>Participate in #TOtech conversations</li>
        <li>Share your work and insights</li>
        <li>Engage with local companies</li>
      </ul>
      
      <h2>Effective Networking Tips</h2>
      <ol>
        <li><strong>Be genuine:</strong> Focus on building relationships, not just collecting contacts</li>
        <li><strong>Give before you ask:</strong> Offer value to others first</li>
        <li><strong>Follow up:</strong> Send a message within 24 hours of meeting someone</li>
        <li><strong>Stay in touch:</strong> Regularly engage with your network</li>
        <li><strong>Be specific:</strong> When asking for help, be clear about what you need</li>
      </ol>
      
      <h2>Coffee Chats</h2>
      <p>One-on-one coffee chats are powerful networking tools:</p>
      <ul>
        <li>Reach out to people in roles you aspire to</li>
        <li>Prepare thoughtful questions</li>
        <li>Meet in person when possible (Toronto has great coffee shops!)</li>
        <li>Respect their time (30 minutes max)</li>
        <li>Send a thank-you note afterward</li>
      </ul>
      
      <h2>Building Your Personal Brand</h2>
      <ul>
        <li>Maintain an updated portfolio or GitHub</li>
        <li>Write blog posts or articles</li>
        <li>Speak at meetups or conferences</li>
        <li>Contribute to open source projects</li>
        <li>Share your expertise on social media</li>
      </ul>
    `
    },
    {
        id: 5,
        title: 'Toronto Tech Market Overview 2026',
        excerpt: 'Get insights into Toronto\'s thriving tech ecosystem, major employers, and emerging opportunities.',
        category: 'toronto',
        icon: '🏙️',
        readTime: '12 min',
        content: `
      <h2>Toronto's Tech Ecosystem</h2>
      <p>Toronto has emerged as one of North America's leading tech hubs, with a thriving ecosystem of startups, scale-ups, and established tech giants.</p>
      
      <h2>Major Tech Employers</h2>
      <h3>Tech Giants</h3>
      <ul>
        <li>Google Canada</li>
        <li>Microsoft Canada</li>
        <li>Amazon Toronto</li>
        <li>Meta (Facebook)</li>
        <li>Apple</li>
        <li>Salesforce</li>
      </ul>
      
      <h3>Canadian Tech Leaders</h3>
      <ul>
        <li>Shopify</li>
        <li>Wealthsimple</li>
        <li>Lightspeed</li>
        <li>Hootsuite</li>
        <li>Wave</li>
        <li>FreshBooks</li>
      </ul>
      
      <h3>Fast-Growing Startups</h3>
      <ul>
        <li>Ritual</li>
        <li>Clearco</li>
        <li>Properly</li>
        <li>League</li>
        <li>Borrowell</li>
      </ul>
      
      <h2>Hot Tech Sectors</h2>
      <h3>1. Fintech</h3>
      <p>Toronto is Canada's financial capital, making it a natural hub for financial technology innovation.</p>
      
      <h3>2. AI & Machine Learning</h3>
      <p>With the Vector Institute and strong university programs, Toronto is a global AI leader.</p>
      
      <h3>3. E-commerce & Retail Tech</h3>
      <p>Companies like Shopify have put Toronto on the map for e-commerce innovation.</p>
      
      <h3>4. Health Tech</h3>
      <p>Growing sector with companies focusing on digital health solutions.</p>
      
      <h3>5. SaaS</h3>
      <p>Strong ecosystem of B2B and B2C SaaS companies.</p>
      
      <h2>Salary Ranges (2026)</h2>
      <ul>
        <li><strong>Junior Developer:</strong> $60K - $80K</li>
        <li><strong>Mid-Level Developer:</strong> $80K - $120K</li>
        <li><strong>Senior Developer:</strong> $120K - $180K</li>
        <li><strong>Engineering Manager:</strong> $140K - $220K</li>
        <li><strong>Product Manager:</strong> $100K - $160K</li>
        <li><strong>Senior Product Manager:</strong> $140K - $200K</li>
        <li><strong>UX Designer:</strong> $70K - $110K</li>
        <li><strong>Senior UX Designer:</strong> $110K - $150K</li>
      </ul>
      
      <p>For detailed salary insights, check our <a href="/salary-insights/">Salary Insights Dashboard</a>.</p>
      
      <h2>Tech Hubs in Toronto</h2>
      <ul>
        <li><strong>Downtown Core:</strong> Financial district, major tech offices</li>
        <li><strong>King West:</strong> Startup hub, creative agencies</li>
        <li><strong>Liberty Village:</strong> Tech and creative companies</li>
        <li><strong>MaRS Discovery District:</strong> Innovation hub, startups</li>
        <li><strong>Waterfront:</strong> Growing tech presence</li>
      </ul>
      
      <h2>Remote Work Trends</h2>
      <p>Post-pandemic, many Toronto tech companies offer:</p>
      <ul>
        <li>Fully remote positions</li>
        <li>Hybrid work (2-3 days in office)</li>
        <li>Flexible work arrangements</li>
        <li>Remote-first culture</li>
      </ul>
      
      <h2>Resources</h2>
      <ul>
        <li><strong>Communitech:</strong> Tech community and resources</li>
        <li><strong>MaRS:</strong> Innovation hub and startup support</li>
        <li><strong>Vector Institute:</strong> AI research and talent</li>
        <li><strong>Toronto Tech Slack:</strong> Community discussions</li>
      </ul>
    `
    },
    {
        id: 6,
        title: 'Transitioning to a Management Role',
        excerpt: 'Moving from individual contributor to manager? Learn what it takes to succeed in a leadership position.',
        category: 'career',
        icon: '📈',
        readTime: '9 min',
        content: `
      <h2>Is Management Right for You?</h2>
      <p>Before pursuing management, consider whether it aligns with your strengths and career goals.</p>
      
      <h3>Signs You're Ready</h3>
      <ul>
        <li>You enjoy mentoring and coaching others</li>
        <li>You're interested in strategy and planning</li>
        <li>You handle conflict well</li>
        <li>You're comfortable with ambiguity</li>
        <li>You want to multiply your impact through others</li>
      </ul>
      
      <h3>Common Misconceptions</h3>
      <ul>
        <li>Management is not the only path to advancement</li>
        <li>You'll spend less time on technical work</li>
        <li>Success is measured differently (team outcomes vs. individual output)</li>
        <li>You need different skills than what made you successful as an IC</li>
      </ul>
      
      <h2>Key Skills for New Managers</h2>
      <h3>1. Communication</h3>
      <ul>
        <li>One-on-one meetings</li>
        <li>Giving constructive feedback</li>
        <li>Active listening</li>
        <li>Clear expectation setting</li>
        <li>Transparent decision-making</li>
      </ul>
      
      <h3>2. People Management</h3>
      <ul>
        <li>Hiring and onboarding</li>
        <li>Performance management</li>
        <li>Career development</li>
        <li>Conflict resolution</li>
        <li>Team building</li>
      </ul>
      
      <h3>3. Strategic Thinking</h3>
      <ul>
        <li>Setting team goals and priorities</li>
        <li>Resource allocation</li>
        <li>Long-term planning</li>
        <li>Stakeholder management</li>
        <li>Risk assessment</li>
      </ul>
      
      <h3>4. Delegation</h3>
      <ul>
        <li>Identifying what to delegate</li>
        <li>Matching tasks to team members' strengths</li>
        <li>Providing context and autonomy</li>
        <li>Following up without micromanaging</li>
        <li>Trusting your team</li>
      </ul>
      
      <h2>Your First 90 Days</h2>
      <h3>Days 1-30: Learn</h3>
      <ul>
        <li>Schedule 1:1s with each team member</li>
        <li>Understand team dynamics and challenges</li>
        <li>Learn about ongoing projects</li>
        <li>Identify quick wins</li>
        <li>Build relationships with stakeholders</li>
      </ul>
      
      <h3>Days 31-60: Plan</h3>
      <ul>
        <li>Set clear team goals</li>
        <li>Establish team processes</li>
        <li>Address any urgent issues</li>
        <li>Create a development plan for each team member</li>
        <li>Define your management style</li>
      </ul>
      
      <h3>Days 61-90: Execute</h3>
      <ul>
        <li>Implement new processes</li>
        <li>Start regular team meetings</li>
        <li>Make necessary changes</li>
        <li>Celebrate early wins</li>
        <li>Gather feedback on your leadership</li>
      </ul>
      
      <h2>Common Pitfalls</h2>
      <ul>
        <li><strong>Doing instead of delegating:</strong> Trust your team</li>
        <li><strong>Avoiding difficult conversations:</strong> Address issues early</li>
        <li><strong>Playing favorites:</strong> Be fair and consistent</li>
        <li><strong>Not setting boundaries:</strong> Protect your time</li>
        <li><strong>Forgetting to manage up:</strong> Keep your manager informed</li>
      </ul>
      
      <h2>Resources for New Managers</h2>
      <h3>Books</h3>
      <ul>
        <li>"The Manager's Path" by Camille Fournier</li>
        <li>"Radical Candor" by Kim Scott</li>
        <li>"The First 90 Days" by Michael Watkins</li>
        <li>"High Output Management" by Andy Grove</li>
      </ul>
      
      <h3>Toronto Management Communities</h3>
      <ul>
        <li>Toronto Engineering Leaders</li>
        <li>Product Management Toronto</li>
        <li>Women in Leadership Toronto</li>
      </ul>
    `
    },
    {
        id: 7,
        title: 'Portfolio Best Practices for Creatives',
        excerpt: 'Stand out in Toronto\'s creative industry with a portfolio that showcases your best work and tells your story.',
        category: 'resume',
        icon: '🎨',
        readTime: '8 min',
        content: `
      <h2>Your Portfolio is Your Story</h2>
      <p>A great portfolio doesn't just show what you've done—it demonstrates how you think, solve problems, and create value.</p>
      
      <h2>What to Include</h2>
      <h3>1. Your Best Work</h3>
      <ul>
        <li>Quality over quantity (8-12 projects max)</li>
        <li>Show variety in skills and mediums</li>
        <li>Include recent work (last 2-3 years)</li>
        <li>Demonstrate growth and evolution</li>
      </ul>
      
      <h3>2. Case Studies</h3>
      <p>For each project, include:</p>
      <ul>
        <li><strong>Challenge:</strong> What problem were you solving?</li>
        <li><strong>Process:</strong> How did you approach it?</li>
        <li><strong>Solution:</strong> What did you create?</li>
        <li><strong>Results:</strong> What was the impact?</li>
      </ul>
      
      <h3>3. About Section</h3>
      <ul>
        <li>Professional photo</li>
        <li>Compelling bio (2-3 paragraphs)</li>
        <li>Your design philosophy</li>
        <li>Skills and tools</li>
        <li>Contact information</li>
      </ul>
      
      <h2>Portfolio Platforms</h2>
      <h3>For Designers</h3>
      <ul>
        <li><strong>Behance:</strong> Industry standard, great for discovery</li>
        <li><strong>Dribbble:</strong> Popular for UI/UX designers</li>
        <li><strong>Adobe Portfolio:</strong> Easy to set up, professional</li>
        <li><strong>Custom website:</strong> Shows technical skills</li>
      </ul>
      
      <h3>For Developers</h3>
      <ul>
        <li><strong>GitHub:</strong> Essential for code samples</li>
        <li><strong>Personal website:</strong> Showcase projects and blog</li>
        <li><strong>CodePen:</strong> For front-end work</li>
        <li><strong>Dev.to:</strong> Technical writing and projects</li>
      </ul>
      
      <h3>For Writers/Content Creators</h3>
      <ul>
        <li><strong>Medium:</strong> Publish articles and essays</li>
        <li><strong>Contently:</strong> Professional portfolio platform</li>
        <li><strong>Personal blog:</strong> Full control over content</li>
        <li><strong>LinkedIn:</strong> Share articles and insights</li>
      </ul>
      
      <h2>Design Tips</h2>
      <ul>
        <li><strong>Keep it clean:</strong> Let your work be the star</li>
        <li><strong>Make it fast:</strong> Optimize images and code</li>
        <li><strong>Mobile-friendly:</strong> Many people will view on mobile</li>
        <li><strong>Easy navigation:</strong> Clear menu and structure</li>
        <li><strong>Consistent branding:</strong> Reflect your personal brand</li>
      </ul>
      
      <h2>Common Mistakes</h2>
      <ul>
        <li>Including too many projects</li>
        <li>Not explaining your process</li>
        <li>Poor quality images or screenshots</li>
        <li>Outdated work</li>
        <li>Broken links or slow loading</li>
        <li>No contact information</li>
        <li>Generic descriptions</li>
      </ul>
      
      <h2>Tailoring for Toronto Market</h2>
      <ul>
        <li>Highlight work for Canadian brands</li>
        <li>Show understanding of local market</li>
        <li>Include bilingual work if applicable</li>
        <li>Reference Toronto design trends</li>
        <li>Showcase collaboration with local agencies</li>
      </ul>
      
      <h2>Keeping It Updated</h2>
      <ul>
        <li>Review quarterly</li>
        <li>Add new projects as you complete them</li>
        <li>Remove outdated work</li>
        <li>Update your bio and skills</li>
        <li>Check all links and functionality</li>
      </ul>
      
      <h2>Getting Feedback</h2>
      <ul>
        <li>Ask peers and mentors for honest feedback</li>
        <li>Join portfolio review sessions at meetups</li>
        <li>Test with people outside your industry</li>
        <li>Track analytics to see what resonates</li>
      </ul>
    `
    },
    {
        id: 8,
        title: 'Understanding Canadian Work Permits',
        excerpt: 'Navigate the Canadian work permit system and understand your options for working in Toronto.',
        category: 'toronto',
        icon: '🍁',
        readTime: '11 min',
        content: `
      <h2>Work Permit Overview</h2>
      <p>If you're not a Canadian citizen or permanent resident, you'll need a work permit to work in Toronto. Understanding your options is crucial for your job search.</p>
      
      <h2>Types of Work Permits</h2>
      <h3>1. Employer-Specific Work Permit</h3>
      <ul>
        <li>Tied to a specific employer</li>
        <li>Requires a Labour Market Impact Assessment (LMIA) in most cases</li>
        <li>Valid for the duration specified on the permit</li>
        <li>Cannot change employers without a new permit</li>
      </ul>
      
      <h3>2. Open Work Permit</h3>
      <ul>
        <li>Work for any employer in Canada</li>
        <li>Available in specific situations (spouse of skilled worker, post-graduation, etc.)</li>
        <li>More flexibility in job search</li>
        <li>Easier to change jobs</li>
      </ul>
      
      <h2>Popular Pathways for Tech Workers</h2>
      <h3>Global Talent Stream (GTS)</h3>
      <ul>
        <li>Fast-tracked LMIA processing (10 business days)</li>
        <li>For highly skilled workers in tech</li>
        <li>Requires employer participation</li>
        <li>Competitive salaries required</li>
      </ul>
      
      <h3>Intra-Company Transfer</h3>
      <ul>
        <li>For employees of multinational companies</li>
        <li>Transfer to Canadian branch</li>
        <li>No LMIA required</li>
        <li>Must have worked for company for 1+ year</li>
      </ul>
      
      <h3>Post-Graduation Work Permit (PGWP)</h3>
      <ul>
        <li>For international students who graduated from Canadian institutions</li>
        <li>Open work permit</li>
        <li>Valid for up to 3 years</li>
        <li>Pathway to permanent residence</li>
      </ul>
      
      <h2>Path to Permanent Residence</h2>
      <h3>Express Entry</h3>
      <p>Points-based system for skilled workers:</p>
      <ul>
        <li><strong>Federal Skilled Worker Program:</strong> For skilled workers with foreign work experience</li>
        <li><strong>Canadian Experience Class:</strong> For those with Canadian work experience</li>
        <li><strong>Federal Skilled Trades Program:</strong> For skilled trades workers</li>
      </ul>
      
      <h3>Provincial Nominee Program (PNP)</h3>
      <ul>
        <li>Ontario Immigrant Nominee Program (OINP)</li>
        <li>Tech Draw stream for in-demand tech occupations</li>
        <li>Additional points in Express Entry</li>
      </ul>
      
      <h2>Job Search Considerations</h2>
      <h3>When You Need Sponsorship</h3>
      <ul>
        <li>Be upfront about your status</li>
        <li>Target companies known to sponsor (tech giants, growing startups)</li>
        <li>Highlight your unique skills and value</li>
        <li>Network within immigrant communities</li>
        <li>Consider companies with Global Talent Stream access</li>
      </ul>
      
      <h3>Companies That Commonly Sponsor</h3>
      <ul>
        <li>Google, Microsoft, Amazon, Meta</li>
        <li>Shopify, Wealthsimple, Lightspeed</li>
        <li>Major banks (RBC, TD, Scotiabank)</li>
        <li>Fast-growing tech startups</li>
      </ul>
      
      <h2>Important Considerations</h2>
      <ul>
        <li><strong>Processing times:</strong> Can vary from weeks to months</li>
        <li><strong>Costs:</strong> Application fees, legal fees if using immigration lawyer</li>
        <li><strong>Documentation:</strong> Keep all work permits and related documents</li>
        <li><strong>Renewal:</strong> Start renewal process 6 months before expiry</li>
        <li><strong>Implied status:</strong> Can continue working while renewal is processing</li>
      </ul>
      
      <h2>Resources</h2>
      <ul>
        <li><strong>IRCC:</strong> Official Immigration, Refugees and Citizenship Canada website</li>
        <li><strong>Immigration lawyers:</strong> Consider consulting for complex cases</li>
        <li><strong>Settlement agencies:</strong> Free services for newcomers</li>
        <li><strong>Online communities:</strong> Reddit r/ImmigrationCanada, Facebook groups</li>
      </ul>
      
      <h2>Tips for Success</h2>
      <ul>
        <li>Start the process early</li>
        <li>Keep copies of all documents</li>
        <li>Maintain legal status at all times</li>
        <li>Build Canadian work experience</li>
        <li>Network within your industry</li>
        <li>Consider professional credential recognition if needed</li>
      </ul>
      
      <p><em>Note: Immigration laws change frequently. Always check official government sources for the most current information.</em></p>
    `
    }
];

// State
let currentCategory = 'all';
let searchQuery = '';

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    renderFeaturedResources();
    renderAllResources();
    setupEventListeners();
});

function setupEventListeners() {
    // Search
    const searchInput = document.getElementById('searchInput');
    const searchBtn = document.getElementById('searchBtn');

    searchBtn.addEventListener('click', handleSearch);
    searchInput.addEventListener('keyup', (e) => {
        if (e.key === 'Enter') handleSearch();
    });

    // Category filters
    const tagBtns = document.querySelectorAll('.tag-btn');
    tagBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tagBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentCategory = btn.dataset.category;
            renderAllResources();
        });
    });
}

function handleSearch() {
    searchQuery = document.getElementById('searchInput').value.toLowerCase();
    renderAllResources();
}

function filterResources(resourceList) {
    return resourceList.filter(resource => {
        const matchesCategory = currentCategory === 'all' || resource.category === currentCategory;
        const matchesSearch = !searchQuery ||
            resource.title.toLowerCase().includes(searchQuery) ||
            resource.excerpt.toLowerCase().includes(searchQuery) ||
            resource.category.toLowerCase().includes(searchQuery);

        return matchesCategory && matchesSearch;
    });
}

function renderFeaturedResources() {
    const grid = document.getElementById('featuredGrid');
    const featured = resources.filter(r => r.featured);

    grid.innerHTML = featured.map(resource => createResourceCard(resource, true)).join('');
}

function renderAllResources() {
    const grid = document.getElementById('resourcesGrid');
    const filtered = filterResources(resources);

    if (filtered.length === 0) {
        grid.innerHTML = `
      <div class="empty-state" style="grid-column: 1 / -1;">
        <div class="empty-state-icon">🔍</div>
        <h3>No resources found</h3>
        <p>Try adjusting your search or filters</p>
      </div>
    `;
        return;
    }

    grid.innerHTML = filtered.map(resource => createResourceCard(resource)).join('');
}

function createResourceCard(resource, isFeatured = false) {
    return `
    <div class="resource-card" onclick="viewResource(${resource.id})">
      <div class="resource-icon">${resource.icon}</div>
      <span class="resource-category">${resource.category}</span>
      <h3>${resource.title}</h3>
      <p>${resource.excerpt}</p>
      <div class="resource-meta">
        <span>📖 ${resource.readTime} read</span>
        ${isFeatured ? '<span>⭐ Featured</span>' : ''}
      </div>
    </div>
  `;
}

function viewResource(id) {
    const resource = resources.find(r => r.id === id);
    if (!resource) return;

    // Create article view
    const main = document.querySelector('.container');
    main.innerHTML = `
    <div class="article-content">
      <div class="article-header">
        <span class="resource-category">${resource.category}</span>
        <h1>${resource.title}</h1>
        <div class="article-meta">
          <span>📖 ${resource.readTime} read</span>
          <span>${resource.icon} ${getCategoryName(resource.category)}</span>
        </div>
      </div>
      <div class="article-body">
        ${resource.content}
      </div>
      <div style="text-align: center; margin-top: 3rem;">
        <button class="btn btn-primary" onclick="location.href='/resources/'">← Back to Resources</button>
      </div>
    </div>
  `;

    window.scrollTo(0, 0);
}

function getCategoryName(category) {
    const names = {
        resume: 'Resume',
        interview: 'Interview',
        career: 'Career Growth',
        salary: 'Salary',
        networking: 'Networking',
        toronto: 'Toronto Market'
    };
    return names[category] || category;
}

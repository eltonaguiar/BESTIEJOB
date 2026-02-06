// Career Resources App
// Handles interactive elements on the career resources page

document.addEventListener('DOMContentLoaded', () => {
  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
        
        // Add a highlight effect
        target.style.transition = 'box-shadow 0.3s';
        target.style.boxShadow = '0 0 0 2px var(--accent)';
        setTimeout(() => {
          target.style.boxShadow = '';
        }, 1000);
      }
    });
  });

  // Save checkbox state to localStorage
  const checkboxes = document.querySelectorAll('.checkbox-item input[type="checkbox"]');
  
  checkboxes.forEach((checkbox, index) => {
    // Load saved state
    const saved = localStorage.getItem(`career-check-${index}`);
    if (saved === 'true') {
      checkbox.checked = true;
    }
    
    // Save on change
    checkbox.addEventListener('change', () => {
      localStorage.setItem(`career-check-${index}`, checkbox.checked);
      updateProgress();
    });
  });

  // Update progress indicator
  function updateProgress() {
    const checked = document.querySelectorAll('.checkbox-item input:checked').length;
    const total = checkboxes.length;
    
    // Create or update progress indicator
    let progressEl = document.querySelector('.progress-indicator');
    if (!progressEl) {
      progressEl = document.createElement('div');
      progressEl.className = 'progress-indicator';
      progressEl.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 12px 16px;
        font-size: 13px;
        color: var(--text);
        backdrop-filter: blur(10px);
        z-index: 100;
      `;
      document.body.appendChild(progressEl);
    }
    
    const percentage = Math.round((checked / total) * 100);
    progressEl.innerHTML = `
      <strong>Resume Checklist:</strong> ${checked}/${total} (${percentage}%)
    `;
    
    if (checked === total) {
      progressEl.innerHTML += ' ✅';
      progressEl.style.borderColor = '#4ade80';
    }
  }

  // Initial progress update
  if (checkboxes.length > 0) {
    updateProgress();
  }

  // Add copy functionality for code snippets or key points
  document.querySelectorAll('.qa-item .question').forEach(q => {
    q.style.cursor = 'pointer';
    q.title = 'Click to copy';
    
    q.addEventListener('click', () => {
      navigator.clipboard.writeText(q.textContent).then(() => {
        const original = q.textContent;
        q.textContent = '✓ Copied!';
        q.style.color = '#4ade80';
        setTimeout(() => {
          q.textContent = original;
          q.style.color = '';
        }, 1000);
      });
    });
  });
});

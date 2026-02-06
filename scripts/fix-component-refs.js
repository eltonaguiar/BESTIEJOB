import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Files that need fixing
const filesToFix = [
    'public/resume-builder/index.html',
    'public/my-jobs/index.html',
    'public/interview-prep/index.html',
    'public/gotjob/salary-insights/index.html',
    'public/gotjob/resume-builder/index.html',
    'public/gotjob/resources/index.html',
    'public/gotjob/my-jobs/index.html',
    'public/gotjob/interview-prep/index.html',
    'public/gotjob/companies/index.html',
    'public/companies/index.html'
];

console.log('╔══════════════════════════════════════════╗');
console.log('║   Fixing Broken Component References    ║');
console.log('╚══════════════════════════════════════════╝\n');

let fixedCount = 0;
let skippedCount = 0;

for (const file of filesToFix) {
    const filePath = path.resolve(__dirname, '..', file);

    if (!fs.existsSync(filePath)) {
        console.log(`⚠️  Skipped (not found): ${file}`);
        skippedCount++;
        continue;
    }

    let content = fs.readFileSync(filePath, 'utf8');
    let modified = false;

    // Remove the broken shared styles reference
    if (content.includes('/components/styles-shared.css')) {
        content = content.replace(
            /\s*<link rel="stylesheet" href="\/components\/styles-shared\.css">\r?\n/g,
            ''
        );
        modified = true;
    }

    // Remove the broken header.js reference
    if (content.includes('/components/header.js')) {
        content = content.replace(
            /\s*<script src="\/components\/header\.js"><\/script>\r?\n/g,
            ''
        );
        modified = true;
    }

    // Remove the initializeLayout call
    if (content.includes('initializeLayout')) {
        content = content.replace(
            /\s*<script>\r?\n\s*\/\/ Initialize layout with active page\r?\n\s*initializeLayout\([^)]+\);\r?\n\s*<\/script>\r?\n/g,
            ''
        );
        modified = true;
    }

    if (modified) {
        fs.writeFileSync(filePath, content, 'utf8');
        console.log(`✅ Fixed: ${file}`);
        fixedCount++;
    } else {
        console.log(`⏭️  No changes needed: ${file}`);
        skippedCount++;
    }
}

console.log('\n╔══════════════════════════════════════════╗');
console.log(`║  ✅ Fixed ${fixedCount} files`);
console.log(`║  ⏭️  Skipped ${skippedCount} files`);
console.log('╚══════════════════════════════════════════╝');

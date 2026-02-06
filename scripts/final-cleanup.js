import { Client as FtpClient } from "basic-ftp";

const FTP_HOST = "ftps2.50webs.com";
const FTP_USER = "ejaguiar1";
const FTP_PASS = "$a^FzN7BqKapSQMsZxD&^FeTJ";

// Directories that should be under /gotjob/, NOT at root
const GOTJOB_DIRS = [
    'admin',
    'findjobs',
    'ai-match-lab',
    'analytics',
    'career',
    'career-resources',
    'companies',
    'experience-hub',
    'interview-prep',
    'market-report',
    'mobile-studio',
    'my-jobs',
    'resume-builder',
    'salaries',
    'salary',
    'salary-insights',
    'tracker',
    'trends'
];

async function main() {
    const client = new FtpClient();
    client.ftp.verbose = false;

    try {
        console.log("╔══════════════════════════════════════════╗");
        console.log("║   Final Cleanup - Remove All Misplaced  ║");
        console.log("╚══════════════════════════════════════════╝\n");

        console.log("🔗 Connecting to FTP server...");

        await client.access({
            host: FTP_HOST,
            user: FTP_USER,
            password: FTP_PASS,
            secure: true,
            secureOptions: { rejectUnauthorized: false }
        });

        console.log("✅ Connected!\n");

        // List root contents
        console.log("📂 Current /findtorontoevents.ca/ directories:\n");
        const rootContents = await client.list("/findtorontoevents.ca/");

        const allDirs = rootContents.filter(item => item.isDirectory);
        allDirs.forEach(item => console.log(`   📁 ${item.name}`));

        // Find BESTIEJOB directories at root
        const toRemove = allDirs.filter(item => GOTJOB_DIRS.includes(item.name));

        if (toRemove.length === 0) {
            console.log("\n✅ Root is clean - no BESTIEJOB directories found!");
            client.close();
            return;
        }

        console.log(`\n🗑️  Removing ${toRemove.length} misplaced directories:\n`);

        // Remove each directory
        for (const item of toRemove) {
            const dirPath = `/findtorontoevents.ca/${item.name}`;
            try {
                console.log(`   Removing ${item.name}...`);
                await client.removeDir(dirPath);
                console.log(`   ✅ Removed!`);
            } catch (error) {
                console.error(`   ❌ Error: ${error.message}`);
            }
        }

        console.log("\n╔══════════════════════════════════════════╗");
        console.log("║          Cleanup Complete!               ║");
        console.log("╚══════════════════════════════════════════╝");

    } catch (error) {
        console.error("\n❌ Failed:", error.message);
        process.exit(1);
    } finally {
        client.close();
    }
}

main();

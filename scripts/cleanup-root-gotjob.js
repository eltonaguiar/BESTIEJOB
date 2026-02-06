import { Client as FtpClient } from "basic-ftp";

const FTP_HOST = "ftps2.50webs.com";
const FTP_USER = "ejaguiar1";
const FTP_PASS = "$a^FzN7BqKapSQMsZxD&^FeTJ";

// ALL these directories should be under /gotjob/, NOT at root
const DIRS_THAT_BELONG_IN_GOTJOB = [
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
        console.log("║   Cleaning Up Misdeployed Directories   ║");
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
        console.log("📂 Listing /findtorontoevents.ca/ contents:\n");
        const rootContents = await client.list("/findtorontoevents.ca/");

        const allDirs = rootContents.filter(item => item.isDirectory);
        console.log("All directories at root:");
        allDirs.forEach(item => console.log(`   📁 ${item.name}`));

        // Find directories that should be in /gotjob/ but are at root
        const toRemove = allDirs.filter(item =>
            DIRS_THAT_BELONG_IN_GOTJOB.includes(item.name)
        );

        if (toRemove.length === 0) {
            console.log("\n✅ No misdeployed directories found at root!");
            client.close();
            return;
        }

        console.log(`\n🗑️  Found ${toRemove.length} misdeployed directories at root:\n`);
        toRemove.forEach(item => console.log(`   📁 ${item.name}`));
        console.log("");

        // Remove each directory from root
        for (const item of toRemove) {
            const dirPath = `/findtorontoevents.ca/${item.name}`;
            try {
                console.log(`🗑️  Removing ${dirPath}...`);
                await client.removeDir(dirPath);
                console.log(`   ✅ Removed!`);
            } catch (error) {
                console.error(`   ❌ Error: ${error.message}`);
            }
        }

        console.log("\n╔══════════════════════════════════════════╗");
        console.log("║          Cleanup Complete!               ║");
        console.log("╚══════════════════════════════════════════╝");
        console.log("\n✅ All directories removed from root.");
        console.log("✅ They should only exist at /findtorontoevents.ca/gotjob/");

    } catch (error) {
        console.error("\n❌ Cleanup failed:", error.message);
        console.error(error);
        process.exit(1);
    } finally {
        client.close();
    }
}

main();

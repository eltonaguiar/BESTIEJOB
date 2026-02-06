import { Client as FtpClient } from "basic-ftp";

const FTP_HOST = process.env.FTP_SERVER || "ftps2.50webs.com";
const FTP_USER = process.env.FTP_USER || "ejaguiar1";
const FTP_PASS = process.env.FTP_PASS;

async function cleanupWrongDeployment() {
    if (!FTP_PASS) {
        console.error("❌ FTP_PASS environment variable is required");
        process.exit(1);
    }

    const client = new FtpClient();
    client.ftp.verbose = true;

    try {
        console.log("╔══════════════════════════════════════════╗");
        console.log("║   Cleaning Up Wrong FTP Deployment      ║");
        console.log("╚══════════════════════════════════════════╝\n");

        await client.access({
            host: FTP_HOST,
            user: FTP_USER,
            password: FTP_PASS,
            secure: true,
            secureOptions: { rejectUnauthorized: false }
        });

        console.log("✅ Connected to FTP server\n");

        // List of directories that were incorrectly deployed to /findtorontoevents
        const wrongDirs = [
            "/findtorontoevents/resources",
            "/findtorontoevents/salary-insights",
            "/findtorontoevents/companies",
            "/findtorontoevents/resume-builder",
            "/findtorontoevents/interview-prep",
            "/findtorontoevents/my-jobs",
            "/findtorontoevents/components"
        ];

        console.log("Removing incorrectly deployed directories from /findtorontoevents:\n");

        for (const dir of wrongDirs) {
            try {
                console.log(`Attempting to remove: ${dir}`);
                await client.removeDir(dir);
                console.log(`✅ Removed: ${dir}`);
            } catch (error) {
                console.log(`⚠️  Could not remove ${dir}: ${error.message}`);
            }
        }

        // Also check and remove from root if they exist
        const rootDirs = [
            "/resources",
            "/salary-insights",
            "/companies",
            "/resume-builder",
            "/interview-prep",
            "/my-jobs",
            "/components"
        ];

        console.log("\nChecking root directory for misplaced files:\n");

        for (const dir of rootDirs) {
            try {
                console.log(`Attempting to remove: ${dir}`);
                await client.removeDir(dir);
                console.log(`✅ Removed: ${dir}`);
            } catch (error) {
                console.log(`⚠️  Could not remove ${dir}: ${error.message}`);
            }
        }

        console.log("\n╔══════════════════════════════════════════╗");
        console.log("║     ✅ Cleanup Complete!                 ║");
        console.log("╚══════════════════════════════════════════╝");
        console.log("\nNow you can redeploy to the correct location under /gotjob");

    } catch (error) {
        console.error("\n❌ Cleanup failed:", error.message);
        process.exit(1);
    } finally {
        client.close();
    }
}

cleanupWrongDeployment();

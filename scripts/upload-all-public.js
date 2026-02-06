import fs from "fs";
import path from "path";
import { Client as FtpClient } from "basic-ftp";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const FTP_HOST = process.env.FTP_SERVER || "ftps2.50webs.com";
const FTP_USER = process.env.FTP_USER || "ejaguiar1";
const FTP_PASS = process.env.FTP_PASS;

// Deploy ALL public directories to /findtorontoevents.ca/
const REMOTE_BASE = "/findtorontoevents.ca";
const LOCAL_DIR = path.resolve(__dirname, "..", "public");

async function uploadDirectory(client, localDir, remoteDir) {
    console.log(`📁 Creating remote directory: ${remoteDir}`);

    try {
        await client.ensureDir(remoteDir);
    } catch (error) {
        console.warn(`⚠️  Could not ensure directory ${remoteDir}: ${error.message}`);
    }

    const items = fs.readdirSync(localDir);

    for (const item of items) {
        const localPath = path.join(localDir, item);
        const remotePath = path.posix.join(remoteDir, item);
        const stat = fs.statSync(localPath);

        if (stat.isDirectory()) {
            await uploadDirectory(client, localPath, remotePath);
        } else {
            console.log(`📤 Uploading: ${item} -> ${remotePath}`);
            try {
                await client.uploadFrom(localPath, remotePath);
            } catch (uploadError) {
                console.error(`❌ Failed to upload ${item}: ${uploadError.message}`);
            }
        }
    }
}

async function main() {
    if (!FTP_PASS) {
        console.error("❌ FTP_PASS environment variable is required");
        console.log("\nSet it with:");
        console.log('  $env:FTP_PASS = "your-password"');
        console.log("  node scripts/upload-all-public.js");
        process.exit(1);
    }

    if (!fs.existsSync(LOCAL_DIR)) {
        console.error(`❌ Local directory not found: ${LOCAL_DIR}`);
        process.exit(1);
    }

    const client = new FtpClient();
    client.ftp.verbose = true;

    try {
        console.log("╔══════════════════════════════════════════╗");
        console.log("║   Deploy ALL Public Directories          ║");
        console.log("╚══════════════════════════════════════════╝\n");

        console.log(`📦 Local directory: ${LOCAL_DIR}`);
        console.log(`🌐 Remote path: ${REMOTE_BASE}`);
        console.log(`🖥️  FTP Host: ${FTP_HOST}\n`);

        console.log("Connecting to FTP server...");
        await client.access({
            host: FTP_HOST,
            user: FTP_USER,
            password: FTP_PASS,
            secure: true,
            secureOptions: { rejectUnauthorized: false }
        });

        console.log("✅ Connected! Uploading all directories...\n");

        // Get all directories in public/
        const dirs = fs.readdirSync(LOCAL_DIR).filter(item => {
            const itemPath = path.join(LOCAL_DIR, item);
            return fs.statSync(itemPath).isDirectory();
        });

        console.log(`Found ${dirs.length} directories to upload:\n${dirs.join(", ")}\n`);

        for (const dir of dirs) {
            const localPath = path.join(LOCAL_DIR, dir);
            const remotePath = path.posix.join(REMOTE_BASE, dir);
            console.log(`\n📂 Uploading directory: ${dir}`);
            await uploadDirectory(client, localPath, remotePath);
        }

        console.log("\n╔══════════════════════════════════════════╗");
        console.log("║     ✅ Deployment Complete!              ║");
        console.log("╚══════════════════════════════════════════╝");
        console.log(`\n🔗 All directories deployed to: https://findtorontoevents.ca/`);

    } catch (error) {
        console.error("\n❌ Deployment failed:", error.message);
        process.exit(1);
    } finally {
        client.close();
    }
}

main();

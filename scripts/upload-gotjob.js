import fs from "fs";
import path from "path";
import { Client as FtpClient } from "basic-ftp";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// FTP Configuration
const FTP_HOST = process.env.FTP_SERVER || "ftps2.50webs.com";
const FTP_USER = process.env.FTP_USER || "ejaguiar1";
const FTP_PASS = process.env.FTP_PASS;

// Deploy to /findtorontoevents.ca/gotjob
const REMOTE_BASE = "/findtorontoevents.ca/gotjob";
const LOCAL_DIR = path.resolve(__dirname, "..", "public", "gotjob");

async function uploadDirectory(client, localDir, remoteDir) {
  console.log(`Creating remote directory: ${remoteDir}`);
  
  try {
    await client.ensureDir(remoteDir);
  } catch (error) {
    console.warn(`Could not ensure directory ${remoteDir}: ${error.message}`);
  }

  const items = fs.readdirSync(localDir);

  for (const item of items) {
    const localPath = path.join(localDir, item);
    const remotePath = path.posix.join(remoteDir, item);
    const stat = fs.statSync(localPath);

    if (stat.isDirectory()) {
      await uploadDirectory(client, localPath, remotePath);
    } else {
      console.log(`Uploading: ${item} -> ${remotePath}`);
      try {
        await client.uploadFrom(localPath, remotePath);
      } catch (uploadError) {
        console.error(`Failed to upload ${item}: ${uploadError.message}`);
      }
    }
  }
}

async function main() {
  if (!FTP_PASS) {
    console.error("❌ FTP_PASS environment variable is required");
    console.log("\nSet it with:");
    console.log('  $env:FTP_PASS = "your-password"');
    console.log("  node scripts/upload-gotjob.js");
    process.exit(1);
  }

  if (!fs.existsSync(LOCAL_DIR)) {
    console.error(`❌ Local directory not found: ${LOCAL_DIR}`);
    console.log("\nMake sure to copy files to public/gotjob first");
    process.exit(1);
  }

  const client = new FtpClient();
  client.ftp.verbose = true;

  try {
    console.log("╔══════════════════════════════════════════╗");
    console.log("║   GotJob - FTP Deployment to gotjob/     ║");
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

    console.log("✅ Connected! Uploading files...\n");
    await uploadDirectory(client, LOCAL_DIR, REMOTE_BASE);

    console.log("\n╔══════════════════════════════════════════╗");
    console.log("║     ✅ Deployment Complete!              ║");
    console.log("╚══════════════════════════════════════════╝");
    console.log(`\n🔗 Site available at: https://findtorontoevents.ca/gotjob/`);
    
  } catch (error) {
    console.error("\n❌ Deployment failed:", error.message);
    
    if (error.message.includes("ENOTFOUND")) {
      console.log("\nCould not connect to FTP server. Check your internet connection.");
    } else if (error.message.includes("530") || error.message.includes("Login")) {
      console.log("\nFTP login failed. Check your FTP_USER and FTP_PASS credentials.");
    }
    
    process.exit(1);
  } finally {
    client.close();
  }
}

main();

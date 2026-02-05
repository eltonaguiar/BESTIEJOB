import fs from "fs";
import path from "path";
import { Client as FtpClient } from "basic-ftp";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const FTP_HOST = process.env.FTP_SERVER || "ftps2.50webs.com";
const FTP_USER = process.env.FTP_USER || "ejaguiar1";
const FTP_PASS = process.env.FTP_PASS;
const REMOTE_BASE = "/findtorontoevents.ca/gotjob";
const LOCAL_DIR = path.resolve(__dirname, "..");

const EXCLUDE = [
  "node_modules",
  ".git",
  ".env",
  ".env.local",
  ".gitignore",
  "jobs.json",
  "upload.js"
];

async function uploadDirectory(client, localDir, remoteDir) {
  await client.ensureDir(remoteDir);

  const items = fs.readdirSync(localDir);

  for (const item of items) {
    if (EXCLUDE.includes(item)) continue;

    const localPath = path.join(localDir, item);
    const remotePath = path.posix.join(remoteDir, item);
    const stat = fs.statSync(localPath);

    if (stat.isDirectory()) {
      console.log(`Creating directory: ${remotePath}`);
      await uploadDirectory(client, localPath, remotePath);
    } else {
      console.log(`Uploading: ${localPath} -> ${remotePath}`);
      await client.uploadFrom(localPath, remotePath);
    }
  }
}

async function main() {
  if (!FTP_PASS) {
    console.error("FTP_PASS environment variable is required");
    process.exit(1);
  }

  const client = new FtpClient();
  client.ftp.verbose = true;

  try {
    console.log(`Connecting to ${FTP_HOST}...`);
    await client.access({
      host: FTP_HOST,
      user: FTP_USER,
      password: FTP_PASS,
      secure: true,
      secureOptions: { rejectUnauthorized: false }
    });

    console.log("Connected. Uploading files...");
    await uploadDirectory(client, LOCAL_DIR, REMOTE_BASE);

    console.log("\n✅ Files uploaded to /findtorontoevents.ca/gotjob!");
    console.log(`Site available at: http://findtorontoevents.ca/gotjob`);
  } catch (error) {
    console.error("Upload failed:", error.message);
    process.exit(1);
  } finally {
    client.close();
  }
}

main();

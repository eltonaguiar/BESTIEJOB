import fs from "fs";
import path from "path";
import { Client as FtpClient } from "basic-ftp";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const FTP_HOST = process.env.FTP_SERVER || "ftps2.50webs.com";
const FTP_USER = process.env.FTP_USER || "ejaguiar1";
const FTP_PASS = process.env.FTP_PASS;

async function uploadToRoot() {
  if (!FTP_PASS) {
    console.error("FTP_PASS required");
    process.exit(1);
  }

  const client = new FtpClient();
  
  try {
    await client.access({
      host: FTP_HOST,
      user: FTP_USER,
      password: FTP_PASS,
      secure: true,
      secureOptions: { rejectUnauthorized: false }
    });

    const publicDir = path.join(__dirname, "..", "public");
    const remoteBase = "/findtorontoevents.ca/gotjob";
    
    // Ensure base directory exists
    await client.ensureDir(remoteBase);
    
    // Upload public folder CONTENTS to root
    const items = fs.readdirSync(publicDir);
    
    for (const item of items) {
      const localPath = path.join(publicDir, item);
      const remotePath = path.posix.join(remoteBase, item);
      const stat = fs.statSync(localPath);
      
      if (stat.isDirectory()) {
        // For admin folder, recreate it
        await client.ensureDir(remotePath);
        const subItems = fs.readdirSync(localPath);
        for (const sub of subItems) {
          const subLocal = path.join(localPath, sub);
          const subRemote = path.posix.join(remotePath, sub);
          await client.uploadFrom(subLocal, subRemote);
          // Set readable permissions
          try { await c.rename(subRemote, subRemote); } catch(e) {}
          console.log(`Uploaded: ${item}/${sub}`);
        }
      } else {
        await client.uploadFrom(localPath, remotePath);
        // Ensure file is readable
        try { await client.rename(remotePath, remotePath); } catch(e) {}
        console.log(`Uploaded: ${item}`);
      }
    }
    
    console.log("\n✅ Files uploaded to /gotjob root!");
    console.log("Site: http://findtorontoevents.ca/gotjob/");
    
  } catch (err) {
    console.error("Upload failed:", err.message);
    process.exit(1);
  } finally {
    client.close();
  }
}

uploadToRoot();

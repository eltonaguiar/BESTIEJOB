import fs from "fs";
import path from "path";
import { Client as FtpClient } from "basic-ftp";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const FTP_HOST = process.env.FTP_SERVER || "ftps2.50webs.com";
const FTP_USER = process.env.FTP_USER || "ejaguiar1";
const FTP_PASS = process.env.FTP_PASS;

async function uploadPublic() {
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
    
    await client.ensureDir(remoteBase);
    
    // Upload index.html
    await client.uploadFrom(
      path.join(publicDir, "index.html"),
      path.posix.join(remoteBase, "index.html")
    );
    console.log("Uploaded: index.html");
    
    // Upload app.js
    await client.uploadFrom(
      path.join(publicDir, "app.js"),
      path.posix.join(remoteBase, "app.js")
    );
    console.log("Uploaded: app.js");
    
    // Upload styles.css
    await client.uploadFrom(
      path.join(publicDir, "styles.css"),
      path.posix.join(remoteBase, "styles.css")
    );
    console.log("Uploaded: styles.css");
    
    // Upload admin folder
    await client.ensureDir(path.posix.join(remoteBase, "admin"));
    await client.uploadFrom(
      path.join(publicDir, "admin", "index.html"),
      path.posix.join(remoteBase, "admin", "index.html")
    );
    console.log("Uploaded: admin/index.html");
    
    console.log("\n✅ Static files uploaded successfully!");
    console.log("Site: http://findtorontoevents.ca/gotjob/");
    console.log("Admin: http://findtorontoevents.ca/gotjob/admin");
    
  } catch (err) {
    console.error("Upload failed:", err.message);
    process.exit(1);
  } finally {
    client.close();
  }
}

uploadPublic();

import { Client as FtpClient } from "basic-ftp";

const FTP_HOST = process.env.FTP_SERVER || "ftps2.50webs.com";
const FTP_USER = process.env.FTP_USER || "ejaguiar1";
const FTP_PASS = process.env.FTP_PASS;
const REMOTE_BASE = "/findtorontoevents.ca/gotjob";

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

    console.log("Connected. Uploading jobs.json...");
    await client.ensureDir(REMOTE_BASE);
    await client.uploadFrom("./jobs.json", `${REMOTE_BASE}/jobs.json`);

    console.log("\n✅ jobs.json uploaded successfully!");
    console.log(`Site: http://findtorontoevents.ca/gotjob`);
  } catch (error) {
    console.error("Upload failed:", error.message);
    process.exit(1);
  } finally {
    client.close();
  }
}

main();

import { Client } from "basic-ftp";

async function listRemote() {
  const client = new Client();
  client.ftp.verbose = true;
  
  try {
    await client.access({
      host: process.env.FTP_SERVER || "ftps2.50webs.com",
      user: process.env.FTP_USER || "ejaguiar1",
      password: process.env.FTP_PASS,
      secure: true,
      secureOptions: { rejectUnauthorized: false }
    });
    
    console.log("\n=== ROOT DIRECTORY ===");
    await client.list("/");
    
    console.log("\n=== PUBLIC_HTML/GOTJOB DIRECTORY ===");
    try {
      await client.list("/public_html/gotjob");
    } catch(e) {
      console.log("No /public_html/gotjob directory");
    }
    
    console.log("\n=== CHECKING OLD GOTJOB ===");
    try {
      await client.list("/gotjob");
    } catch(e) {
      console.log("No /gotjob directory");
    }
    
  } catch (err) {
    console.error("FTP Error:", err.message);
  } finally {
    client.close();
  }
}

listRemote();

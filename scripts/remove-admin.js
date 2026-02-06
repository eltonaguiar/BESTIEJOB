import { Client as FtpClient } from "basic-ftp";

const FTP_HOST = "ftps2.50webs.com";
const FTP_USER = "ejaguiar1";
const FTP_PASS = "$a^FzN7BqKapSQMsZxD&^FeTJ";

async function main() {
    const client = new FtpClient();
    client.ftp.verbose = false;

    try {
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

        // Remove admin directory if it exists
        if (allDirs.some(item => item.name === 'admin')) {
            console.log("\n🗑️  Removing /findtorontoevents.ca/admin...");
            await client.removeDir("/findtorontoevents.ca/admin");
            console.log("   ✅ Removed!");
        } else {
            console.log("\n✅ No admin directory found at root");
        }

    } catch (error) {
        console.error("\n❌ Failed:", error.message);
        process.exit(1);
    } finally {
        client.close();
    }
}

main();

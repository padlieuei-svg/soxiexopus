const {
    default: makeWASocket,
    useMultiFileAuthState,
    DisconnectReason,
    fetchLatestBaileysVersion,
} = require("@whiskeysockets/baileys");
const P = require("pino");

const PAIRING_NUMBER = process.env.WA_NUMBER || "";

let sock = null;
let pairingCodeRequested = false;

async function startBot() {
    const { state, saveCreds } = await useMultiFileAuthState("auth");
    const { version } = await fetchLatestBaileysVersion();

    sock = makeWASocket({
        version,
        printQRInTerminal: false,
        auth: state,
        logger: P({ level: "silent" }),
        browser: ["Chrome (Linux)", "Chrome", "121.0.0.0"],
    });

    if (!sock.authState.creds.registered && !pairingCodeRequested) {
        pairingCodeRequested = true;

        if (!PAIRING_NUMBER) {
            console.log("WA_NUMBER belum di-set!");
            return;
        }

        setTimeout(async () => {
            try {
                let nomor = PAIRING_NUMBER.replace(/[^0-9]/g, "");
                if (nomor.startsWith("0")) nomor = "62" + nomor.slice(1);
                if (!nomor.startsWith("62")) nomor = "62" + nomor;

                const code = await sock.requestPairingCode(nomor);
                console.log("\n🔑 PAIRING CODE: " + code + "\n");
            } catch (err) {
                console.log("Gagal pairing:", err.message);
            }
        }, 3000);
    }

    sock.ev.on("connection.update", async (update) => {
        const { connection, lastDisconnect } = update;
        if (connection === "close") {
            const shouldReconnect =
                lastDisconnect?.error?.output?.statusCode !== DisconnectReason.loggedOut;
            if (shouldReconnect) startBot();
        } else if (connection === "open") {
            console.log("Terhubung ke WhatsApp");
        }
    });

    sock.ev.on("creds.update", saveCreds);
}

startBot().catch((err) => console.error(err.message));

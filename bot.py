 # bot.py

import os
from telegram.ext import Updater, CommandHandler
import logging

# Token
TOKEN = os.getenv("BOT_TOKEN")

print("🚀 Bot is starting...")
print("✅ Token:", TOKEN)

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Start Command
def start(update, context):
    update.message.reply_text("✅ Bot is Working!")

# Main Function
def main():
    if not TOKEN:
        print("❌ BOT_TOKEN not found in environment variables.")
        return

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    print("📡 Bot polling started...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

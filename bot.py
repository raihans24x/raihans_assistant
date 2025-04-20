# bot.py

import os
from telegram.ext import Updater, CommandHandler
import logging

# Load Token from Railway Environment Variables
TOKEN = os.getenv("TELEGRAM_TOKEN")

print("🚀 RayhanBot is starting...")
print("🔐 Loaded TOKEN:", TOKEN)

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# /start command handler
def start(update, context):
    update.message.reply_text("হাই! আমি RayhanBot ✅ কাজ করছি!")

# main function
def main():
    if not TOKEN:
        print("❌ TOKEN NOT FOUND! Make sure it's set in Railway variables.")
        return

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    print("📡 Bot is polling...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

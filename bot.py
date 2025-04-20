import os
from dotenv import load_dotenv
load_dotenv()

from telegram.ext import Updater, CommandHandler
from transformers import pipeline
import logging

# Telegram Bot Token
TOKEN = os.getenv("BOT_TOKEN")

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Load text generation model
generator = pipeline("text-generation", model="distilgpt2")

# Handlers
def start(update, context):
    update.message.reply_text("হ্যালো! আমি তোমার AI বন্ধু RaihanBot 🤖। আমাকে প্রশ্ন করো /ask দিয়ে।")

def help_command(update, context):
    update.message.reply_text("/ask প্রশ্ন লিখো - উত্তর পাবে\n/start - শুরু করো\n/help - সাহায্য")

def ask(update, context):
    user_input = ' '.join(context.args)
    if user_input:
        update.message.reply_text("এক সেকেন্ড... ভাবছি!")
        result = generator(user_input, max_length=100, num_return_sequences=1)[0]['generated_text']
        update.message.reply_text(result)
    else:
        update.message.reply_text("প্রশ্ন দাও! যেমন: /ask তুমি কে?")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("ask", ask))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

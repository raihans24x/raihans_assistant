import os
from dotenv import load_dotenv
load_dotenv()

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
from generate import generate_text
from image_gen import generate_image

# ✅ ঠিক করলাম এখানে
TOKEN = os.getenv("TELEGRAM_TOKEN")

print("🚀 Starting RayhanBot...")
print("🔐 TOKEN LOADED:", TOKEN)



# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Handlers
def start(update, context):
    update.message.reply_text("হাই! আমি তোমার AI বন্ধু RayhanBot। আমাকে প্রশ্ন করো বা ছবি বানাতে বলো!")

def help(update, context):
    update.message.reply_text("/ask প্রশ্ন লিখো - উত্তর পাবে\n/draw ছবি বানাতে চাও\n/start - শুরু করো")

def ask(update, context):
    user_input = ' '.join(context.args)
    if user_input:
        update.message.reply_text("এক সেকেন্ড দোস্ত... ভাবছি!")
        response = generate_text(user_input)
        update.message.reply_text(response)
    else:
        update.message.reply_text("প্রশ্ন দাও! যেমন: /ask তুমি কে?")

def draw(update, context):
    user_input = ' '.join(context.args)
    if user_input:
        update.message.reply_text("ছবি বানানো হচ্ছে... একটু অপেক্ষা করো!")
        img_path = generate_image(user_input)
        update.message.reply_photo(photo=open(img_path, 'rb'))
    else:
        update.message.reply_text("দয়া করে `/draw sunset in Bangladesh` এরকম লেখো!")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("ask", ask))
    dp.add_handler(CommandHandler("draw", draw))
    dp.add_handler(MessageHandler(Filters.text, ask))  # সাধারন টেক্সটও `/ask` হিসাবে ধরবে

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

import os
import logging
import openai
import requests
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# --- আপনার Token এবং API Key এখানে বসান ---
TELEGRAM_TOKEN = os.getenv("7852399803:AAHHeKLm98JF-t_yf2k4w53aOIi1mtB7jcE")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

# --- লগিং ---
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- OWNER ---
OWNER_ID = 123456789  # এখানে @userinfobot থেকে পাওয়া Telegram ID বসান
OWNER_NAME = "Rayhan Boss"

# --- /start কমান্ড হ্যান্ডলার ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"আসসালামু আলাইকুম! আমি {OWNER_NAME}-এর তৈরি AI বট। আমি তার সকল আদেশ পালন করতে বাধ্য।")

# --- চেক করবে ইউজার 'ছবি/image' টাইপ চায় কিনা ---
def is_image_request(text):
    keywords = ["ছবি", "image", "generate", "draw", "picture"]
    return any(word in text.lower() for word in keywords)

# --- মেইন মেসেজ হ্যান্ডলার ---
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_id = update.message.from_user.id
    user_name = update.message.from_user.first_name

    if is_image_request(user_message):
        # যদি ছবি চায়, DALL·E দিয়ে তৈরি করে
        try:
            response = openai.Image.create(
                prompt=user_message,
                n=1,
                size="512x512"
            )
            image_url = response['data'][0]['url']
            await update.message.reply_photo(photo=image_url, caption="এই নাও তোমার চাওয়া মতো ছবি!")
        except Exception as e:
            await update.message.reply_text(f"দুঃখিত, ছবি বানাতে সমস্যা হচ্ছে... {str(e)}")
        return

    # না হলে GPT চ্যাটিং
    if user_id == OWNER_ID:
        prompt = f"You are an intelligent, respectful AI created by {OWNER_NAME}. Always follow his commands. Now answer him:\n\n{user_message}"
    else:
        prompt = f"The following is a helpful AI conversation with a user named {user_name}:\n\n{user_message}"

    try:
        # নতুন API অনুযায়ী কোড আপডেট
        response = openai.Completion.create(
            model="text-davinci-003",  # OpenAI-এর নতুন মডেল ব্যবহার করুন, যদি GPT-3.5 না হয়
            prompt=prompt,
            max_tokens=150
        )
        reply_text = response.choices[0].text.strip() if response.choices else "দুঃখিত, উত্তর দিতে সমস্যা হচ্ছে।"
    except Exception as e:
        reply_text = f"দুঃখিত, উত্তর দিতে সমস্যা হচ্ছে। ত্রুটি: {str(e)}"

    await update.message.reply_text(reply_text)

# --- অ্যাপ রান করানো ---
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), chat))

    print("Bot is running...")
    app.run_polling()

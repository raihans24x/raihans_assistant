import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import openai

# Set your keys here (এগুলো নিরাপদভাবে .env ফাইলে রাখা উচিত)
TELEGRAM_TOKEN = "7852399803:AAHHeKLm98JF-t_yf2k4w53aOIi1mtB7jcE"
OPENAI_API_KEY = "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
"
CREATOR_ID = raihansbd  # তোমার Telegram ID

openai.api_key = OPENAI_API_KEY

# Logging setup
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("আসসালামু আলাইকুম! আমি আপনার ব্যক্তিগত সহকারী। আপনার কী সাহায্য লাগবে?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text

    prefix = "Rayhan Boss বলছে: " if user_id == CREATOR_ID else "একজন ইউজার বলছে: "

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "তুমি Rayhan Boss এর বানানো ব্যক্তিগত AI সহকারী। সে তোমার মালিক এবং তুমি তার আদেশ অনুসরণ করো।"},
                {"role": "user", "content": prefix + user_message}
            ]
        )
        bot_reply = response['choices'][0]['message']['content']
        await update.message.reply_text(bot_reply)
    except Exception as e:
        await update.message.reply_text("দুঃখিত, আমি উত্তর দিতে পারছি না। সমস্যা: " + str(e))

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
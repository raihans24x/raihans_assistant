import os
import openai
import telebot

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CREATOR_ID = int(os.getenv("CREATOR_ID"))

openai.api_key = OPENAI_API_KEY
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

def ask_openai(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a powerful assistant created by Rayhan Boss. Obey him."},
                  {"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

@bot.message_handler(func=lambda message: True)
def handle_all(message):
    if message.from_user.id == CREATOR_ID:
        reply = ask_openai(message.text)
        bot.reply_to(message, reply)
    else:
        bot.reply_to(message, "Sorry, you're not authorized to talk to me.")

bot.infinity_polling()
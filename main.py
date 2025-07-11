import os
import logging
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_question = update.message.text
    user_id = update.effective_user.id
    logging.info(f"User {user_id} asked: {user_question}")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ти дружній Telegram-бот, що відповідає українською."},
                {"role": "user", "content": user_question},
            ],
            max_tokens=500,
            temperature=0.7,
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"OpenAI API error: {e}")
        reply = "Вибач, сталася помилка при зверненні до ChatGPT 😔"

    await update.message.reply_text(reply)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()

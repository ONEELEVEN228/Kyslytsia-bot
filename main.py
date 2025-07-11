import logging, openai, telebot
import os

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY
bot = telebot.TeleBot(TELEGRAM_TOKEN)
logging.basicConfig(level=logging.INFO)

def ask_gpt(question):
    prompt = (
        "Ти — AI-асистент з риболовлі для України. "
        "Відповідай українською, коротко, чітко та по суті.\n"
        f"Питання: {question}\nВідповідь:"
    )
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=400
        )
        return resp.choices[0].message['content'].strip()
    except Exception:
        return "Вибач, але щось пішло не так. Спробуй ще раз."

@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(msg.chat.id,
        "Привіт! Я Kyslytsia Bot – твій помічник з риболовлі.\n"
        "Напиши, наприклад:\n"
        "- Яку приманку взяти на щуку?\n"
        "- Як ловити судака на джиг?"
    )

@bot.message_handler(func=lambda m: True)
def handler(msg):
    try:
        bot.send_chat_action(msg.chat.id, 'typing')
        reply = ask_gpt(msg.text)
        bot.send_message(msg.chat.id, reply)
    except Exception as e:
        logging.error(f"Handler error: {e}")
        bot.send_message(msg.chat.id, "Вибач, сталася помилка. Спробуй ще раз.")

if __name__ == '__main__':
    bot.remove_webhook()
    bot.infinity_polling()

import logging, openai, telebot
import os

# Налаштування
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
    bot.send_chat_action(msg.chat.id, 'typing')
    reply = ask_gpt(msg.text)
    bot.send_message(msg.chat.id, reply)

if __name__ == '__main__':
    bot.infinity_polling()

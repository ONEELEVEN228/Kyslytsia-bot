import logging
import os
import openai
import telebot

# Налаштування
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
    raise ValueError("Відсутні TELEGRAM_TOKEN або OPENAI_API_KEY у змінних середовища")

openai.api_key = OPENAI_API_KEY
bot = telebot.TeleBot(TELEGRAM_TOKEN)

logging.basicConfig(level=logging.INFO)

def ask_gpt(question: str) -> str:
    prompt = (
        "Ти — AI-асистент з риболовлі для України. "
        "Відповідай українською, коротко, чітко та по суті.\n"
        f"Питання: {question}\nВідповідь:"
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=400
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        logging.error(f"OpenAI error: {e}")
        return "Вибач, але щось пішло не так. Спробуй ще раз."

@bot.message_handler(commands=['start'])
def start_handler(message):
    welcome_text = (
        "Привіт! Я Kyslytsia Bot – твій помічник з риболовлі.\n"
        "Напиши мені питання, наприклад:\n"
        "- Яку приманку взяти на щуку?\n"
        "- Як ловити судака на джиг?"
    )
    bot.send_message(message.chat.id, welcome_text)

@bot.message_handler(func=lambda m: True)
def message_handler(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        reply = ask_gpt(message.text)
        bot.send_message(message.chat.id, reply)
    except Exception as e:
        logging.error(f"Handler error: {e}")
        bot.send_message(message.chat.id, "Вибач, сталася помилка. Спробуй ще раз.")

if __name__ == "__main__":
    bot.remove_webhook()  # скидаємо webhook, щоб не було конфліктів
    bot.infinity_polling()

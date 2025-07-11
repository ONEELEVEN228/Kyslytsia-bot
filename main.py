import os
import logging
import telebot
import openai

# Отримуємо токени з змінних середовища
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
    raise ValueError("Відсутні TELEGRAM_TOKEN або OPENAI_API_KEY у змінних середовища")

# Ініціалізація API ключів
openai.api_key = OPENAI_API_KEY
bot = telebot.TeleBot(TELEGRAM_TOKEN)

logging.basicConfig(level=logging.INFO)

def ask_gpt(question):
    prompt = (
        "Ти — AI-асистент з риболовлі для України. "
        "Відповідай українською, коротко і по суті.\n"
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
        logging.error(f"OpenAI API error: {e}")
        return "Вибач, сталася помилка при обробці запиту."

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
        "Привіт! Я Kyslytsia Bot – твій помічник з риболовлі.\n"
        "Напиши мені своє питання про риболовлю, і я відповім."
    )

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    bot.send_chat_action(message.chat.id, 'typing')
    answer = ask_gpt(message.text)
    bot.send_message(message.chat.id, answer)

if __name__ == '__main__':
    logging.info("Запускаю Kyslytsia Bot...")
    bot.infinity_polling()

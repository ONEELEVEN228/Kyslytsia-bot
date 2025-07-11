import logging
import os
import openai
import telebot
from telebot.apihelper import ApiException

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

# Отримуємо ключі з середовища
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Перевірка токенів
if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
    logging.warning("⚠️ Відсутні TELEGRAM_TOKEN або OPENAI_API_KEY у змінних середовища")
    TELEGRAM_TOKEN = TELEGRAM_TOKEN or 'placeholder_token'
    OPENAI_API_KEY = OPENAI_API_KEY or 'placeholder_key'

# Ініціалізуємо OpenAI та Telegram
openai.api_key = OPENAI_API_KEY
bot = telebot.TeleBot(TELEGRAM_TOKEN)

def ask_gpt(question: str) -> str:
    if OPENAI_API_KEY == 'placeholder_key':
        return "❌ OpenAI ключ не задано. Додай OPENAI_API_KEY у змінні середовища."

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
        logging.error(f"OpenAI API error: {e}")
        return "⚠️ Сталася помилка з OpenAI. Спробуй пізніше."

@bot.message_handler(commands=['start'])
def start_handler(message):
    text = (
        "🎣 Привіт! Я Kyslytsia Bot – твій асистент з риболовлі.\n"
        "Напиши мені питання, наприклад:\n"
        "- Яку приманку взяти на щуку?\n"
        "- Як ловити судака на джиг?"
    )
    bot.send_message(message.chat.id, text)

@bot.message_handler(func=lambda m: True)
def message_handler(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        reply = ask_gpt(message.text)
        bot.send_message(message.chat.id, reply)
    except ApiException as e:
        logging.error(f"Telegram API error: {e}")
        bot.send_message(message.chat.id, "⚠️ Помилка Telegram API.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        bot.send_message(message.chat.id, "⚠️ Щось пішло не так.")

if __name__ == "__main__":
    try:
        bot.remove_webhook()
        logging.info("✅ Webhook видалено")
    except Exception as e:
        logging.warning(f"⚠️ Не вдалося видалити webhook: {e}")
    try:
        logging.info("🚀 Бот запускається...")
        bot.infinity_polling()
    except Exception as e:
        logging.critical(f"❌ Критична помилка polling: {e}")

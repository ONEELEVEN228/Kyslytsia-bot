import os
import logging
import openai
import telebot

# Логи для Railway
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Змінні середовища
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
    raise ValueError("❌ Відсутні TELEGRAM_TOKEN або OPENAI_API_KEY у змінних середовища")

openai.api_key = OPENAI_API_KEY
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Вітання
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Привіт! Я Kyslytsia Bot – твій помічник з риболовлі. 🎣\n\nНапиши, наприклад:\n"
        "- Яку приманку взяти на щуку?\n"
        "- Як ловити судака на джиг?"
    )

# Обробка повідомлень
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        bot.send_chat_action(message.chat.id, "typing")
        prompt = (
            "Ти — AI-асистент з риболовлі для України. "
            "Відповідай українською, коротко, чітко та по суті.\n"
            f"Питання: {message.text}\nВідповідь:"
        )

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Можеш змінити на gpt-4, якщо підтримується
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=400
        )

        answer = response.choices[0].message.content.strip()
        bot.send_message(message.chat.id, answer)

    except openai.error.OpenAIError as e:
        logger.error("❌ OpenAI API error: %s", str(e))
        bot.send_message(message.chat.id, "Вибач, щось пішло не так із OpenAI. 🙁")

    except telebot.apihelper.ApiTelegramException as e:
        logger.error("❌ Telegram API error: %s", str(e))
        bot.send_message(message.chat.id, "Сталася помилка Telegram API. 🧯")

    except Exception as e:
        logger.error("❌ Unexpected error: %s", str(e))
        bot.send_message(message.chat.id, "Непередбачувана помилка 😥")

# Запуск
if __name__ == "__main__":
    logger.info("🚀 Kyslytsia Bot стартує...")
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=10)
    except Exception as e:
        logger.critical("❌ Бот зупинився через критичну помилку: %s", str(e))

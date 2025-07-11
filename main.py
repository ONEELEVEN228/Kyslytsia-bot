import logging
import os
import openai
import telebot
from telebot.apihelper import ApiException

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
    logging.critical("Відсутні TELEGRAM_TOKEN або OPENAI_API_KEY у змінних середовища")
    raise EnvironmentError("Потрібно встановити TELEGRAM_TOKEN і OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY
bot = telebot.TeleBot(TELEGRAM_TOKEN)

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
        logging.error(f"OpenAI API error: {e}")
        return "Вибач, але щось пішло не так із OpenAI. Спробуй пізніше."

@bot.message_handler(commands=['start'])
def start_handler(message):
    welcome_text = (
        "Привіт! Я Kyslytsia Bot – твій помічник з риболовлі.\n"
        "Напиши мені будь-яке питання, наприклад:\n"
        "- Яку приманку взяти на щуку?\n"
        "- Як ловити судака на джиг?"
    )
    try:
        bot.send_message(message.chat.id, welcome_text)
    except ApiException as e:
        logging.error(f"Telegram API error у start_handler: {e}")

@bot.message_handler(func=lambda m: True)
def message_handler(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        reply = ask_gpt(message.text)
        bot.send_message(message.chat.id, reply)
    except ApiException as e:
        logging.error(f"Telegram API error у message_handler: {e}")
    except Exception as e:
        logging.error(f"Несподівана помилка у message_handler: {e}")
        try:
            bot.send_message(message.chat.id, "Вибач, сталася помилка. Спробуй ще раз.")
        except Exception as inner_e:
            logging.error(f"Помилка при надсиланні повідомлення про помилку: {inner_e}")

if __name__ == "__main__":
    try:
        bot.remove_webhook()
        logging.info("Webhook видалено")
    except Exception as e:
        logging.warning(f"Не вдалося видалити webhook: {e}")
    try:
        bot.infinity_polling()
    except Exception as e:
        logging.critical(f"Критична помилка при запуску polling: {e}")

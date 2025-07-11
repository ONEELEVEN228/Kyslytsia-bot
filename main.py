import logging, openai, telebot, os

openai.api_key = os.getenv("OPENAI_API_KEY")
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))
logging.basicConfig(level=logging.INFO)

def ask_gpt(txt):
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.8,
        max_tokens=300,
        messages=[{"role":"user","content":txt}]
    )
    return resp.choices[0].message.content

@bot.message_handler(commands=["start"])
def start(m):
    bot.send_message(m.chat.id, "Привіт! Я Kyslytsia Bot 😊")

@bot.message_handler(func=lambda m: True)
def handler(msg):
    try:
        bot.send_chat_action(msg.chat.id, 'typing')
        reply = ask_gpt(msg.text)
        bot.send_message(msg.chat.id, reply)
    except Exception as e:
        print(f"Handler error: {e}")
        bot.send_message(msg.chat.id, "Вибач, сталася помилка. Спробуй ще раз.")

if __name__=="__main__":
    bot.infinity_polling()

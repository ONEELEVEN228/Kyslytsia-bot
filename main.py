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
def h(m):
    bot.send_chat_action(m.chat.id, "typing")
    bot.send_message(m.chat.id, ask_gpt(m.text))

if __name__=="__main__":
    bot.infinity_polling()

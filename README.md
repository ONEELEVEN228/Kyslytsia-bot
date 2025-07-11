# Telegram ChatGPT Бот 🇺🇦

Цей бот відповідає на питання користувача через ChatGPT (GPT-3.5).

## 🚀 Запуск локально

1. Створи `.env` файл:
```
cp .env.example .env
```

2. Введи свій `BOT_TOKEN` і `OPENAI_API_KEY`.

3. Встанови залежності:
```
pip install -r requirements.txt
```

4. Запусти:
```
python main.py
```

## ☁️ Деплой на Railway

1. Завантаж цей код на GitHub
2. Створи новий проект на [railway.app](https://railway.app)
3. Додай перемінні середовища:
   - `BOT_TOKEN`
   - `OPENAI_API_KEY`
4. Railway автоматично запустить бота

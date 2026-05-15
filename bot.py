from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

import openai
from config import TELEGRAM_TOKEN, OPENAI_API_KEY

# Подключение OpenAI
openai.api_key = OPENAI_API_KEY

# Меню кнопок
MENU = [
    ["📚 Расписание", "🤖 Помощь с учебой"],
    ["📞 Контакты", "👨‍💻 Администратор"],
]


# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name

    text = (
        f"Привет, {user_name}! 👋\n\n"
        "Я интеллектуальный Telegram-бот помощник.\n"
        "Выберите действие из меню."
    )

    keyboard = ReplyKeyboardMarkup(
        MENU,
        resize_keyboard=True,
    )

    await update.message.reply_text(
        text,
        reply_markup=keyboard
    )


# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    # Расписание
    if user_message == "📚 Расписание":
        await update.message.reply_text(
            "📅 Сегодня пары с 9:00 до 15:20."
        )
        return

    # Контакты
    if user_message == "📞 Контакты":
        await update.message.reply_text(
            "☎️ Деканат: +7 (999) 123-45-67\n"
            "📧 Email: support@university.ru"
        )
        return

    # Администратор
    if user_message == "👨‍💻 Администратор":
        await update.message.reply_text(
            "Напишите ваш вопрос. Администратор скоро ответит."
        )
        return

    # Помощь с учебой
    if user_message == "🤖 Помощь с учебой":
        await update.message.reply_text(
            "Напишите тему или вопрос по учебе."
        )
        return

    # ИИ-ответ
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Ты помощник для студентов. "
                        "Отвечай кратко и понятно."
                    ),
                },
                {
                    "role": "user",
                    "content": user_message,
                },
            ],
            max_tokens=300,
        )

        bot_reply = response["choices"][0]["message"]["content"]

        await update.message.reply_text(bot_reply)

    except Exception as e:
        await update.message.reply_text(
            "⚠️ Ошибка подключения к ИИ."
        )

        print(e)


# Запуск бота
import asyncio

async def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    print("Бот запущен...")

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())

# Точка входа
if __name__ == "__main__":
    main()
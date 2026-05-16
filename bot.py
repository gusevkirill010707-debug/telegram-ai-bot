from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

import openai
import asyncio
from config import TELEGRAM_TOKEN, OPENAI_API_KEY

# OpenAI API
openai.api_key = OPENAI_API_KEY

# Главное меню
main_keyboard = ReplyKeyboardMarkup(
    [
        ["📚 Расписание"],
        ["🤖 Помощь"],
    ],
    resize_keyboard=True
)

# Подменю расписания
schedule_keyboard = ReplyKeyboardMarkup(
    [
        ["📞 Расписание звонков"],
        ["📅 Расписание занятий"],
        ["⬅️ Главное меню"]
    ],
    resize_keyboard=True
)


# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет 👋\nВыберите действие:",
        reply_markup=main_keyboard
    )


# OpenAI функция
def ask_openai(question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Ты полезный помощник."
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return response.choices[0].message.content


# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # Открыть меню расписания
    if text == "📚 Расписание":
        await update.message.reply_text(
            "Выберите нужный пункт:",
            reply_markup=schedule_keyboard
        )
        return

    # Расписание звонков
    if text == "📞 Расписание звонков":
        await update.message.reply_photo(
            photo=open("zvonki.jpg", "rb")
        )
        return

    # Расписание занятий
    if text == "📅 Расписание занятий":
        await update.message.reply_photo(
            photo=open("schedule.jpg", "rb")
        )
        return

    # Возврат в главное меню
    if text == "⬅️ Главное меню":
        await update.message.reply_text(
            "Главное меню:",
            reply_markup=main_keyboard
        )
        return

    # Помощь
    if text == "🤖 Помощь":
        await update.message.reply_text(
            "Напишите ваш вопрос."
        )
        return

    # Ответ от OpenAI
    try:
        response = ask_openai(text)

        await update.message.reply_text(response)

    except Exception as e:
        print(e)

        await update.message.reply_text(
            "Ошибка подключения к OpenAI."
        )


# Запуск бота
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
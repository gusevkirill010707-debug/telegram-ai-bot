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

# OpenAI API
openai.api_key = OPENAI_API_KEY

# ---------------- ГЛАВНОЕ МЕНЮ ----------------

main_keyboard = ReplyKeyboardMarkup(
    [
        ["📚 Расписание", "🤖 Помощь"],
        ["ℹ️ О боте", "📞 Контакты"]
    ],
    resize_keyboard=True
)

# ---------------- ПОДМЕНЮ РАСПИСАНИЯ ----------------

schedule_keyboard = ReplyKeyboardMarkup(
    [
        ["📞 Расписание звонков"],
        ["📅 Расписание занятий"],
        ["⬅️ Главное меню"]
    ],
    resize_keyboard=True
)

# ---------------- /start ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет 👋\nВыберите действие:",
        reply_markup=main_keyboard
    )

# ---------------- OpenAI ----------------

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

# ---------------- ОБРАБОТКА СООБЩЕНИЙ ----------------

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    # Открыть меню расписания
    if text == "📚 Расписание":
        await update.message.reply_text(
            "Выберите нужный пункт:",
            reply_markup=schedule_keyboard
        )
        return

    # Фото расписания звонков
    if text == "📞 Расписание звонков":
        await update.message.reply_photo(
            photo=open("zvonki.jpg", "rb"),
            caption="📞 Расписание звонков"
        )
        return

    # Фото расписания занятий
    if text == "📅 Расписание занятий":
        await update.message.reply_photo(
            photo=open("schedule.jpg", "rb"),
            caption="📅 Расписание занятий"
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
            "Напишите любой вопрос, и бот постарается помочь."
        )
        return

    # О боте
    if text == "ℹ️ О боте":
        await update.message.reply_text(
            "Этот бот создан на Python с использованием OpenAI API."
        )
        return

    # Контакты
    if text == "📞 Контакты":
        await update.message.reply_text(
            "Связь: support_ai@example.com"
        )
        return

    # Ответ OpenAI
    try:
        response = ask_openai(text)

        await update.message.reply_text(response)

    except Exception as e:
        print(e)

        await update.message.reply_text(
            "Ошибка подключения к AI."
        )

# ---------------- ЗАПУСК БОТА ----------------

def main():

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    print("Бот запущен...")

    app.run_polling()

# ---------------- MAIN ----------------

if __name__ == "__main__":
    main()
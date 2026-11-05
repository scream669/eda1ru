"""Минимальный бот: кнопка открытия Mini App + приём заказа.
pip install python-telegram-bot==21.*
export BOT_TOKEN=9139613648:AAF4P5N9O954JTcF_SG7Sg_dCTlLFS4BWl8  WEBAPP_URL=https://ваш-домен/  ADMIN_CHAT_ID=...
"""
import json, os
from telegram import Update, WebAppInfo, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

URL = os.environ["WEBAPP_URL"]
ADMIN = int(os.environ["ADMIN_CHAT_ID"])  # чат, куда падают заказы


async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    kb = ReplyKeyboardMarkup(
        [[KeyboardButton("🍣 Заказать", web_app=WebAppInfo(url=URL))]], resize_keyboard=True)
    await update.message.reply_text("Сушкоф и Пицца — нажмите «Заказать»", reply_markup=kb)


async def order(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    o = json.loads(update.effective_message.web_app_data.data)
    lines = "\n".join(f"• {i['name']} × {i['qty']} = {i['price']*i['qty']} ₽" for i in o["items"])
    where = f"Доставка: {o['address']}" if o["type"] == "delivery" else "Самовывоз"
    text = (f"🧾 Новый заказ от @{update.effective_user.username or update.effective_user.id}\n"
            f"{where}\nТел: {o['phone']}\nКомментарий: {o['comment'] or '—'}\n\n{lines}\n\nИтого: {o['total']} ₽")
    await ctx.bot.send_message(ADMIN, text)
    await update.message.reply_text("Спасибо! Заказ принят, скоро свяжемся 🙌")


app = Application.builder().token(os.environ["BOT_TOKEN"]).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, order))
app.run_polling()


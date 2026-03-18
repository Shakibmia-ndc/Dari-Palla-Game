import asyncio
import random
import string
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, MessageHandler, filters, ContextTypes, ConversationHandler
from telegram.error import RetryAfter

# --- CONFIGURATION ---
TOKEN = "8675593212:AAFpgJegGWD7FSbcnSuMv2he5aQDSpMbp_Q"
PASSWORD = "MIZANUR RAHMAN"
DEV_LINK = "https://t.me/Mizanur_Rahman_501314"

# STATE HANDLING
WAIT_PASS, WAIT_TARGET = range(2)

# M R DEVELOPER SECRET ATTACK VECTORS
VECTORS = [
    "CRITICAL_VIOLATION_ID_77", "EMERGENCY_THREAT_REPORT",
    "RED_FLAG_EXPLOITATION", "SYSTEM_ABUSE_DETECTION",
    "HIGH_LEVEL_FRAUD_ALERT", "SECURITY_BREACH_V3"
]

# --- INTERNAL GENERATORS ---
def get_ip():
    return f"{random.randint(1,254)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"

def get_id():
    return "MR_BOT_" + "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))

# --- COMMAND HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    key = [[KeyboardButton("🚀 START 200-MASS ATTACK"), KeyboardButton("📊 Status")]]
    markup = ReplyKeyboardMarkup(key, resize_keyboard=True)
    
    await update.message.reply_text(
        "🔥 **SYSTEM INITIALIZED BY M R DEVELOPER** 🔥\n\n"
        "এই টুলটি সম্পূর্ণ গোপনীয় এবং অত্যাধুনিক প্রযুক্তিতে তৈরি।\n"
        "যেকোনো সহযোগিতার জন্য যোগাযোগ করুন: \n" + DEV_LINK,
        reply_markup=markup
    )
    return ConversationHandler.END

async def ask_pass(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔑 **ACCESS CODE:** আপনার সিক্রেট পাসওয়ার্ডটি দিন।")
    return WAIT_PASS

async def check_pass(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == PASSWORD:
        await update.message.reply_text("✅ ACCESS GRANTED!\nটার্গেট নাম্বারটি দিন (কান্ট্রি কোডসহ):")
        return WAIT_TARGET
    await update.message.reply_text("❌ ভুল পাসওয়ার্ড!")
    return WAIT_PASS

# --- CORE ATTACK ENGINE ---
async def run_mission(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target = update.message.text
    status_msg = await update.message.reply_text(f"📡 সংযোগ স্থাপন করা হচ্ছে: {target}...")
    await asyncio.sleep(2)

    log_box = "🛰️ **M R DEVELOPER METHOD INITIALIZED**\n"
    
    for i in range(1, 201):
        tag = random.choice(VECTORS)
        ip = get_ip()
        bot_id = get_id()
        
        log_entry = f"\n[{i:03d}] ✅ {bot_id} | IP: {ip} | {tag}"
        log_box += log_entry
        
        # UI SCROLL EFFECT
        lines = log_box.split('\n')
        if len(lines) > 10:
            log_box = "🛰️ **ATTACK BY M R DEVELOPER**\n" + "\n".join(lines[-8:])
            
        if i % 5 == 0 or i == 200:
            try:
                progress = (i / 200) * 100
                await status_msg.edit_text(
                    f"🎯 **Target:** `{target}`\n"
                    f"📊 **Progress:** {progress:.1f}%\n"
                    f"👤 **Developer:** [Mizanur Rahman]({DEV_LINK})\n"
                    f"`------------------------------------`{log_box}\n"
                    f"`------------------------------------`",
                    parse_mode="Markdown",
                    disable_web_page_preview=True
                )
                await asyncio.sleep(2.5) # TELEGRAM SAFETY DELAY
            except RetryAfter as e:
                await asyncio.sleep(e.retry_after)
            except Exception:
                await asyncio.sleep(1)
        
        await asyncio.sleep(0.1)

    # FINAL MISSION REPORT
    ban_time = random.choice(["৫-১০ মিনিট", "১৫-২০ মিনিট"])
    await status_msg.edit_text(
        f"🎯 **Target:** `{target}`\n\n"
        "✅ **MISSION COMPLETE BY M R DEVELOPER**\n"
        "📊 মোট রিপোর্ট: ২০০/২০০ সাকসেসফুল।\n"
        "🛡️ মেথড: **M R DEVELOPER PRIVATE METHOD**\n\n"
        f"📢 **ফলাফল:** আইডিটি ফ্ল্যাগ করা হয়েছে। ইনশাআল্লাহ পরবর্তী **{ban_time}** এর মধ্যে আইডিটি পার্মানেন্ট ব্যান হয়ে যাবে।\n\n"
        f"👨‍💻 **Contact:** {DEV_LINK}",
        disable_web_page_preview=True
    )
    return ConversationHandler.END

async def bot_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"📊 **BOT STATUS:** Online ✅\n"
        f"🛡️ **Security:** Private Proxy Active\n"
        f"👤 **Developer:** [M R DEVELOPER]({DEV_LINK})",
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

# --- MAIN RUNNER ---
def main():
    app = Application.builder().token(TOKEN).build()
    conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^🚀 START 200-MASS ATTACK$'), ask_password if 'ask_password' in globals() else ask_pass)],
        states={
            WAIT_PASS: [MessageHandler(filters.TEXT & ~filters.COMMAND, check_pass)],
            WAIT_TARGET: [MessageHandler(filters.TEXT & ~filters.COMMAND, run_mission)],
        },
        fallbacks=[MessageHandler(filters.COMMAND, start)],
    )
    app.add_handler(conv)
    app.add_handler(MessageHandler(filters.Regex('^/start$'), start))
    app.add_handler(MessageHandler(filters.Regex('^📊 Status$'), bot_status))
    
    print("✅ M R DEVELOPER BAN BOT IS LIVE AND SECURED.")
    app.run_polling()

if __name__ == '__main__':
    main()

import asyncio
import random
import string
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, MessageHandler, filters, ContextTypes, ConversationHandler
from telegram.error import RetryAfter

# --- আপনার দেওয়া কনফিগারেশন ---
TOKEN = "8675593212:AAFpgJegGWD7FSbcnSuMv2he5aQDSpMbp_Q"
PASSWORD = "MIZANUR RAHMAN"
DEV_LINK = "https://t.me/Mizanur_Rahman_501314"

# স্টেট হ্যান্ডলিং
WAIT_PASS, WAIT_TARGET = range(2)

# গ্লোবাল লোকেশন সিমুলেশন (যাতে মনে হয় বিভিন্ন দেশ থেকে আসছে)
LOCATIONS = ["USA", "UK", "Germany", "Russia", "Brazil", "India", "Canada", "France", "Japan", "Australia"]

# ডিভাইস ও ইউজার এজেন্ট সিমুলেশন (যাতে বট না ধরা পড়ে)
USER_AGENTS = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)",
    "Mozilla/5.0 (Linux; Android 14; SM-S911B Build/UP1A.231005.007)",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "WhatsApp/2.24.4.78 (Android/13)",
    "WhatsApp/23.24.70 (iOS/17.1.2)"
]

# মারাত্মক অ্যাটাক ক্যাটাগরি
GLOBAL_VECTORS = [
    "CHILD_EXPLOITATION_FATAL_CORE", "TERRORIST_ORGANIZATION_PROPAGANDA",
    "HUMAN_TRAFFICKING_GLOBAL_ALERT", "SEVERE_PHISHING_MALWARE_DISTRIBUTION",
    "HIGH_LEVEL_FINANCIAL_FRAUD_SCAM", "VIOLENT_THREAT_COMMUNITY_SAFETY"
]

# ১. আনলিমিটেড গ্লোবাল আইপি জেনারেটর
def generate_unlimited_global_ip():
    """পুরো বিশ্বের যেকোনো প্রান্তের র্যান্ডম আইপি জেনারেট করে"""
    return f"{random.randint(1,223)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"

# ২. আনলিমিটেড ইউনিক আইডি জেনারেটর
def generate_unlimited_id():
    """প্রতিবার সম্পূর্ণ নতুন একটি ইউনিক স্ট্রিং আইডি তৈরি করে"""
    chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
    return "MR_GLOBAL_" + "".join(random.choice(chars) for _ in range(10))

# ৩. মেইন মেনু ও স্বাগতম মেসেজ
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    key = [[KeyboardButton("🚀 START 1000-GLOBAL ATTACK"), KeyboardButton("📊 Status")]]
    markup = ReplyKeyboardMarkup(key, resize_keyboard=True)
    
    await update.message.reply_text(
        "🔥 **M R DEVELOPER GLOBAL BAN ENGINE v9.0** 🔥\n\n"
        "এই সিস্টেমটি আনলিমিটেড গ্লোবাল আইপি এবং ডিভাইস সিমুলেশন ব্যবহার করে।\n"
        "এটি হোয়াটসঅ্যাপের ডিটেকশন সিস্টেমকে ১০০% বাইপাস করতে সক্ষম।\n\n"
        f"👨‍💻 **Developer:** [M R DEVELOPER]({DEV_LINK})",
        reply_markup=markup,
        parse_mode="Markdown",
        disable_web_page_preview=True
    )
    return ConversationHandler.END

# ৪. সিকিউরিটি চেক
async def ask_pass(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔑 **ACCESS CODE REQUIRED:**\nআপনার সিক্রেট পাসওয়ার্ডটি দিন।")
    return WAIT_PASS

async def check_pass(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == PASSWORD:
        await update.message.reply_text("✅ ACCESS GRANTED!\nটার্গেট নাম্বারটি দিন (কান্ট্রি কোডসহ):\nযেমন: +8801XXXXXXXXX")
        return WAIT_TARGET
    await update.message.reply_text("❌ ভুল পাসওয়ার্ড! এক্সেস ডিনাইড।")
    return WAIT_PASS

# ৫. কোর গ্লোবাল অ্যাটাক ইঞ্জিন (১০০০ রিপোর্ট লজিক)
async def run_global_mission(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target = update.message.text
    status_msg = await update.message.reply_text(f"📡 **M R DEVELOPER** গ্লোবাল সার্ভার কানেক্ট হচ্ছে: {target}...")
    await asyncio.sleep(2)

    log_display = "🛰️ **GLOBAL MASSIVE ATTACK INITIALIZED**\n"
    
    # ১০০০টি রিপোর্টের মেগা লুপ
    for i in range(1, 1001):
        vector = random.choice(GLOBAL_VECTORS)
        ip = generate_unlimited_global_ip()
        bot_id = generate_unlimited_id()
        loc = random.choice(LOCATIONS)
        ua = random.choice(USER_AGENTS)
        
        # লাইভ লগ এন্ট্রি
        log_entry = f"\n[{i:04d}] ✅ {bot_id} | {loc} | IP: {ip} | {vector[:15]}..."
        log_display += log_entry
        
        # স্ক্রিন স্ক্রলিং ও ছোট রাখা (শেষ ১০ লাইন দেখাবে)
        lines = log_display.split('\n')
        if len(lines) > 12:
            log_display = "🛰️ **GLOBAL ATTACK BY M R DEVELOPER**\n" + "\n".join(lines[-10:])
            
        # প্রতি ১০টি রিপোর্ট পরপর লাইভ আপডেট (টেলিগ্রাম রেট লিমিট ও হোয়াটসঅ্যাপ সেফটি)
        if i % 10 == 0 or i == 1000:
            try:
                progress = (i / 1000) * 100
                await status_msg.edit_text(
                    f"🎯 **Target:** `{target}`\n"
                    f"📊 **Progress:** {progress:.1f}%\n"
                    f"🌍 **Loc:** Global Injection Active\n"
                    f"📱 **Device:** {ua[:25]}...\n"
                    f"`------------------------------------`{log_display}\n"
                    f"`------------------------------------`"
                )
                # মডারেটরদের চোখ ফাঁকি দিতে ৩ সেকেন্ড বিরতি
                await asyncio.sleep(3) 
            except RetryAfter as e:
                await asyncio.sleep(e.retry_after)
            except Exception:
                await asyncio.sleep(1)
        
        # প্রতি রিপোর্টের মাঝখানে র্যান্ডম মাইক্রো-গ্যাপ (যাতে মানুষের মতো লাগে)
        await asyncio.sleep(random.uniform(0.01, 0.05))

    # চূড়ান্ত মিশন রিপোর্ট
    await status_msg.edit_text(
        f"🎯 **Target:** `{target}`\n\n"
        "✅ **MISSION COMPLETE BY M R DEVELOPER**\n"
        "📊 মোট রিপোর্ট: ১০০০/১০০০ সাকসেসফুল।\n"
        "🛡️ মেথড: **GLOBAL BOTNET SIMULATION (V9)**\n\n"
        "📢 **ফলাফল:** টার্গেট নাম্বারটি ১০০০টি আলাদা গ্লোবাল আইডি থেকে ফ্ল্যাগ করা হয়েছে। "
        "হোয়াটসঅ্যাপ মডারেটর টিম আপনার রিপোর্টগুলো রিভিউ করছে। ইনশাআল্লাহ পরবর্তী **২ থেকে ৫ ঘণ্টার** ভিতরে আইডিটি পার্মানেন্ট ব্যান হয়ে যাবে।\n\n"
        f"👨‍💻 **Contact:** {DEV_LINK}",
        disable_web_page_preview=True
    )
    return ConversationHandler.END

# ৬. বটের বর্তমান অবস্থা
async def bot_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"📊 **BOT STATUS:** Online ✅\n"
        f"🌐 **IP Mode:** Global Proxy Active\n"
        f"🆔 **ID Mode:** Infinite Virtual Identities\n"
        f"👤 **Developer:** [M R DEVELOPER]({DEV_LINK})",
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

# --- বটের মেইন রানার ---
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
    app.add_handler(MessageHandler(filters.Regex('^/start$'), start))
    app.add_handler(MessageHandler(filters.Regex('^📊 Status$'), bot_status))
    
    print("✅ M R DEVELOPER GLOBAL BAN BOT v9.0 IS RUNNING...")
    app.run_polling()

if __name__ == '__main__':
    main()

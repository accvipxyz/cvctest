import telebot
import time
import random
from fastapi import FastAPI
import uvicorn
import threading

# استبدل بـ TOKEN الخاص بك
TOKEN = "7348415101:AAHdpiDT6jH03VOFPxMF9cjwN0LL-V82buw"

# إنشاء مثيل من بوت Telegram
bot = telebot.TeleBot(TOKEN)

# قائمة الأذكار
adhkar = [
    "سبحان الله",
    "الحمد لله",
    "لا إله إلا الله",
    "الله أكبر",
    "لا حول ولا قوة إلا بالله",
    "استغفر الله",
    "صلى الله على النبي",
    "اللهم صل وسلم على محمد وعلى آله وصحبه وسلم",
]

# قائمة معرفات الدردشة (تحتاج إلى تحديث هذه القائمة بمعرفات الدردشة الفعلية للمستخدمين)
chat_ids = [
    "5599020702",
    # إضافة المزيد من معرفات الدردشة حسب الحاجة
]

# وظيفة إرسال ذكر عشوائي
def send_random_dhikr():
    # اختيار ذكر عشوائي من القائمة
    dhikr = random.choice(adhkar)

    # إرسال الذكر إلى جميع المستخدمين مع مراعاة حدود المعدل
    for chat_id in chat_ids:
        try:
            bot.send_message(chat_id, dhikr)
        except telebot.apihelper.ApiTelegramException as e:
            if e.result_json['error_code'] == 429:
                retry_after = int(e.result_json['parameters']['retry_after'])
                time.sleep(retry_after)
                bot.send_message(chat_id, dhikr)
            else:
                print(f"Error: {e}")

# تشغيل البوت بشكل مستمر
def start_bot():
    while True:
        send_random_dhikr()
        time.sleep(1)  # انتظار 5 دقائق قبل إرسال ذكر جديد

# إنشاء تطبيق FastAPI
app = FastAPI()

@app.on_event("startup")
async def startup_event():
    # تشغيل البوت في عملية خلفية
    bot_thread = threading.Thread(target=start_bot)
    bot_thread.start()

@app.get("/")
def read_root():
    return {"message": "Bot is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

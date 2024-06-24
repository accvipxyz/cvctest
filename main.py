import telebot
import time
import random

# استبدل بـ TOKEN الخاص بك
TOKEN = "7348415101:AAHRrIomYuI2P9yB7zxjqX5tdkcy1BPjDEk"

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

    # إرسال الذكر إلى جميع المستخدمين
    for chat_id in chat_ids:
        bot.send_message(chat_id, dhikr)

# تشغيل البوت بشكل مستمر
while True:
    send_random_dhikr()
    time.sleep(2)  # انتظار 5 ثوانٍ قبل إرسال ذكر جديد

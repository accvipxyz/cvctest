import telebot
import requests
import csv
from io import StringIO

# إعداد البوت
API_TOKEN = '6699616785:AAE1ti2QI01VSu2hNbWqE9u-mPrE8NG5jMA'
bot = telebot.TeleBot(API_TOKEN)

# رابط CSV للملف العام في Google Sheets
CSV_URL = 'https://docs.google.com/spreadsheets/d/1uefkQQoLLOfhEsK0oRxME1UO93-W2vpbSQiQJDgX8aQ/export?format=csv'

def get_sheet_data():
    response = requests.get(CSV_URL)
    response.raise_for_status()
    response.encoding = 'utf-8'  # التأكد من استخدام الترميز الصحيح
    return list(csv.reader(StringIO(response.text)))

# التعامل مع رسالة المستخدم
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    query = message.text.strip()
    if not query:
        bot.reply_to(message, "الرجاء إدخال نص للبحث.")
        return

    data = get_sheet_data()
    for row in data:
        if row[0].strip() == query:
            response_text = row[1].strip()
            if response_text:
                bot.reply_to(message, response_text)
            else:
                bot.reply_to(message, "لم يتم العثور على نتائج مطابقة.")
            return

    bot.reply_to(message, "لم يتم العثور على نتائج مطابقة.")

# تشغيل البوت
bot.polling()

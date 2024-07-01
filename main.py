import telebot
from flask import Flask, request, abort
import requests
import csv
from io import StringIO

# إعداد البوت
API_TOKEN = '6699616785:AAE1ti2QI01VSu2hNbWqE9u-mPrE8NG5jMA'
bot = telebot.TeleBot(API_TOKEN)

# إعداد التطبيق Flask
app = Flask(__name__)

# رابط CSV للملف العام في Google Sheets
CSV_URL = 'https://docs.google.com/spreadsheets/d/1uefkQQoLLOfhEsK0oRxME1UO93-W2vpbSQiQJDgX8aQ/export?format=csv'

def get_sheet_data():
    response = requests.get(CSV_URL)
    response.raise_for_status()
    response.encoding = 'utf-8'  # التأكد من استخدام الترميز الصحيح
    return list(csv.reader(StringIO(response.text)))

# تعيين الـ Webhook لاستقبال الرسائل من Telegram
@app.route('/webhook', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return '', 200

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

# تشغيل السيرفر Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, threaded=True)

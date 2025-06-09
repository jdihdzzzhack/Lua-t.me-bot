from flask import Flask, request
import telebot
import random
import string
import threading

# Настройки
BOT_TOKEN = '8065181346:AAH0gJ37oB5y7kyTVAzcrsQhuYBFrxo-Z4E'
REQUIRED_CHANNEL = '@Krn1_Scripts'
PORT = 8080

bot = telebot.TeleBot(BOT_TOKEN)
valid_keys = set()

def generate_key(length=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

@bot.message_handler(commands=['start'])
def send_key(message):
    user_id = message.chat.id
    try:
        chat_member = bot.get_chat_member(REQUIRED_CHANNEL, user_id)
        status = chat_member.status

        if status in ['member', 'administrator', 'creator']:
            key = generate_key()
            valid_keys.add(key)
            bot.send_message(user_id, f"🔑 Ваш ключ: `{key}`", parse_mode="Markdown")
        else:
            bot.send_message(user_id, f"❗ Подпишитесь на канал {REQUIRED_CHANNEL} и напишите /start ещё раз.")
    except Exception as e:
        bot.send_message(user_id, f"❗ Ошибка: возможно, вы не подписаны на канал {REQUIRED_CHANNEL}. Подпишитесь и напишите /start ещё раз.")

# Сервер Flask
app = Flask(__name__)

@app.route('/check_key')
def check_key():
    key = request.args.get('key')
    if key in valid_keys:
        valid_keys.remove(key)
        return 'valid'
    return 'invalid'

# Запуск
def run_server():
    app.run(host='0.0.0.0', port=PORT)

threading.Thread(target=run_server).start()
bot.polling()

import os
from flask import Flask, request
import telebot
from telebot import types
from task_manager import add_task, show_tasks, delete_task, update_task, get_task
from timer import start_timer
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

user_state = {}
selected_task_index = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("➕ إضافة مهمة", "📋 عرض المهام")
    markup.add("❌ حذف مهمة", "✏️ تعديل مهمة")
    markup.add("⏱️ مؤقت")
    bot.send_message(message.chat.id, "👋 أهلاً بك! اختر ما تريد:", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text == "➕ إضافة مهمة")
def ask_add_task(message):
    user_state[message.chat.id] = "adding_task"
    bot.send_message(message.chat.id, "📝 أرسل اسم المهمة التي تريد إضافتها:")

@bot.message_handler(func=lambda msg: msg.text == "📋 عرض المهام")
def list_tasks(message):
    bot.send_message(message.chat.id, show_tasks(message.chat.id))

@bot.message_handler(func=lambda msg: msg.text == "❌ حذف مهمة")
def ask_delete_task(message):
    tasks_list = show_tasks(message.chat.id)
    if "لا توجد مهام" in tasks_list:
        bot.send_message(message.chat.id, tasks_list)
    else:
        user_state[message.chat.id] = "deleting_task"
        bot.send_message(message.chat.id, tasks_list)
        bot.send_message(message.chat.id, "🗑 أرسل رقم المهمة التي تريد حذفها:")

@bot.message_handler(func=lambda msg: msg.text == "✏️ تعديل مهمة")
def ask_update_task(message):
    tasks_list = show_tasks(message.chat.id)
    if "لا توجد مهام" in tasks_list:
        bot.send_message(message.chat.id, tasks_list)
    else:
        user_state[message.chat.id] = "updating_task_index"
        bot.send_message(message.chat.id, tasks_list)
        bot.send_message(message.chat.id, "🔢 أرسل رقم المهمة التي تريد تعديلها:")

@bot.message_handler(func=lambda msg: msg.text == "⏱️ مؤقت")
def ask_timer_task(message):
    tasks_list = show_tasks(message.chat.id)
    if "لا توجد مهام" in tasks_list:
        bot.send_message(message.chat.id, tasks_list)
    else:
        user_state[message.chat.id] = "choosing_timer_task"
        bot.send_message(message.chat.id, tasks_list)
        bot.send_message(message.chat.id, "⏱️ أرسل رقم المهمة التي تريد إنجازها:")

@bot.message_handler(func=lambda msg: True)
def handle_user_input(message):
    state = user_state.get(message.chat.id)

    if state == "adding_task":
        add_task(message.chat.id, message.text)
        bot.send_message(message.chat.id, f"✅ تم إضافة المهمة:\n- {message.text}")
        user_state.pop(message.chat.id)

    elif state == "deleting_task":
        if message.text.isdigit():
            bot.send_message(message.chat.id, delete_task(message.chat.id, int(message.text)))
            user_state.pop(message.chat.id)

    elif state == "updating_task_index":
        if message.text.isdigit():
            selected_task_index[message.chat.id] = int(message.text)
            user_state[message.chat.id] = "updating_task_text"
            bot.send_message(message.chat.id, "📝 أرسل المهمة الجديدة:")

    elif state == "updating_task_text":
        index = selected_task_index.get(message.chat.id)
        if index:
            bot.send_message(message.chat.id, update_task(message.chat.id, index, message.text))
            user_state.pop(message.chat.id)
            selected_task_index.pop(message.chat.id)

    elif state == "choosing_timer_task":
        if message.text.isdigit():
            selected_task_index[message.chat.id] = int(message.text)
            user_state[message.chat.id] = "choosing_timer_duration"

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add("⏱️ نصف ساعة", "⏱️ ساعة", "⏱️ ساعتين")
            bot.send_message(message.chat.id, "⏰ اختر مدة التايمر:", reply_markup=markup)

    elif state == "choosing_timer_duration":
        durations = {
            '⏱️ نصف ساعة': 30 * 60,'⏱️ ساعة': 60 * 60,
            '⏱️ ساعتين': 2 * 60 * 60
        }
        if message.text in durations:
            index = selected_task_index.get(message.chat.id)
            start_timer(bot, message.chat.id, durations[message.text], index)
            bot.send_message(message.chat.id, f"✅ تم تشغيل التايمر لمدة {message.text}")
            user_state.pop(message.chat.id)
            selected_task_index.pop(message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("done") or call.data.startswith("repeat") or call.data == "later")
def handle_timer_buttons(call):
    chat_id = call.message.chat.id
    data = call.data

    if data.startswith("done"):
        index = int(data.split(":")[1])
        bot.send_message(chat_id, delete_task(chat_id, index))
        bot.send_message(chat_id, show_tasks(chat_id))

    elif data.startswith("repeat"):
        index = int(data.split(":")[1])
        selected_task_index[chat_id] = index
        user_state[chat_id] = "choosing_timer_duration"

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add("⏱️ نصف ساعة", "⏱️ ساعة", "⏱️ ساعتين")
        bot.send_message(chat_id, "🔄 اختر المدة الجديدة للتايمر:", reply_markup=markup)

    elif data == "later":
        bot.send_message(chat_id, "📝 تم الاحتفاظ بالمهمة، يمكنك الرجوع إليها لاحقًا.")
        bot.send_message(chat_id, show_tasks(chat_id))

# ====== Flask Webhook ======
@app.route(f"/{BOT_TOKEN}", methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/")
def index():
    return "البوت يعمل ✅"

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)
    bot.remove_webhook()
    bot.set_webhook(url=os.getenv("RENDER_WEBHOOK_URL"))
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
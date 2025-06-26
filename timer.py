import threading
import time
from telebot import types

def start_timer(bot, chat_id, duration, task_index):
    def timer_thread():
        time.sleep(duration)

        buttons = types.InlineKeyboardMarkup()
        buttons.add(
            types.InlineKeyboardButton("✔️ تم الإنجاز", callback_data=f"done:{task_index}"),
            types.InlineKeyboardButton("🔁 لم يتم الإنجاز", callback_data="later"),
            types.InlineKeyboardButton("🔄 إعادة التايمر", callback_data=f"repeat:{task_index}")
        )
        bot.send_message(chat_id, "⏰ انتهى الوقت! هل أنجزت المهمة؟", reply_markup=buttons)

    thread = threading.Thread(target=timer_thread)
    thread.start()
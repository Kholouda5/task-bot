import time
import threading
from telebot import TeleBot, types

def start_timer(bot: TeleBot, chat_id: int, duration: int, task_index: int):
    def countdown():
        time.sleep(duration)

        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("✔️ تم الإنجاز", callback_data=f"done:{task_index}"),
            types.InlineKeyboardButton("🔄 إعادة التايمر", callback_data=f"repeat:{task_index}"),
            types.InlineKeyboardButton("🔁 لم يتم الإكمال", callback_data="later")
        )

        bot.send_message(chat_id, "⏰ انتهى الوقت! هل أنجزت المهمة؟", reply_markup=markup)

    threading.Thread(target=countdown).start()
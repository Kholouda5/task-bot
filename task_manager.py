import json
import os

TASKS_FILE = 'tasks.json'

# تحميل المهام
def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return {}
    with open(TASKS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# حفظ المهام
def save_tasks(tasks):
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

# إضافة مهمة
def add_task(user_id, task):
    tasks = load_tasks()
    tasks.setdefault(str(user_id), []).append(task)
    save_tasks(tasks)

# عرض المهام
def show_tasks(user_id):
    tasks = load_tasks().get(str(user_id), [])
    if not tasks:
        return "📭 لا توجد مهام حالياً."
    return "\n".join([f"{i+1}. {task}" for i, task in enumerate(tasks)])

# حذف مهمة
def delete_task(user_id, index):
    tasks = load_tasks()
    user_tasks = tasks.get(str(user_id), [])
    if 0 < index <= len(user_tasks):
        deleted = user_tasks.pop(index - 1)
        tasks[str(user_id)] = user_tasks
        save_tasks(tasks)
        return f"🗑️ تم حذف المهمة: {deleted}"
    return "❌ رقم غير صالح."

# تعديل مهمة
def update_task(user_id, index, new_task):
    tasks = load_tasks()
    user_tasks = tasks.get(str(user_id), [])
    if 0 < index <= len(user_tasks):
        old_task = user_tasks[index - 1]
        user_tasks[index - 1] = new_task
        tasks[str(user_id)] = user_tasks
        save_tasks(tasks)
        return f"✏️ تم تعديل المهمة:\nمن: {old_task}\nإلى: {new_task}"
    return "❌ رقم غير صالح."

# جلب مهمة واحدة
def get_task(user_id, index):
    tasks = load_tasks().get(str(user_id), [])
    if 0 < index <= len(tasks):
        return tasks[index - 1]
    return None
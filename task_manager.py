tasks = []

def add_task(task):
    tasks.append(task)

def show_tasks():
    if not tasks:
        return "📭 لا توجد مهام حالياً."
    result = "📋 قائمة المهام:\n"
    for i, task in enumerate(tasks, 1):
        result += f"{i}. {task}\n"
    return result

def delete_task(index):
    try:
        task = tasks.pop(index - 1)
        return f"✅ تم حذف المهمة: {task}"
    except IndexError:
        return "❌ رقم المهمة غير صحيح."

def update_task(index, new_task):
    try:
        old_task = tasks[index - 1]
        tasks[index - 1] = new_task
        return f"✏️ تم تعديل المهمة:\nمن: {old_task}\nإلى: {new_task}"
    except IndexError:
        return "❌ رقم المهمة غير صحيح."

def get_task(index):
    try:
        return tasks[index - 1]
    except IndexError:
        return None
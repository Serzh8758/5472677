import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import json
import os

TASKS_FILE = 'tasks.json'

PREDEFINED_TASKS = [
    {'title': 'Прочитать статью', 'type': 'учёба'},
    {'title': 'Сделать зарядку', 'type': 'спорт'},
    {'title': 'Завершить проект', 'type': 'работа'},
    {'title': 'Посмотреть обучающее видео', 'type': 'учёба'},
    {'title': 'Пробежка', 'type': 'спорт'},
    {'title': 'Разобрать почту', 'type': 'работа'}
]

class TaskGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.tasks = PREDEFINED_TASKS.copy()
        self.history = []
        self.selected_type = tk.StringVar(value='all')
        self.load_history()

        # --- UI ---
        self.create_widgets()

    def create_widgets(self):
        # Фильтр по типу
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(pady=5)
        tk.Label(filter_frame, text="Фильтр по типу:").pack(side='left')
        types = ['all', 'учёба', 'спорт', 'работа']
        tk.OptionMenu(filter_frame, self.selected_type, *types, command=self.update_history_list).pack(side='left')

        # Генерация задачи
        tk.Button(self.root, text="Сгенерировать задачу", command=self.generate_task).pack(pady=5)

        # Добавить новую задачу
        tk.Button(self.root, text="Добавить новую задачу", command=self.add_new_task).pack(pady=5)

        # История
        tk.Label(self.root, text="История сгенерированных задач:").pack()
        self.history_listbox = tk.Listbox(self.root, width=50)
        self.history_listbox.pack(padx=10, pady=5)

        self.update_history_list()

    def filter_tasks(self):
        task_type = self.selected_type.get()
        if task_type == 'all':
            return self.tasks
        return [t for t in self.tasks if t['type'] == task_type]

    def generate_task(self):
        filtered = self.filter_tasks()
        if not filtered:
            messagebox.showinfo("Нет задач", "Нет задач данного типа!")
            return
        task = random.choice(filtered)
        self.history.append(task)
        self.save_history()
        self.update_history_list()
        messagebox.showinfo("Ваша задача", f"{task['title']} ({task['type']})")

    def update_history_list(self, *args):
        task_type = self.selected_type.get()
        self.history_listbox.delete(0, tk.END)
        for task in self.history:
            if task_type == 'all' or task['type'] == task_type:
                self.history_listbox.insert(tk.END, f"{task['title']} ({task['type']})")

    def add_new_task(self):
        title = simpledialog.askstring("Добавить задачу", "Введите название задачи:")
        if not title or title.strip() == '':
            messagebox.showerror("Ошибка", "Название задачи не может быть пустым!")
            return
        task_type = simpledialog.askstring("Тип задачи", "Введите тип (учёба/спорт/работа):")
        if task_type not in ['учёба', 'спорт', 'работа']:
            messagebox.showerror("Ошибка", "Тип задачи должен быть: учёба, спорт или работа.")
            return
        new_task = {'title': title.strip(), 'type': task_type}
        self.tasks.append(new_task)
        messagebox.showinfo("Успех", "Задача добавлена!")

    def save_history(self):
        try:
            with open(TASKS_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка сохранения истории: {e}")

    def load_history(self):
        if os.path.exists(TASKS_FILE):
            try:
                with open(TASKS_FILE, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            except Exception:
                self.history = []

if __name__ == '__main__':
    root = tk.Tk()
    app = TaskGeneratorApp(root)
    root.mainloop()

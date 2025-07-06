import tkinter as tk
from tkinter import messagebox
from task_manager import TaskManager
from notification import NotificationManager
from datetime import datetime

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.task_manager = TaskManager()
        self.notification_manager = NotificationManager(self)
        self.setup_ui()
        self.notification_manager.check_deadlines()

    def setup_ui(self):
        # Configurare fereastră principală
        self.root.minsize(600, 400)  # Dimensiune minimă
        self.root.geometry("800x600")  # Dimensiune inițială

        # Frame pentru adăugarea task-urilor
        self.add_frame = tk.Frame(self.root)
        self.add_frame.pack(pady=10, fill=tk.X, padx=10)  # fill=tk.X pentru a ocupa lățimea

        tk.Label(self.add_frame, text="Task:").grid(row=0, column=0, padx=5, sticky="e")
        self.task_entry = tk.Entry(self.add_frame, width=30)
        self.task_entry.grid(row=0, column=1, padx=5, sticky="ew")  # sticky="ew" pentru expansiune orizontală
        self.add_frame.grid_columnconfigure(1, weight=1)  # Permite expansiunea câmpului de intrare

        tk.Label(self.add_frame, text="Deadline (YYYY-MM-DD):").grid(row=1, column=0, padx=5, sticky="e")
        self.deadline_entry = tk.Entry(self.add_frame, width=30)
        self.deadline_entry.grid(row=1, column=1, padx=5, sticky="ew")

        tk.Label(self.add_frame, text="Priority (1-5):").grid(row=2, column=0, padx=5, sticky="e")
        self.priority_entry = tk.Entry(self.add_frame, width=30)
        self.priority_entry.grid(row=2, column=1, padx=5, sticky="ew")

        tk.Button(self.add_frame, text="Add Task", command=self.add_task).grid(row=3, column=0, columnspan=2, pady=10)

        # Listbox pentru afișarea task-urilor
        self.task_listbox = tk.Listbox(self.root, width=50, height=10)
        self.task_listbox.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)  # Responsiv
        self.task_listbox.bind('<<ListboxSelect>>', self.on_select)

        # Frame pentru butoane de editare/ștergere
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10, fill=tk.X, padx=10)
        tk.Button(self.button_frame, text="Edit Task", command=self.edit_task).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="Delete Task", command=self.delete_task).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="Mark as Completed", command=self.mark_completed).pack(side=tk.LEFT, padx=5)

        self.refresh_task_list()

    def add_task(self):
        task = self.task_entry.get()
        deadline = self.deadline_entry.get()
        priority = self.priority_entry.get()

        if not task or not deadline or not priority:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        try:
            datetime.strptime(deadline, "%Y-%m-%d")
        except ValueError:
            messagebox.showwarning("Input Error", "Deadline must be in YYYY-MM-DD format.")
            return

        try:
            priority = int(priority)
            if not 1 <= priority <= 5:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Input Error", "Priority must be a number between 1 and 5.")
            return

        self.task_manager.add_task(task, deadline, priority)
        self.refresh_task_list()
        self.clear_entries()
        self.notification_manager.check_deadlines()

    def edit_task(self):
        selected = self.task_listbox.curselection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a task to edit.")
            return

        task_id = int(self.task_listbox.get(selected[0]).split(" (ID: ")[1].split(")")[0])
        task = self.task_entry.get()
        deadline = self.deadline_entry.get()
        priority = self.priority_entry.get()

        if not task or not deadline or not priority:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        try:
            priority = int(priority)
            if not 1 <= priority <= 5:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Input Error", "Priority must bea number between 1 and 5.")
            return

        self.task_manager.edit_task(task_id, task, deadline, priority)
        self.refresh_task_list()
        self.clear_entries()
        self.notification_manager.check_deadlines()

    def delete_task(self):
        selected = self.task_listbox.curselection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")
            return

        task_id = int(self.task_listbox.get(selected[0]).split(" (ID: ")[1].split(")")[0])
        self.task_manager.delete_task(task_id)
        self.refresh_task_list()
        self.notification_manager.check_deadlines()

    def mark_completed(self):
        selected = self.task_listbox.curselection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a task to mark as completed.")
            return

        task_id = int(self.task_listbox.get(selected[0]).split(" (ID: ")[1].split(")")[0])
        self.task_manager.mark_task_completed(task_id)
        self.refresh_task_list()
        self.notification_manager.check_deadlines()

    def refresh_task_list(self):
        self.task_listbox.delete(0, tk.END)
        tasks = self.task_manager.get_tasks()
        for task in tasks:
            status = "Completed" if task[4] else "Pending"
            self.task_listbox.insert(tk.END, f"{task[1]} (ID: {task[0]}) - Deadline: {task[2]} - Priority: {task[3]} - {status}")

    def clear_entries(self):
        self.task_entry.delete(0, tk.END)
        self.deadline_entry.delete(0, tk.END)
        self.priority_entry.delete(0, tk.END)

    def on_select(self, event):
        selected = self.task_listbox.curselection()
        if selected:
            task_data = self.task_listbox.get(selected[0]).split(" - ")
            task = task_data[0].split(" (ID: ")[0]
            deadline = task_data[1].split(": ")[1]
            priority = task_data[2].split(": ")[1]
            self.task_entry.delete(0, tk.END)
            self.task_entry.insert(0, task)
            self.deadline_entry.delete(0, tk.END)
            self.deadline_entry.insert(0, deadline)
            self.priority_entry.delete(0, tk.END)
            self.priority_entry.insert(0, priority)

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()

from datetime import datetime, timedelta
from tkinter import messagebox
from task_manager import TaskManager

class NotificationManager:
    def __init__(self, app):
        self.app = app
        self.task_manager = TaskManager()

    def check_deadlines(self):
        tasks = self.task_manager.get_tasks()
        current_time = datetime.now()

        for task in tasks:
            task_id, task_name, deadline, priority, completed = task
            if completed:
                continue

            try:
                deadline_time = datetime.strptime(deadline, "%Y-%m-%d")
                if current_time >= deadline_time - timedelta(days=1) and current_time <= deadline_time:
                    messagebox.showinfo(
                        "Deadline Reminder",
                        f"Task '{task_name}' is due soon!\nDeadline: {deadline}\nPriority: {priority}"
                    )
            except ValueError:
                continue

        self.app.root.after(60000, self.check_deadlines)  # Check every minute

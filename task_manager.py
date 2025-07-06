import sqlite3
from database import Database

class TaskManager:
    def __init__(self):
        self.db = Database()

    def add_task(self, task, deadline, priority):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (task, deadline, priority, completed) VALUES (?, ?, ?, ?)",
            (task, deadline, priority, False)
        )
        conn.commit()
        conn.close()

    def edit_task(self, task_id, task, deadline, priority):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tasks SET task = ?, deadline = ?, priority = ? WHERE id = ?",
            (task, deadline, priority, task_id)
        )
        conn.commit()
        conn.close()

    def delete_task(self, task_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()

    def mark_task_completed(self, task_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", (True, task_id))
        conn.commit()
        conn.close()

    def get_tasks(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks ORDER BY deadline, priority DESC")
        tasks = cursor.fetchall()
        conn.close()
        return tasks

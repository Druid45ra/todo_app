import sqlite3

class Database:
    def __init__(self):
        self.db_name = "todo_list.db"
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                deadline TEXT NOT NULL,
                priority INTEGER NOT NULL,
                completed BOOLEAN NOT NULL
            )
        """)
        conn.commit()
        conn.close()

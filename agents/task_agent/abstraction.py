from core.database import DatabaseManager
from core.base import BaseAbstraction

class TaskAbstraction(BaseAbstraction):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self._create_table()

    def _create_table(self):
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                description TEXT,
                priority INT,
                status TEXT,
                due_date DATE,
                created_at DATE
            )
        """)

    def add_task(self, title, content='', due_date=None, priority='normal'):
        self.db.execute(
            "INSERT INTO tasks (title, description, due_date, priority, status) VALUES (?, ?, ?, ?, ?)",
            (title, content, due_date, priority, 'pending')
        )

    def update_task(self, task_id, **fields):
        set_clause = ', '.join([f"{field} = '{value}'" for field, value in fields.items()])
        params = list(fields.values()) + [task_id]
        sql = (f"UPDATE tasks SET {set_clause} WHERE id = ?")
        self.db.execute(sql, (task_id,))
        self.db.commit()

    def complite_task(self, task_id):
        # print("""UPDATE tasks SET status = ? WHERE id = ?;""", ('done',task_id,))
        self.db.execute("""UPDATE tasks SET status = ? WHERE id = ?;""", ('done',task_id,))
        # self.db.commit()
        # self.db.close()

    def delete_task(self, task_id):
        self.db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))

    def get_tasks(self, filter_type='all', search=None):
        # filter_type: all, plan, done, overdue
        q = """SELECT id, title, description, due_date, priority, status, created_at FROM tasks"""
        conds = []
        params = []
        if filter_type == 'plan':
            conds.append("status = 'pending'")
        elif filter_type == 'done':
            conds.append("status = 'done'")
        elif filter_type == 'overdue':
            conds.append("status = 'pending' AND due_date IS NOT NULL AND due_date < datetime('now')")
        if search:
            conds.append("(title LIKE ? OR description LIKE ?)")
            params.extend((f"%{search}%", f"%{search}%"))
        if conds:
            q += " WHERE " + " AND ".join(conds)
        q += " ORDER BY due_date IS NULL, due_date ASC, id DESC"
        return self.db.fetchall(q, params)

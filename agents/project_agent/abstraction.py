
from core.database import DatabaseManager
from core.base import BaseAbstraction
from datetime import datetime

class ProjectAbstraction(BaseAbstraction):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self._create_table()

    def _create_table(self):
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS project (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                description TEXT,
                priority INT,
                status TEXT,
                due_date DATE,
                created_at DATE
            )
        """)

    def add_project(self, title, content='', due_date=None, priority='normal'):
        self.db.execute(
            "INSERT INTO project (title, description, due_date, priority) VALUES (?, ?, ?, ?)",
            (title, content, due_date, priority)
        )

    def update_project(self, project_id, **fields):
        set_clause = ', '.join([f"{k} = ?" for k in fields.keys()])
        params = list(fields.values()) + [project_id]
        sql = (f"UPDATE project SET {set_clause} WHERE id = ?")
        self.db.execute(sql, params)

    def delete_project(self, project_id):
        self.db.execute("DELETE FROM project WHERE id = ?", (project_id,))

    def get_projects(self, filter_type='all', search=None):
        # filter_type: all, plan, done, overdue
        q = """SELECT id, title, description, due_date, priority, status, created_at FROM project"""
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

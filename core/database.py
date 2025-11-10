import sqlite3
from pathlib import Path

class DatabaseManager:
    _instance = None
    def __new__(cls, db_path="/base_app.db"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init(db_path)
        return cls._instance
    def _init(self, db_path):
        db_dir = Path("db")
        self.db_path = 'db/base_app.db'
        print(self.db_path)
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        self._create_meta_table()
    def _create_meta_table(self):
        cur = self.connection.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS agents_meta (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_name TEXT NOT NULL,
                version TEXT,
                last_sync TEXT,
                UNIQUE(agent_name)
            )
        """)
        self.connection.commit()
    def execute(self, query, params=None):
        debug = False
        cur = self.connection.cursor()
        cur.execute(query, params or [])

        if debug:
            if params is not None:
                debug_sql = query.replace("?", "%s") % tuple(repr(p) for p in params)
                print("QUERY:", debug_sql)

        self.connection.commit()
        return cur
    def fetchall(self, query, params=None):
        cur = self.connection.cursor()
        cur.execute(query, params or [])
        return cur.fetchall()
    def fetchone(self, query, params=None):
        cur = self.connection.cursor()
        cur.execute(query, params or [])
        return cur.fetchone()
    def register_agent(self, name, version="1.0"):
        self.execute("""
            INSERT OR IGNORE INTO agents_meta (agent_name, version)
            VALUES (?, ?)
        """, (name, version))

    def commit(self):  # Добавляем метод
        self.connection.commit()

    def close(self):
        try:
            self.connection.close()
        except Exception:
            pass

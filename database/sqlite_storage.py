# database/sqlite_storage.py
import sqlite3
from typing import Optional
from user.user import User  # ✅ Абсолютный импорт

class SQLiteUserStorage:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    first_name TEXT,
                    level TEXT DEFAULT 'beginner',
                    trainings_completed INTEGER DEFAULT 0
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS achievements (
                    user_id INTEGER,
                    achievement_id TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """)
            conn.commit()

    def save_user(self, user):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO users (id, first_name, level, trainings_completed)
                VALUES (?, ?, ?, ?)
            """, (user.id, user.first_name, user.level, user.trainings_completed))
            conn.commit()

    def load_user(self, user_id: int):
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
            if row:
                return User(id=row[0], first_name=row[1], level=row[2], trainings_completed=row[3])
            return None

    def add_achievement(self, user_id: int, achievement_id: str):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT INTO achievements (user_id, achievement_id) VALUES (?, ?)",
                         (user_id, achievement_id))
            conn.commit()

    def get_achievements(self, user_id: int):
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute("SELECT achievement_id FROM achievements WHERE user_id = ?", (user_id,)).fetchall()
            return [r[0] for r in rows]
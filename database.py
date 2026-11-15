import sqlite3
from pathlib import Path

DB_PATH = Path("data/index.db")

def create_database():
    """
    Creates the SQLite database and the 'files' table if they do not exist.
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                path TEXT NOT NULL UNIQUE,
                extension TEXT NOT NULL,
                size INTEGER NOT NULL
            )
        ''')

        columns = [
            row[1]
            for row in conn.execute("PRAGMA table_info(files)")     #Extracting all column names into a list or set. This is often used to verify if a column exists before running an ALTER TABLE migration.
        ]
        
        if "content" not in columns:
            conn.execute("ALTER TABLE files ADD COLUMN content TEXT")

def save_file(name, path, extension, size, content):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO files (name, path, extension, size, content)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(path) DO UPDATE SET
                name = excluded.name,
                extension = excluded.extension,
                size = excluded.size,
                content = excluded.content
        """, (name, path, extension, size, content))


if __name__ == "__main__":
    create_database()
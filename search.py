import sqlite3
from database import DB_PATH


def search_files(keyword):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("""
            SELECT name, path, extension, size
            FROM files
            WHERE name LIKE ? OR path LIKE ? OR content LIKE ?
        """, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))

        return cursor.fetchall()

if __name__ == "__main__":
    results = search_files("veterinary appointment system")

    for file in results:
        print(file)
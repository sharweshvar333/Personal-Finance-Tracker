import sqlite3

conn = sqlite3.connect("finance.db")
cursor = conn.cursor()

try:
    cursor.execute("""
        ALTER TABLE users
        ADD COLUMN is_admin BOOLEAN NOT NULL DEFAULT 0
    """)
    conn.commit()
    print("✅ is_admin column added successfully.")
except sqlite3.OperationalError as e:
    print("⚠️", e)

conn.close()

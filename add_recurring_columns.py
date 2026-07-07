import sqlite3

conn = sqlite3.connect("instance/finance.db")
cursor = conn.cursor()

columns = [
    ("is_recurring", "BOOLEAN NOT NULL DEFAULT 0"),
    ("recurrence", "TEXT"),
    ("start_date", "DATE"),
    ("end_date", "DATE"),
    ("last_processed", "DATE"),
]

for column_name, column_type in columns:
    try:
        cursor.execute(
            f"ALTER TABLE transactions ADD COLUMN {column_name} {column_type}"
        )
        print(f"✅ Added column: {column_name}")
    except sqlite3.OperationalError as e:
        print(f"⚠️ {column_name}: {e}")

conn.commit()
conn.close()

print("\nFinished.")

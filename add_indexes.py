import sqlite3

conn = sqlite3.connect("instance/finance.db")
cursor = conn.cursor()

indexes = [
    (
        "idx_transactions_category",
        "CREATE INDEX idx_transactions_category ON transactions(category)"
    ),
    (
        "idx_transactions_type",
        "CREATE INDEX idx_transactions_type ON transactions(transaction_type)"
    ),
    (
        "idx_transactions_date",
        "CREATE INDEX idx_transactions_date ON transactions(date)"
    ),
    (
        "idx_users_username",
        "CREATE INDEX idx_users_username ON users(username)"
    ),
]

for name, sql in indexes:
    try:
        cursor.execute(sql)
        print(f"✅ Created {name}")
    except sqlite3.OperationalError as e:
        print(f"⚠️ {name}: {e}")

conn.commit()
conn.close()

print("\nFinished creating indexes.")

import sqlite3

conn = sqlite3.connect("instance/finance.db")
cursor = conn.cursor()

queries = [
    (
        "Filter by category",
        "SELECT * FROM transactions WHERE category = 'Food'"
    ),
    (
        "Filter by transaction type",
        "SELECT * FROM transactions WHERE transaction_type = 'expense'"
    ),
    (
        "Filter by date",
        "SELECT * FROM transactions WHERE date >= '2026-07-01'"
    ),
    (
        "Lookup user",
        "SELECT * FROM users WHERE username = 'sharwesh'"
    )
]

print("\n===== QUERY PROFILING =====\n")

for title, query in queries:
    print(f"{title}")
    print("-" * 50)

    cursor.execute(f"EXPLAIN QUERY PLAN {query}")

    for row in cursor.fetchall():
        print(row)

    print()

conn.close()

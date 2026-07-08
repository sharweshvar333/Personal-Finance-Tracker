import sqlite3
import timeit

conn = sqlite3.connect("instance/finance.db")
cursor = conn.cursor()

query = """
SELECT *
FROM transactions
WHERE category='Food'
"""

def run_query():
    cursor.execute(query)
    cursor.fetchall()

execution_time = timeit.timeit(run_query, number=1000)

print("\n===== QUERY PERFORMANCE =====")
print(f"Executed 1000 times")
print(f"Total Time : {execution_time:.6f} seconds")
print(f"Average    : {execution_time/1000:.8f} seconds")

conn.close()

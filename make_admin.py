import sqlite3

# Connect to the SAME database used by Flask
conn = sqlite3.connect("instance/finance.db")
cursor = conn.cursor()

username = input("Enter username to make admin: ")

cursor.execute(
    "UPDATE users SET is_admin = 1 WHERE username = ?",
    (username,)
)

conn.commit()

if cursor.rowcount > 0:
    print(f"✅ {username} is now an admin.")
else:
    print("❌ User not found.")

conn.close()

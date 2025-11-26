# SQL - Structured Query Language - Язык структурированных запросов
# CRUD:
# CREATE - INSERT - Создать запись
# READ - SELECT - получить запись
# UPDATE - UPDATE - изменить запись
# DELETE - DELETE - удалить запись

# import sqlite3
#
# def main():
#     conn = sqlite3.connect('ourdb.sqlite')
#     cur = conn.cursor()
#
#     cur.execute("""
#     CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         username TEXT NOT NULL,
#         email TEXT
#     )
#     """)
#
#     cur.execute("INSERT INTO users (username, email) VALUES (?, ?)",
#                 ("Emily", "dagisova@icloud.com"))
#     conn.commit()
#
#     cur.execute("SELECT id, username, email FROM users")
#     rows = cur.fetchall()
#     for r in rows:
#         print(r)
#
#     cur.close()
#     conn.close()
#
# if __name__ == "__main__":
#     main()

import sqlite3

conn = sqlite3.connect("users.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT
)
""")

cur.execute("INSERT INTO users (username, email) VALUES (?, ?)",
            ("Lionel Messi", "lm10@icloud.com"))
cur.execute("INSERT INTO users (username, email) VALUES (?, ?)",
            ("Cristiano Ronaldo", "cr7@icloud.com"))

cur.execute("SELECT id, username, email FROM users")
for row in cur.fetchall():
    print(row)

cur.execute("UPDATE users SET email=? WHERE username=?",
            ("leomessi10@gmail.com", "Lionel Messi"))

cur.execute("DELETE FROM users WHERE username=?", ("Cristiano Ronaldo",))

conn.commit()
conn.close()
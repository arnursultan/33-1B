from core.db import get_conn, put_conn
import hashlib


class UsersRepo:
    @staticmethod
    def auth(u, p):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, username, password_hash, role FROM users WHERE username=%s",
            (u,)
        )
        row = cur.fetchone()
        put_conn(conn)

        if not row:
            return None

        if row[2] != hashlib.sha256(p.encode()).hexdigest():
            return None

        return type("User", (), {
            "id": row[0],
            "username": row[1],
            "role": row[3]
        })()


class StudentsRepo:
    @staticmethod
    def all():
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT id, name, age, email FROM students ORDER BY id")
        rows = cur.fetchall()
        put_conn(conn)
        return rows

    @staticmethod
    def add(n, a, e):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO students(name, age, email) VALUES (%s, %s, %s)",
            (n, a, e)
        )
        conn.commit()
        put_conn(conn)

    @staticmethod
    def update(i, n, a, e):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "UPDATE students SET name=%s, age=%s, email=%s WHERE id=%s",
            (n, a, e, i)
        )
        conn.commit()
        put_conn(conn)

    @staticmethod
    def delete(i):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM students WHERE id=%s", (i,))
        conn.commit()
        put_conn(conn)


class TeachersRepo:
    @staticmethod
    def all():
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, full_name, subject, email, phone, experience, status
            FROM teachers ORDER BY id
        """)
        rows = cur.fetchall()
        put_conn(conn)
        return rows

    @staticmethod
    def add(fn, subj, email, phone, exp, status):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO teachers(full_name, subject, email, phone, experience, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (fn, subj, email, phone, exp, status))
        conn.commit()
        put_conn(conn)

    @staticmethod
    def update(i, fn, subj, email, phone, exp, status):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            UPDATE teachers SET full_name=%s, subject=%s, email=%s, phone=%s,
            experience=%s, status=%s WHERE id=%s
        """, (fn, subj, email, phone, exp, status, i))
        conn.commit()
        put_conn(conn)

    @staticmethod
    def delete(i):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM teachers WHERE id=%s", (i,))
        conn.commit()
        put_conn(conn)

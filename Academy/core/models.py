from core.db import get_conn, put_conn
import hashlib


def init_all_tables():
    create_students()
    create_teachers()
    create_users()


def create_students():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            age INT,
            email VARCHAR(200)
        );
    """)
    conn.commit()
    put_conn(conn)


def create_teachers():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS teachers (
            id SERIAL PRIMARY KEY,
            full_name VARCHAR(150) NOT NULL,
            subject VARCHAR(100) NOT NULL,
            email VARCHAR(150),
            phone VARCHAR(30),
            experience INT DEFAULT 0,
            status VARCHAR(20) DEFAULT 'active'
        );
    """)
    conn.commit()
    put_conn(conn)



def create_users():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE,
            password_hash TEXT,
            role VARCHAR(20)
        );
    """)

    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        cur.execute(
            "INSERT INTO users(username, password_hash, role) VALUES (%s, %s, %s)",
            ("admin", hashlib.sha256(b"admin").hexdigest(), "admin")
        )

    conn.commit()
    put_conn(conn)

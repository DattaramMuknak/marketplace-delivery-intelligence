import os
import re
import bcrypt
import mysql.connector
import streamlit as st
from dotenv import load_dotenv


def _db_config():
    # Streamlit Cloud: read credentials from App Settings > Secrets
    try:
        if "mysql" in st.secrets:
            config = st.secrets["mysql"]
            return {
                "host": config["host"],
                "port": int(config.get("port", 3306)),
                "user": config["username"],
                "password": config["password"],
                "database": config["database"],
                "connection_timeout": 10,
                "ssl_disabled": False,
            }
    except Exception:
        # Fall back to local .env when Cloud secrets aren't available
        pass

    # Local development: read credentials from .env
    load_dotenv()

    return {
        "host": os.getenv("MYSQL_HOST", ""),
        "port": int(os.getenv("MYSQL_PORT", "3306")),
        "user": os.getenv("MYSQL_USER", ""),
        "password": os.getenv("MYSQL_PASSWORD", ""),
        "database": os.getenv("MYSQL_DATABASE", ""),
        "connection_timeout": 10,
        "ssl_disabled": False,
    }


def get_connection():
    cfg = _db_config()

    if not cfg["host"] or not cfg["user"] or not cfg["database"] or not cfg["password"]:
        raise RuntimeError(
            "MySQL configuration is missing. Configure [mysql] in "
            "Streamlit Cloud Secrets or fill in your local .env file."
        )

    return mysql.connector.connect(**cfg)


def init_db():
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS app_users (
                id BIGINT AUTO_INCREMENT PRIMARY KEY,
                full_name VARCHAR(120) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        cur.close()
    finally:
        conn.close()


def register_user(name, email, password):
    name = (name or "").strip()
    email = (email or "").strip().lower()

    if len(name) < 2:
        return False, "Enter your full name."

    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        return False, "Enter a valid email address."

    if len(password or "") < 8:
        return False, "Password must contain at least 8 characters."

    hashed = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO app_users
               (full_name, email, password_hash)
               VALUES (%s, %s, %s)""",
            (name, email, hashed)
        )
        conn.commit()
        cur.close()
        return True, "Account created successfully."

    except mysql.connector.IntegrityError:
        return False, "An account with this email already exists."

    finally:
        conn.close()


def login_user(email, password):
    email = (email or "").strip().lower()

    conn = get_connection()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            """SELECT id, full_name, email, password_hash
               FROM app_users WHERE email = %s""",
            (email,)
        )
        row = cur.fetchone()
        cur.close()

        if not row or not bcrypt.checkpw(
            (password or "").encode("utf-8"),
            row["password_hash"].encode("utf-8")
        ):
            return False, "Invalid email or password.", None

        return True, "Login successful.", {
            "id": row["id"],
            "name": row["full_name"],
            "email": row["email"],
        }

    finally:
        conn.close()
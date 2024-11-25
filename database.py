import sqlite3


DATABASE_PATH = 'bot_database.db'

def get_db_connection():

    return sqlite3.connect(DATABASE_PATH, check_same_thread=False)


def check_user(user_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        return cursor.fetchone() is not None

def register(user_id, user_name, phone_number):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (user_id, user_name, phone_number) VALUES (?, ?, ?)",
                       (user_id, user_name, phone_number))
        conn.commit()


def get_pr_buttons():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM products")
        return [row[0] for row in cursor.fetchall()]

def get_product_info(product_name):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, description, image, price FROM products WHERE name = ?", (product_name,))
        return cursor.fetchone()

def get_exact_price(product_name):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT price FROM products WHERE name = ?", (product_name,))
        price = cursor.fetchone()
        return price[0] if price else 0.0


def add_to_cart(user_id, pr_name, pr_count):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cart (user_id, pr_name, pr_count) VALUES (?, ?, ?)",
                       (user_id, pr_name, pr_count))
        conn.commit()

def show_cart(user_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cart WHERE user_id = ?", (user_id,))
        return cursor.fetchall()

def clear_cart(user_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))
        conn.commit()

def make_order(user_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))
        conn.commit()

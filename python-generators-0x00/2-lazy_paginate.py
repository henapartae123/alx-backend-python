import mysql.connector
from mysql.connector import Error

def paginate_users(page_size, offset):
    """
    Fetch one page of users from the database starting at the given offset.
    Returns a list of users limited by page_size.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
        cursor.execute(query, (page_size, offset))
        rows = cursor.fetchall()
        return rows
    except Error as e:
        print(f"❌ Database error: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def lazy_paginate(page_size):
    """
    Generator that lazily fetches pages of users.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
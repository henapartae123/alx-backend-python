import mysql.connector
from mysql.connector import Error

def stream_users_in_batches(batch_size):
    """
    Generator that fetches rows from user_data table in batches.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch

    except Error as e:
        print(f"❌ Database error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def batch_processing(batch_size):
    """
    Processes batches of users and filters those over age 25.
    """
    for batch in stream_users_in_batches(batch_size):
        
        filtered_users = [user for user in batch if float(user["age"]) > 25]
        return filtered_users
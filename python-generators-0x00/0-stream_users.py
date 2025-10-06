import mysql.connector
from mysql.connector import Error

def stream_users():
    """
    Generator function that fetches and yields rows one by one
    from the user_data table in the ALX_prodev database.
    """
    try:
        # Connect to ALX_prodev database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="ALX_prodev"
        )

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        # ✅ Single loop - yield each row one by one
        for row in cursor:
            yield row

    except Error as e:
        print(f"❌ Database error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Example usage (only runs when executed directly)
if __name__ == "__main__":
    for user in stream_users():
        print(user)

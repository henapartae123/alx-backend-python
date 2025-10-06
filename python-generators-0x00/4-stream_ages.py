import mysql.connector
from mysql.connector import Error

def stream_user_ages():
    """
    Generator that yields user ages one by one from the database.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="ALX_prodev"
        )
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")

        for (age,) in cursor:
            yield float(age)

    except Error as e:
        print(f"❌ Database error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def calculate_average_age():
    """
    Uses the stream_user_ages generator to compute the average age
    """
    total = 0
    count = 0

    for age in stream_user_ages():
        total += age
        count += 1

    average = total / count if count > 0 else 0
    print(f"Average age of users: {average:.2f}")
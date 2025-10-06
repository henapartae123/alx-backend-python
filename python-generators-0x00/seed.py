#!/usr/bin/env python3
"""
seed.py

Provides:
- connect_db()
- create_database(connection)
- connect_to_prodev()
- create_table(connection)
- insert_data(connection, data)
- stream_user_rows(connection)  -> generator that yields rows one by one
"""

import os
import csv
import uuid

import mysql.connector
from mysql.connector import Error



def connect_db() -> Optional[mysql.connector.connection_cext.CMySQLConnection]:
    """Connect to the MySQL server"""

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password"
        )
        if connection.is_connected():
            print("✅ Connected to MySQL server")
            
        return connection
    except Error as e:
        print(f"Error connecting to MySQL server: {e}")
        return None


def create_database(connection):
    """Create database ALX_prodev if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        print("✅ Database 'ALX_prodev' is ready.")
    except Error as e:
        print(f"Error creating database: {e}")

def connect_to_prodev():
    """connects to the ALX_prodev database."""

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="ALX_prodev"
        )
        if connection.is_connected():
            print("✅ Connected to database 'ALX_prodev'")
        return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None


def create_table(connection: mysql.connector.connection_cext.CMySQLConnection) -> None:
    """Create user_data table if it does not exist. """

    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL(3,0) NOT NULL,
                INDEX (user_id)
            );
        """)
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}")


def insert_data(connection, data):
    """Inserts data into the user_data table if email does not already exist."""

    try:
        cursor = connection.cursor()

        for row in data:
            name, email, age = row
            cursor.execute("SELECT * FROM user_data WHERE email = %s", (email,))
            existing = cursor.fetchone()
            if not existing:
                user_id = str(uuid.uuid4())
                cursor.execute("""
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, name, email, age))
        connection.commit()
        print("✅ Data inserted successfully.")
    except Error as e:
        print(f"Error inserting data: {e}")


# ---------- MAIN SCRIPT ----------

if __name__ == "__main__":
    # Step 1: Connect to MySQL server
    conn = connect_db()
    if not conn:
        exit()

    # Step 2: Create database
    create_database(conn)
    conn.close()

    # Step 3: Connect to ALX_prodev database
    db_conn = connect_to_prodev()
    if not db_conn:
        exit()

    # Step 4: Create table
    create_table(db_conn)

    # Step 5: Read from CSV file
    data = []
    try:
        with open("user_data.csv", "r", encoding="utf-8") as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header
            for row in csv_reader:
                if len(row) >= 3:
                    data.append((row[0].strip(), row[1].strip(), row[2].strip()))
        print(f"📄 Loaded {len(data)} records from CSV.")
    except FileNotFoundError:
        print("❌ user_data.csv not found.")
        exit()

    # Step 6: Insert data into database
    insert_data(db_conn, data)

    db_conn.close()
    print("✅ All done!")
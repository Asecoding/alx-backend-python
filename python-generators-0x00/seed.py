#!/usr/bin/python3
"""
This module provides functions to set up and populate the ALX_prodev database.
"""

import mysql.connector
import csv
import uuid
import os
from mysql.connector import errorcode

# 1. Connect to MySQL server (no DB selected yet)
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password"
    )

# 2. Create database if it doesn't exist
def create_database(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("✅ Database 'ALX_prodev' ensured.")
    finally:
        cursor.close()

# 3. Connect to ALX_prodev database
def connect_to_prodev():
    return mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="ALX_prodev"
    )

# 4. Create user_data table with UUID primary key
def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            age DECIMAL(3,0) NOT NULL,
            INDEX (user_id)
        )
    """)
    connection.commit()
    print("✅ Table 'user_data' ensured.")
    cursor.close()

# 5. Insert data from CSV if not already present
def insert_data(connection, data):
    cursor = connection.cursor()
    for row in data:
        user_id = str(uuid.uuid4())
        name, email, age = row
        cursor.execute("""
            SELECT COUNT(*) FROM user_data WHERE email = %s
        """, (email,))
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
            """, (user_id, name, email, age))
    connection.commit()
    print("✅ Data inserted.")
    cursor.close()

# 6. Load CSV data
def load_csv_data(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        return [row for row in reader]

# 7. Main execution
if __name__ == "__main__":
    try:
        conn = connect_db()
        create_database(conn)
        conn.close()

        conn = connect_to_prodev()
        create_table(conn)
        data = load_csv_data("user_data.csv")
        insert_data(conn, data)
        conn.close()
    except mysql.connector.Error as err:
        print(f"❌ MySQL Error: {err}")

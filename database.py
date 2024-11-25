import sqlite3
import pandas as pd

def create_connection(db_name='meal_service.db'):
    """Create or connect to a database"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    return conn, cursor

def create_tables(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY,
        subscription_type TEXT,
        start_date TEXT,
        end_date TEXT,
        status TEXT,
        dietary_preference TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        order_date TEXT,
        meal_category TEXT,
        dietary_preference TEXT,
        order_value REAL,
        FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
    )
    ''')

def insert_customer_data(cursor, customer_data):
    """Insert customer data into the database"""
    cursor.executemany('''
    INSERT INTO customers (customer_id, subscription_type, start_date, end_date, status, dietary_preference)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', customer_data)

def insert_order_data(cursor, order_data):
    """Insert order data into the database"""
    cursor.executemany('''
    INSERT INTO orders (order_id, customer_id, order_date, meal_category, dietary_preference, order_value)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', order_data)

def fetch_data_from_db():
    conn, cursor = create_connection()
    
    cursor.execute("SELECT * FROM customers")
    customers_data = cursor.fetchall()

    cursor.execute("SELECT * FROM orders")
    orders_data = cursor.fetchall()

    # Convert the data to DataFrames for easier manipulation
    customers_df = pd.DataFrame(customers_data, columns=["customer_id", "subscription_type", "start_date", "end_date", "status", "dietary_preference"])
    orders_df = pd.DataFrame(orders_data, columns=["order_id", "customer_id", "order_date", "meal_category", "dietary_preference", "order_value"])

    conn.close()

    return customers_df, orders_df

def clear_all_data(cursor):
    # Clear data from 'customers' and 'orders' tables
    cursor.execute("DELETE FROM customers")
    cursor.execute("DELETE FROM orders")
    cursor.connection.commit()


def commit_and_close(conn):
    """Commit changes and close the database connection"""
    conn.commit()
    conn.close()



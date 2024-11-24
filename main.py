import pandas as pd
from database import create_connection, create_tables, insert_customer_data, insert_order_data, commit_and_close
from data_generation import generate_subscription_data, generate_order_data


conn, cursor = create_connection()

# Create tables if they don't exist
create_tables(cursor)

# Generate subscription data for 1000 customers
num_customers = 1000
subscription_data = generate_subscription_data(num_customers)

# Insert subscription data into the database
insert_customer_data(cursor, subscription_data)

# Convert subscription data to DataFrame for generating orders
subscription_df = pd.DataFrame(subscription_data, columns=["customer_id", "subscription_type", "start_date", "end_date", "status", "dietary_preference"])

# Generate order data
order_data = generate_order_data(subscription_df)

# Insert order data into the database
insert_order_data(cursor, order_data)


commit_and_close(conn)


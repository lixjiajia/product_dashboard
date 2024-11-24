import pandas as pd
import random
from faker import Faker
from datetime import timedelta

fake = Faker()

# List of dietary preferences
dietary_preferences = ["Vegetarian", "Vegan", "Keto", "Gluten-Free", "None"]

# Function to generate subscription data
def generate_subscription_data(num_customers):
    data = []
    for customer_id in range(1, num_customers + 1):
        subscription_type = random.choice(["Weekly", "Monthly"])
        start_date = fake.date_between(start_date='-1y', end_date='today')
        
        # Calculate end_date based on subscription type
        if subscription_type == "Weekly":
            end_date = start_date + timedelta(weeks=1)
        else:  # Monthly
            end_date = start_date + timedelta(days=30)
        
        # Simulate churn based on subscription type
        churn_probability = 0.1 if subscription_type == "Monthly" else 0.3  # Monthly subscriptions have lower churn probability
        
        churned = random.random() < churn_probability  # If random value is less than churn probability, customer churns
        status = "Churned" if churned else "Renewed"
        
        # Assign a random dietary preference
        dietary_preference = random.choice(dietary_preferences)
        
        # Append to dataset
        data.append((customer_id, subscription_type, start_date, end_date, status, dietary_preference))
    
    return data


# Generate orders for customers
def generate_order_data(subscription_data, max_orders_per_customer=10):
    orders = []
    order_id = 1  # Initialize order ID counter
    
    subscription_data['dietary_preference'] = subscription_data['dietary_preference'].fillna('None').astype(str)
    meal_categories = ["Breakfast", "Lunch", "Dinner"]
    category_weights = [0.2, 0.4, 0.55]

    for _, row in subscription_data.iterrows():
        customer_id = row['customer_id']
        subscription_type = row['subscription_type']
        dietary_preference = row['dietary_preference']
        start_date = row['start_date']
        end_date = row['end_date']
        
        # Generate a random number of orders for this customer
        num_orders = random.randint(1, max_orders_per_customer)
        for _ in range(num_orders):
            # Randomize order date within subscription period
            order_date = fake.date_between(start_date=start_date, end_date=end_date)
            
            meal_category = random.choices(meal_categories, weights=category_weights, k=1)[0]
            order_value = round(random.uniform(10, 50), 2)  # Order value between $10 and $50
            

            orders.append((order_id,customer_id,order_date,meal_category, dietary_preference, order_value))
            order_id += 1  # Increment order ID
    
    return orders


import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from database import fetch_data_from_db
import datetime

app = dash.Dash(__name__)

# Fetch data from the database
customers_data, orders_data = fetch_data_from_db()

# Preprocessing data for the dashboard
customers_data['start_date'] = pd.to_datetime(customers_data['start_date'])
customers_data['end_date'] = pd.to_datetime(customers_data['end_date'])
orders_data['order_date'] = pd.to_datetime(orders_data['order_date'])

# Calculate metrics
aov = orders_data['order_value'].mean()
avg_orders_per_customer = orders_data.groupby('customer_id').size().mean()
customers_data['customer_lifetime'] = (customers_data['end_date'] - customers_data['start_date']).dt.days
average_lifetime = customers_data['customer_lifetime'].mean()
cltv = aov * avg_orders_per_customer * (average_lifetime / 30)
retention_rate = 1 - (len(customers_data[customers_data['status'] == 'Churned']) / len(customers_data))
churn_by_type = customers_data[customers_data['status'] == 'Churned'].groupby('subscription_type').size().reset_index(name='churn_count')
meal_category_counts = orders_data.groupby('meal_category').size().reset_index(name='order_count')
orders_data['month'] = orders_data['order_date'].dt.to_period('M')
revenue_over_time = orders_data.groupby('month')['order_value'].sum().reset_index()
revenue_over_time['month'] = revenue_over_time['month'].dt.to_timestamp()
most_popular_dietary = orders_data['dietary_preference'].mode()[0]

# Prepare visualizations
retention_fig = px.pie(values=[retention_rate, 1 - retention_rate], names=["Retained", "Churned"], title="Retention Rate")
monthly_orders = orders_data.groupby('month').size().reset_index(name='order_count')
monthly_orders['month'] = monthly_orders['month'].dt.to_timestamp()
orders_trend_fig = px.line(monthly_orders, x='month', y='order_count', title='Monthly Orders Trend', labels={'month': 'Month', 'order_count': 'Order Count'})
meal_category_fig = px.bar(
    meal_category_counts,
    x='meal_category',
    y='order_count',
    title='Popular Meal Categories',
    labels={'meal_category': 'Meal Category', 'order_count': 'Orders'}
)
orders_with_subscription = pd.merge(
    orders_data,
    customers_data[['customer_id', 'subscription_type']],  # Select relevant columns
    on='customer_id',
    how='left'
)

revenue_by_subscription = orders_with_subscription.groupby(['month', 'subscription_type'])['order_value'].sum().reset_index()
revenue_by_subscription['month'] = revenue_by_subscription['month'].dt.to_timestamp()

revenue_subscription_fig = px.line(
    revenue_by_subscription,
    x='month',
    y='order_value',
    color='subscription_type',
    title='Monthly Revenue by Subscription Type',
    labels={'order_value': 'Revenue ($)', 'month': 'Month', 'subscription_type': 'Subscription Type'}
)


app.layout = html.Div([
    html.H1('FreshMeals Metrics Dashboard', style={'text-align': 'center', 'margin-bottom': '30px'}),
    
 # Key Metrics Section
    html.Div([
        html.H3('Key Metrics', style={'text-align': 'center'}),

        html.Div([
            # CLTV Metric
            html.Div([
                html.H4('Average Customer Lifetime Value (CLTV)'),
                html.P(f"${cltv:.2f}", style={'font-size': '24px'})
            ], className='metric-box'),

            # Retention Rate 
            html.Div([
                html.H4('Retention Rate'),
                html.P(f"{retention_rate:.2%}", style={'font-size': '24px'})
            ], className='metric-box'),

            # Average Order Value 
            html.Div([
                html.H4('Average Order Value (AOV)'),
                html.P(f"${aov:.2f}", style={'font-size': '24px'})
            ], className='metric-box'),

            # Most Popular Dietary Preference 
            html.Div([
                html.H4('Most Popular Dietary Preference'),
                html.P(f"{most_popular_dietary}", style={'font-size': '24px'})
            ], className='metric-box'),

        ], className='metrics-container'),
    ], style={'margin-bottom': '30px'}),
    
    # Visualization Section  
  html.Div([
    # Retention Rate Pie Chart
    html.Div([
        dcc.Graph(id='retention-rate-graph', figure=retention_fig)
    ], style={'padding': '20px', 'flex': '1', 'min-width': '300px'}), 

    # Popular Meal Categories Bar Chart
    html.Div([
        dcc.Graph(id='meal-category-graph', figure=meal_category_fig)
    ], style={'padding': '20px', 'flex': '1', 'min-width': '300px'}),  
], style={'display': 'flex', 'justify-content': 'space-between', 'flex-wrap': 'wrap', 'gap': '20px'}),  
    # Monthly Orders Trend
    html.Div([
        dcc.Graph(id='orders-trend-graph', figure=orders_trend_fig)
    ], style={'padding': '20px', 'width': '100%'}),  
    #Monthly Revenue By Subscription Type
    dcc.Graph(id='revenue-subscription-graph', figure=revenue_subscription_fig, style={'width': '100%'})
    ])


if __name__ == '__main__':
    app.run_server(debug=True)



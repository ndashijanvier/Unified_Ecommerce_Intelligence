from pymongo import MongoClient
import pandas as pd

# 1. Connect to MongoDB
client = MongoClient("mongodb://ecommerce_mongodb:27017/")
db = client["Unified_Ecommerce_DB"]

print("Extracting datasets from MongoDB collections for cross-engine integration...")
# Fetch users without strict field exclusions to capture both name styles
users_cursor = db.users.find({}, {"geo_data.country": 1, "user_id": 1, "name": 1, "first_name": 1, "last_name": 1})
tx_cursor = db.transactions.find({}, {"transaction_id": 1, "user_id": 1, "total": 1, "status": 1})

df_users = pd.DataFrame(list(users_cursor))
df_tx = pd.DataFrame(list(tx_cursor))

# Clean country mapping safely
if 'geo_data' in df_users.columns:
    df_users['country'] = df_users['geo_data'].apply(lambda x: x.get('country') if isinstance(x, dict) else "Unknown")
else:
    df_users['country'] = "Unknown"

# Construct a safe display name field dynamically
if 'name' in df_users.columns:
    df_users['display_name'] = df_users['name']
elif 'first_name' in df_users.columns and 'last_name' in df_users.columns:
    df_users['display_name'] = df_users['first_name'] + " " + df_users['last_name']
else:
    df_users['display_name'] = df_users['user_id']

# Filter fields for joining
df_users = df_users[['user_id', 'display_name', 'country']]
if '_id' in df_tx.columns:
    df_tx = df_tx.drop(columns=['_id'])

# Filter completed sales metrics
completed_tx = df_tx[df_tx['status'] == 'completed']

print("Calculating integrated Customer Lifetime Value (CLV) index...")
user_value = completed_tx.groupby('user_id').agg(
    total_spent=('total', 'sum'),
    order_count=('transaction_id', 'count')
).reset_index()

# Join user demographics with purchase history calculations
integrated_report = pd.merge(df_users, user_value, on='user_id', how='inner')
top_vips = integrated_report.sort_values(by='total_spent', ascending=False).head(5)

print("\n========================================================")
print("     UNIFIED INTEGRATED PLATFORM METRICS REPORT")
print("========================================================")
for idx, row in top_vips.iterrows():
    print(f"VIP User: {row['display_name']} ({row['user_id']})")
    print(f"  -> Country: {row['country']}")
    print(f"  -> Order Frequency: {row['order_count']} orders placed")
    print(f"  -> Calculated CLV Metric: ${row['total_spent']:.2f}")
    print("-" * 50)

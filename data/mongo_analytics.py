from pymongo import MongoClient
import json

client = MongoClient("mongodb://ecommerce_mongodb:27017/")
db = client["Unified_Ecommerce_DB"]

# --- Pipeline 1: Revenue Analytics by Product Category ---
print("\n--- Pipeline 1: Total Revenue by Product Category ---")
revenue_pipeline = [
    {"$unwind": "$items"},
    {
        "$lookup": {
            "from": "products",
            "localField": "items.product_id",
            "foreignField": "product_id",
            "as": "product_info"
        }
    },
    {"$unwind": "$product_info"},
    {
        "$group": {
            "_id": "$product_info.category_id",
            "total_revenue": {"$sum": "$items.subtotal"},
            "total_quantity_sold": {"$sum": "$items.quantity"}
        }
    },
    {"$sort": {"total_revenue": -1}}
]

revenue_results = db.transactions.aggregate(revenue_pipeline)
for res in revenue_results:
    print(f"Category: {res['_id']} | Total Revenue: ${res['total_revenue']:.2f} | Items Sold: {res['total_quantity_sold']}")


# --- Pipeline 2: Product Popularity Analysis (Top 5 Best Sellers) ---
print("\n--- Pipeline 2: Top 5 Best-Selling Products ---")
popularity_pipeline = [
    {"$unwind": "$items"},
    {
        "$group": {
            "_id": "$items.product_id",
            "units_sold": {"$sum": "$items.quantity"},
            "times_ordered": {"$sum": 1}
        }
    },
    {
        "$lookup": {
            "from": "products",
            "localField": "_id",
            "foreignField": "product_id",
            "as": "details"
        }
    },
    {"$unwind": "$details"},
    {
        "$project": {
            "product_id": "$_id",
            "product_name": "$details.name",
            "units_sold": 1,
            "base_price": "$details.base_price"
        }
    },
    {"$sort": {"units_sold": -1}},
    {"$limit": 5}
]

popularity_results = db.transactions.aggregate(popularity_pipeline)
for idx, res in enumerate(popularity_results, start=1):
    print(f"{idx}. {res['product_name']} ({res['product_id']}) | Units Sold: {res['units_sold']} | Price: ${res['base_price']}")

import json
from pymongo import MongoClient

# Connect to the MongoDB Container
# If running inside the Jupyter container, use 'ecommerce_mongodb' as the host.
# If running directly from your host PC, use 'localhost'.
client = MongoClient("mongodb://ecommerce_mongodb:27017/")
db = client["Unified_Ecommerce_DB"]

def load_json_to_mongo(file_path, collection_name):
    print(f"Loading {file_path} into collection '{collection_name}'...")
    with open(file_path, 'r') as file:
        data = json.load(file)
        collection = db[collection_name]
        
        # Clear existing data to avoid duplicates if re-run
        collection.delete_many({}) 
        
        if isinstance(data, list):
            collection.insert_many(data)
        else:
            collection.insert_one(data)
    print(f"Successfully loaded {collection.count_documents({})} documents.")

# Change the paths at the bottom of your mongo_ingestion.py file to this:
load_json_to_mongo("work/data/users.json", "users")
load_json_to_mongo("work/data/products.json", "products")
load_json_to_mongo("work/data/categories.json", "categories")
load_json_to_mongo("work/data/transactions.json", "transactions")

print("MongoDB Ingestion Complete!")

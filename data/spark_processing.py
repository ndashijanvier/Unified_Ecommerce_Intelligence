from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, to_timestamp

# 1. Initialize Distributed Spark Session
spark = SparkSession.builder \
    .appName("Unified_Ecommerce_Intelligence_Spark") \
    .config("spark.sql.shuffle.partitions", "4") \
    .getOrCreate()

print("Spark Session started successfully. Processing datasets...")

# 2. Batch load datasets from mounted storage files
users_df = spark.read.option("multiLine", "true").json("work/data/users.json")
transactions_df = spark.read.option("multiLine", "true").json("work/data/transactions.json")


# 3. Data Cleaning & Normalization Pipeline
# Standardize raw transaction string timestamps to true system timestamp objects
cleaned_transactions_df = transactions_df.withColumn(
    "timestamp", 
    to_timestamp(col("timestamp"))
).na.fill({"discount": 0.0, "total": 0.0}) # handle empty fields gracefully

print("\n--- Cleaned & Normalized Transactions Schema View ---")
cleaned_transactions_df.printSchema()

# 4. Cohort Registration Analysis (Grouping users by geographic location metrics)
print("\n--- User Volume Distribution by Regional Demographics ---")
geo_cohort_summary = users_df.groupBy("geo_data.country", "geo_data.state") \
    .count() \
    .orderBy(col("count").desc())

geo_cohort_summary.show(5)

# 5. Spark SQL Query Registration Engine
cleaned_transactions_df.createOrReplaceTempView("transactions")

print("\n--- Spark SQL Query Result: High-Value Transactions (> $400) ---")
high_value_sales = spark.sql("""
    SELECT transaction_id, user_id, total, payment_method, status
    FROM transactions 
    WHERE total > 400.00
    ORDER BY total DESC
""")
high_value_sales.show(5)

spark.stop()
print("Spark Processing Pipeline Completed successfully.")

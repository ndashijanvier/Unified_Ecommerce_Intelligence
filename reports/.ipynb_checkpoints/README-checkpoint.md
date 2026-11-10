# Unified_Ecommerce_Intelligence
### Distributed Multi-Model Analytics for E-commerce Data
**Course:** AUCA Big Data Analytics Final Project  
**Author:** Janvier Ndashimye  
**Date:** November 2026  

---

## Project Overview
This project implements a multi-faceted big data analytics ecosystem handling large-scale, heterogeneous e-commerce datasets spanning users, products, categories, sessions, and transactions. The platform leverages the distinct strengths of:
1. **MongoDB (Document Store):** Managing highly structured user profiles, product catalogs, and transactional order documents.
2. **HBase (Wide-Column Store):** Archiving high-volume, sparse time-series clickstream sessions optimized via custom row-keys (`user_id + timestamp`).
3. **Apache Spark (Distributed Processing Engine):** Orchestrating large-scale batch processing, cleaning nested schemas, and integrating multi-database metrics to calculate Customer Lifetime Value (CLV).

---

## Repository & Project Structure
All data management scripts, analytical pipelines, and notebook assets are centrally grouped within the primary project directory for execution simplicity:

```text
Unified_Ecommerce_Intelligence/
├── data/
│   ├── users.json                         # Generated synthetic user profiles
│   ├── products.json                      # Product catalog dataset
│   ├── categories.json                    # Product categories hierarchy
│   ├── transactions.json                  # Multi-line nested transactions dataset
│   ├── sessions_0.json                    # Sparse browsing telemetry stream
│   ├── mongo_ingestion.py                 # MongoDB data loading pipeline
│   ├── mongo_analytics.py                 # MongoDB aggregation analytics pipelines
│   ├── hbase_ingestion.py                 # Happybase high-volume storage pipeline
│   ├── hbase_query.py                     # HBase time-series verification script
│   ├── spark_processing.py                # Distributed batch cleaning & SQL submission
│   ├── spark_interactive_analytics.ipynb  # Interactive Spark browser workspace notebook
│   ├── unified_analytics.py               # Cross-engine consolidation & CLV pipeline
│   └── generate_visualizations.py         # Static plot visualization generator script
├── docker-compose.yml                     # Infrastructure cluster setup configuration
└── README.md                              # Operational execution manual
```

---

## System Requirements & Prerequisites
Before executing the pipeline, ensure the following infrastructure blocks are installed on your host machine:
* **Docker Desktop** (with Docker Compose V2)
* Minimum 8GB RAM allocated to the Docker Engine daemon.

---

## Step-by-Step Deployment & Execution Guide

### Step 1: Boot Up the Multi-Model Cluster Infrastructure
Open your host system terminal (CMD/PowerShell), navigate to your root project directory, and initialize the active background database containers:
```bash
cd C:\Users\Janvier\Documents\Unified_Ecommerce_Intelligence
docker-compose up -d
```
Verify all services (`ecommerce_jupyter`, `ecommerce_mongodb`, `ecommerce_hbase`) are completely operational and healthy:
```bash
docker ps
```

### Step 2: Initialize the HBase Database Schema
Enter the interactive HBase shell environment inside the active cluster container to provision the physical table and column families:
```bash
docker exec -it ecommerce_hbase hbase shell
```
Inside the interactive HBase prompt, run the schema compilation directives:
```hbase
create 'user_sessions', 'info', 'activity'
list
exit
```

### Step 3: Run the Data Loading and Analytical Scripts
Execute the underlying storage and analytics routines sequentially from your command prompt using the configured Python engine container:

#### A. MongoDB Layer Ingestion & Analytical Aggregations
Load user, catalog, and transactional records into MongoDB, and execute complex aggregation pipelines (Category Revenue Analysis & Top 5 Best-Sellers):
```bash
docker exec -it ecommerce_jupyter python work/data/mongo_ingestion.py
docker exec -it ecommerce_jupyter python work/data/mongo_analytics.py
```

#### B. HBase Layer Telemetry Ingestion & Query Verification
Install the Thrift client connection library and ingest the 20,000 real-time browsing stream logs before executing a custom row-key lookup:
```bash
docker exec -it ecommerce_jupyter pip install happybase
docker exec -it ecommerce_jupyter python work/data/hbase_ingestion.py
docker exec -it ecommerce_jupyter python work/data/hbase_query.py
```

#### C. Apache Spark Distributed Batch Engine Execution
Submit the core Spark cluster job to clean, normalize, and query high-value nested datasets:
```bash
docker exec -it ecommerce_jupyter spark-submit work/data/spark_processing.py
```

#### D. Multi-Engine Analytics Integration (CLV Report)
Run the analytical join operation connecting MongoDB data layers and transactional variables to measure Customer Lifetime Value:
```bash
docker exec -it ecommerce_jupyter python work/data/unified_analytics.py
```

#### E. Static Visualizations Suite Generation
Generate the 4 mandatory high-resolution static graphs specified in the assignment evaluation rubric:
```bash
docker exec -it ecommerce_jupyter python work/data/generate_visualizations.py
```
*Generated plots (`1_category_revenue.png`, `2_payment_methods.png`, `3_session_durations.png`, `4_transaction_funnel.png`) will be automatically saved into the workspace directory for validation.*

---

## Web Browser Cluster Dashboards

### 1. Interactive Jupyter Lab Workspace Terminal
To visually verify scripts or run the interactive file tracking pipeline cell-by-cell:
* **URL:** `http://localhost:8888`
* **Access Token Retrieval:** Run `docker exec -it ecommerce_jupyter jupyter server list` to fetch the authentication key.
* Open and run `spark_interactive_analytics.ipynb` within the browser environment.

### 2. Live Apache Spark Web UI Application Master
To audit the cluster's parallel thread orchestration, stages distribution timeline, and DAG lineage maps during live tasks:
* **URL:** `http://localhost:4040` *(Accessible while a Spark session is actively executing inside the notebook environment).*

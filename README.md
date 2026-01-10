💱 Exchange Rates Analytics Pipeline

Daily Currency Conversion & USD Strength Analysis

📌 Project Overview

This project implements a production-style ELT data pipeline for daily exchange rate analysis, designed to showcase modern Data Engineering best practices:

- Containerized infrastructure with Docker
- Orchestration using Apache Airflow
- Data Lake architecture (Bronze / Silver / Gold)
- Incremental and idempotent processing
- Analytical modeling for BI dashboards (Power BI)

The pipeline ingests daily currency exchange rates, processes them through structured layers, and exposes business-ready analytical views for geo-economic insights and USD strength analysis.

💡 Main Idea

Daily analysis of exchange rates and currency conversion against USD, enabling:

- Historical tracking of exchange rates
- Currency appreciation and depreciation analysis
- Volatility analysis
- Geographic exposure (continent & country level)
- SQL-based analytics ready for Power BI consumption

🌍 Data Source
ExchangeRate API

Provider: ExchangeRate-API

Endpoint: GET https://v6.exchangerate-api.com/v6/YOUR_API_KEY/latest/USD


🏗️ Architecture Overview

ExchangeRate API
        ↓
[ Bronze ] → MinIO (Raw JSON / Parquet)
        ↓
[ Silver ] → PostgreSQL Data Warehouse (Normalized rates)
        ↓
[ Gold ]   → SQL Views / dbt-ready models
        ↓
Power BI / Analytics


🧱 Tech Stack

| Layer           | Technology              |
| --------------- | ----------------------- |
| Orchestration   | Apache Airflow          |
| Containers      | Docker & Docker Compose |
| Data Lake       | MinIO (S3-compatible)   |
| Processing      | Python (Pandas, s3fs)   |
| Data Warehouse  | PostgreSQL              |
| Transformations | SQL (dbt-ready)         |
| BI              | Microsoft Power BI      |
| Metadata DB     | PostgreSQL (Airflow)    |

🔄 ELT Flow by Layer

🥉 Bronze — Raw Ingestion

Purpose: Extract and store raw data exactly as received.

- Python container calls the ExchangeRate API
- Full API response stored in MinIO
- Timestamp-based idempotency check
- Storage format: Parquet

![alt text](image.png)

🥈 Silver — Structured & Normalized

Purpose: Transform raw data into an analytical format.

- Reads Bronze data from MinIO
- Filters only new exchange rate records
- Unpivots conversion rates using melt
- Loads normalized data into PostgreSQL

![alt text](image-1.png)

🥇 Gold — Analytical Models (SQL)

Business-oriented SQL views designed for BI consumption:

- Currency appreciation & depreciation
- Monthly and yearly volatility
- USD strength by continent
- Latest exchange rate snapshot
- Geo-economic USD exposure

These views act as the semantic layer for analytics.

🧠 Orchestration with Airflow
DAG: exchange_rates_pipeline

- Implemented using DockerOperator
- Fully containerized execution
- Idempotent and restart-safe

Task Flow:    bronze_task → silver_task

| Task        | Description                |
| ----------- | -------------------------- |
| bronze_task | API extraction → MinIO     |
| silver_task | Normalization → PostgreSQL |


📊 Analytical SQL Views (Gold Layer)
🌎 USD Strength by Continent

continent_usd_strength_view

- Average USD exchange rate
- Volatility by continent
- Currency coverage per region

📉 Currency Appreciation / Depreciation

currency_appreciation_depreciation_view

- Daily deltas using window functions
- Identifies appreciating vs depreciating currencies

🌪️ Currency Volatility Analysis

currency_volatility_view

- Monthly volatility (e.g. October / November)
- Full-year performance
- Min / Max / Average values

🧭 Geo-Economic USD Exposure

geoeconomic_usd_exposure_view

- Country and continent exposure
- USD volatility and range movement

⏱️ Latest Exchange Rate Snapshot

latest_exchange_rate_view

- Most recent valid exchange rate per currency
- Cleaned and BI-ready


📈 Microsoft Power BI Integration

PostgreSQL DirectQuery

Visual Tools:

- USD strength by continent
- Currency volatility ranking
- Daily exchange rate trends
- Regional exposure analysis
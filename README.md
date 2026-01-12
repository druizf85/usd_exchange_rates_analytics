💱 Exchange Rates Analytics Pipeline -> Daily Currency Conversion & USD Strength Analysis


📌 Project Overview: 
This project implements a production-style ELT data pipeline for daily exchange rate analysis, designed to showcase modern Data Engineering best practices:

- Containerized infrastructure with Docker
- Orchestration using Apache Airflow
- Data Lake architecture (Bronze / Silver / Gold)
- Incremental and idempotent processing
- Analytical modeling for BI dashboards (Power BI)

The pipeline ingests daily currency exchange rates, processes them through structured layers, and exposes business-ready analytical views for geo-economic insights and USD strength analysis.


💡 Main Idea: Daily analysis of exchange rates and currency conversion against USD, enabling:

- Historical tracking of exchange rates
- Currency appreciation and depreciation analysis
- Volatility analysis
- Geographic exposure (continent & country level)
- SQL-based analytics ready for Power BI consumption


🌍 Data Source: ExchangeRate API
Endpoint: GET https://v6.exchangerate-api.com/v6/API_KEY/latest/USD


🏗️ Architecture Overview

ExchangeRate API
        ↓
[ Bronze ] → MinIO (Raw JSON / Parquet)
        ↓
[ Silver ] → PostgreSQL Data Warehouse (Normalized rates)
        ↓
[ Gold ]   → SQL Views
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
| Transformations | SQL views        |
| BI              | Microsoft Power BI      |
| Metadata DB     | PostgreSQL (Airflow)    |


🔄 ELT Flow by Layer

🥉 Bronze — Raw Ingestion

Purpose: Extract and store raw data exactly as received.

- Python container calls the ExchangeRate API
- Full API response stored in MinIO
- Timestamp-based idempotency check
- Storage format: Parquet

<img width="2232" height="1119" alt="Captura de pantalla 2026-01-10 173645" src="https://github.com/user-attachments/assets/4fd45a50-ef03-4075-9864-afce477383c8" />


🥈 Silver — Structured & Normalized

Purpose: Transform raw data into an analytical format.

- Reads Bronze data from MinIO
- Filters only new exchange rate records
- Unpivots conversion rates using melt
- Loads normalized data into PostgreSQL

<img width="2879" height="1460" alt="Captura de pantalla 2026-01-10 180519" src="https://github.com/user-attachments/assets/77ab92a3-5f41-4fa3-8c6d-9b80bdcd23a6" />


🥇 Gold — Analytical Models (SQL)

Business-oriented SQL views designed for BI consumption. These views act as the semantic layer for analytics, mainly focused on these aspects:

- Currency appreciation & depreciation
- Monthly and yearly volatility
- USD strength by continent
- Latest exchange rate snapshot
- Geo-economic USD exposure

Analytical SQL Views

1. USD Strength by Continent

- Average USD exchange rate
- Volatility by continent
- Currency coverage per region

2. Currency Appreciation / Depreciation

- Daily deltas using window functions
- Identifies appreciating vs depreciating currencies

3. Currency Volatility Analysis

- Monthly volatility (e.g. October / November)
- Full-year performance
- Min / Max / Average values

4. Geo-Economic USD Exposure

- Country and continent exposure
- USD volatility and range movement

5. Latest Exchange Rate Snapshot

- Most recent valid exchange rate per currency
- Cleaned and BI-ready

📊 Microsoft Power BI Integration: PostgreSQL DirectQuery

Visual Tools:

- USD strength by continent
- Currency volatility ranking
- Daily exchange rate trends
- Regional exposure analysis



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


📈 Project Impact:





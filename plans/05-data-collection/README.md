# Data Collection and Pipeline Plans for LegiSim

This directory contains the comprehensive plans for collecting, processing, and storing the data required to power the LegiSim policy simulation engine. The data serves as the foundation for building realistic cohorts, calibrating mathematical models, and providing historical context for AI analysis.

## Overview of Data Sources

LegiSim relies on the following primary data sources:

1. **Census of India**: Core demographic data for building population cohorts.
2. **Ministry of Statistics and Programme Implementation (MoSPI)**: Macroeconomic indicators, inflation data, and national accounts.
3. **Reserve Bank of India (RBI)**: Monetary policy data, interest rates, exchange rates.
4. **Periodic Labour Force Survey (PLFS)**: Employment statistics, wages, labor force participation.
5. **Household Consumer Expenditure Survey (HCES)**: Consumption patterns across different demographics and income groups.
6. **National Family Health Survey (NFHS)**: Health, nutrition, and welfare indicators.
7. **Government Microdata (microdata.gov.in)**: Detailed unit-level data for deeper analysis.
8. **Union and State Budgets**: Fiscal data, subsidies, expenditures.

## Ingestion Pipeline Architecture

The overall data pipeline architecture follows a standardized ETL process:

1. **Extraction**:
   - **Manual Downloads**: Some government portals require manual navigation and captcha solving. For these, detailed download instructions are provided, and data will be stored in a centralized raw storage layer (MinIO or S3-compatible).
   - **Automated Scraping**: Where possible, Python-based scrapers (using `requests`, `BeautifulSoup`, `playwright`) will automatically fetch data on a schedule.
   - **API Integration**: Direct connections to official APIs (like RBI DBIE API) where available.

2. **Transformation**:
   - Python-based ETL scripts (using `pandas`, `pyspark` for large datasets).
   - Cleaning missing values, normalizing geographic names (State/District harmonization across different surveys).
   - Time-series alignment (interpolating missing data, standardizing frequencies).
   - Constructing base cohorts and calculating weights.

3. **Loading**:
   - **PostgreSQL**: Primary structured storage for cleaned demographic tables, economic time series, and configuration metadata.
   - **pgvector**: Storage for vector embeddings of historical policy analogues and research documents to enable semantic search.
   - **Parquet**: Storage format for large unit-level microdata sets that are too large for efficient relational querying but needed for specialized analysis.

## Component Plans

- [Census Data Collection Plan](./01-census-data/plan.md): Focuses on demographic data and cohort building.
- [Economic Data Collection Plan](./02-economic-data/plan.md): Covers macroeconomic indicators, labor, and expenditure surveys.
- [Policy Analogues Library Plan](./03-policy-analogues/plan.md): Details the construction of a historical policy database with vector embeddings for AI retrieval.

## Subagent Assignments

- `data-pipeline-engineer`: Responsible for building and orchestrating the ETL pipelines, ensuring data quality, and loading data into appropriate stores.
- `data-analyst`: Conducts initial exploratory data analysis, validates cohort weights against known aggregates, and verifies economic model assumptions.
- `opencode`: Writes boilerplate scraping scripts, download utilities, and basic data cleaning routines.
- `database-architect`: Designs the PostgreSQL schemas, manages pgvector indexes, and optimizes query performance.
- `copilot`: Handles complex analogue mapping, semantic search tuning, and AI-driven data extraction tasks.

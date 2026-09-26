# Economic Data Collection Plan

## Objective
To collect macroeconomic indicators, employment statistics, and household expenditure data necessary for calibrating the mathematical simulation models in LegiSim.

## Data Sources & Download Procedures

### 1. Reserve Bank of India (RBI) Data
- **Data Elements**: Inflation (CPI/WPI), Repo Rates, GDP estimates, Sector-wise credit, Exchange rates.
- **Source**: RBI Database on Indian Economy (DBIE) portal.
- **Procedure**: RBI provides APIs and Excel downloads. We will use the RBI DBIE API or web scraping where APIs fall short.
- **URL**: `https://dbie.rbi.org.in/`

### 2. Ministry of Statistics and Programme Implementation (MoSPI)
- **Data Elements**: Index of Industrial Production (IIP), National Accounts Statistics (GDP breakdown).
- **Source**: MoSPI official website.
- **Procedure**: Automated scraping of PDF/Excel reports or consuming APIs if available on the newer data portals.
- **URL**: `https://mospi.gov.in/`

### 3. Periodic Labour Force Survey (PLFS)
- **Data Elements**: Labour Force Participation Rate (LFPR), Worker Population Ratio (WPR), Unemployment Rate (UR), average earnings by industry and occupation.
- **Source**: Microdata available via MoSPI or specific PLFS annual reports.
- **Procedure**: Download unit-level data (usually in fixed-width text formats with STATA/SPSS dictionaries). Convert to Parquet format for processing.

### 4. Household Consumer Expenditure Survey (HCES)
- **Data Elements**: Monthly Per Capita Consumption Expenditure (MPCE), spending patterns on food, fuel, education, etc.
- **Source**: MoSPI microdata portal.
- **Procedure**: Similar to PLFS, requires processing raw unit-level data files into structured Parquet tables.

### 5. State Budgets
- **Data Elements**: Revenue receipts, capital expenditure, allocations to specific schemes, subsidies.
- **Source**: RBI's "State Finances: A Study of Budgets" report, PRS Legislative Research.
- **Procedure**: Scrape/extract data from RBI's consolidated Excel annexures.

## Standardization & Time Series Alignment

Economic data arrives at different frequencies (daily, monthly, quarterly, annual).
- We will standardize all macro time-series data to a **monthly** and **quarterly** frequency table in PostgreSQL.
- Interpolation techniques (e.g., cubic spline) will be used for lower-frequency data when higher frequency is required for simulation steps.

## PostgreSQL Schema (Macro Indicators)

```sql
CREATE TABLE macro_indicators (
    indicator_id SERIAL PRIMARY KEY,
    indicator_code VARCHAR(50) UNIQUE NOT NULL,
    indicator_name VARCHAR(255) NOT NULL,
    frequency VARCHAR(20), -- 'MONTHLY', 'QUARTERLY', 'ANNUAL'
    unit VARCHAR(50)
);

CREATE TABLE macro_time_series (
    series_id SERIAL PRIMARY KEY,
    indicator_id INTEGER REFERENCES macro_indicators(indicator_id),
    date_period DATE NOT NULL,
    value NUMERIC NOT NULL,
    source VARCHAR(100),
    UNIQUE(indicator_id, date_period)
);
```

## Subagent Assignments

- **`opencode`**: Write web scrapers for RBI DBIE and MoSPI portals using `playwright` or `requests`. Write parsers for PLFS/HCES fixed-width files.
- **`data-pipeline-engineer`**: Build robust ETL pipelines using Apache Airflow or Prefect to manage the regular ingestion of time-series data. Handle Parquet conversion for microdata.
- **`data-analyst`**: Analyze PLFS and HCES data to compute income distributions and consumption propensities for the population cohorts. Align time series data and handle missing values.

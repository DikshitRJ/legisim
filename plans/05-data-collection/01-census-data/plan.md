# Census Data Collection Plan

## Objective
To collect, clean, and process Census of India 2011 data to construct base population cohorts and their representative weights for LegiSim simulations.

## Required Data Tables (Census 2011)

We need the following primary tables (typically available in Excel/CSV formats):

1. **Primary Census Abstract (PCA)**: Total population, SC/ST population, literates, main workers, marginal workers, non-workers by State/District/Sub-district (Urban/Rural).
2. **C-14 Single Year Age Data**: Population by single-year age, gender, and residence (Urban/Rural).
3. **C-8 Educational Attainment**: Population by educational level, age group, and gender.
4. **B-1 Main Workers, Marginal Workers and Non-Workers**: By age, gender, and residence.

## Download Procedure

Since `censusindia.gov.in` has dynamic portals and sometimes requires captchas, manual download followed by automated processing is the most robust approach for the initial bulk load.

1. Navigate to the [Office of the Registrar General & Census Commissioner, India](https://censusindia.gov.in/).
2. Go to Data -> Census Tables.
3. Select "2011 Census Data".
4. Download the specific C-Series (Age, Education) and B-Series (Economic Activity) tables in Excel/CSV format.
5. Place the downloaded files in a standardized `raw_data/census_2011/` directory in the MinIO/S3 bucket.

## Data Cleaning and Normalization

- **Header Standardization**: Census Excel files often have complex multi-row headers. We will write Python scripts using `pandas` to skip header rows, set proper column names, and unpivot (melt) the data into a tidy format.
- **Geographic Normalization**: Standardize State and District names (e.g., "Odisha" vs "Orissa") using a master lookup table to ensure joins with other datasets (like NFHS/PLFS) work seamlessly.
- **Age Grouping**: Group single-year age data into standard brackets (e.g., 0-14, 15-24, 25-34, 35-44, 45-54, 55-64, 65+).

## Cohort Weight Generation

To simulate policies, we build distinct demographic cohorts. A cohort is defined by a unique combination of attributes: State, Urban/Rural, Age Group, Gender, and Income/Class (derived later by joining with PLFS/HCES). The "weight" of the cohort represents how many real individuals it represents.

## PostgreSQL Schema

```sql
CREATE TABLE location_master (
    location_id SERIAL PRIMARY KEY,
    state_name VARCHAR(100) NOT NULL,
    district_name VARCHAR(100),
    is_urban BOOLEAN NOT NULL,
    UNIQUE(state_name, district_name, is_urban)
);

CREATE TABLE cohort_demographics (
    cohort_id SERIAL PRIMARY KEY,
    location_id INTEGER REFERENCES location_master(location_id),
    age_group VARCHAR(20) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    education_level VARCHAR(50),
    employment_status VARCHAR(50),
    base_population_weight NUMERIC NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_cohort_location ON cohort_demographics(location_id);
```

## Python ETL Snippet

```python
import pandas as pd
from sqlalchemy import create_engine

def process_age_data(file_path):
    # Read C-14 table, skipping the first few complex header rows
    df = pd.read_excel(file_path, skiprows=6)
    
    # Rename columns to standard names
    df.columns = ['table_name', 'state_code', 'district_code', 'area_name', 
                  'total_rural_urban', 'age', 'total_persons', 'total_males', 'total_females']
    
    # Filter for relevant rows (e.g., State level summaries)
    df = df[df['district_code'] == '000'] 
    
    # Clean and transform
    df['age'] = pd.to_numeric(df['age'], errors='coerce')
    # Group into buckets...
    
    return df

# Further processing and loading to PostgreSQL
```

## Subagent Assignments

- **`opencode`**: Write download scripts (if applicable via API) and the specific `pandas` cleaning scripts for the complex Excel headers of the Census files.
- **`data-pipeline-engineer`**: Orchestrate the ETL pipeline, handle the database connections, and load the cleaned data into PostgreSQL.
- **`data-analyst`**: Validate the total population counts against known aggregates to ensure no data loss during cleaning.

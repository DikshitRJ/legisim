# Policy Analogues Library Plan

## Objective
To build a comprehensive, vector-embedded database of historical Indian policy events. This library allows the AI modules in LegiSim to find historical precedents for proposed policies, understand real-world impacts, and identify unintended consequences.

## Key Policy Events to Document

We will systematically gather documents, news reports, research papers, and outcome reports for the following events:

1. **Demonetisation (2016)**: Impact on cash circulation, digital payments, informal sector employment.
2. **GST Implementation (2017)**: State revenue impacts, formalization of economy, initial disruption.
3. **Farm Laws (2020-2021)**: Market deregulation attempts, stakeholder reaction, repeal.
4. **Rice Export Restrictions (2007-2011 & Recent)**: Impact on domestic inflation vs farmer income.
5. **Fuel Price Deregulation (2010/2014)**: Impact on inflation, transport costs, and fiscal deficit.
6. **MGNREGA Launch (2005)**: Rural wage impacts, labor migration shifts.
7. **Pradhan Mantri Jan Dhan Yojana (2014)**: Financial inclusion, bank account penetration.
8. **Direct Benefit Transfer (DBT) Rollout**: Leakage reduction, targeting efficiency.
9. **EV Subsidy (FAME Scheme)**: Adoption rates, fiscal burden, industry response.
10. **Free Bus Travel Schemes (State-level, e.g., Shakti in Karnataka)**: Female labor force participation impacts, state transport corporation finances.
11. **Minimum Wage Revisions**: Impact on formal employment and inflation.

## Data Structure and Schema

For each analogue, we capture metadata, structured summaries, and dense vector embeddings of the full text to enable semantic search.

```sql
-- Requires pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE policy_analogues (
    analogue_id SERIAL PRIMARY KEY,
    policy_name VARCHAR(255) NOT NULL,
    implementation_date DATE,
    sector VARCHAR(100),
    target_demographic VARCHAR(255),
    description TEXT,
    measured_outcomes TEXT,
    unintended_consequences TEXT,
    data_sources JSONB -- Array of URLs and citations
);

CREATE TABLE policy_documents (
    document_id SERIAL PRIMARY KEY,
    analogue_id INTEGER REFERENCES policy_analogues(analogue_id),
    title VARCHAR(255),
    content TEXT,
    source_url VARCHAR(500),
    embedding vector(1536) -- Using OpenAI text-embedding-3-small or similar
);

-- HNSW index for fast similarity search
CREATE INDEX ON policy_documents USING hnsw (embedding vector_cosine_ops);
```

## Analogue Matching Algorithm

When a user proposes a new policy in LegiSim:
1. The AI extracts the core mechanisms, target demographics, and sector of the proposed policy.
2. We generate an embedding for this policy description.
3. We perform a vector similarity search (Cosine distance) against `policy_documents`.
4. We retrieve the top $K$ matching documents and their associated `policy_analogues`.
5. An LLM (`copilot`) synthesizes these historical precedents to generate a "Historical Context & Risk Warning" report for the simulation.

## Subagent Assignments

- **`data-pipeline-engineer`**: Set up the PostgreSQL schema with pgvector. Build the ingestion pipeline that takes raw text, calls the embedding API, and stores the results.
- **`copilot`**: Responsible for the deep research. Given the list of policies, the copilot will search the web, extract comprehensive descriptions, identify measured outcomes, and summarize unintended consequences.
- **`opencode`**: Build simple web scraping utilities to download specific research papers, government reports, or news archives when provided URLs by the copilot.

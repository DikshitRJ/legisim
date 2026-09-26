#!/usr/bin/env bash
set -e

# ==============================================================================
# LegiSim PostgreSQL Database Initialization Script
# ==============================================================================
# Executed automatically on container first startup via
# /docker-entrypoint-initdb.d/init-db.sh
# ==============================================================================

echo "==> [init-db] Initializing LegiSim PostgreSQL database..."

TARGET_USER="${POSTGRES_USER:-legisim}"
TARGET_DB="${POSTGRES_DB:-legisim}"

# Create pgvector extension on the primary database
echo "==> [init-db] Creating extensions 'vector' and 'uuid-ossp' on database '$TARGET_DB'..."
psql -v ON_ERROR_STOP=1 --username "$TARGET_USER" --dbname "$TARGET_DB" <<-EOSQL
    CREATE EXTENSION IF NOT EXISTS vector;
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
EOSQL

# If the target database wasn't 'legisim', ensure 'legisim' database exists and has vector extension
if [ "$TARGET_DB" != "legisim" ]; then
    echo "==> [init-db] Ensuring 'legisim' database exists..."
    psql -v ON_ERROR_STOP=1 --username "$TARGET_USER" --dbname "$TARGET_DB" <<-EOSQL
        SELECT 'CREATE DATABASE legisim'
        WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'legisim')\gexec
EOSQL
    echo "==> [init-db] Enabling extensions on 'legisim' database..."
    psql -v ON_ERROR_STOP=1 --username "$TARGET_USER" --dbname "legisim" <<-EOSQL
        CREATE EXTENSION IF NOT EXISTS vector;
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
EOSQL
fi

echo "==> [init-db] Database initialization completed successfully. pgvector extension is active."

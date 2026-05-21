"""Load tips data into DuckDB. Paths are env-var configurable for CI."""

import os
import duckdb

# Default paths fall back to local Codespaces; CI sets env vars
DUCKDB_PATH = os.environ.get(
    "DUCKDB_PATH",
    "/workspaces/snowflake-dbt-pipeline/duckdb_warehouse.duckdb"
)
CSV_PATH = os.environ.get(
    "CSV_PATH",
    "/workspaces/snowflake-dbt-pipeline/data/raw/superstore.csv"
)

SCHEMA = "raw"
TABLE = "superstore"


def main():
    print(f"📂 Reading CSV from: {CSV_PATH}")

    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"CSV not found at {CSV_PATH}")

    print(f"🦆 Connecting to DuckDB at: {DUCKDB_PATH}")
    con = duckdb.connect(DUCKDB_PATH)

    con.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA}")

    print(f"⬇️  Loading data into {SCHEMA}.{TABLE}")
    con.execute(f"""
        CREATE OR REPLACE TABLE {SCHEMA}.{TABLE} AS
        SELECT * FROM read_csv_auto('{CSV_PATH}')
    """)

    row_count = con.execute(f"SELECT COUNT(*) FROM {SCHEMA}.{TABLE}").fetchone()[0]
    print(f"✅ Loaded {row_count} rows into {SCHEMA}.{TABLE}")

    con.close()
    print("🎉 Done!")


if __name__ == "__main__":
    main()

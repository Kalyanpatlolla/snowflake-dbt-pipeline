"""
Load tips data into Snowflake.

Credentials are read from environment variables — NEVER hardcoded.
Set them in your Codespace by running (or via Codespaces Secrets):

    export SNOWFLAKE_USER="..."
    export SNOWFLAKE_PASSWORD="..."
    export SNOWFLAKE_ACCOUNT="..."
"""

import os
import sys
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas


def get_required_env(name: str) -> str:
    """Fetch an environment variable or exit with a helpful error."""
    value = os.environ.get(name)
    if not value:
        sys.exit(
            f"❌ Missing required environment variable: {name}\n"
            f"   Set it with:  export {name}='your_value'"
        )
    return value


def main():
    # Load CSV into pandas DataFrame
    csv_path = "data/raw/superstore.csv"
    df = pd.read_csv(csv_path)
    print(f"📂 Dataset loaded from {csv_path}")
    print(df.head())

    # Pull credentials from environment (never from code)
    user = get_required_env("SNOWFLAKE_USER")
    password = get_required_env("SNOWFLAKE_PASSWORD")
    account = get_required_env("SNOWFLAKE_ACCOUNT")

    # Connection parameters with safe defaults for non-sensitive fields
    warehouse = os.environ.get("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH")
    database = os.environ.get("SNOWFLAKE_DATABASE", "SNOWFLAKE_DBT_DB")
    schema = os.environ.get("SNOWFLAKE_SCHEMA", "RAW")
    role = os.environ.get("SNOWFLAKE_ROLE", "ACCOUNTADMIN")

    # Connect to Snowflake
    conn = snowflake.connector.connect(
        user=user,
        password=password,
        account=account,
        warehouse=warehouse,
        database=database,
        schema=schema,
        role=role,
    )
    print("❄️  Connected to Snowflake successfully.")

    # Upload DataFrame to Snowflake table
    success, nchunks, nrows, _ = write_pandas(
        conn,
        df,
        table_name="SUPERSTORE",
        auto_create_table=True,
        overwrite=True,
    )
    print(f"✅ {nrows} rows loaded into SUPERSTORE.")

    # Close connection
    conn.close()
    print("🔒 Snowflake connection closed.")


if __name__ == "__main__":
    main()
import pandas as pd
import sqlite3
import os

DB_PATH = "bluestock_mf.db"
PROCESSED_PATH = "data/processed"
SCHEMA_PATH = "sql/schema.sql"

print("=" * 80)
print("DAY 2 - SQLITE LOADING STARTED")
print("=" * 80)

# =========================================================
# Load processed datasets
# =========================================================
fund_master = pd.read_csv(f"{PROCESSED_PATH}/01_fund_master_cleaned.csv")
nav_history = pd.read_csv(f"{PROCESSED_PATH}/02_nav_history_cleaned.csv")
aum = pd.read_csv(f"{PROCESSED_PATH}/03_aum_by_fund_house_cleaned.csv")
sip = pd.read_csv(f"{PROCESSED_PATH}/04_monthly_sip_inflows_cleaned.csv")
category_inflows = pd.read_csv(f"{PROCESSED_PATH}/05_category_inflows_cleaned.csv")
folio = pd.read_csv(f"{PROCESSED_PATH}/06_industry_folio_count_cleaned.csv")
performance = pd.read_csv(f"{PROCESSED_PATH}/07_scheme_performance_cleaned.csv")
transactions = pd.read_csv(f"{PROCESSED_PATH}/08_investor_transactions_cleaned.csv")
holdings = pd.read_csv(f"{PROCESSED_PATH}/09_portfolio_holdings_cleaned.csv")
benchmark = pd.read_csv(f"{PROCESSED_PATH}/10_benchmark_indices_cleaned.csv")

# =========================================================
# Create dim_date from all available dates
# =========================================================
all_dates = pd.concat([
    pd.to_datetime(nav_history["date"], errors="coerce"),
    pd.to_datetime(aum["date"], errors="coerce"),
    pd.to_datetime(sip["month"], errors="coerce"),
    pd.to_datetime(category_inflows["month"], errors="coerce"),
    pd.to_datetime(folio["month"], errors="coerce"),
    pd.to_datetime(transactions["transaction_date"], errors="coerce"),
    pd.to_datetime(holdings["portfolio_date"], errors="coerce"),
    pd.to_datetime(benchmark["date"], errors="coerce")
]).dropna().drop_duplicates().sort_values()

dim_date = pd.DataFrame({"full_date": all_dates})
dim_date["year"] = dim_date["full_date"].dt.year
dim_date["quarter"] = dim_date["full_date"].dt.quarter
dim_date["month"] = dim_date["full_date"].dt.month
dim_date["month_name"] = dim_date["full_date"].dt.month_name()
dim_date["day"] = dim_date["full_date"].dt.day
dim_date["weekday_name"] = dim_date["full_date"].dt.day_name()

# =========================================================
# Prepare fact tables
# =========================================================
nav_fact = nav_history.rename(columns={"date": "nav_date"})
aum_fact = aum.rename(columns={"date": "aum_date"})

performance_fact = performance[
    [
        "amfi_code", "return_1yr_pct", "return_3yr_pct", "return_5yr_pct",
        "benchmark_3yr_pct", "alpha", "beta", "sharpe_ratio",
        "sortino_ratio", "std_dev_ann_pct", "max_drawdown_pct",
        "aum_crore", "expense_ratio_pct", "morningstar_rating", "risk_grade"
    ]
].copy()

transactions_fact = transactions[
    [
        "investor_id", "transaction_date", "amfi_code", "transaction_type",
        "amount_inr", "state", "city", "city_tier", "age_group",
        "gender", "annual_income_lakh", "payment_mode", "kyc_status"
    ]
].copy()

# =========================================================
# Create SQLite DB and execute schema.sql
# =========================================================
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
    schema_sql = f.read()

cursor.executescript(schema_sql)
conn.commit()

print("Schema executed successfully from sql/schema.sql")

# =========================================================
# Load data into SQLite tables
# =========================================================
fund_master.to_sql("dim_fund", conn, if_exists="append", index=False)
dim_date.to_sql("dim_date", conn, if_exists="append", index=False)
nav_fact.to_sql("fact_nav", conn, if_exists="append", index=False)
transactions_fact.to_sql("fact_transactions", conn, if_exists="append", index=False)
performance_fact.to_sql("fact_performance", conn, if_exists="append", index=False)
aum_fact.to_sql("fact_aum", conn, if_exists="append", index=False)

conn.commit()

print("All cleaned datasets loaded into SQLite successfully.")

# =========================================================
# Verify row counts
# =========================================================
tables = [
    "dim_fund",
    "dim_date",
    "fact_nav",
    "fact_transactions",
    "fact_performance",
    "fact_aum"
]

print("\nRow Counts in SQLite Database")
print("-" * 50)

for table in tables:
    count = pd.read_sql_query(f"SELECT COUNT(*) AS cnt FROM {table}", conn)["cnt"][0]
    print(f"{table}: {count}")

conn.close()

print("\nSQLite loading completed successfully.")
print(f"Database created at: {DB_PATH}")
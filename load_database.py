
import sqlite3
import pandas as pd
from pathlib import Path

csv_path = Path("data/processed/sales_analysis.csv")
db_path = Path("data/processed/retail.db")

if not csv_path.exists():
    raise FileNotFoundError(
        f"Missing cleaned dataset: {csv_path}"
    )

db_path.parent.mkdir(parents=True, exist_ok=True)

print("Loading cleaned sales data...")
df = pd.read_csv(
    csv_path,
    dtype={"InvoiceNo": "string", "StockCode": "string"},
    low_memory=False
)

# SQLite is built into Python; no separate database server needed.
with sqlite3.connect(db_path) as conn:
    df.to_sql("sales", conn, if_exists="replace", index=False)

    row_count = conn.execute(
        "SELECT COUNT(*) FROM sales"
    ).fetchone()[0]

    print("Rows loaded:", row_count)

    columns = conn.execute(
        "PRAGMA table_info(sales)"
    ).fetchall()

    print("\nDatabase columns:")
    for column in columns:
        print(f"- {column[1]} ({column[2]})")

print(f"\nDatabase created at: {db_path}")

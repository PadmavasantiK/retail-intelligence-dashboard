
import pandas as pd
from pathlib import Path

# File paths
RAW_FILE = Path("Online Retail.xlsx")
OUTPUT_DIR = Path("data/processed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 1. Load original dataset
df = pd.read_excel(RAW_FILE)

print("Original rows:", len(df))

# 2. Remove exact duplicate rows
duplicates = df.duplicated().sum()
df = df.drop_duplicates().copy()

print("Exact duplicates removed:", duplicates)
print("Rows after deduplication:", len(df))

# 3. Standardize text columns
for col in ["InvoiceNo", "StockCode", "Description", "Country"]:
    df[col] = df[col].astype("string").str.strip()

# Treat blank descriptions as missing
df["Description"] = df["Description"].replace("", pd.NA)

# 4. Ensure correct data types
df["InvoiceDate"] = pd.to_datetime(
    df["InvoiceDate"], errors="coerce"
)
df["Quantity"] = pd.to_numeric(
    df["Quantity"], errors="coerce"
)
df["UnitPrice"] = pd.to_numeric(
    df["UnitPrice"], errors="coerce"
)

# 5. Calculate line amount
df["LineRevenue"] = df["Quantity"] * df["UnitPrice"]

# 6. Identify cancellations, returns and invalid values
df["IsCancellation"] = (
    df["InvoiceNo"].str.startswith("C", na=False)
)

df["IsReturnOrNegativeQuantity"] = df["Quantity"] < 0
df["IsNonPositivePrice"] = df["UnitPrice"] <= 0

# Save cleaned records while retaining returns/cancellations
cleaned_file = OUTPUT_DIR / "transactions_cleaned.csv"
df.to_csv(cleaned_file, index=False)

# 7. Create a separate dataset for initial sales analysis
sales = df[
    (~df["IsCancellation"])
    & (df["Quantity"] > 0)
    & (df["UnitPrice"] > 0)
    & (df["InvoiceDate"].notna())
    & (df["InvoiceNo"].notna())
    & (df["StockCode"].notna())
    & (df["Description"].notna())
].copy()

sales_file = OUTPUT_DIR / "sales_analysis.csv"
sales.to_csv(sales_file, index=False)

# 8. Generate a quality report
report = {
    "original_rows": len(pd.read_excel(RAW_FILE)),
    "exact_duplicates_removed": int(duplicates),
    "cleaned_rows": len(df),
    "sales_analysis_rows": len(sales),
    "missing_customer_ids": int(df["CustomerID"].isna().sum()),
    "missing_descriptions": int(df["Description"].isna().sum()),
    "cancellation_rows": int(df["IsCancellation"].sum()),
    "negative_quantity_rows": int(
        df["IsReturnOrNegativeQuantity"].sum()
    ),
    "nonpositive_price_rows": int(
        df["IsNonPositivePrice"].sum()
    ),
}

print("\n========== CLEANING REPORT ==========")
for key, value in report.items():
    print(f"{key}: {value}")

print("\nSaved:", cleaned_file)
print("Saved:", sales_file)
print("\nData cleaning completed!")

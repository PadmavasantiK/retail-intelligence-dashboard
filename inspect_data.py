
import pandas as pd
from pathlib import Path

# Find the Excel file in the current folder
files = list(Path(".").glob("*.xlsx"))

if not files:
    raise FileNotFoundError(
        "No .xlsx file found in the retail folder."
    )

file_path = files[0]
print("Dataset:", file_path.name)

# Load the dataset
df = pd.read_excel(file_path)

# Inspect the data
print("\n--- Dataset Shape ---")
print(df.shape)

print("\n--- Column Names ---")
print(df.columns.tolist())

print("\n--- First 5 Rows ---")
print(df.head())

print("\n--- Data Types ---")
print(df.dtypes)

print("\n--- Missing Values ---")
print(df.isnull().sum())

print("\n--- Duplicate Rows ---")
print(df.duplicated().sum())

# Retail Intelligence Dashboard

An interactive retail sales analytics dashboard built using **Python, Pandas, SQL, Streamlit, and Plotly**. The project explores retail transaction data to identify sales trends, compare country-level performance, and analyze popular products and order activity.

## Project Overview

Retail businesses generate large volumes of transaction data. Analyzing this data can help identify revenue trends, understand customer purchasing activity, and recognize high-performing products and markets.

This project processes retail transaction data and presents key business metrics through an interactive dashboard with filters and visualizations.

## Features

- **Data Cleaning:** Handles duplicate records, missing values, cancelled transactions, and invalid quantities or prices.
- **Sales Analysis:** Examines sales performance, order activity, and average order value.
- **Country-Level Analysis:** Compares sales across countries.
- **Product Performance:** Identifies products with high sales and quantities sold.
- **Interactive Dashboard:** Provides KPI cards, filters, and interactive charts.
- **Data Exploration:** Allows users to inspect filtered data and download it as a CSV file.

## Tech Stack

- **Programming Language:** Python
- **Data Analysis:** Pandas
- **Database:** SQLite
- **SQL:** Aggregations, grouping, filtering, and business analysis
- **Dashboard:** Streamlit
- **Visualization:** Plotly

## Project Structure

```text
retail-intelligence-dashboard/
├── app.py
├── inspect_data.py
├── clean_data.py
├── load_database.py
├── requirements.txt
├── README.md
└── data/
    └── processed/
        ├── sales_sample.csv
        └── .gitkeep
```

## Dataset

The project uses the Online Retail dataset, which contains retail transaction records, including invoice numbers, product descriptions, quantities, invoice dates, unit prices, customer identifiers, and countries.

The full dataset and intermediate files are not included in this repository because of their size. A smaller sample of the processed sales data is provided for exploration.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/PadmavasantiK/retail-intelligence-dashboard.git
cd retail-intelligence-dashboard
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

Activate it on macOS or Linux:

```bash
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the dashboard

```bash
streamlit run app.py
```

The dashboard will open in your browser. Ensure that the application can locate the sample CSV or the full processed dataset before running it.

## Key Business Metrics

The dashboard is designed to explore:

- Total sales
- Number of orders
- Identified customers
- Average order value
- Monthly sales trends
- Country-wise sales performance
- Top-performing products
- Monthly order activity

## Data Processing Notes

- Duplicate and invalid transaction records are addressed during preprocessing.
- Sales analysis focuses on positive-sales transactions.
- Cancellation records, non-positive quantities, and non-positive prices are excluded from the sales analysis dataset.
- Consequently, the reported sales figures represent positive-sales activity rather than net revenue after returns.
- Customer-level metrics depend on the availability of customer identifiers.

## Future Improvements

- Deploy the dashboard so it can be accessed online.
- Add customer segmentation and repeat-purchase analysis.
- Introduce product-category and seasonal trend analysis.
- Add forecasting for future sales.
- Improve automated data ingestion and database integration.

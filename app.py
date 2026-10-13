
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# -----------------------------
# 1. Page configuration
# -----------------------------
st.set_page_config(
    page_title="Retail Intelligence",
    page_icon="🛍️",
    layout="wide"
)

# -----------------------------
# 2. Load cleaned sales data
# -----------------------------
DATA_PATH = Path(__file__).parent / "data" / "processed" / "sales_analysis.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)

    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"], errors="coerce"
    )

    df["LineRevenue"] = df["Quantity"] * df["UnitPrice"]
    df["Country"] = df["Country"].fillna("Unknown")
    df["Description"] = df["Description"].fillna("Unknown")

    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error(f"Could not find the dataset at: {DATA_PATH}")
    st.stop()

# -----------------------------
# 3. Dashboard title
# -----------------------------
st.title("🛍️ Retail Intelligence Dashboard")
st.caption("Sales performance, customer activity and product insights")

# -----------------------------
# 4. Sidebar filters
# -----------------------------
st.sidebar.header("Dashboard Filters")

countries = sorted(df["Country"].dropna().unique().tolist())

selected_countries = st.sidebar.multiselect(
    "Select countries",
    options=countries,
    default=["United Kingdom"] if "United Kingdom" in countries else countries
)

min_date = df["InvoiceDate"].min().date()
max_date = df["InvoiceDate"].max().date()

date_range = st.sidebar.date_input(
    "Select date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

filtered_df = df.copy()

if selected_countries:
    filtered_df = filtered_df[
        filtered_df["Country"].isin(selected_countries)
    ]
else:
    filtered_df = filtered_df.iloc[0:0]

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range

    filtered_df = filtered_df[
        filtered_df["InvoiceDate"].dt.date.between(
            start_date, end_date
        )
    ]

if filtered_df.empty:
    st.warning("No data matches the selected filters.")
    st.stop()

# -----------------------------
# 5. KPI calculations
# -----------------------------
total_sales = filtered_df["LineRevenue"].sum()
total_orders = filtered_df["InvoiceNo"].nunique()
identified_customers = filtered_df["CustomerID"].nunique()

order_values = filtered_df.groupby("InvoiceNo")["LineRevenue"].sum()
average_order_value = order_values.mean()

# -----------------------------
# 6. KPI cards
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", f"{total_sales:,.2f}")
col2.metric("Total Orders", f"{total_orders:,}")
col3.metric("Identified Customers", f"{identified_customers:,}")
col4.metric("Average Order Value", f"{average_order_value:,.2f}")

st.divider()

# -----------------------------
# 7. Monthly sales trend
# -----------------------------
st.subheader("Monthly Sales Trend")

monthly_df = filtered_df.copy()
monthly_df["Sales Month"] = (
    monthly_df["InvoiceDate"].dt.to_period("M").astype(str)
)

monthly_sales = (
    monthly_df.groupby("Sales Month", as_index=False)
    .agg(
        Sales=("LineRevenue", "sum"),
        Orders=("InvoiceNo", "nunique")
    )
)

fig_monthly = px.line(
    monthly_sales,
    x="Sales Month",
    y="Sales",
    markers=True,
    title="Sales Value by Month",
    hover_data=["Orders"]
)

fig_monthly.update_layout(
    xaxis_title="Month",
    yaxis_title="Sales Value",
    hovermode="x unified"
)

st.plotly_chart(fig_monthly, use_container_width=True)

# -----------------------------
# 8. Country performance
# -----------------------------
st.subheader("Sales by Country")

country_sales = (
    filtered_df.groupby("Country", as_index=False)
    .agg(
        Sales=("LineRevenue", "sum"),
        Orders=("InvoiceNo", "nunique")
    )
    .sort_values("Sales", ascending=False)
    .head(10)
)

fig_country = px.bar(
    country_sales.sort_values("Sales"),
    x="Sales",
    y="Country",
    orientation="h",
    title="Top 10 Countries by Sales",
    hover_data=["Orders"]
)

st.plotly_chart(fig_country, use_container_width=True)

# -----------------------------
# 9. Top products
# -----------------------------
st.subheader("Top 10 Products by Sales")

product_sales = (
    filtered_df.groupby("Description", as_index=False)
    .agg(
        Sales=("LineRevenue", "sum"),
        Units_Sold=("Quantity", "sum")
    )
    .sort_values("Sales", ascending=False)
    .head(10)
)

fig_products = px.bar(
    product_sales.sort_values("Sales"),
    x="Sales",
    y="Description",
    orientation="h",
    title="Highest Revenue Products",
    hover_data=["Units_Sold"]
)

st.plotly_chart(fig_products, use_container_width=True)

# -----------------------------
# 10. Monthly order activity
# -----------------------------
st.subheader("Monthly Order Activity")

fig_orders = px.bar(
    monthly_sales,
    x="Sales Month",
    y="Orders",
    title="Number of Orders by Month"
)

st.plotly_chart(fig_orders, use_container_width=True)

# -----------------------------
# 11. Data preview and download
# -----------------------------
with st.expander("Explore filtered sales data"):
    st.dataframe(filtered_df.head(500), use_container_width=True)

csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download filtered data as CSV",
    data=csv_data,
    file_name="retail_filtered_data.csv",
    mime="text/csv"
)

st.caption(
    "Note: Sales are calculated from the filtered positive-sales dataset. "
    "Returns and cancellations are not included in these KPIs."
)

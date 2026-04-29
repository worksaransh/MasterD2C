import pandas as pd
import streamlit as st

from d2c_ingestion.pipeline import process_upload

st.set_page_config(page_title="D2C Analytics Dashboard", layout="wide")
st.title("D2C Analytics Dashboard")

uploaded_file = st.file_uploader("Upload Shopify or Meta Ads export", type=["csv", "xlsx"])
template_key = st.selectbox("Template", ["shopify", "meta_ads"])

if uploaded_file:
    temp_path = f"/tmp/{uploaded_file.name}"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    result = process_upload(temp_path, template_key)

    if result["errors"]:
        for err in result["errors"]:
            st.warning(err)

    data = pd.DataFrame(result["standardized_records"])
    if data.empty:
        st.error("No standardized mapped data available. Please complete mapping first.")
        st.stop()

    for col in ["REVENUE", "SPEND"]:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")

    if "ORDER_DATE" in data.columns:
        data["ORDER_DATE"] = pd.to_datetime(data["ORDER_DATE"], errors="coerce")

    st.sidebar.header("Filters")
    if "ORDER_DATE" in data.columns and data["ORDER_DATE"].notna().any():
        min_date = data["ORDER_DATE"].min().date()
        max_date = data["ORDER_DATE"].max().date()
        date_range = st.sidebar.date_input("Date", (min_date, max_date), min_value=min_date, max_value=max_date)
        if len(date_range) == 2:
            start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
            data = data[(data["ORDER_DATE"] >= start_date) & (data["ORDER_DATE"] <= end_date)]

    def apply_select_filter(df: pd.DataFrame, col: str, label: str) -> pd.DataFrame:
        if col not in df.columns:
            return df
        options = sorted(df[col].dropna().astype(str).unique().tolist())
        selected = st.sidebar.multiselect(label, options)
        if selected:
            return df[df[col].astype(str).isin(selected)]
        return df

    data = apply_select_filter(data, "SKU", "Product")
    data = apply_select_filter(data, "CAMPAIGN_NAME", "Campaign")
    data = apply_select_filter(data, "CITY", "City")
    data = apply_select_filter(data, "PINCODE", "Pincode")

    revenue = float(data["REVENUE"].sum()) if "REVENUE" in data.columns else 0.0
    spend = float(data["SPEND"].sum()) if "SPEND" in data.columns else 0.0
    roas = (revenue / spend) if spend else 0.0

    c1, c2, c3 = st.columns(3)
    c1.metric("Revenue", f"{revenue:,.2f}")
    c2.metric("Spend", f"{spend:,.2f}")
    c3.metric("ROAS", f"{roas:,.2f}")

    st.subheader("Product-wise Performance")
    if "SKU" in data.columns:
        product_perf = data.groupby("SKU", dropna=False).agg({"REVENUE": "sum", "SPEND": "sum"}).reset_index()
        product_perf["ROAS"] = product_perf.apply(lambda r: (r["REVENUE"] / r["SPEND"]) if r["SPEND"] else 0, axis=1)
        st.dataframe(product_perf.sort_values("REVENUE", ascending=False))

    st.subheader("City-wise Performance")
    if "CITY" in data.columns:
        city_perf = data.groupby("CITY", dropna=False).agg({"REVENUE": "sum", "SPEND": "sum"}).reset_index()
        city_perf["ROAS"] = city_perf.apply(lambda r: (r["REVENUE"] / r["SPEND"]) if r["SPEND"] else 0, axis=1)
        st.dataframe(city_perf.sort_values("REVENUE", ascending=False))

    st.subheader("Pincode-wise Performance")
    if "PINCODE" in data.columns:
        pin_perf = data.groupby("PINCODE", dropna=False).agg({"REVENUE": "sum", "SPEND": "sum"}).reset_index()
        pin_perf["ROAS"] = pin_perf.apply(lambda r: (r["REVENUE"] / r["SPEND"]) if r["SPEND"] else 0, axis=1)
        st.dataframe(pin_perf.sort_values("REVENUE", ascending=False))

    st.subheader("Filtered Data Preview")
    st.dataframe(data.head(200))

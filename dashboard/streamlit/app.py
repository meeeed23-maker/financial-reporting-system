import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Financial Dashboard", layout="wide")
st.title("💰 Financial Performance Dashboard")
st.markdown("**Automated Reporting & Anomaly Detection — Superstore Data**")

df = pd.read_csv("data/processed/financial_data_scored.csv")

# Filtres
months = sorted(df['month'].unique())
selected_month = st.sidebar.selectbox("📅 Select Month", months, index=len(months)-1)
depts = st.sidebar.multiselect("🏢 Departments", df['department'].unique(), default=df['department'].unique())

filtered = df[(df['month'] == selected_month) & (df['department'].isin(depts))]

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Budget", f"${filtered['budget'].sum():,.0f}")
col2.metric("Total Actual", f"${filtered['actual'].sum():,.0f}")
col3.metric("Variance", f"${(filtered['actual'] - filtered['budget']).sum():,.0f}")
anomalies = (filtered['anomaly_label'] == 'Anomaly').sum()
col4.metric("🚨 Anomalies", anomalies)

# Graphique
fig = px.bar(filtered, x='department', y='variance_pct',
             color='anomaly_label',
             color_discrete_map={'Normal': '#2ecc71', 'Anomaly': '#e74c3c'},
             title=f"Variance % by Department — {selected_month}")
st.plotly_chart(fig, use_container_width=True)

# Tableau
st.subheader("📋 Detailed Data")
st.dataframe(filtered[['month', 'department', 'budget', 'actual', 'variance', 'variance_pct', 'anomaly_label']],
             use_container_width=True)
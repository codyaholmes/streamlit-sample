import streamlit as st
from data.taxi_trips import load_trips

st.title("Taxi Insights")


# Load taxi trip data
df = load_trips()
df.columns = [col.title().replace("_", " ") for col in df.columns]

metrics, raw_data = st.tabs(["Metrics", "Raw Data"])

# Metric Calculations
total_passengers = df["Passengers"].sum()
total_fare = df["Fare"].sum()
total_distance = df["Distance"].sum()
total_tips = df["Tip"].sum()

with metrics:

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Passengers", f"{total_passengers:,.0f}", border=True)
    with col2:
        st.metric("Total Fares", f"${total_fare:,.0f}", border=True)

with raw_data:
    st.dataframe(
        df,
    )

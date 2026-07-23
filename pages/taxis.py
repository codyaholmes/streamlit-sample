import streamlit as st
from data.taxi_trips import load_trips


st.title("Taxi Insights")


# Load taxi trip data
df = load_trips()
df.columns = [col.title().replace("_", " ") for col in df.columns]

metrics, raw_data = st.tabs(["Metrics", "Raw Data"])

with metrics:
    st.text("Metrics go here")

with raw_data:
    st.dataframe(df, hide_index=True)
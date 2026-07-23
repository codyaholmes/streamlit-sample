import streamlit as st
import seaborn as sns

@st.cache_data
def load_trips():
    df = sns.load_dataset("taxis")
    return df
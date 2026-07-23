import streamlit as st
import random

st.title("Executive Summary")
st.markdown("""
This page presents summary-level metrics for executives. It was commissioned by the CEO who said:
> "If we don't have metrics, we don't have s***. So somebody better go out and there and build me something or there is going to be hell to pay!"
""")
st.text("And this is why this report exists...")
st.space("xsmall")


# Initialize the metric values
if "revenue" not in st.session_state:
    st.session_state.revenue = 1_234_567
if "orders" not in st.session_state:
    st.session_state.orders = 98_765


col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="Total Revenue",
        value=f"${st.session_state.revenue:,.0f}",
        delta=f"{0.459:.1%}",
        help="The total amount of revenue.",
        border=True
    )
    if st.button("Generate Revenue", type="secondary"):
        st.session_state.revenue = random.randint(500_000, 2_500_000)
        st.rerun()

with col2:
    st.metric(
        label="Total Orders",
        value=f"{st.session_state.orders:,.0f}",
        delta=f"{0.393:.1%}",
        help="The total amount of orders created.",
        border=True
    )
    if st.button("Generate Orders", type="secondary"):
        st.session_state.orders = random.randint(10_000, 180_000)
        st.rerun()


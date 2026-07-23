import streamlit as st

home = st.Page("pages/home.py", title="Home", icon=":material/home:", default=True)
info = st.Page("pages/info.py", title="Info", icon=":material/book:")
exec_summ = st.Page("pages/exec_summary.py", title="Executive Summary", icon=":material/summarize:")
taxis = st.Page("pages/taxis.py", title="Taxi Insights", icon=":material/car_crash:")

pages = {
    "Main": [home, exec_summ, taxis],
    "About": [info]
}

pg = st.navigation(pages=pages, expanded=True)
pg.run()
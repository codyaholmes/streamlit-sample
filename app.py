import streamlit as st

home = st.Page("pages/home.py", title="Home", icon=":material/home:", default=True)
info = st.Page("pages/info.py", title="Info", icon=":material/book:")

pages = {
    "Main": [home],
    "About": [info]
}

pg = st.navigation(pages=pages, expanded=True)
pg.run()
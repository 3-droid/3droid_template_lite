import streamlit as st
from st_bridge import bridge, html
import streamlit.components.v1 as components
from utils.helpers import load_style, load_landing_page, load_footer

st.set_page_config(layout="wide", page_icon="./static/logo.png")


html(f"""
{load_landing_page()}
{load_footer()}
{load_style()}
""")
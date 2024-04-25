from pathlib import Path
import streamlit as st

st.set_page_config(
    page_title="VIS Workshop 2024 RAG", page_icon="ipt_logo.png", layout="wide"
)

st.markdown(Path("README.md").read_text())

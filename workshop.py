import streamlit as st
from st_pages import Page, add_page_title, show_pages

st.set_page_config(
    page_title="VIS Workshop 2024 RAG",
    page_icon="ipt_logo.png",
)

st.sidebar.success("Select a task below.")

add_page_title()
show_pages([
    Page("pages/home.py", "VIS Workshop 2024 RAG", ':house:'),
    Page("pages/task1.py", "Task 1: Prompt Engineering", ":gear:"),
    Page("pages/task2.py", "Task 2: Retrieval Augmented Generation", ":brain:"),
    Page("pages/bonus.py", "Bonus: Challenge", ":flying_saucer:"),
])


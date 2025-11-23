import streamlit as st
from utils.api_client import ask_backend
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "db", "history.db")

st.set_page_config(page_title="Agentic Research Assistant", layout="wide")
st.title("🤖 Agentic Research Assistant")

query = st.text_input("Ask your research question:")

if st.button("Run Research"):
    if query.strip():
        with st.spinner("Thinking..."):
            response = ask_backend(query)
        st.markdown(response)
    else:
        st.warning("Please enter a question.")

# Sidebar: Show recent history
st.sidebar.header("Recent Queries")
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
rows = c.execute("SELECT query, timestamp FROM history ORDER BY id DESC LIMIT 5")

for q, ts in rows:
    st.sidebar.write(f"**{q}** — {ts}")

conn.close()

import streamlit as st
from utils.api_client import ask_backend
import sqlite3
import os
import time

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "db", "history.db")

st.set_page_config(page_title="Agentic Research Assistant", layout="wide", page_icon="🤖")

# Custom CSS for better UX
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
    }
    .status-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .success {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .info {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
    }
    .stSpinner > div {
        border-top-color: #FF4B4B !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🤖 Agentic Research Assistant</div>', unsafe_allow_html=True)

# Add helpful description
st.markdown("""
Welcome to the **Agentic Research Assistant**! Ask any research question and our multi-agent system will:
- 🔍 Search for relevant information
- 📊 Analyze and extract key claims
- ✍️ Generate a comprehensive report
""")

st.markdown("---")

# Main query input
query = st.text_area(
    "Enter your research question:",
    placeholder="E.g., What are the latest developments in agentic AI systems?",
    height=100
)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    run_button = st.button("🚀 Run Research", use_container_width=True, type="primary")

if run_button:
    if query.strip():
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Step 1: Validate query
        status_text.markdown('<div class="status-box info">🔄 Validating query...</div>', unsafe_allow_html=True)
        progress_bar.progress(10)
        time.sleep(0.3)
        
        # Step 2: Research phase
        status_text.markdown('<div class="status-box info">🔍 Researching sources...</div>', unsafe_allow_html=True)
        progress_bar.progress(30)
        
        # Step 3: Analysis phase
        status_text.markdown('<div class="status-box info">📊 Analyzing information...</div>', unsafe_allow_html=True)
        progress_bar.progress(60)
        
        # Step 4: Writing phase
        status_text.markdown('<div class="status-box info">✍️ Generating report...</div>', unsafe_allow_html=True)
        progress_bar.progress(80)
        
        try:
            # Make API call
            response = ask_backend(query)
            
            # Complete
            progress_bar.progress(100)
            status_text.markdown('<div class="status-box success">✅ Research completed!</div>', unsafe_allow_html=True)
            time.sleep(0.5)
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
            
            # Display results
            st.markdown("## 📋 Research Results")
            st.markdown(response)
            
            # Download option
            st.download_button(
                label="📥 Download Report",
                data=response,
                file_name=f"research_report_{int(time.time())}.md",
                mime="text/markdown"
            )
            
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"❌ Error: {str(e)}")
            st.info("Please try again or check if the backend server is running.")
    else:
        st.warning("⚠️ Please enter a research question.")

st.markdown("---")

# Sidebar: Recent history with better formatting
st.sidebar.header("📚 Recent Queries")

try:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT query, timestamp FROM history ORDER BY id DESC LIMIT 5")
    rows = c.fetchall()
    conn.close()
    
    if rows:
        for idx, (q, ts) in enumerate(rows, 1):
            with st.sidebar.expander(f"#{idx}: {q[:50]}..."):
                st.write(f"**Query:** {q}")
                st.write(f"**Time:** {ts}")
    else:
        st.sidebar.info("No queries yet. Start by asking a question!")
        
except Exception as e:
    st.sidebar.error(f"Unable to load history: {str(e)}")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("""
**System Status:**  
✅ Backend: Running  
✅ Database: Connected  
✅ Agents: Ready  

Built with ❤️ for INFO 7375
""")
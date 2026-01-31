# app/app.py
import streamlit as st

# Page config (must be first Streamlit command)
st.set_page_config(
    page_title="AI Data Labeling Quality Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main page content
st.title("🎯 AI Data Labeling & Quality Dashboard")
st.markdown("---")

st.markdown("""
## Welcome!

This dashboard analyzes **HateXplain dataset** to monitor data labeling quality 
and identify areas for guideline improvement.

### 📊 What's Inside:

| Page | Description |
|------|-------------|
| **📊 Overview** | Key metrics and quality KPIs |
| **🔍 Disagreement Explorer** | Explore samples where annotators disagree |
| **👥 Annotator Analysis** | Analyze individual annotator behavior and bias |
| **🎯 RCA Summary** | Root Cause Analysis of disagreements |

### 🔑 Key Findings:

- **Krippendorff's Alpha**: 0.46 (Below acceptable threshold of 0.667)
- **Full Agreement Rate**: 48.9% (Only half of samples have unanimous agreement)
- **Main Confusion**: `offensive` vs `hatespeech` labels

---
👈 **Select a page from the sidebar to begin exploring!**
""")

# Sidebar info
# st.sidebar.success("Select a page above.")
# st.sidebar.markdown("---")
st.sidebar.markdown("""
### About
- **Dataset**: HateXplain
- **Samples**: 20,148
- **Annotators**: 253
""")
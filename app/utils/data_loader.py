import pandas as pd
import streamlit as st
from pathlib import Path

@st.cache_data
def load_posts():
    """Load posts analysis data"""
    path = Path(__file__).parent.parent.parent / "data" / "posts_analysis.csv"
    return pd.read_csv(path)

@st.cache_data
def load_annotators():
    """Load annotators analysis data"""
    path = Path(__file__).parent.parent.parent / "data" / "annotators_analysis.csv"
    return pd.read_csv(path)

@st.cache_data
def load_summary():
    """Load summary metrics data"""
    path = Path(__file__).parent.parent.parent / "data" / "summary_metrics.csv"
    df = pd.read_csv(path)
    # Convert to dictionary for easy access
    return dict(zip(df['metric'], df['value']))

@st.cache_data
def load_disagreements():
    """Load disagreement samples data"""
    path = Path(__file__).parent.parent.parent / "data" / "disagreement_samples.csv"
    return pd.read_csv(path)
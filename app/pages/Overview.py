# app/pages/1_📊_Overview.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from utils.data_loader import load_posts, load_summary, load_annotators

# Page config
st.set_page_config(page_title="Overview", page_icon="📊", layout="wide")

st.title("📊 Overview: Quality Metrics Dashboard")
st.markdown("---")

# Load data
posts = load_posts()
summary = load_summary()
annotators = load_annotators()

# ===================
# ROW 1: Key KPIs
# ===================
st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Samples",
        value=f"{int(summary['total_posts']):,}"
    )

with col2:
    alpha = float(summary['krippendorff_alpha'])
    st.metric(
        label="Krippendorff's Alpha",
        value=f"{alpha:.3f}",
        delta="Below threshold",
        delta_color="inverse"
    )

with col3:
    st.metric(
        label="Full Agreement Rate",
        value=f"{summary['full_agreement_rate']}%"
    )

with col4:
    st.metric(
        label="Total Annotators",
        value=f"{int(summary['total_annotators'])}"
    )

st.markdown("---")

# ===================
# ROW 2: Agreement & Label Distribution
# ===================
st.subheader("Distribution Analysis")

col1, col2 = st.columns(2)

with col1:
    # Agreement Type Distribution
    agreement_data = posts['agreement_type'].value_counts().reset_index()
    agreement_data.columns = ['Agreement Type', 'Count']
    
    fig1 = px.pie(
        agreement_data, 
        values='Count', 
        names='Agreement Type',
        title='Annotator Agreement Distribution',
        color='Agreement Type',
        color_discrete_map={'Full': '#2ecc71', 'Partial': '#f39c12', 'None': '#e74c3c'}
    )
    fig1.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # Majority Label Distribution
    label_data = posts['majority_label'].value_counts().reset_index()
    label_data.columns = ['Label', 'Count']
    
    fig2 = px.pie(
        label_data, 
        values='Count', 
        names='Label',
        title='Majority Label Distribution',
        color='Label',
        color_discrete_map={'normal': '#3498db', 'hatespeech': '#e74c3c', 'offensive': '#f39c12'}
    )
    fig2.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig2, use_container_width=True)

# Analysis note
st.info("""
**What I found interesting:** Only about half of samples (48.9%) have full agreement among all 3 annotators. 
This is lower than expected for a hate speech dataset. The main issue seems to be distinguishing 
between 'offensive' and 'hatespeech' - both make up roughly 30% each, which suggests annotators 
are often split between these two categories.
""")

st.markdown("---")

# ===================
# ROW 3: Alpha Scale Visualization
# ===================
st.subheader("Krippendorff's Alpha: Quality Assessment")

# Create gauge chart for Alpha
fig3 = go.Figure(go.Indicator(
    mode="gauge+number+delta",
    value=alpha,
    domain={'x': [0, 1], 'y': [0, 1]},
    title={'text': "Inter-Annotator Agreement", 'font': {'size': 20}},
    delta={'reference': 0.667, 'increasing': {'color': "green"}, 'decreasing': {'color': "red"}},
    gauge={
        'axis': {'range': [0, 1], 'tickwidth': 1, 'tickcolor': "darkblue"},
        'bar': {'color': "#3498db"},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",
        'steps': [
            {'range': [0, 0.667], 'color': '#ffcccc'},
            {'range': [0.667, 0.8], 'color': '#fff3cd'},
            {'range': [0.8, 1], 'color': '#d4edda'}
        ],
        'threshold': {
            'line': {'color': "red", 'width': 4},
            'thickness': 0.75,
            'value': 0.667
        }
    }
))

fig3.update_layout(height=300)
st.plotly_chart(fig3, use_container_width=True)

# Interpretation - more conversational
col1, col2, col3 = st.columns(3)
with col1:
    st.error("**< 0.667**: Poor")
with col2:
    st.warning("**0.667 - 0.8**: Acceptable")
with col3:
    st.success("**≥ 0.8**: Reliable")

st.markdown("""
Our alpha of **0.46** falls in the 'Poor' range. According to Krippendorff's guidelines (2004), 
this means the data isn't reliable enough for drawing strong conclusions. However, this is 
actually common for subjective tasks like hate speech detection - the boundary between 
'offensive' and 'hatespeech' is genuinely ambiguous in many cases.
""")

st.markdown("---")

# ===================
# ROW 4: Annotator Bias Distribution
# ===================
st.subheader("Annotator Bias Overview")

col1, col2 = st.columns(2)

with col1:
    # Bias category distribution
    bias_data = annotators['bias_category'].value_counts().reset_index()
    bias_data.columns = ['Bias Category', 'Count']
    
    fig4 = px.bar(
        bias_data,
        x='Bias Category',
        y='Count',
        title='Annotator Bias Distribution',
        color='Bias Category',
        color_discrete_map={
            'Lenient (soft)': '#2ecc71',
            'Balanced': '#3498db',
            'Strict (harsh)': '#e74c3c'
        }
    )
    st.plotly_chart(fig4, use_container_width=True)

with col2:
    st.markdown("### Bias Summary")
    st.markdown(f"""
    | Category | Percentage |
    |----------|------------|
    | Lenient (soft) | {summary['lenient_annotators_pct']}% |
    | Balanced | {summary['balanced_annotators_pct']}% |
    | Strict (harsh) | {summary['strict_annotators_pct']}% |
    """)
    
    st.markdown("""
    There's a noticeable skew toward lenient annotators - about 43% tend to label content as 'normal' 
    more often than average. This could be a problem if we're trying to catch harmful content, 
    since these annotators might be missing some borderline cases.
    
    On the flip side, only 18% are strict. So the dataset as a whole probably under-labels hate speech 
    rather than over-labels it.
    """)

st.markdown("---")

# ===================
# ROW 5: Quick Stats Table
# ===================
st.subheader("All Metrics Summary")

metrics_df = pd.DataFrame([
    {"Metric": "Total Posts", "Value": f"{int(summary['total_posts']):,}"},
    {"Metric": "Total Annotations", "Value": f"{int(summary['total_annotations']):,}"},
    {"Metric": "Krippendorff's Alpha", "Value": f"{summary['krippendorff_alpha']}"},
    {"Metric": "Full Agreement Rate", "Value": f"{summary['full_agreement_rate']}%"},
    {"Metric": "Partial Agreement Rate", "Value": f"{summary['partial_agreement_rate']}%"},
    {"Metric": "No Agreement Rate", "Value": f"{summary['no_agreement_rate']}%"},
    {"Metric": "Samples with Rationales", "Value": f"{summary['samples_with_rationales_pct']}%"},
    {"Metric": "Top RCA Category", "Value": summary['top_rca_category']},
])

st.dataframe(metrics_df, use_container_width=True, hide_index=True)
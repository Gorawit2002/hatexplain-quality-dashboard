# app/pages/3_👥_Annotator_Analysis.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from utils.data_loader import load_annotators, load_summary

# Page config
st.set_page_config(page_title="Annotator Analysis", page_icon="👥", layout="wide")

st.title("👥 Annotator Analysis")
st.markdown("Analyze individual annotator behavior, bias patterns, and quality metrics")
st.markdown("---")

# Load data
annotators = load_annotators()
summary = load_summary()

# ===================
# ROW 1: Summary Stats
# ===================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Annotators (100+ labels)", f"{len(annotators)}")
with col2:
    st.metric("Mean Agreement Rate", f"{summary['annotator_mean_agreement']}%")
with col3:
    st.metric("Strict Annotators", f"{summary['strict_annotators_pct']}%")
with col4:
    st.metric("Lenient Annotators", f"{summary['lenient_annotators_pct']}%")

st.markdown("---")

# ===================
# ROW 2: Bias Distribution
# ===================
st.subheader("Annotator Bias Distribution")

col1, col2 = st.columns(2)

with col1:
    # Pie chart of bias categories
    bias_counts = annotators['bias_category'].value_counts().reset_index()
    bias_counts.columns = ['Bias Category', 'Count']
    
    fig1 = px.pie(
        bias_counts,
        values='Count',
        names='Bias Category',
        title='Bias Category Distribution',
        color='Bias Category',
        color_discrete_map={
            'Lenient (soft)': '#2ecc71',
            'Balanced': '#3498db',
            'Strict (harsh)': '#e74c3c'
        }
    )
    fig1.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("""
    ### How I defined bias categories
    
    I calculated a **strictness score** for each annotator:
    
    `Strictness = % hatespeech labels - % normal labels`
    
    - **Strict (score > 20)**: Labels 'hatespeech' much more than 'normal'
    - **Lenient (score < -20)**: Labels 'normal' much more than 'hatespeech'  
    - **Balanced (between -20 and 20)**: Relatively even distribution
    
    The threshold of ±20 is somewhat arbitrary - I chose it because it captures 
    annotators who are clearly skewed in one direction.
    """)

st.markdown("---")

# ===================
# ROW 3: Scatter Plot - Strictness vs Agreement
# ===================
st.subheader("Strictness vs Agreement Rate")

fig2 = px.scatter(
    annotators,
    x='strictness_score',
    y='agreement_rate',
    size='total_labels',
    color='bias_category',
    hover_data=['annotator_id', 'total_labels', 'hatespeech_pct', 'normal_pct'],
    title='Annotator Behavior Map',
    labels={
        'strictness_score': 'Strictness Score (- Lenient, + Strict)',
        'agreement_rate': 'Agreement Rate with Majority',
        'bias_category': 'Bias Category'
    },
    color_discrete_map={
        'Lenient (soft)': '#2ecc71',
        'Balanced': '#3498db',
        'Strict (harsh)': '#e74c3c'
    }
)

# Add reference lines
fig2.add_hline(y=annotators['agreement_rate'].mean(), line_dash="dash", 
               line_color="gray", annotation_text="Mean Agreement")
fig2.add_vline(x=0, line_dash="dash", line_color="gray")

fig2.update_layout(height=500)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("""
**How to read this chart:**

The ideal annotators are at the **top** (high agreement with majority), regardless of whether 
they're strict or lenient. The concerning ones are at the **bottom** - these annotators 
frequently disagree with their peers.

Notice that most low-agreement annotators are on the **left side** (lenient). This suggests 
that being too lenient correlates with lower quality more than being too strict. 
Maybe it's easier to spot obvious hate speech than to correctly identify borderline 'normal' content?
""")

st.markdown("---")

# ===================
# ROW 4: Agreement Rate Distribution
# ===================
st.subheader("Agreement Rate Distribution")

fig3 = px.histogram(
    annotators,
    x='agreement_rate',
    nbins=20,
    title='Distribution of Annotator Agreement Rates',
    labels={'agreement_rate': 'Agreement Rate', 'count': 'Number of Annotators'},
    color_discrete_sequence=['#3498db']
)
fig3.add_vline(x=annotators['agreement_rate'].mean(), line_dash="dash", 
               line_color="red", annotation_text=f"Mean: {annotators['agreement_rate'].mean():.1%}")
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# ===================
# ROW 5: Top/Bottom Annotators
# ===================
st.subheader("Annotator Leaderboard")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Top 10 by Agreement Rate")
    top_annotators = annotators.nlargest(10, 'agreement_rate')[
        ['annotator_id', 'total_labels', 'agreement_rate', 'bias_category']
    ].copy()
    top_annotators['agreement_rate'] = top_annotators['agreement_rate'].apply(lambda x: f"{x:.1%}")
    st.dataframe(top_annotators, use_container_width=True, hide_index=True)

with col2:
    st.markdown("### Bottom 10 by Agreement Rate")
    bottom_annotators = annotators.nsmallest(10, 'agreement_rate')[
        ['annotator_id', 'total_labels', 'agreement_rate', 'bias_category']
    ].copy()
    bottom_annotators['agreement_rate'] = bottom_annotators['agreement_rate'].apply(lambda x: f"{x:.1%}")
    st.dataframe(bottom_annotators, use_container_width=True, hide_index=True)

st.markdown("""
Looking at the bottom 10, most have the 'Lenient' bias. These annotators might benefit from 
reviewing the guidelines again, especially around what counts as 'offensive' vs 'normal'.
""")

st.markdown("---")

# ===================
# ROW 6: Individual Annotator Deep Dive
# ===================
st.subheader("Individual Annotator Deep Dive")

# Select annotator
selected_id = st.selectbox(
    "Select Annotator ID",
    options=annotators['annotator_id'].tolist(),
    index=0
)

if selected_id:
    ann = annotators[annotators['annotator_id'] == selected_id].iloc[0]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Labels", f"{int(ann['total_labels']):,}")
        st.metric("Agreement Rate", f"{ann['agreement_rate']:.1%}")
    
    with col2:
        st.metric("Strictness Score", f"{ann['strictness_score']:.1f}")
        st.metric("Bias Category", ann['bias_category'])
    
    with col3:
        # Mini pie chart for label distribution
        fig4 = go.Figure(data=[go.Pie(
            labels=['Normal', 'Offensive', 'Hatespeech'],
            values=[ann['normal_pct'], ann['offensive_pct'], ann['hatespeech_pct']],
            hole=0.4,
            marker_colors=['#3498db', '#f39c12', '#e74c3c']
        )])
        fig4.update_layout(
            title=f"Label Distribution",
            height=250,
            margin=dict(t=50, b=0, l=0, r=0)
        )
        st.plotly_chart(fig4, use_container_width=True)
    
    # Interpretation - more natural language
    if ann['bias_category'] == 'Strict (harsh)':
        st.warning(f"""
        This annotator labels **{ann['hatespeech_pct']:.1f}%** as hatespeech - higher than average.
        Worth checking if they're catching things others miss, or if they're being overly aggressive.
        """)
    elif ann['bias_category'] == 'Lenient (soft)':
        st.warning(f"""
        This annotator labels **{ann['normal_pct']:.1f}%** as normal - higher than average.
        They might be missing some borderline harmful content.
        """)
    else:
        st.success(f"This annotator has a fairly balanced distribution across all three labels.")
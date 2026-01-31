# app/pages/4_🎯_RCA_Summary.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from utils.data_loader import load_disagreements, load_summary

# Page config
st.set_page_config(page_title="RCA Summary", page_icon="🎯", layout="wide")

st.title("🎯 Root Cause Analysis (RCA) Summary")
st.markdown("Understanding why annotators disagree")
st.markdown("---")

# Load data
disagreements = load_disagreements()
summary = load_summary()

# ===================
# ROW 1: RCA Overview
# ===================
st.subheader("RCA Category Overview")

# Calculate RCA stats
rca_counts = disagreements['rca_category'].value_counts().reset_index()
rca_counts.columns = ['RCA Category', 'Count']
rca_counts['Percentage'] = (rca_counts['Count'] / rca_counts['Count'].sum() * 100).round(1)

col1, col2 = st.columns([2, 1])

with col1:
    # Bar chart
    fig1 = px.bar(
        rca_counts,
        x='Count',
        y='RCA Category',
        orientation='h',
        title='Disagreement Samples by RCA Category',
        color='Count',
        color_continuous_scale='Reds',
        text='Count'
    )
    fig1.update_layout(yaxis={'categoryorder': 'total ascending'}, height=400)
    fig1.update_traces(textposition='outside')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("### Category Breakdown")
    st.dataframe(
        rca_counts,
        use_container_width=True,
        hide_index=True,
        column_config={
            "RCA Category": st.column_config.TextColumn("Category"),
            "Count": st.column_config.NumberColumn("Count", format="%d"),
            "Percentage": st.column_config.NumberColumn("Percentage", format="%.1f%%")
        }
    )

st.markdown("---")

# ===================
# ROW 2: Main Findings (more conversational)
# ===================
st.subheader("What's causing the disagreements?")

st.markdown("""
After looking at thousands of disagreement cases, a few patterns stand out:

**1. The 'Other/Unclear' problem (57%)**

More than half of disagreements don't fit neatly into any category. This isn't surprising - 
hate speech is genuinely ambiguous. A lot of these are cases where context matters a lot, 
or where the post is using sarcasm/irony that some annotators catch and others don't.

**2. Group references without clear hate (6.4%)**

Words like "white", "black", "immigrants" appear a lot in disagreements. The issue is that 
these words aren't inherently hateful - it depends entirely on context. "White people" in 
"I love white people's cooking" vs "White people are ruining everything" are completely different.

**3. The offensive vs hatespeech line (multiple categories)**

This is really the core problem. Across Racial Slurs, Gender/Sexuality, and Religious Terms 
categories, the disagreement is usually between "offensive" and "hatespeech" - not between 
"normal" and the others. Annotators seem to agree something is wrong, but not *how* wrong.
""")

st.markdown("---")

# ===================
# ROW 3: Specific Category Analysis
# ===================
st.subheader("Category Deep Dive")

# Only show the most important categories with real insights
tab1, tab2, tab3 = st.tabs(["Group References", "Slurs & Identity", "Profanity"])

with tab1:
    st.markdown("""
    ### Group References (663 samples)
    
    **The problem:** Mentioning a demographic group isn't hate by itself.
    
    **Examples from the data:**
    - "white people be like..." - Is this stereotyping or just casual observation?
    - "immigrants are..." - Depends entirely on what comes next
    
    **My suggestion:** Create a rule that group mention alone = normal. 
    Only escalate if there's a negative generalization or threat attached.
    """)

with tab2:
    st.markdown("""
    ### Slurs & Identity Terms (Racial, Gender, Religious combined ~25%)
    
    **The problem:** Even obvious slurs cause disagreement between offensive/hatespeech.
    
    **What I noticed:** When slurs are directed at a specific group with intent to demean, 
    it's almost always hatespeech. But slurs used casually (like in rap lyrics or 
    reclaimed usage) are harder to categorize.
    
    **My suggestion:** Default to hatespeech for slurs targeting protected groups, 
    unless there's clear evidence of reclaimed/quoted usage.
    """)

with tab3:
    st.markdown("""
    ### Profanity (243 samples)
    
    **The problem:** "Fuck" by itself isn't hate speech. "Fuck [group]" might be.
    
    **What I noticed:** Pure profanity without a target usually gets labeled offensive, 
    but some annotators mark it normal. The bigger issue is profanity + group mention.
    
    **My suggestion:** General profanity = offensive (not normal, not hate). 
    Profanity directed at protected group = needs careful evaluation.
    """)

st.markdown("---")

# ===================
# ROW 4: Proposed Guidelines
# ===================
st.subheader("Proposed Guideline Updates")

st.markdown("""
Based on this analysis, here's what I think should change in the labeling guidelines:

| Issue | Current Problem | Proposed Change |
|-------|-----------------|-----------------|
| offensive vs hatespeech | No clear boundary | Hatespeech needs: target group + negative intent |
| Group mentions | Inconsistent handling | Group mention alone = not hate |
| Slurs | Some inconsistency | Default to hatespeech unless clearly reclaimed |
| Profanity | Mixed with normal | Pure profanity = offensive, not normal |

**Important caveat:** These are my interpretations based on the data. A real deployment 
would need discussion with the annotation team and possibly legal review for edge cases.
""")

st.markdown("---")

# ===================
# ROW 5: Impact Estimate
# ===================
st.subheader("What improvement could we expect?")

col1, col2 = st.columns(2)

with col1:
    # Current vs Target metrics
    metrics_comparison = pd.DataFrame({
        'Metric': ['Krippendorff\'s Alpha', 'Full Agreement Rate'],
        'Current': [0.46, 48.9],
        'Estimated After': [0.60, 65.0]
    })
    
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        name='Current',
        x=metrics_comparison['Metric'],
        y=metrics_comparison['Current'],
        marker_color='#e74c3c'
    ))
    fig2.add_trace(go.Bar(
        name='Estimated After',
        x=metrics_comparison['Metric'],
        y=metrics_comparison['Estimated After'],
        marker_color='#2ecc71'
    ))
    fig2.update_layout(
        title='Current vs Estimated Metrics',
        barmode='group',
        yaxis_title='Value'
    )
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.markdown("""
    ### Realistic expectations
    
    I'm estimating we could get alpha from **0.46 → ~0.60** with better guidelines.
    
    **Why not higher?**
    - Some disagreement is inherent to subjective tasks
    - Sarcasm/context will always cause some splits
    - Different cultural backgrounds affect interpretation
    
    **To get above 0.67** (acceptable threshold), we'd probably also need:
    - Annotator calibration sessions
    - More detailed examples in guidelines
    - Maybe reduce to 2 categories instead of 3
    
    That last point is worth considering - the offensive/hatespeech distinction 
    might be too fine-grained for reliable annotation.
    """)

st.markdown("---")

# ===================
# ROW 6: Review Queue
# ===================
st.subheader("High-Priority Review Queue")

st.markdown("""
These are samples where **all 3 annotators disagreed** (1 vote each for normal, offensive, hatespeech). 
These edge cases could help refine the guidelines.
""")

# Filter high-priority samples (no agreement cases)
no_agreement = disagreements[disagreements['agreement_type'] == 'None'].head(20)

if len(no_agreement) > 0:
    st.dataframe(
        no_agreement[['post_id', 'text', 'label_1', 'label_2', 'label_3', 'rca_category']],
        use_container_width=True,
        hide_index=True,
        column_config={
            "post_id": st.column_config.TextColumn("ID", width="small"),
            "text": st.column_config.TextColumn("Text", width="large"),
            "label_1": st.column_config.TextColumn("L1", width="small"),
            "label_2": st.column_config.TextColumn("L2", width="small"),
            "label_3": st.column_config.TextColumn("L3", width="small"),
            "rca_category": st.column_config.TextColumn("RCA", width="medium"),
        }
    )
else:
    st.info("No samples with complete disagreement found.")

st.markdown("---")

# ===================
# ROW 7: Export Options
# ===================
st.subheader("Export Data")

col1, col2, col3 = st.columns(3)

with col1:
    csv_rca = rca_counts.to_csv(index=False)
    st.download_button(
        label="Download RCA Summary",
        data=csv_rca,
        file_name="rca_summary.csv",
        mime="text/csv"
    )

with col2:
    csv_review = no_agreement.to_csv(index=False)
    st.download_button(
        label="Download Review Queue",
        data=csv_review,
        file_name="review_queue.csv",
        mime="text/csv"
    )

with col3:
    csv_all = disagreements.to_csv(index=False)
    st.download_button(
        label="Download All Disagreements",
        data=csv_all,
        file_name="all_disagreements.csv",
        mime="text/csv"
    )
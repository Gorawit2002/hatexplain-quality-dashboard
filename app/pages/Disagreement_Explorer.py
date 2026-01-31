# app/pages/2_🔍_Disagreement_Explorer.py
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from utils.data_loader import load_posts, load_disagreements

# Page config
st.set_page_config(page_title="Disagreement Explorer", page_icon="🔍", layout="wide")

st.title("🔍 Disagreement Explorer")
st.markdown("Explore samples where annotators disagreed on labels")
st.markdown("---")

# Load data
posts = load_posts()
disagreements = load_disagreements()

# ===================
# Sidebar Filters
# ===================
st.sidebar.header("Filters")

# Filter by agreement type
agreement_filter = st.sidebar.multiselect(
    "Agreement Type",
    options=['Partial', 'None'],
    default=['Partial', 'None']
)

# Filter by majority label
majority_filter = st.sidebar.multiselect(
    "Majority Label",
    options=['normal', 'offensive', 'hatespeech'],
    default=['normal', 'offensive', 'hatespeech']
)

# Filter by RCA category
rca_options = disagreements['rca_category'].unique().tolist()
rca_filter = st.sidebar.multiselect(
    "RCA Category",
    options=rca_options,
    default=rca_options
)

# Apply filters
filtered_df = disagreements[
    (disagreements['agreement_type'].isin(agreement_filter)) &
    (disagreements['majority_label'].isin(majority_filter)) &
    (disagreements['rca_category'].isin(rca_filter))
]

st.sidebar.markdown(f"**Showing: {len(filtered_df):,} samples**")

# ===================
# ROW 1: Summary Stats
# ===================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Disagreements", f"{len(disagreements):,}")
with col2:
    st.metric("Filtered Samples", f"{len(filtered_df):,}")
with col3:
    partial_count = len(filtered_df[filtered_df['agreement_type'] == 'Partial'])
    st.metric("Partial (2/3)", f"{partial_count:,}")
with col4:
    none_count = len(filtered_df[filtered_df['agreement_type'] == 'None'])
    st.metric("No Agreement (1/1/1)", f"{none_count:,}")

st.markdown("---")

# ===================
# ROW 2: Visualizations
# ===================
col1, col2 = st.columns(2)

with col1:
    # Disagreement by Label Combination
    label_combo = filtered_df.apply(
        lambda x: f"{x['label_1']} vs {x['label_2']} vs {x['label_3']}", axis=1
    )
    combo_counts = label_combo.value_counts().head(10).reset_index()
    combo_counts.columns = ['Label Combination', 'Count']
    
    fig1 = px.bar(
        combo_counts,
        x='Count',
        y='Label Combination',
        orientation='h',
        title='Top 10 Label Disagreement Patterns',
        color='Count',
        color_continuous_scale='Reds'
    )
    fig1.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # Disagreement by RCA Category
    rca_counts = filtered_df['rca_category'].value_counts().reset_index()
    rca_counts.columns = ['RCA Category', 'Count']
    
    fig2 = px.pie(
        rca_counts,
        values='Count',
        names='RCA Category',
        title='Disagreements by RCA Category',
        hole=0.4
    )
    fig2.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig2, use_container_width=True)

# Add insight based on data
top_pattern = combo_counts.iloc[0]['Label Combination'] if len(combo_counts) > 0 else "N/A"
st.info(f"""
**Quick observation:** The most common disagreement pattern is "{top_pattern}". 
This confirms what we saw in the RCA analysis - the offensive/hatespeech boundary 
is where most confusion happens.
""")

st.markdown("---")

# ===================
# ROW 3: Sample Explorer
# ===================
st.subheader("Sample Explorer")

# Search box
search_term = st.text_input("Search in text", placeholder="Enter keyword to search...")

if search_term:
    filtered_df = filtered_df[filtered_df['text'].str.contains(search_term, case=False, na=False)]
    st.info(f"Found {len(filtered_df)} samples containing '{search_term}'")

# Display samples
st.markdown(f"**Showing {min(100, len(filtered_df))} of {len(filtered_df)} samples**")

# Select columns to display
display_cols = ['post_id', 'text', 'label_1', 'label_2', 'label_3', 
                'majority_label', 'agreement_type', 'rca_category']

# Paginated table
if len(filtered_df) > 0:
    st.dataframe(
        filtered_df[display_cols].head(100),
        use_container_width=True,
        hide_index=True,
        column_config={
            "post_id": st.column_config.TextColumn("Post ID", width="small"),
            "text": st.column_config.TextColumn("Text", width="large"),
            "label_1": st.column_config.TextColumn("Label 1", width="small"),
            "label_2": st.column_config.TextColumn("Label 2", width="small"),
            "label_3": st.column_config.TextColumn("Label 3", width="small"),
            "majority_label": st.column_config.TextColumn("Majority", width="small"),
            "agreement_type": st.column_config.TextColumn("Agreement", width="small"),
            "rca_category": st.column_config.TextColumn("RCA Category", width="medium"),
        }
    )
else:
    st.warning("No samples match the current filters.")

st.markdown("---")

# ===================
# ROW 4: Detailed Sample View
# ===================
st.subheader("Detailed Sample View")

if len(filtered_df) > 0:
    # Select a sample to view details
    sample_ids = filtered_df['post_id'].tolist()[:50]
    selected_id = st.selectbox("Select a sample to view details", sample_ids)
    
    if selected_id:
        sample = filtered_df[filtered_df['post_id'] == selected_id].iloc[0]
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("**Text:**")
            st.info(sample['text'])
            
            st.markdown("**Highlighted Words:**")
            if pd.notna(sample['highlighted_words']) and sample['highlighted_words']:
                st.warning(sample['highlighted_words'])
            else:
                st.text("No highlighted words available")
        
        with col2:
            st.markdown("**Annotator Labels:**")
            st.write(f"- Annotator 1: `{sample['label_1']}`")
            st.write(f"- Annotator 2: `{sample['label_2']}`")
            st.write(f"- Annotator 3: `{sample['label_3']}`")
            
            st.markdown("**Analysis:**")
            st.write(f"- Majority Label: `{sample['majority_label']}`")
            st.write(f"- Agreement Type: `{sample['agreement_type']}`")
            st.write(f"- RCA Category: `{sample['rca_category']}`")
            
            st.markdown("**Target Groups:**")
            st.write(f"`{sample['target_groups']}`")
        
        # Add some interpretation
        labels = [sample['label_1'], sample['label_2'], sample['label_3']]
        if 'hatespeech' in labels and 'offensive' in labels:
            st.markdown("""
            ---
            **Why this disagreement matters:** This is a hatespeech/offensive split - exactly the kind of 
            case where clearer guidelines would help. Looking at the highlighted words might reveal 
            why annotators saw it differently.
            """)
# 🎯 AI Data Labeling Quality Dashboard

An interactive dashboard for analyzing data labeling quality and inter-annotator agreement using the **HateXplain** dataset.

---

## 🎯 Project Overview

Data labeling quality is critical for training reliable AI models. This project analyzes a real hate speech dataset to:

- Measure inter-annotator agreement using **Krippendorff's Alpha**
- Identify patterns in annotator disagreements
- Perform **Root Cause Analysis (RCA)** on labeling inconsistencies
- Provide actionable recommendations for guideline improvements

---

## 📈 Key Findings

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Krippendorff's Alpha | **0.46** | Below acceptable threshold (0.667) |
| Full Agreement Rate | **48.9%** | Less than half have unanimous agreement |
| Main Confusion | **offensive ↔ hatespeech** | Boundary between these labels is unclear |
| Annotator Bias | **43% lenient** | Dataset likely under-labels hate speech |

---

## 🛠️ Skills Demonstrated

| Skill | Application |
|-------|-------------|
| **Inter-Annotator Agreement** | Krippendorff's Alpha calculation and interpretation |
| **Quality Metrics & KPIs** | Dashboard tracking key quality indicators |
| **Root Cause Analysis** | Categorized disagreement patterns into 7 RCA categories |
| **Annotator Performance** | Bias detection (strict vs lenient annotators) |
| **Data Visualization** | Interactive Plotly charts for stakeholder communication |
| **Dashboard Development** | Multi-page Streamlit application |

---

## 📁 Project Structure

```
hatexplain-quality-dashboard/
├── app/
│   ├── app.py                    # Main Streamlit app
│   ├── pages/
│   │   ├── Overview.py      # Quality metrics dashboard
│   │   ├── Disagreement_Explorer.py
│   │   ├── Annotator_Analysis.py
│   │   └── RCA_Summary.py
│   └── utils/
│       └── data_loader.py
├── data/
│   ├── posts_analysis.csv
│   ├── annotators_analysis.csv
│   ├── summary_metrics.csv
│   └── disagreement_samples.csv
├── notebooks/
│   └── HateXplain_Data_Exploration.ipynb
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### Run Locally

```bash
# Clone the repository
git clone https://github.com/yourusername/hatexplain-quality-dashboard.git
cd hatexplain-quality-dashboard

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app/app.py
```

### Deactivate venv (when done)

```bash
deactivate
```

---

## 📊 Dashboard Pages

### 1. 📊 Overview
Key metrics at a glance: Krippendorff's Alpha gauge, agreement distribution, label distribution, and annotator bias summary.

### 2. 🔍 Disagreement Explorer
Interactive exploration of 10,303 samples where annotators disagreed. Filter by agreement type, label, and RCA category.

### 3. 👥 Annotator Analysis
Individual annotator performance: bias detection (strict/lenient/balanced), agreement rates, and quality leaderboard.

### 4. 🎯 RCA Summary
Root cause analysis findings, proposed guideline updates, and priority review queue for edge cases.

---

## 📐 Methodology

### Why Krippendorff's Alpha?

Simple percentage agreement doesn't account for chance. With 3 labels, random guessing yields ~33% agreement. Krippendorff's Alpha corrects for this.

**Thresholds (Krippendorff, 2004):**
- α ≥ 0.8: Reliable
- α ≥ 0.667: Acceptable  
- α < 0.667: Poor ← Our dataset (0.46)

### Annotator Bias Detection

```
Strictness Score = % hatespeech - % normal
```

| Score | Category | Percentage |
|-------|----------|------------|
| > 20 | Strict | 18% |
| -20 to 20 | Balanced | 39% |
| < -20 | Lenient | 43% |

### RCA Categories

| Category | % of Disagreements |
|----------|-------------------|
| Other/Unclear | 57.0% |
| Group References | 6.4% |
| Profanity | 2.4% |
| Racial Slurs | 2.3% |
| Gender/Sexuality | 2.2% |
| Religious Terms | 1.9% |
| Dehumanizing | 1.4% |

---

## 💡 Key Recommendations

Based on the analysis:

1. **Clarify offensive vs hatespeech**: Hatespeech requires target group + negative intent
2. **Group references**: Mention alone ≠ hate speech (context matters)
3. **Slurs**: Default to hatespeech unless clearly reclaimed/quoted
4. **Calibration sessions**: Focus on the 43% lenient annotators

---

## 🔧 Tech Stack

- **Python 3.9+**
- **Streamlit** - Interactive dashboard
- **Pandas** - Data manipulation
- **Plotly** - Interactive visualizations
- **Krippendorff** - Agreement calculation

---

## 📝 Dataset

**HateXplain** (Mathew et al., 2020)

- 20,148 posts from Twitter and Gab
- 3 annotators per sample
- Labels: `normal`, `offensive`, `hatespeech`
- Includes rationales (highlighted words)

📎 Source: [HateXplain GitHub](https://github.com/hate-alert/HateXplain)

---

## 📄 License

MIT License - This project is for educational/portfolio purposes.

---

## 👤 Author

Built as a data quality analysis portfolio project demonstrating skills relevant to AI data labeling and annotation quality roles.
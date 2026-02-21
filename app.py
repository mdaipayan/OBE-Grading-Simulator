import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="OBE Grading Simulator", layout="wide")
st.title("Safeguarding OBE: Protocol A vs. Protocol B Simulator")
st.markdown("A computational approach to mitigating grade inflation in zero-inflated cohorts.")

# --- Sidebar Inputs ---
st.sidebar.header("Simulation Parameters")
N_active = st.sidebar.slider("Number of Active Learners", 20, 100, 39)
N_outliers = st.sidebar.slider("Number of Non-Performers", 0, 50, 23)
max_marks = 100
ese_marks = 60
h_ese = 0.20 * ese_marks  # 12 marks hurdle

# --- Data Generation (Zero-Inflated Bimodal) ---
np.random.seed(42)
# Active learners clustered around 65
active_scores = np.random.normal(loc=65, scale=12, size=N_active)
active_scores = np.clip(active_scores, h_ese, max_marks) 

# Non-performers clustered near 8 (failing the 12 mark hurdle)
outlier_scores = np.random.normal(loc=8, scale=4, size=N_outliers)
outlier_scores = np.clip(outlier_scores, 0, h_ese - 0.1)

all_scores = np.concatenate([active_scores, outlier_scores])
df = pd.DataFrame({'Total_Marks': all_scores})

# --- Algorithmic Processing ---
# Protocol A: Strict Exclusion (Filter out < 12 marks)
df_protocol_a = df[df['Total_Marks'] >= h_ese]
mu_a = np.mean(df_protocol_a['Total_Marks'])
sigma_a = np.std(df_protocol_a['Total_Marks'])

# Protocol B: Inclusive Calculation
mu_b = np.mean(df['Total_Marks'])
sigma_b = np.std(df['Total_Marks'])

# --- Dashboard Layout ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Protocol A (Strict Exclusion / OBE-Compliant)")
    st.metric(label="Class Mean (μ)", value=f"{mu_a:.2f}")
    st.metric(label="Standard Deviation (σ)", value=f"{sigma_a:.2f}")
    st.markdown(f"**'A' Grade Threshold (μ + 1.0σ):** `{mu_a + sigma_a:.2f}`")

with col2:
    st.subheader("Protocol B (Inclusive / Prone to Inflation)")
    st.metric(label="Class Mean (μ)", value=f"{mu_b:.2f}", delta=f"{mu_b - mu_a:.2f}", delta_color="inverse")
    st.metric(label="Standard Deviation (σ)", value=f"{sigma_b:.2f}")
    st.markdown(f"**'A' Grade Threshold (μ + 1.0σ):** `{mu_b + sigma_b:.2f}`")

# --- Visualizing the Distortion ---
st.divider()
st.subheader("Raw Score Distribution (The Bimodal Problem)")

# Provide a raw score distribution plot using Streamlit's native charting
st.bar_chart(np.histogram(all_scores, bins=10)[0])

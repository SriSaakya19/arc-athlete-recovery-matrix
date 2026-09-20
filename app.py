import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- THEME CONFIGURATION: ARC-Alpha Ice-Blue Minimalist Matrix ---
st.set_page_config(
    page_title="ARC - Alpha Athlete Recovery Matrix v1.0",
    page_icon="❄️",
    layout="wide"
)

# Custom Premium CSS Injection
st.markdown("""
    <style>
    .main { background-color: #0A192F; color: #E2E8F0; }
    h1, h2, h3 { color: #64FFDA !important; font-family: 'Helvetica Neue', sans-serif; }
    .stButton>button { background-color: #172A45; color: #64FFDA; border: 1px solid #64FFDA; border-radius: 5px; }
    .stButton>button:hover { background-color: #64FFDA; color: #0A192F; }
    div[data-testid="stMetricValue"] { color: #00B4D8 !important; font-size: 28px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("ARC — ATHLETE RECOVERY MATRIX v1.0 ❄️🧠")
st.subheader("Predictive Thermal-Kinetic Recovery Suite for Elite All-Rounders")
st.write("Engineered by **Sri Saakya** | Founder & Lead Architect, *The Cricket Alchemist*")

st.markdown("---")

# --- SIDEBAR INTERFACE: ATHLETIC PROFILING ---
st.sidebar.header("🏆 ATHLETE LIVE PERFORMANCE INPUTS")
athlete_name = st.sidebar.selectbox("Select Target Athlete", ["Nitish Kumar Reddy", "Smaran Ravichandran", "Aman Rao"])
jersey_number = 88 if athlete_name == "Nitish Kumar Reddy" else 19

recent_overs = st.sidebar.slider("Recent Workload (Overs Bowled in Last 7 Days)", 0.0, 50.0, 24.0, step=0.5)
chronic_overs = st.sidebar.slider("Chronic Workload (Avg Weekly Overs Last 4 Weeks)", 5.0, 40.0, 18.0, step=0.5)
knee_flexion = st.sidebar.slider("Biomechanical Knee Flexion Angle (Stride Impact °)", 120.0, 180.0, 142.5, step=0.5)

# --- CORE MATHEMATICAL ENGINE ---
# Calculate rolling ACWR (Acute-to-Chronic Workload Ratio)
acwr_score = recent_overs / chronic_overs if chronic_overs > 0 else 1.0

# Calculate Downstream Micro-Strain Fatigue Index
fatigue_index = (acwr_score * 50) + ((180 - knee_flexion) * 1.5)

# Calculate Automated Cryotherapy Recovery Parameters
if fatigue_index > 75:
    status = "🔴 CRITICAL STRAIN ZONE"
    optimal_temp = 8.0  # Deep cryo flush needed
    duration_mins = 12.0
elif 45 <= fatigue_index <= 75:
    status = "🟡 OPTIMAL LOAD RECOVERY"
    optimal_temp = 11.0
    duration_mins = 9.5
else:
    status = "🟢 BASELINE MAINTENANCE"
    optimal_temp = 13.0
    duration_mins = 7.0

# --- DASHBOARD LAYOUT & METRIC RENDERING ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Target Athlete", f"{athlete_name} (#{jersey_number})")
with col2:
    st.metric("Calculated ACWR", f"{acwr_score:.2f}")
with col3:
    st.metric("Cryo Temperature", f"{optimal_temp}°C")
with col4:
    st.metric("Immersion Duration", f"{duration_mins} Mins")

st.markdown(f"### **Current Status:** `{status}`")

# --- VISUALIZATION: THERMAL-KINETIC FATIGUE TRAJECTORY ---
st.markdown("---")
st.subheader("📊 Thermal-Kinetic Recovery Calibration Map")

categories = ['ACWR Fatigue Metric', 'Knee Impact Strain', 'Lactic Acid Index', 'Neural Baseline Depletion']
values = [acwr_score * 40, (180 - knee_flexion) * 2, fatigue_index * 0.8, (recent_overs / 50) * 100]

fig = go.Figure()
fig.add_trace(go.Scatterpolar(
      r=values,
      theta=categories,
      fill='toself',
      name='Fatigue Footprint',
      line_color='#64FFDA',
      fillcolor='rgba(0, 180, 216, 0.3)'
))

fig.update_layout(
  polar=dict(
    radialaxis=dict(visible=True, range=[0, 100], gridcolor="#172A45"),
    bgcolor="#0A192F"
  ),
  showlegend=False,
  paper_bgcolor="#0A192F",
  plot_bgcolor="#0A192F",
  font=dict(color="#E2E8F0")
)

st.plotly_chart(fig, use_container_width=True)

# --- EXECUTIVE FOOTER ---
st.markdown("---")
st.info(f"💡 **ARC Automated Recommendation:** For {athlete_name}, based on an ACWR of {acwr_score:.2f} and a Stride Knee Flexion of {knee_flexion}°, execute an immediate ice-bath immersion at exactly {optimal_temp}°C for {duration_mins} minutes to prevent post-match joint stiffness and maximize neuromuscular recovery velocity.")

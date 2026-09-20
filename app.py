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
st.subheader("Predictive Thermal-Kinetic Recovery Suite for Elite Indian Athletes")
st.write("Engineered by **Sri Saakya** | Founder & Lead Architect, *The Cricket Alchemist*")

st.markdown("---")

# --- COMPLETE INDIAN ATHLETE DATABASE ---
athlete_db = {
    "Nitish Kumar Reddy": {"jersey": 88, "role": "Fast Bowling All-Rounder", "default_recent": 24.0, "default_chronic": 18.0, "default_flexion": 142.5},
    "Jasprit Bumrah": {"jersey": 93, "role": "Premier Fast Bowler", "default_recent": 28.0, "default_chronic": 20.0, "default_flexion": 138.0},
    "Mohammed Siraj": {"jersey": 73, "role": "Fast Bowler", "default_recent": 30.0, "default_chronic": 22.0, "default_flexion": 140.0},
    "Mohammed Shami": {"jersey": 11, "role": "Fast Bowler", "default_recent": 26.0, "default_chronic": 21.0, "default_flexion": 141.0},
    "Hardik Pandya": {"jersey": 33, "role": "Fast Bowling All-Rounder", "default_recent": 18.0, "default_chronic": 15.0, "default_flexion": 145.0},
    "Arshdeep Singh": {"jersey": 2, "role": "Left-Arm Fast Bowler", "default_recent": 22.0, "default_chronic": 19.0, "default_flexion": 143.0},
    "Prasidh Krishna": {"jersey": 24, "role": "Fast Bowler", "default_recent": 25.0, "default_chronic": 17.0, "default_flexion": 139.0},
    "Akash Deep": {"jersey": 41, "role": "Fast Bowler", "default_recent": 27.0, "default_chronic": 20.0, "default_flexion": 142.0},
    "Harshit Rana": {"jersey": 22, "role": "Fast Bowler", "default_recent": 21.0, "default_chronic": 16.0, "default_flexion": 144.0},
    "Mayank Yadav": {"jersey": 7, "role": "Express Fast Bowler", "default_recent": 16.0, "default_chronic": 12.0, "default_flexion": 136.0},
    "Smaran Ravichandran": {"jersey": 19, "role": "Emerging Pace All-Rounder", "default_recent": 20.0, "default_chronic": 16.0, "default_flexion": 145.0},
    "Aman Rao": {"jersey": 12, "role": "Emerging Pace All-Rounder", "default_recent": 19.0, "default_chronic": 15.0, "default_flexion": 146.0}
}

# --- SIDEBAR INTERFACE: ATHLETIC PROFILING ---
st.sidebar.header("🏆 SELECT INDIAN ATHLETE")
athlete_name = st.sidebar.selectbox("Choose Athlete", list(athlete_db.keys()))

selected_athlete = athlete_db[athlete_name]
jersey_number = selected_athlete["jersey"]
role = selected_athlete["role"]

st.sidebar.markdown(f"**Role:** `{role}`")

recent_overs = st.sidebar.slider("Recent Workload (Overs Bowled in Last 7 Days)", 0.0, 50.0, float(selected_athlete["default_recent"]), step=0.5)
chronic_overs = st.sidebar.slider("Chronic Workload (Avg Weekly Overs Last 4 Weeks)", 5.0, 40.0, float(selected_athlete["default_chronic"]), step=0.5)
knee_flexion = st.sidebar.slider("Biomechanical Knee Flexion Angle (Stride Impact °)", 120.0, 180.0, float(selected_athlete["default_flexion"]), step=0.5)

# --- CORE MATHEMATICAL ENGINE ---
acwr_score = recent_overs / chronic_overs if chronic_overs > 0 else 1.0
fatigue_index = (acwr_score * 50) + ((180 - knee_flexion) * 1.5)

if fatigue_index > 75:
    status = "🔴 CRITICAL STRAIN ZONE"
    optimal_temp = 8.0
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
st.info(f"💡 **ARC Automated Recommendation:** For **{athlete_name}** ({role}), based on an ACWR of {acwr_score:.2f} and a Stride Knee Flexion of {knee_flexion}°, execute an immediate ice-bath immersion at exactly {optimal_temp}°C for {duration_mins} minutes to prevent post-match joint stiffness and maximize neuromuscular recovery velocity.")

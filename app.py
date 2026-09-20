import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- THEME CONFIGURATION ---
st.set_page_config(
    page_title="ARC - Predictive Recovery Matrix",
    page_icon="❄️",
    layout="wide"
)

# HIGH-CONTRAST DARK CSS INJECTION
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@1,600&family=Plus+Jakarta+Sans:ital,wght@0,300;0,500;1,300&display=swap');

    /* Global Dark Background & White Text */
    .stApp {
        background-color: #050B14 !important;
        color: #FFFFFF !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Header Styles */
    .aesthetic-title {
        font-family: 'Lucida Calligraphy', 'Playfair Display', cursive, serif !important;
        font-style: italic !important;
        background: linear-gradient(135deg, #00F2FE 0%, #4FACFE 50%, #00EA97 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem !important;
        font-weight: 700;
        line-height: 1.3 !important;
        padding-bottom: 5px;
    }

    .aesthetic-subtitle {
        font-family: 'Lucida Calligraphy', cursive, serif !important;
        font-style: italic !important;
        color: #CBD5E1 !important;
        font-size: 1.1rem !important;
    }

    /* FIX SIDEBAR TEXT VISIBILITY */
    section[data-testid="stSidebar"] {
        background-color: #0B132B !important;
        border-right: 1px solid rgba(255, 255, 255, 0.15);
    }

    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span {
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }

    /* METRIC CARDS & LABELS FIX */
    div[data-testid="stMetric"] {
        background: #0F172A !important;
        border: 1px solid #00F2FE !important;
        border-radius: 14px !important;
        padding: 15px !important;
        box-shadow: 0px 4px 20px rgba(0, 242, 254, 0.15) !important;
    }

    div[data-testid="stMetricLabel"] p {
        color: #94A3B8 !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }

    div[data-testid="stMetricValue"] div {
        color: #00F2FE !important;
        font-size: 26px !important;
        font-weight: 700 !important;
    }

    /* Section Headings */
    .section-header {
        font-family: 'Lucida Calligraphy', cursive, serif !important;
        font-style: italic !important;
        color: #64FFDA !important;
        font-size: 1.6rem !important;
        border-bottom: 1px dashed rgba(100, 255, 218, 0.2);
        padding-bottom: 8px;
        margin-top: 25px;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER SECTION ---
st.markdown('<div class="aesthetic-title">ARC — Athlete Recovery Matrix ❄️✨</div>', unsafe_allow_html=True)
st.markdown('<div class="aesthetic-subtitle">Thermal-Kinetic Biomechanical Engine & Cryo Suite</div>', unsafe_allow_html=True)
st.write("*Engineered by **Sri Saakya** | Lead Architect, The Cricket Alchemist*")

st.markdown("---")

# --- COMPLETE INDIAN ATHLETE DATABASE ---
athlete_db = {
    "Nitish Kumar Reddy": {"jersey": 88, "role": "Fast Bowling All-Rounder", "default_recent": 18.0, "default_chronic": 18.0, "default_flexion": 155.0},
    "Jasprit Bumrah": {"jersey": 93, "role": "Premier Fast Bowler", "default_recent": 28.0, "default_chronic": 18.0, "default_flexion": 138.0},
    "Mohammed Siraj": {"jersey": 73, "role": "Fast Bowler", "default_recent": 24.0, "default_chronic": 20.0, "default_flexion": 145.0},
    "Mohammed Shami": {"jersey": 11, "role": "Fast Bowler", "default_recent": 16.0, "default_chronic": 21.0, "default_flexion": 160.0},
    "Hardik Pandya": {"jersey": 33, "role": "Fast Bowling All-Rounder", "default_recent": 12.0, "default_chronic": 15.0, "default_flexion": 165.0},
    "Arshdeep Singh": {"jersey": 2, "role": "Left-Arm Fast Bowler", "default_recent": 20.0, "default_chronic": 19.0, "default_flexion": 150.0},
    "Prasidh Krishna": {"jersey": 24, "role": "Fast Bowler", "default_recent": 25.0, "default_chronic": 17.0, "default_flexion": 139.0},
    "Akash Deep": {"jersey": 41, "role": "Fast Bowler", "default_recent": 22.0, "default_chronic": 20.0, "default_flexion": 148.0},
    "Harshit Rana": {"jersey": 22, "role": "Fast Bowler", "default_recent": 18.0, "default_chronic": 16.0, "default_flexion": 152.0},
    "Mayank Yadav": {"jersey": 7, "role": "Express Fast Bowler", "default_recent": 24.0, "default_chronic": 12.0, "default_flexion": 136.0},
    "Smaran Ravichandran": {"jersey": 19, "role": "Emerging Pace All-Rounder", "default_recent": 14.0, "default_chronic": 16.0, "default_flexion": 158.0},
    "Aman Rao": {"jersey": 12, "role": "Emerging Pace All-Rounder", "default_recent": 10.0, "default_chronic": 15.0, "default_flexion": 168.0}
}

# --- SIDEBAR INTERFACE ---
st.sidebar.markdown('<div style="font-family:\'Lucida Calligraphy\', cursive; font-style:italic; font-size:1.3rem; color:#00F2FE;">Athlete Telemetry Input</div>', unsafe_allow_html=True)
athlete_name = st.sidebar.selectbox("Target Athlete", list(athlete_db.keys()))

selected_athlete = athlete_db[athlete_name]
jersey_number = selected_athlete["jersey"]
role = selected_athlete["role"]

st.sidebar.markdown(f"**Role:** `{role}`")

recent_overs = st.sidebar.slider("Recent Workload (Last 7 Days Overs)", 0.0, 50.0, float(selected_athlete["default_recent"]), step=0.5)
chronic_overs = st.sidebar.slider("Chronic Workload (Avg Weekly Overs)", 5.0, 40.0, float(selected_athlete["default_chronic"]), step=0.5)
knee_flexion = st.sidebar.slider("Stride Knee Flexion Angle (°)", 120.0, 180.0, float(selected_athlete["default_flexion"]), step=0.5)

# --- CORE ENGINE LOGIC ---
acwr_score = recent_overs / chronic_overs if chronic_overs > 0 else 1.0
fatigue_index = (acwr_score * 40) + ((180 - knee_flexion) * 1.1)

# Dynamic REALISTIC STATUS THRESHOLDS
if fatigue_index > 90:
    status = "🔴 CRITICAL STRAIN ZONE"
    optimal_temp = 8.0
    duration_mins = 12.0
elif 65 <= fatigue_index <= 90:
    status = "🟡 OPTIMAL LOAD RECOVERY"
    optimal_temp = 11.0
    duration_mins = 9.5
else:
    status = "🟢 BASELINE MAINTENANCE"
    optimal_temp = 13.0
    duration_mins = 7.0

# --- METRICS DISPLAY ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Target Athlete", f"{athlete_name}", f"#{jersey_number}")
with col2:
    st.metric("ACWR Ratio", f"{acwr_score:.2f}")
with col3:
    st.metric("Cryo Target Temp", f"{optimal_temp}°C")
with col4:
    st.metric("Immersion Duration", f"{duration_mins} Mins")

st.markdown(f"<br><div style='font-family:\"Lucida Calligraphy\", cursive; font-style:italic; font-size:1.35rem; color:#FFFFFF;'>Recovery Status: <span style='color:#00F2FE;'>{status}</span></div>", unsafe_allow_html=True)

# --- STACKED GRAPHICAL LAYOUT ---
st.markdown('<div class="section-header">Biomechanical Fatigue & Workload Analytics ✨</div>', unsafe_allow_html=True)

# 1. RADAR FOOTPRINT GRAPH
categories = ['ACWR Fatigue', 'Knee Strain', 'Lactic Stress', 'Neural Depletion']
values = [acwr_score * 35, (180 - knee_flexion) * 1.5, fatigue_index * 0.7, (recent_overs / 50) * 100]

fig_radar = go.Figure()
fig_radar.add_trace(go.Scatterpolar(
    r=values,
    theta=categories,
    fill='toself',
    name='Fatigue Matrix',
    line=dict(color='#00F2FE', width=2),
    fillcolor='rgba(0, 242, 254, 0.25)'
))

fig_radar.update_layout(
    title=dict(text="<em>Biomechanics Fatigue Radar Footprint</em>", font=dict(family="Lucida Calligraphy", size=18, color="#64FFDA")),
    polar=dict(
        radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(255,255,255,0.15)", tickfont=dict(color="#FFFFFF")),
        angularaxis=dict(gridcolor="rgba(255,255,255,0.15)", tickfont=dict(color="#FFFFFF", size=13)),
        bgcolor="#050B14"
    ),
    paper_bgcolor="#050B14",
    plot_bgcolor="#050B14",
    showlegend=False,
    height=450,
    margin=dict(l=40, r=40, t=50, b=40)
)
st.plotly_chart(fig_radar, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# 2. WORKLOAD TREND LINE GRAPH
days = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Match Day', 'Post Match']
workload_trend = [recent_overs*0.2, recent_overs*0.4, recent_overs*0.1, recent_overs*0.6, recent_overs*0.3, recent_overs, 0]
recovery_curve = [100 - (w * 1.8) for w in workload_trend]

fig_line = go.Figure()
fig_line.add_trace(go.Scatter(x=days, y=workload_trend, mode='lines+markers', name='Workload Trend (Overs)', line=dict(color='#FF007F', width=3)))
fig_line.add_trace(go.Scatter(x=days, y=recovery_curve, mode='lines+markers', name='Neuromuscular Baseline %', line=dict(color='#00EA97', width=3, dash='dot')))

fig_line.update_layout(
    title=dict(text="<em>7-Day Workload vs Neuromuscular Recovery Velocity</em>", font=dict(family="Lucida Calligraphy", size=18, color="#64FFDA")),
    paper_bgcolor="#050B14",
    plot_bgcolor="#050B14",
    xaxis=dict(gridcolor="rgba(255,255,255,0.1)", tickfont=dict(color="#FFFFFF")),
    yaxis=dict(gridcolor="rgba(255,255,255,0.1)", tickfont=dict(color="#FFFFFF")),
    legend=dict(font=dict(color="#FFFFFF")),
    height=400,
    margin=dict(l=40, r=40, t=50, b=40)
)
st.plotly_chart(fig_line, use_container_width=True)

# --- EXECUTIVE FOOTER ---
st.markdown("---")
st.markdown(f"""
<div style="background: rgba(15, 23, 42, 0.85); border: 1px solid #00F2FE; border-radius: 12px; padding: 20px;">
    <h4 style="font-family:'Lucida Calligraphy', cursive; font-style:italic; color:#00F2FE; margin-top:0;">Automated Sports Science Protocol</h4>
    <p style="color:#FFFFFF; font-size:1.05rem;">For <b>{athlete_name}</b> ({role}), based on calculated ACWR ratio of <b>{acwr_score:.2f}</b> and Knee Flexion Stride Angle of <b>{knee_flexion}°</b>, execute an immediate ice-bath immersion at <b>{optimal_temp}°C</b> for <b>{duration_mins} minutes</b> to flush lactic accumulation & prevent joint micro-strain.</p>
</div>
""", unsafe_allow_html=True)

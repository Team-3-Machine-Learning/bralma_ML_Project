import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import math
from datetime import datetime, date

# Streamlit App Configuration
st.set_page_config(page_title="Dashboard", layout="wide", page_icon="🤖")
st.title("Machine Learning Predictions Dashboard")
st.markdown("*Kies een voorspellingsmodel om mee te starten*")

st.markdown("---")

# Create two columns for navigation buttons
col1, col2 = st.columns(2)

with col1:
    st.markdown("### ⚡ Electricity Demand Predictor")
    st.markdown("""
    Voorspel **UK elektriciteitsvraag** op basis van:
    - 🌬️ Windkracht (5 categorieën)
    - ☀️ Zonne-energie (auto-berekend)
    - ⏰ Tijdstip (48 settlement periods)
    - 📅 Seizoen (winter/lente/zomer/herfst)
    """)
    st.markdown("")  # Spacer
    
with col2:
    st.markdown("### 🏠 UK Housing Type Predictor")
    st.markdown("""
    Voorspel **property type** (D/S/T/F) op basis van:
    - 💰 Prijs (categorieën of exact)
    - 📍 Locatie (stad, county, regio)
    - 🏗️ Kenmerken (freehold/leasehold, nieuw/oud)
    """)
    st.markdown("")  # Spacer

# Buttons on same row below descriptions
col_btn1, col_btn2 = st.columns(2)

with col_btn1:
    if st.button("➡️ Ga naar Electricity Demand", type="primary", use_container_width=True):
        st.switch_page("pages/0_Electricity_Demand.py")

with col_btn2:
    if st.button("➡️ Ga naar UK Housing", type="primary", use_container_width=True):
        st.switch_page("pages/1_🏠_UK_Housing.py")

st.markdown("---")

# Dataset info section
st.markdown("## 📊 Dataset Overzicht")

col_dataset1, col_dataset2 = st.columns(2)

with col_dataset1:
    st.markdown("### ⚡ Electricity Demand Dataset")
    st.markdown("""
    **📅 Periode:** 2001-2025  
    **📊 Aantal Records:** ~1.2M observations  
    **⏰ Resolutie:** 30-minuten intervals (48 per dag)  
    **🌍 Regio:** United Kingdom
    
    **Features:**
    - Settlement Period (1-48)
    - England & Wales Demand (MW)
    - Embedded Wind Generation (MW)
    - Embedded Wind Capacity (MW)
    - Embedded Solar Generation (MW)
    - Embedded Solar Capacity (MW)
    
    """)

with col_dataset2:
    st.markdown("### 🏠 UK Housing Price Dataset")
    st.markdown("""
    **📅 Periode:** 2001-2017  
    **📊 Aantal Records:** ~600K transactions  
    **🌍 Regio:** England, Wales, Scotland, Northern Ireland  
    **💰 Prijsbereik:** £10K - £10M+
    
    **Features:**
    - Price (transactie prijs)
    - Old/New (Bestaande/Nieuwbouw)
    - Duration (Freehold/Leasehold)
    - Location (City, County, Region)
    
    """)


st.markdown("---")

# Sidebar - API Status & Quick Info
st.sidebar.title("🤖 ML Predictions")
st.sidebar.markdown("### 📖 Quick Info")
st.sidebar.markdown("""
**⚡ Electricity Demand:**
- Type: Regression
- Output: MW demand
- Features: 6 parameters

**🏠 UK Housing:**
- Type: Classification  
- Output: Property type (D/S/T/F)
- Features: 8 parameters
""")

st.sidebar.markdown("---")
st.sidebar.caption("🚀 .NET 9 + Streamlit")
st.sidebar.caption("📅 November 2025")

# Instructions to run the app:
# Powershell commands (WINDOWS):
# 1. cd "c:\Users\Brent\Desktop\3APP\Machine Learning\Cloud AI\bralma_ML_Project\Bralma_frontend"
# 2. streamlit run App.py
# 3. Open browser: http://localhost:8501
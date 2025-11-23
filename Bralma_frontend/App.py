import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import math
from datetime import datetime, date

# Streamlit App Configuration
st.set_page_config(page_title="⚡ Electricity Demand Predictor", layout="wide")
st.title("⚡ UK Electricity Demand Predictor")
st.markdown("*Voorspel de elektriciteitsvraag op basis van weer, tijd en seizoen*")

# API URL
# API_URL = "https://bralma-backend.onrender.com"

# Sidebar - API Status & Quick Info
st.sidebar.title("⚙️ Instellingen")

st.sidebar.markdown("### 🔗 API Status")
try:
    health_check = requests.get(f"{API_URL}/health", timeout=5)
    if health_check.status_code == 200:
        st.sidebar.success("✅ API Verbonden")
        st.sidebar.caption("Backend actief")
    else:
        st.sidebar.error("❌ API Error")
except:
    st.sidebar.warning("⚠️ API Offline")
    st.sidebar.caption("Render.com wake-up: ~15 sec")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📚 Snelle Voorbeelden")

st.sidebar.markdown("""
**🌙 Nacht (Laag demand)**
- Seizoen: Winter
- Tijd: Period 6 (03:00)
- Wind: Matig
- Verwacht: ~22 GW

**🏭 Avondpiek (Hoog demand)**
- Seizoen: Winter  
- Tijd: Period 36 (18:00)
- Wind: Weinig
- Verwacht: ~45 GW

**☀️ Zomerdag (Veel hernieuwbaar)**
- Seizoen: Zomer
- Tijd: Period 26 (13:00)
- Wind: Veel
- Verwacht: 50%+ hernieuwbaar

**🌬️ Stormdag**
- Seizoen: Winter
- Tijd: Period 20 (10:00)
- Wind: Storm
- Verwacht: 60%+ hernieuwbaar
""")

st.sidebar.markdown("---")
st.sidebar.markdown("### 💡 Tips")
st.sidebar.info("""
- **Peak demand**: 17:00-20:00 (winter)
- **Laagste demand**: 03:00-05:00
- **Beste hernieuwbaar**: zomer middag + veel wind
- **Slechtste**: winter nacht + windstil
""")

st.sidebar.markdown("---")
st.sidebar.caption("🚀 .NET 9 + Streamlit")
st.sidebar.caption("📅 November 2025")

# Instructions to run the app:
# Powershell commands (WINDOWS):
# 1. cd "c:\Users\Brent\Desktop\3APP\Machine Learning\Cloud AI\bralma_ML_Project\Bralma_frontend"
# 2. streamlit run App.py
# 3. Open browser: http://localhost:8501
import streamlit as st

# Homepage configuration
st.set_page_config(
    page_title="🤖 ML Predictions Hub",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Machine Learning Predictions Hub")
st.markdown("### Welkom bij het ML voorspellings platform")

st.markdown("---")

# Introduction
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ## ⚡ Electricity Demand Predictor
    
    Voorspel **UK elektriciteitsvraag** op basis van:
    - 🌬️ Windkracht (5 categorieën)
    - ☀️ Zonne-energie (auto-berekend)
    - ⏰ Tijdstip (48 settlement periods)
    - 📅 Seizoen (winter/lente/zomer/herfst)
    
    **Features:**
    - Eenvoudige voorspelling (1 waarde)
    - 24-uurs forecast met grafieken
    - Hernieuwbaar energie percentage
    - Download CSV forecast data
    
    **Dataset:** UK National Grid 2001-2017 (~300k observaties)
    """)
    
    st.page_link("pages/0_Electricity_Demand.py", label="➡️ Ga naar Electricity Demand", icon="⚡")

with col2:
    st.markdown("""
    ## 🏠 UK Housing Type Predictor
    
    Voorspel **property type** (D/S/T/F) op basis van:
    - 💰 Prijs (5 categorieën of exact)
    - 📍 Locatie (stad, county, regio)
    - 🏗️ Kenmerken (freehold/leasehold, nieuw/oud)
    
    **Property Types:**
    - **D** = Detached (vrijstaand)
    - **S** = Semi-detached (2-onder-1-kap)
    - **T** = Terraced (rijtjeshuis)
    - **F** = Flat (appartement)
    
    **Dataset:** UK Land Registry 2001-2017 (~1.5M transacties)
    """)
    
    st.page_link("pages/1_🏠_UK_Housing.py", label="➡️ Ga naar UK Housing", icon="🏠")

st.markdown("---")

# Quick stats
st.markdown("## 📊 Platform Overzicht")

col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)

with col_stat1:
    st.metric("📁 Datasets", "2", help="Electricity + Housing")

with col_stat2:
    st.metric("🤖 ML Models", "2", help="Regression + Classification")

with col_stat3:
    st.metric("📊 Training Data", "1.8M+", help="Combined observations")

with col_stat4:
    st.metric("📅 Periode", "2001-2017", help="17 jaar UK data")

st.markdown("---")

# Features comparison
st.markdown("## 🔍 Model Vergelijking")

comparison_df = {
    "Aspect": ["Type", "Input Features", "Output", "Accuracy", "Use Case"],
    "⚡ Electricity": [
        "Regression", 
        "13 (wind, solar, tijd, interconnectors)",
        "MW demand (continue waarde)",
        "RMSE ~1500 MW",
        "Grid balancing, forecasting"
    ],
    "🏠 Housing": [
        "Classification",
        "8 (prijs, locatie, duration, old/new)",
        "Property type (D/S/T/F)",
        "~75-85%",
        "Valuation, market analysis"
    ]
}

import pandas as pd
st.dataframe(pd.DataFrame(comparison_df), use_container_width=True, hide_index=True)

st.markdown("---")

# Architecture info
col_arch1, col_arch2 = st.columns(2)

with col_arch1:
    st.markdown("""
    ## 🏗️ Technische Architectuur
    
    **Frontend:**
    - Streamlit (Python) - Multi-page app
    - Plotly - Interactieve grafieken
    - User-friendly input (categorieën → API waardes)
    
    **Backend:**
    - .NET 9 Web API
    - ML.NET / scikit-learn models
    - Render.com deployment (free tier)
    
    **Data:**
    - UK National Grid ESO (electricity)
    - UK Land Registry (housing)
    - Cleaned & processed (outliers behandeld)
    """)

with col_arch2:
    st.markdown("""
    ## 📚 Belangrijke Overwegingen
    
    **UX Design:**
    - ❌ **Niet**: "3124 MW wind" (te technisch)
    - ✅ **Wel**: "Matig wind" (begrijpelijk)
    - Auto-calculate solar op basis van tijd + seizoen
    
    **API Realisme:**
    - Wind categorie → realistic MW (capacity factors)
    - Prijs categorie → typical GBP ranges
    - Default waardes voor complexe features
    
    **Voorspelling Quality:**
    - Multiple inputs → betere accuracy
    - Context info (typical ranges, regio effects)
    - Probability distributions (housing)
    """)

st.markdown("---")

# Quick start guide
st.markdown("## 🚀 Aan de Slag")

st.markdown("""
### 1️⃣ Kies een Model

**Electricity Demand** - Als je wilt weten:
- Hoeveel stroom nodig bij bepaalde wind/zon condities
- Peak demand tijden (17-20u winter)
- Impact van hernieuwbare energie op grid

**UK Housing** - Als je wilt weten:
- Welk type property bij bepaalde prijs/locatie
- Verschil tussen London en Manchester prijzen
- Freehold vs Leasehold impact

### 2️⃣ Vul Inputs In

- Gebruik **categorieën** voor gemak (Matig wind, Middensegment prijs)
- Of **exacte waardes** voor precisie (1800 MW, £245,000)
- Geavanceerde opties zijn optioneel (defaults zijn goed)

### 3️⃣ Analyseer Resultaat

- **Voorspelling** + confidence/probability
- **Visualisaties** (pie charts, line graphs)
- **Context** (typische ranges, interpretatie)

### 4️⃣ Experimenteer

- Probeer verschillende scenario's
- Vergelijk winter vs zomer (electricity)
- Vergelijk London vs Leeds (housing)
- Download forecast data (CSV)
""")

st.markdown("---")

# Footer
st.sidebar.title("🤖 ML Predictions")
st.sidebar.markdown("### Navigatie")
st.sidebar.page_link("pages/0_Electricity_Demand.py", label="⚡ Electricity Demand")
st.sidebar.page_link("pages/1_🏠_UK_Housing.py", label="🏠 UK Housing")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔗 Links")
st.sidebar.markdown("[GitHub Repository](https://github.com/Team-3-Machine-Learning/bralma_ML_Project)")
st.sidebar.markdown("[API Swagger](https://bralma-backend.onrender.com/swagger)")

st.sidebar.markdown("---")
st.sidebar.caption("🚀 Powered by .NET 9 + Streamlit")
st.sidebar.caption("📅 November 2025")
st.sidebar.caption("🎓 Machine Learning - Cloud AI")

# API status check
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔗 API Status")

import requests
API_URL = "https://bralma-backend.onrender.com"

try:
    health_check = requests.get(f"{API_URL}/health", timeout=5)
    if health_check.status_code == 200:
        st.sidebar.success("✅ Backend Online")
    else:
        st.sidebar.error("❌ API Error")
except:
    st.sidebar.warning("⚠️ Backend Offline")
    st.sidebar.caption("Render.com wake-up: ~15 sec")

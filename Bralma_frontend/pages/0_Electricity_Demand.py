import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import math
from datetime import datetime, date

# Page configuration
st.set_page_config(page_title="⚡ Electricity Demand", layout="wide", page_icon="⚡")
st.title("⚡ UK Electricity Demand Predictor")
st.markdown("*Voorspel de elektriciteitsvraag op basis van weer, tijd en seizoen*")

# API URL
API_URL = "https://bralma-ml-project.onrender.co/prediction/elecdemand"

# Mapping functies: User-friendly → API values
def map_wind_to_mw(category, capacity=6000):
    """Map wind category to realistic MW generation"""
    mapping = {
        "Geen (windstil)": 0.02,      # 2% capacity factor
        "Weinig": 0.15,                # 15%
        "Matig": 0.30,                 # 30% (typical average)
        "Veel": 0.60,                  # 60%
        "Storm": 0.90                  # 90% (near max)
    }
    return int(capacity * mapping.get(category, 0.30))

def map_season_to_solar_factor(season):
    """Map season to solar capacity factor multiplier"""
    mapping = {
        "Winter": 0.15,    # Short days, low sun
        "Lente": 0.50,     # Medium
        "Zomer": 0.80,     # Long days, high sun
        "Herfst": 0.40     # Medium-low
    }
    return mapping.get(season, 0.50)

def calculate_solar_generation(hour, season, solar_capacity=13000):
    """Calculate solar based on time of day + season"""
    # Solar only between 6:00-20:00
    if hour < 6 or hour > 20:
        return 0
    
    # Sine curve centered at 13:00
    solar_factor = math.sin((hour - 6) * math.pi / 14)
    season_factor = map_season_to_solar_factor(season)
    
    return int(solar_capacity * season_factor * max(0, solar_factor))

def get_time_label(settlement_period):
    """Convert settlement period to readable time label"""
    hour = (settlement_period - 1) // 2
    if 0 <= hour < 6:
        return "🌙 Nacht"
    elif 6 <= hour < 12:
        return "🌅 Ochtend"
    elif 12 <= hour < 18:
        return "☀️ Middag"
    else:
        return "🌆 Avond"

# API prediction function
def predict_demand_api(payload):
    """Call API with full feature set"""
    try:
        response = requests.post(
            f"{API_URL}",
            json=payload,
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get('prediction'), data.get('confidence', None)
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None, None
            
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Kan niet verbinden met API. Backend is mogelijk aan het opstarten (15 sec wachten).")
        return None, None
    except requests.exceptions.Timeout:
        st.error("⏱️ API timeout - probeer opnieuw.")
        return None, None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None, None

# Create tabs for better organization
tab1, tab2 = st.tabs(["🎯 Voorspelling", "ℹ️ Info"])

with tab1:
    st.subheader("🎯 Eenvoudige Voorspelling")
    st.markdown("*Kies begrijpelijke opties - wij vertalen het naar technische waardes*")
    
    # Layout: 2 columns (simplified)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📅 Wanneer?")
        
        # Season selection
        season = st.selectbox(
            "Seizoen",
            ["Winter", "Lente", "Zomer", "Herfst"],
            index=0,
            help="Bepaalt zonlicht beschikbaarheid"
        )
        
        # Time of day (simplified slider)
        settlement_period = st.slider(
            "Tijdstip van de dag", 
            min_value=1, 
            max_value=48, 
            value=36,
            format="%d",
            help="Sleep om tijd te kiezen (1-48 = 00:00-23:30)"
        )
        
        # Calculate and display readable time
        hour = (settlement_period - 1) // 2
        minute = "00" if settlement_period % 2 == 1 else "30"
        time_label = get_time_label(settlement_period)
        
        st.info(f"⏰ **{time_label}** ({hour:02d}:{minute})")
        
        # Show typical demand for this time
        if hour in [17, 18, 19]:
            st.warning("⚡ **Peak demand** periode (17:00-20:00)")
        elif hour in [0, 1, 2, 3, 4]:
            st.success("💤 **Laag demand** periode (nacht)")
    
    with col2:
        st.markdown("### 🌬️☀️ Weer Condities")
        
        # Wind category (user-friendly)
        wind_category = st.select_slider(
            "Windkracht",
            options=["Geen (windstil)", "Weinig", "Matig", "Veel", "Storm"],
            value="Matig",
            help="Hoeveel wind is er? Dit bepaalt wind energie productie"
        )
        
        # Calculate wind generation based on category
        wind_capacity = 6000  # Realistic 2017 capacity
        wind_generation = map_wind_to_mw(wind_category, wind_capacity)
        wind_utilization = (wind_generation / wind_capacity * 100)
        
        # Show calculated wind values
        col_wind1, col_wind2 = st.columns(2)
        with col_wind1:
            st.metric("🌬️ Wind Productie", f"{wind_generation:,} MW")
        with col_wind2:
            st.metric("Benutting", f"{wind_utilization:.0f}%")
        
        # Solar is auto-calculated (tijd + seizoen)
        solar_capacity = 12000  # Realistic 2017 capacity
        solar_generation = calculate_solar_generation(hour, season, solar_capacity)
        solar_utilization = (solar_generation / solar_capacity * 100) if solar_capacity > 0 else 0
        
        st.markdown("---")
        
        # Show calculated solar values
        col_solar1, col_solar2 = st.columns(2)
        with col_solar1:
            st.metric("☀️ Solar Productie", f"{solar_generation:,} MW")
        with col_solar2:
            st.metric("Benutting", f"{solar_utilization:.0f}%")
        
        if solar_generation == 0:
            st.caption("🌙 Geen zonne-energie ('s nachts)")
        elif solar_utilization > 60:
            st.caption("☀️ Uitstekende zon conditie!")
    
        england_wales_demand = 25000
    
    # Predict button
    st.markdown("---")
    
    # Summary before prediction
    col_sum1, col_sum2, col_sum3 = st.columns(3)
    with col_sum1:
        st.info(f"📅 {season} | {time_label}")
    with col_sum2:
        st.info(f"🌬️ {wind_category}")
    with col_sum3:
        renewable_total = wind_generation + solar_generation
        st.info(f"♻️ {renewable_total:,} MW hernieuwbaar")
    
    if st.button("🚀 Voorspel Demand", type="primary", use_container_width=True):
        # Build payload for API
        payload = {
            "settlement_period": settlement_period,
            "embedded_wind_generation": float(wind_generation),
            "embedded_wind_capacity": float(wind_capacity),
            "embedded_solar_generation": float(solar_generation),
            "embedded_solar_capacity": float(solar_capacity)
        }
        
        with st.spinner("⏳ API call in progress..."):
            prediction, confidence = predict_demand_api(payload)
            
            if prediction is not None:
                # Display results
                st.markdown("### 🎯 Resultaten")
                col_res1, col_res2, col_res3 = st.columns(3)
                
                with col_res1:
                    st.metric(
                        "Voorspelde Vraag", 
                        f"{prediction:,.0f} MW"
                    )
                
                with col_res2:
                    renewable_pct = ((wind_generation + solar_generation) / prediction * 100) if prediction > 0 else 0
                    st.metric("♻️ Hernieuwbaar Aandeel", f"{renewable_pct:.1f}%")
                
                with col_res3:
                    if confidence:
                        st.metric("📊 Betrouwbaarheid", f"{confidence:.1%}")
                    else:
                        # Calculate typical demand range for context
                        if hour in [17, 18, 19]:
                            st.metric("Typisch (17-20u)", "40-48k MW")
                        elif hour in [0, 1, 2, 3]:
                            st.metric("Typisch (nacht)", "20-25k MW")
                        else:
                            st.metric("Typisch (dag)", "25-35k MW")
                
                st.success("✅ Voorspelling succesvol!")
                
with tab2:
    st.subheader("ℹ️ Over deze applicatie")
    
    col_info1, col_info2 = st.columns(2)
    
    with col_info1:
        st.markdown("""
        ### 🎯 Wat doet deze app?
        
        Voorspel **UK elektriciteitsvraag** op basis van:
        - ⏰ **Tijdstip**: Peak (18:00) vs nacht (03:00)
        - 📅 **Seizoen**: Winter vs zomer (solar impact)
        - 🌬️ **Windkracht**: Geen → Storm (5 categorieën)
        - ☀️ **Zonne-energie**: Auto-berekend op basis van tijd + seizoen
        
        ### 🧠 Waarom deze aanpak?
        
        **Probleem**: Gewone gebruikers kennen geen "3124 MW wind generation"
        
        **Oplossing**: 
        - 👤 **User-friendly**: Kies "Veel wind" of "Weinig wind"
        - 🤖 **Backend mapping**: App vertaalt naar realistische MW waardes
        - 📊 **Realistisch**: Gebaseerd op 2017 UK grid capaciteit
        
        ### 📊 Wat zijn Settlement Periods?
        
        - **48 periodes per dag** (elk 30 minuten)
        - Period 1 = 00:00-00:30
        - Period 36 = 18:00-18:30 (typisch **peak demand**)
        - Period 48 = 23:30-00:00
        
        ### 🌬️ Windkracht → MW Conversie
        
        | Categorie | Capacity Factor | MW (bij 6 GW capaciteit) |
        |-----------|----------------|---------------------------|
        | Geen (windstil) | 2% | ~120 MW |
        | Weinig | 15% | ~900 MW |
        | **Matig** | 30% | **~1,800 MW** |
        | Veel | 60% | ~3,600 MW |
        | Storm | 90% | ~5,400 MW |
        
        *Matig wind (30%) = UK gemiddelde over een jaar*
        """)
    
    with col_info2:
        st.markdown("""
        ### ☀️ Solar Berekening
        
        **Automatisch berekend** op basis van:
        1. **Tijdstip**: 0 MW 's nachts, max rond 13:00
        2. **Seizoen**: 
           - Winter: 15% max capacity
           - Lente: 50%
           - Zomer: 80%
           - Herfst: 40%
        
        **Voorbeeld** (12 GW capaciteit):
        - Zomer, 13:00 → ~9,600 MW (80% × 12 GW)
        - Winter, 13:00 → ~1,800 MW (15% × 12 GW)
        - Altijd 0 tussen 20:00-06:00
        
        ### 🔌 Interconnectors (Geavanceerd)
        
        Verbindingen met buurlanden:
        - **IFA2** 🇫🇷 France (1000 MW)
        - **BritNed** 🇳🇱 Netherlands (1000 MW)
        - **Moyle** Northern Ireland (500 MW)
        - **East-West** 🇮🇪 Ireland (500 MW)
        - **Nemo** 🇧🇪 Belgium (1000 MW)
        
        *Default waardes: typisch import scenario (UK importeert meestal)*
        
        ### 🤖 Model Informatie
        
        - **Trainingsdata**: UK electricity 2001-2017 (16 jaar)
        - **Features**: 13 input variabelen
        - **API**: .NET 9 backend (Render.com)
        - **Latency**: ~500ms per voorspelling
        - **Free tier**: 15sec wake-up tijd (first request)
        
        ### 📚 Bronnen
        
        - **Data**: UK National Grid ESO
        - **Capaciteit 2017**: 
          - Wind: ~6 GW embedded
          - Solar: ~12 GW embedded
        - **Typische vraag**: 
          - Nacht: 20-25 GW
          - Dag: 30-40 GW  
          - Peak: 45-50 GW (winter evening)
        
        ### 🔗 Links
        
        - [GitHub Repository](https://github.com/Team-3-Machine-Learning/bralma_ML_Project)
        - [API Swagger]({API_URL}/swagger)
        
        ### 👥 Team
        
        **Machine Learning - Cloud AI**  
        November 2025
        
        ---
        
        💡 **Tip**: Probeer verschillende scenario's:
        - Winter nacht + weinig wind = hoge vraag + weinig hernieuwbaar
        - Zomer middag + veel wind = lagere vraag + veel hernieuwbaar
        """)

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
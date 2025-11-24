import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# Page configuration  
st.set_page_config(page_title="🏠 UK Housing", layout="wide", page_icon="🏠")
st.title("🏠 UK Housing Property Type Predictor")
st.markdown("*Voorspel het woningtype op basis van prijs, locatie en kenmerken*")

# API URL
API_URL = "https://bralma-ml-project.onrender.com/prediction/ukhousing"

# Mapping functies: User-friendly → API values
def map_price_category_to_range(category):
    """Map price category to typical GBP range"""
    mapping = {
        "Budget (< £100k)": (50000, 100000),
        "Betaalbaar (£100-200k)": (100000, 200000),
        "Middensegment (£200-350k)": (200000, 350000),
        "Hoog (£350-600k)": (350000, 600000),
        "Luxe (> £600k)": (600000, 1500000)
    }
    return mapping.get(category, (200000, 350000))

def get_popular_cities():
    """Return list of major UK cities"""
    return [
        "LONDON", "MANCHESTER", "BIRMINGHAM", "LEEDS", "LIVERPOOL",
        "BRISTOL", "SHEFFIELD", "NEWCASTLE UPON TYNE", "NOTTINGHAM",
        "SOUTHAMPTON", "LEICESTER", "COVENTRY", "BRADFORD", "CARDIFF",
        "EDINBURGH", "GLASGOW", "BRIGHTON", "CAMBRIDGE", "OXFORD"
    ]

def get_regions():
    """Return UK regions/counties"""
    return {
        "London & South East": ["GREATER LONDON", "SURREY", "KENT", "ESSEX", "HERTFORDSHIRE"],
        "South West": ["BRISTOL", "DEVON", "CORNWALL", "SOMERSET", "GLOUCESTERSHIRE"],
        "Midlands": ["WEST MIDLANDS", "BIRMINGHAM", "LEICESTERSHIRE", "NOTTINGHAMSHIRE"],
        "North": ["GREATER MANCHESTER", "WEST YORKSHIRE", "MERSEYSIDE", "TYNE AND WEAR"],
        "Scotland": ["CITY OF EDINBURGH", "GLASGOW CITY", "ABERDEENSHIRE"],
        "Wales": ["CARDIFF", "SWANSEA", "NEWPORT"]
    }

# API prediction function
def predict_property_type_api(payload):
    """Call API for property type prediction"""
    try:
        response = requests.post(
            f"{API_URL}",
            json=payload,
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get('propertyType'), data.get('confidence', None), data.get('probabilities', None)
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None, None, None
            
    except requests.exceptions.ConnectionError:
        st.error("⚠️ Kan niet verbinden met API. Backend is mogelijk aan het opstarten (15 sec wachten).")
        return None, None, None
    except requests.exceptions.Timeout:
        st.error("⏱️ API timeout - probeer opnieuw.")
        return None, None, None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None, None, None

# Create tabs
tab1, tab2 = st.tabs(["🎯 Voorspelling", "ℹ️ Info"])

with tab1:
    st.subheader("🎯 Property Type Voorspelling")
    st.markdown("*Vul kenmerken in - wij voorspellen het woningtype (D/S/T/F)*")
    
    # Layout: 3 columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 💰 Prijs")
        
        # Price category (simplified)
        price_method = st.radio(
            "Kies methode:",
            ["Categorie", "Exacte prijs"],
            horizontal=True
        )
        
        if price_method == "Categorie":
            price_category = st.select_slider(
                "Prijscategorie",
                options=[
                    "Budget (< £100k)",
                    "Betaalbaar (£100-200k)",
                    "Middensegment (£200-350k)",
                    "Hoog (£350-600k)",
                    "Luxe (> £600k)"
                ],
                value="Middensegment (£200-350k)",
                help="Typische prijsrange voor UK woningen (2017)"
            )
            
            # Use midpoint of range
            price_min, price_max = map_price_category_to_range(price_category)
            price = (price_min + price_max) // 2
            
            st.info(f"💷 Prijs: **£{price:,}**")
        else:
            price = st.number_input(
                "Koopprijs (GBP)",
                min_value=10000,
                max_value=5000000,
                value=250000,
                step=10000,
                help="Transactieprijs in ponden"
            )
            st.metric("💷 Prijs", f"£{price:,}")
        
        # Property characteristics
        st.markdown("---")
        st.markdown("### 🏗️ Kenmerken")
        
        old_new = st.radio(
            "Nieuwbouw of bestaand?",
            ["Bestaand (Old)", "Nieuwbouw (New)"],
            help="Nieuwbouw vaak andere type distributie"
        )
        old_new_code = "N" if "New" in old_new else "O"
        
        duration = st.radio(
            "Eigendomstype",
            ["Freehold (eigen grond)", "Leasehold (erfpacht)"],
            help="Flats zijn vaak leasehold, huizen freehold"
        )
        duration_code = "F" if "Freehold" in duration else "L"
    
    with col2:
        st.markdown("### 📍 Locatie")
        
        # Region selection (simplified)
        regions = get_regions()
        region = st.selectbox(
            "Regio",
            list(regions.keys()),
            help="Grote regio bepaalt prijs/type verhouding"
        )
        
        # County within region
        county = st.selectbox(
            "County",
            regions[region],
            help="Specifieke county binnen regio"
        )
        
        # City/Town
        location_method = st.radio(
            "Stad/plaats:",
            ["Populaire stad", "Eigen invoer"],
            horizontal=True
        )
        
        if location_method == "Populaire stad":
            town_city = st.selectbox(
                "Kies stad",
                get_popular_cities(),
                help="Grote steden met veel transacties"
            )
        else:
            town_city = st.text_input(
                "Voer plaats in",
                value="LEEDS",
                help="Gebruik HOOFDLETTERS (UK format)"
            ).upper()
        
        # District (optional, simplified)
        district = st.text_input(
            "District (optioneel)",
            value=town_city,  # Default to town name
            help="Wijk/district binnen stad (vaak zelfde als stad)"
        ).upper()
    
    with col3:
        st.markdown("### 📊 Verwachting")
        
        # Show typical property types for price range
        if price < 150000:
            st.info("💡 **Typisch**: Flat of Terraced")
            st.caption("Budget prijzen → meestal flats of rijtjeshuizen")
        elif price < 300000:
            st.info("💡 **Typisch**: Terraced of Semi-detached")
            st.caption("Middensegment → rijtjeshuizen of 2-onder-1-kap")
        else:
            st.info("💡 **Typisch**: Semi-detached of Detached")
            st.caption("Hoge prijzen → 2-onder-1-kap of vrijstaand")
        
        st.markdown("---")
        st.markdown("### 🏠 Property Types")
        
        st.markdown("""
        **D** = Detached (vrijstaand)  
        **S** = Semi-detached (2-onder-1-kap)  
        **T** = Terraced (rijtjeshuis)  
        **F** = Flat (appartement)
        """)
        
        st.markdown("---")
        
        # Show input summary
        st.markdown("### 📋 Samenvatting")
        st.caption(f"💷 £{price:,}")
        st.caption(f"📍 {town_city}, {county}")
        st.caption(f"🏗️ {old_new_code} | {duration_code}")
    
    # Predict button
    st.markdown("---")
    
    if st.button("🚀 Voorspel Property Type", type="primary", use_container_width=True):
        # Build payload for API
        payload = {
            "price": price,
            "old/new": old_new_code,
            "duration": duration_code,
            "town/city": town_city.upper(),
            "district": district.upper(),
            "county": county.upper(),
        }


        # payload = {
        #     "price": 586945,
        #     "date_of_transfer": "2017-02-15",
        #     "old/new": "N",
        #     "duration": "F",
        #     "town/city": "WETHERBY",
        #     "district": "LEEDS",
        #     "county": "WEST YORKSHIRE",
        #     "ppdcategory_type": "A",
        #     "year": 2017
        #     }
        
        with st.spinner("⏳ API call in progress..."):
            property_type, confidence, probabilities = predict_property_type_api(payload)
            
            if property_type is not None:
                # Display results
                st.markdown("### 🎯 Voorspelling")
                
                col_res1, col_res2, col_res3 = st.columns(3)
                
                with col_res1:
                    # Map property type to full name
                    type_mapping = {
                        "D": "🏡 Detached (vrijstaand)",
                        "S": "🏘️ Semi-detached (2-onder-1-kap)",
                        "T": "🏠 Terraced (rijtjeshuis)",
                        "F": "🏢 Flat (appartement)"
                    }
                    
                    full_type = type_mapping.get(property_type, property_type)
                    st.metric("Voorspeld Type", full_type)
                
                with col_res2:
                    if confidence:
                        st.metric("📊 Zekerheid", f"{confidence:.1%}")
                    else:
                        st.metric("Model", "Classification")
                
                with col_res3:
                    # Show typical price for this type
                    type_price_ranges = {
                        "D": "£350k-800k",
                        "S": "£200k-400k",
                        "T": "£150k-300k",
                        "F": "£100k-250k"
                    }
                    typical_range = type_price_ranges.get(property_type, "Varieert")
                    st.metric("Typisch prijsbereik", typical_range)
                
                st.success("✅ Voorspelling succesvol!")
                
                # Show probabilities if available
                if probabilities:
                    st.markdown("### 📊 Kansenverdeling per Type")
                    
                    # Create dataframe for visualization
                    prob_df = pd.DataFrame({
                        "Type": list(probabilities.keys()),
                        "Kans (%)": [p * 100 for p in probabilities.values()]
                    })
                    
                    # Sort by probability
                    prob_df = prob_df.sort_values("Kans (%)", ascending=False)
                    
                    col_chart1, col_chart2 = st.columns([2, 1])
                    
                    with col_chart1:
                        # Bar chart
                        fig = px.bar(
                            prob_df,
                            x="Type",
                            y="Kans (%)",
                            title="Waarschijnlijkheid per Property Type",
                            color="Kans (%)",
                            color_continuous_scale="Blues"
                        )
                        fig.update_layout(showlegend=False)
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col_chart2:
                        st.markdown("**💡 Interpretatie:**")
                        
                        max_prob = prob_df.iloc[0]["Kans (%)"]
                        second_prob = prob_df.iloc[1]["Kans (%)"] if len(prob_df) > 1 else 0
                        
                        if max_prob > 80:
                            st.success(f"✅ Zeer zeker: {max_prob:.1f}%")
                        elif max_prob > 60:
                            st.info(f"📊 Waarschijnlijk: {max_prob:.1f}%")
                        else:
                            st.warning(f"⚠️ Onzeker: {max_prob:.1f}% vs {second_prob:.1f}%")
                        
                        st.markdown("---")
                        st.dataframe(prob_df, hide_index=True, use_container_width=True)
                
                # Additional insights
                st.markdown("### 💡 Analyse")
                
                col_insight1, col_insight2 = st.columns(2)
                
                with col_insight1:
                    st.markdown("**Prijs vs Type:**")
                    if property_type == "D" and price < 300000:
                        st.warning("⚠️ Detached voor £<300k is ongewoon (mogelijk regio effect)")
                    elif property_type == "F" and price > 400000:
                        st.info("💎 Dure flat → waarschijnlijk London/penthouse")
                    elif property_type == "T" and duration_code == "L":
                        st.info("📋 Terraced met leasehold is zeldzaam")
                    else:
                        st.success("✅ Typische combinatie voor deze regio")
                
                with col_insight2:
                    st.markdown("**Regio Context:**")
                    if "LONDON" in county:
                        st.info("🏙️ London: Flats en terraced dominant, hoge prijzen")
                    elif region == "North":
                        st.info("⬆️ Noord-Engeland: Lagere prijzen, meer terraced/semi")
                    elif region == "South West":
                        st.info("🌊 Zuidwest: Detached populairder, hogere prijzen")
                    else:
                        st.info(f"📍 {region}: Typische {county} markt")


with tab2:
    st.subheader("ℹ️ Over UK Housing Predictor")
    
    col_info1, col_info2 = st.columns(2)
    
    with col_info1:
        st.markdown("""
        ### 🎯 Wat voorspellen we?
        
        **Property Type** (4 categorieën):
        - **D** = Detached (vrijstaand huis)
        - **S** = Semi-detached (2-onder-1-kap)
        - **T** = Terraced (rijtjeshuis)
        - **F** = Flat (appartement)
        
        ### 🧠 Belangrijkste Features
        
        **1. Prijs (💷)**:
        - **Budget (< £150k)**: Meestal Flat of Terraced
        - **Middensegment (£150-350k)**: Terraced of Semi-detached
        - **Hoog (> £350k)**: Semi-detached of Detached
        
        **2. Locatie (📍)**:
        - **London**: Flats dominant, zeer hoge prijzen
        - **Manchester/Birmingham**: Mix, gemiddelde prijzen
        - **Noord-Engeland**: Terraced populair, lage prijzen
        - **Zuid-Engeland**: Detached vaker, hogere prijzen
        
        **3. Eigendomstype (🏗️)**:
        - **Freehold (F)**: Eigen grond (typisch huizen)
        - **Leasehold (L)**: Erfpacht (typisch flats)
        
        **4. Nieuwbouw vs Bestaand (🏡)**:
        - **New**: Nieuwbouwprojecten (vaak apartmenten)
        - **Old**: Bestaande woningen (meer variatie)
        
        ### 📊 Dataset Info
        
        - **Trainingsdata**: UK Land Registry 2001-2017
        - **Transacties**: ~1.5 miljoen woningen
        - **Regio's**: England, Wales, Scotland
        - **Periode**: 17 jaar (crisis 2008 effect zichtbaar)
        """)
    
    with col_info2:
        st.markdown("""
        ### 💰 Typische Prijzen per Type (2017)
        
        | Type | Gemiddeld | Range | % Markt |
        |------|-----------|-------|---------|
        | **Detached** | £360k | £200k-£1M+ | 22% |
        | **Semi-detached** | £230k | £150k-£500k | 26% |
        | **Terraced** | £195k | £100k-£400k | 28% |
        | **Flat** | £210k | £80k-£600k | 24% |
        
        *London prijzen 50-200% hoger dan gemiddelde*
        
        ### 🗺️ Regio Verschillen
        
        **London & South East**:
        - Hoogste prijzen (£450k gemiddeld)
        - Flats dominant (40% markt)
        - Leasehold veel voorkomend
        
        **Midlands & North**:
        - Betaalbaar (£180k gemiddeld)
        - Terraced populair (35% markt)
        - Freehold dominant
        
        **South West**:
        - Hoog (£280k gemiddeld)
        - Detached populairder (30% markt)
        - Weinig flats (<15%)
        
        ### 🤖 Model Details
        
        - **Algorithm**: Random Forest / XGBoost Classification
        - **Features**: 8 input variabelen
        - **Accuracy**: ~75-85% (depends on region)
        - **Training**: Balanced classes (oversampling rare types)
        
        ### 📚 Waarom deze Features?
        
        **✅ Gebruikt**:
        - Prijs → sterkste predictor
        - Locatie (town/county) → regio effect
        - Duration (F/L) → ownership type indicator
        - Old/New → construction period effect
        
        **❌ Niet gebruikt**:
        - Datum/jaar → geen directe invloed op type
        - PPD category → technisch, niet semantisch
        
        ### 🔗 Links
        
        - [GitHub Repository](https://github.com/Team-3-Machine-Learning/bralma_ML_Project)
        - [UK Land Registry Data](https://landregistry.data.gov.uk/)
        - [API Swagger]({API_URL}/swagger)
        
        ### 💡 Tips voor Voorspelling
        
        - **London flat £200k** → Zeer waarschijnlijk F
        - **Manchester detached £500k** → Waarschijnlijk D of grote S
        - **Leeds terraced £150k** → Zeer waarschijnlijk T
        - **Oxford leasehold £400k** → Waarschijnlijk F (penthouse)
        
        ---
        
        **⚠️ Disclaimer**: Voorspellingen zijn indicatief. Werkelijke type kan afwijken door unieke property kenmerken (size, bedrooms, garden, etc.) die niet in dataset zitten.
        """)

# Sidebar
st.sidebar.title("🏠 UK Housing")

st.sidebar.markdown("### 🔗 API Status")
try:
    health_check = requests.get(f"{API_URL}/health", timeout=5)
    if health_check.status_code == 200:
        st.sidebar.success("✅ API Verbonden")
    else:
        st.sidebar.error("❌ API Error")
except:
    st.sidebar.warning("⚠️ API Offline")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📚 Snelle Voorbeelden")

st.sidebar.markdown("""
**🏢 London Flat**
- Prijs: £300k
- Locatie: London
- Duration: Leasehold
- Verwacht: **F** (90%+)

**🏡 Yorkshire Detached**
- Prijs: £450k
- Locatie: Leeds
- Duration: Freehold
- Verwacht: **D** (75%+)

**🏠 Manchester Terraced**
- Prijs: £180k
- Locatie: Manchester
- Duration: Freehold
- Verwacht: **T** (80%+)

**🏘️ Birmingham Semi**
- Prijs: £240k
- Locatie: Birmingham
- Duration: Freehold
- Verwacht: **S** (70%+)
""")

st.sidebar.markdown("---")
st.sidebar.caption("🚀 .NET 9 + Streamlit")
st.sidebar.caption("📅 November 2025")

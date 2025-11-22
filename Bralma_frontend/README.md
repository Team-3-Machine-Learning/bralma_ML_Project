# 🤖 ML Predictions Frontend

Multi-page Streamlit applicatie voor Machine Learning voorspellingen.

## 📁 Structuur

```
Bralma_frontend/
├── Home.py                           # Homepage (landing page)
├── pages/
│   ├── 0_Electricity_Demand.py      # ⚡ UK Electricity Demand Predictor
│   └── 1_🏠_UK_Housing.py            # 🏠 UK Housing Type Predictor
└── README.md                         # Deze file
```

## 🚀 Starten

### Windows PowerShell:

```powershell
# 1. Activeer virtual environment
cd "c:\Users\Brent\Desktop\3APP\Machine Learning\Cloud AI"
.\.venv\Scripts\Activate.ps1

# 2. Navigeer naar frontend folder
cd "bralma_ML_Project\Bralma_frontend"

# 3. Start Streamlit (opent Home.py automatisch)
streamlit run Home.py
```

### Browser:
- **URL**: http://localhost:8501
- **Auto-reload**: Bij code wijzigingen (development mode)

## 📊 Pagina's

### 🏠 **Home** (`Home.py`)
- Landing page met overzicht
- Model vergelijking (Electricity vs Housing)
- Quick start guide
- API status check

### ⚡ **Electricity Demand** (`pages/0_Electricity_Demand.py`)
**Functionaliteit:**
- Voorspel UK elektriciteitsvraag (MW)
- Input: Seizoen, tijd, windkracht (categorieën)
- Auto-calculate: Solar op basis van tijd + seizoen
- 24-uurs forecast met grafieken

**Features:**
- User-friendly categorieën (Geen/Weinig/Matig/Veel/Storm wind)
- Realistische mapping naar MW waardes (capacity factors)
- Hernieuwbaar energie percentage
- Download CSV forecast

**API Endpoint:**
```
POST https://bralma-backend.onrender.com/api/predict
```

### 🏠 **UK Housing** (`pages/1_🏠_UK_Housing.py`)
**Functionaliteit:**
- Voorspel property type (D/S/T/F)
- Input: Prijs, locatie, kenmerken
- Output: Type + probability distribution

**Property Types:**
- **D** = Detached (vrijstaand)
- **S** = Semi-detached (2-onder-1-kap)
- **T** = Terraced (rijtjeshuis)
- **F** = Flat (appartement)

**Features:**
- Prijs categorieën (Budget → Luxe) of exact bedrag
- Populaire steden dropdown (London, Manchester, etc.)
- Regio context (London vs Noord vs Zuid)
- Probability bar chart

**API Endpoint:**
```
POST https://bralma-backend.onrender.com/api/housing/predict
```

## 🎨 UX Design Principes

### ✅ **User-Friendly Inputs**

**Probleem:** Eindgebruikers kennen geen "3124 MW wind generation"

**Oplossing:**
- **Frontend**: "Matig wind" (categorie)
- **Backend**: Vertaal naar 1800 MW (30% capacity factor van 6 GW)
- **Transparant**: Toon berekende MW waarde aan gebruiker

### 📊 **Mapping Logica**

**Electricity - Wind:**
```python
"Geen (windstil)" → 2% capacity  → ~120 MW
"Weinig"          → 15%           → ~900 MW
"Matig"           → 30% (UK avg) → ~1,800 MW
"Veel"            → 60%           → ~3,600 MW
"Storm"           → 90%           → ~5,400 MW
```

**Electricity - Solar:**
- Auto-berekend: `sine curve × seizoen factor × capaciteit`
- Winter 13:00 → 15% × 0.5 × 12 GW = ~900 MW
- Zomer 13:00  → 80% × 1.0 × 12 GW = ~9,600 MW
- Nacht (20-06u) → 0 MW (always)

**Housing - Price:**
```python
"Budget (< £100k)"        → midpoint £75k
"Betaalbaar (£100-200k)"  → midpoint £150k
"Middensegment (£200-350k)" → midpoint £275k
"Hoog (£350-600k)"        → midpoint £475k
"Luxe (> £600k)"          → midpoint £1M
```

## 🔧 Technische Details

### **Dependencies:**
```txt
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.17.0
requests>=2.31.0
```

### **API Integration:**
- **Base URL**: `https://bralma-backend.onrender.com`
- **Timeout**: 15 seconden
- **Free tier**: 15sec wake-up bij eerste request
- **Health check**: `GET /health`

### **Error Handling:**
- Connection errors → "Backend is mogelijk aan het opstarten"
- Timeout → "Probeer opnieuw"
- 4xx/5xx → Toon status code + response text

### **Streamlit Multi-Page:**
- `Home.py` = main entry point
- `pages/` = auto-detected sub-pages
- Sidebar navigatie automatic
- File naming: `0_Name.py` (order), `emoji_Name.py` (icon)

## 📚 Code Structuur

### **Helper Functions** (beide pagina's):

```python
# Electricity
map_wind_to_mw(category, capacity=6000)
map_season_to_solar_factor(season)
calculate_solar_generation(hour, season, capacity=12000)
get_time_label(settlement_period)

# Housing
map_price_category_to_range(category)
get_popular_cities()
get_regions()
```

### **API Call Pattern:**

```python
def predict_*_api(payload):
    try:
        response = requests.post(f"{API_URL}/api/*", json=payload, timeout=15)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code}")
    except requests.exceptions.ConnectionError:
        st.error("Backend opstarten (15 sec)")
    except requests.exceptions.Timeout:
        st.error("Timeout")
```

## 🎯 Deployment

### **Local Development:**
```bash
streamlit run Home.py
```

### **Production (Render.com/Streamlit Cloud):**

**Option 1: Streamlit Cloud**
1. Push to GitHub
2. Connect repository in Streamlit Cloud
3. Set `Home.py` as entrypoint
4. Deploy (auto-detects `pages/`)

**Option 2: Render.com**
```yaml
# render.yaml
services:
  - type: web
    name: bralma-frontend
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "streamlit run Home.py --server.port=$PORT --server.address=0.0.0.0"
```

### **Environment Variables:**
```bash
API_URL=https://bralma-backend.onrender.com
```
*(Hardcoded in code for school project)*

## 🐛 Troubleshooting

### "API Offline"
- **Oorzaak**: Render.com free tier auto-sleep
- **Oplossing**: Wacht 15 seconden, refresh
- **Check**: Open `{API_URL}/health` in browser

### "Module not found"
```bash
pip install streamlit pandas plotly requests
```

### "Port already in use"
```bash
streamlit run Home.py --server.port=8502
```

### "Pages not showing"
- Controleer `pages/` folder bestaat
- File naming: `0_Name.py` of `1_emoji_Name.py`
- Restart Streamlit server

## 📖 Gebruikers Instructies

### **Electricity Demand:**
1. Kies **seizoen** (Winter/Lente/Zomer/Herfst)
2. Sleep **tijdstip** slider (1-48)
3. Kies **windkracht** (5 opties)
4. Solar wordt automatisch berekend
5. Klik "🚀 Voorspel Demand"
6. Bekijk resultaat + energy mix pie chart

**24u Forecast:**
1. Tab "📊 24u Forecast"
2. Kies seizoen + windkracht (constant)
3. Klik "🔮 Genereer 24u Forecast"
4. Wacht ~30-60 sec (48 API calls)
5. Download CSV als nodig

### **UK Housing:**
1. Kies **prijscategorie** (of exacte prijs)
2. Select **regio** → **county** → **stad**
3. Kies **nieuwbouw/bestaand**
4. Kies **freehold/leasehold**
5. Klik "🚀 Voorspel Property Type"
6. Bekijk type + probability chart

## 🔗 Links

- **Backend API**: https://bralma-backend.onrender.com
- **Swagger Docs**: https://bralma-backend.onrender.com/swagger
- **GitHub**: https://github.com/Team-3-Machine-Learning/bralma_ML_Project
- **Data Sources**:
  - UK National Grid ESO (electricity)
  - UK Land Registry (housing)

## 👥 Team

**Machine Learning - Cloud AI**  
November 2025

---

## 📝 TODO

- [ ] Batch voorspelling (CSV upload) voor housing
- [ ] Caching API calls (reduce latency)
- [ ] Historical comparison (2017 vs 2025 data)
- [ ] Export forecast als PDF/Excel
- [ ] Confidence intervals voor electricity demand
- [ ] Map visualization voor housing (geographic heatmap)

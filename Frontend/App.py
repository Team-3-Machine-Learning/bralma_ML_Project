import streamlit as st
import pandas as pd
import plotly.express as px
import random
import requests
import os
import json

# Streamlit App Configuration
st.set_page_config(page_title="ML Predictions Demo", layout="wide")
st.title("⚡ Electricity Demand Predictor")

# API URL
API_URL = os.getenv("API_URL", "http://localhost:8501") # local testing

# API prediction function (replaces mock)
def predict_demand_api(wind, solar, hour):
    try:
        response = requests.post(
            f"{API_URL}/api/predict",
            json={
                "wind": wind,
                "solar": solar,
                "hour": hour
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            return data['prediction'], data.get('confidence', None)
        else:
            st.error(f"API Error: {response.status_code}")
            return None, None
            
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to API. Make sure it's running.")
        return None, None
    except requests.exceptions.Timeout:
        st.error("API request timed out.")
        return None, None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None, None

# UI
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Input Parameters")
    wind = st.slider("Wind Generation (MW)", 0, 10000, 5000)
    solar = st.slider("Solar Generation (MW)", 0, 5000, 2000)
    hour = st.selectbox("Hour of Day", range(24), index=18)
    
    if st.button("Predict", type="primary"):
        with st.spinner("Getting prediction from API..."):
            prediction, confidence = predict_demand_api(wind, solar, hour)
            
            if prediction is not None:
                st.metric("Predicted Demand", f"{prediction:,.0f} MW")
                if confidence:
                    st.metric("Confidence", f"{confidence:.1%}")
                st.success("Prediction complete!")

with col2:
    st.subheader("24-Hour Forecast")
    
    if st.button("Generate 24h Forecast"):
        with st.spinner("Generating forecast..."):
            forecast_data = []
            
            # Call API for each hour
            for h in range(24):
                pred, _ = predict_demand_api(wind, solar, h)
                if pred is not None:
                    forecast_data.append({"Hour": h, "Demand (MW)": pred})
            
            if forecast_data:
                df = pd.DataFrame(forecast_data)
                fig = px.line(df, x="Hour", y="Demand (MW)", markers=True)
                st.plotly_chart(fig, use_container_width=True)

# API Status indicator
st.sidebar.title("API Status")
try:
    health_check = requests.get(f"{API_URL}/health", timeout=5)
    if health_check.status_code == 200:
        st.sidebar.success("✅ API Connected")
    else:
        st.sidebar.error("❌ API Error")
except:
    st.sidebar.error("❌ API Offline")
    st.sidebar.info(f"Trying to connect to: {API_URL}")

# Show sample data (optional)
st.subheader("Sample Historical Data")
try:
    sample_df = pd.read_csv("../Dataset2_Demand/6_Elec_Demand_Final.csv", nrows=100)
    st.dataframe(sample_df.head(10))
except:
    st.info("Historical data not available")

# Instructions to run the app:
# Powershell commands (WINDOWS):
# move to: cd "c:\Users\Brent\Desktop\3APP\Machine Learning\Cloud AI\bralma_ML_Project\Frontend"
# run: streamlit run App.py

# (Mac):
#
#
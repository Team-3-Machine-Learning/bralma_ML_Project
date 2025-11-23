from fastapi import FastAPI
from pycaret.regression import load_model, predict_model
import pandas as pd

app = FastAPI()

model = load_model("./england_wales_demand_predictor")

@app.post("/predict")
def predict(data: dict):
    df = pd.DataFrame([data])

    df["settlement_date"] = pd.to_datetime(df["settlement_date"])
    df["month"] = df["settlement_date"].dt.month
    df["day_of_week"] = df["settlement_date"].dt.dayofweek
    df["is_weekend"] = df["day_of_week"].isin([5,6]).astype(int)
    # Capacity utilization ratios
    df["wind_utilization"] = df["embedded_wind_generation"] / (df["embedded_wind_capacity"] + 1)
    df["solar_utilization"] = df["embedded_solar_generation"] / (df["embedded_solar_capacity"] + 1)
    # Net cross-border flow sum
    flow_cols = ["ifa2_flow","britned_flow","moyle_flow","east_west_flow","nemo_flow"]
    df["net_crossborder_flow"] = df[flow_cols].sum(axis=1)

    pred_df = predict_model(model, df)
    predicted_value = pred_df.loc[0, "Label"] if "Label" in pred_df.columns else pred_df.iloc[0, 0]

    return {"EnglandWalesDemand": predicted_value}

@app.get("/")
def root():
    return {"message": "API is running! Elec Demand"}

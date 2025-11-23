from fastapi import FastAPI
from pycaret.regression import load_model, predict_model
import pandas as pd

app = FastAPI()

model = load_model("./england_wales_demand_model")

@app.post("/predict")
def predict(data: dict):
    df = pd.DataFrame([data])
    pred = predict_model(model, df)
    return {
        "label": pred.loc[0, "prediction_label"],
    }

@app.get("/")
def root():
    return {"message": "API is running! Elec Demand"}

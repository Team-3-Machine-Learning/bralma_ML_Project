from fastapi import FastAPI
from pycaret.classification import load_model, predict_model
import pandas as pd

app = FastAPI()

model = load_model("./england_wales_demand_predictor")

@app.post("/predict")
def predict(data: dict):
    df = pd.DataFrame([data])

    if hasattr(model, "silent"):
        delattr(model, "silent")

    pred_df = predict_model(model, df)
    predicted_value = pred_df.loc[0, "Label"] if "Label" in pred_df.columns else pred_df.iloc[0, 0]

    return {"EnglandWalesDemand": predicted_value}

@app.get("/")
def root():
    return {"message": "API is running!"}

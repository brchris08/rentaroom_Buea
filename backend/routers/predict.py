from fastapi import APIRouter
from pydantic import BaseModel
import pandas as pd
import joblib
import os

router = APIRouter()

# Load model and encoders
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
model = joblib.load(os.path.join(BASE_DIR, "ml", "rent_model.pkl"))
ohe = joblib.load(os.path.join(BASE_DIR, "ml", "ohe_encoder.pkl"))
feature_columns = joblib.load(os.path.join(BASE_DIR, "ml", "feature_columns.pkl"))
room_type_order = joblib.load(os.path.join(BASE_DIR, "ml", "room_type_order.pkl"))

# --- Pydantic schema ---
class PredictRequest(BaseModel):
    neighborhood: str
    room_type: str
    water: int
    electricity: int
    wifi: int
    actual_price: float

# --- Fairness label ---
def get_fairness_label(actual_price: float, predicted_price: float):
    difference = actual_price - predicted_price
    percentage = (difference / predicted_price) * 100
    if percentage < -10:
        return "Good Deal"
    elif percentage > 10:
        return "Overpriced"
    else:
        return "Fair"

# --- Endpoint ---
@router.post("/")
def predict_price(request: PredictRequest):
    # Encode neighborhood
    neighborhood_df = pd.DataFrame([[request.neighborhood]], columns=["neighborhood"])
    neighborhood_encoded = ohe.transform(neighborhood_df)
    neighborhood_columns = ohe.get_feature_names_out(["neighborhood"])
    neighborhood_df_encoded = pd.DataFrame(neighborhood_encoded, columns=neighborhood_columns)

    # Encode room type
    room_type_encoded = room_type_order.get(request.room_type, 0)

    # Build features dataframe
    features = pd.DataFrame([{
        "room_type_encoded": room_type_encoded,
        "water": request.water,
        "electricity": request.electricity,
        "wifi": request.wifi
    }])

    # Combine with neighborhood
    features = pd.concat([features, neighborhood_df_encoded], axis=1)
    features = features[feature_columns]

    # Make prediction
    predicted_price = model.predict(features)[0]
    fairness = get_fairness_label(request.actual_price, predicted_price)

    return {
        "predicted_price": round(predicted_price, 2),
        "actual_price": request.actual_price,
        "fairness_label": fairness
    }
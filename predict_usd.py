import pandas as pd
import joblib
from datetime import datetime

model, start_date = joblib.load("usd_model.joblib")

def predict_usd(input_date: str):
    target_date = datetime.strptime(input_date, "%Y-%m-%d")
    days_since_start = (target_date - start_date).days
    df = pd.DataFrame({"days": [days_since_start]})
    predicted = model.predict(df)[0]
    return round(predicted, 2)

print("Sana: 2025-07-01")
print("Bashorat qilingan USD kursi:", predict_usd("2025-07-01"))

import pandas as pd
import joblib
from datetime import datetime

model, start_date = joblib.load("weather_model.joblib")

if isinstance(start_date, pd.Timestamp):
    start_date = start_date.to_pydatetime()

def predict_weather(date_str: str) -> float:
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d")
        days = (target_date - start_date).days
        df = pd.DataFrame({"days_since_start": [days]})
        predicted = model.predict(df)[0]
        return round(predicted, 2)
    except Exception as e:
        print(f"❌ Xatolik: {e}")
        return None

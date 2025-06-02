import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import datetime
import joblib

df = pd.read_csv("tashkent_weather_openmeteo.csv")

df["date"] = pd.to_datetime(df["date"])

start_date = df["date"].min()
df["days_since_start"] = (df["date"] - start_date).dt.days

X = df[["days_since_start"]]
y = df["avg_temp"]

model = LinearRegression()
model.fit(X, y)

joblib.dump((model, start_date), "weather_model.joblib")
print("Model saqlandi: weather_model.joblib")

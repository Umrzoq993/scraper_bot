import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import datetime
import joblib

df = pd.read_csv("usd_eur_rub_rates.csv")

df = df[df['currency'] == 'USD'].copy()

df["date"] = pd.to_datetime(df["date"], format="%d.%m.%Y")

start_date = df["date"].min()
df["days_since_start"] = (df["date"] - start_date).dt.days

X = df[["days_since_start"]]
y = df["rate"]

model = LinearRegression()
model.fit(X, y)

joblib.dump((model, start_date), "usd_model.joblib")
print("✅ Model saqlandi: usd_model.joblib")

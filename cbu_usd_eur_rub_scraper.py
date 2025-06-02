import requests
import pandas as pd
from datetime import datetime, timedelta

TARGET_CURRENCIES = {"USD", "EUR", "RUB"}

def fetch_rates(date_str):
    url = f"https://cbu.uz/uz/arkhiv-kursov-valyut/json/all/{date_str}/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"{date_str} uchun xatolik: {e}")
    return []

start_date = datetime(2022, 1, 1)
end_date = datetime(2025, 6, 1)

all_data = []
current_date = start_date

while current_date <= end_date:
    date_str = current_date.strftime("%Y-%m-%d")
    print(f"{date_str} uchun ma'lumot yuklanmoqda...")
    rates = fetch_rates(date_str)

    for item in rates:
        if item["Ccy"] in TARGET_CURRENCIES:
            all_data.append({
                "date": item["Date"],
                "currency": item["Ccy"],
                "rate": float(item["Rate"]),
                "diff": float(item["Diff"]),
            })

    current_date += timedelta(days=1)

# DataFrame → CSV
df = pd.DataFrame(all_data)
df.to_csv("usd_eur_rub_rates.csv", index=False, encoding="utf-8-sig")
print("Fayl tayyor: usd_eur_rub_rates.csv")

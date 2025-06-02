import requests
import pandas as pd

latitude = 41.31
longitude = 69.24

start_date = "2024-01-01"
end_date = "2024-12-31"

url = (
    "https://archive-api.open-meteo.com/v1/archive?"
    f"latitude={latitude}&longitude={longitude}"
    f"&start_date={start_date}&end_date={end_date}"
    "&daily=temperature_2m_max,temperature_2m_min"
    "&timezone=Asia/Tashkent"
)

response = requests.get(url)
data = response.json()

df = pd.DataFrame({
    "date": data["daily"]["time"],
    "temp_min": data["daily"]["temperature_2m_min"],
    "temp_max": data["daily"]["temperature_2m_max"],
})

df["avg_temp"] = df[["temp_min", "temp_max"]].mean(axis=1)

df.to_csv("tashkent_weather_openmeteo.csv", index=False)
print("Fayl saqlandi: tashkent_weather_openmeteo.csv")

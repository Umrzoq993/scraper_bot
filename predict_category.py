import joblib

# 🔄 Modelni yuklash
model = joblib.load("news_category_model.joblib")

def predict_category(text: str) -> str:
    return model.predict([text])[0]

# 🔎 Sinov
sample_texts = [
    "O‘zbekiston va Turkmaniston o‘rtasidagi hamkorlik yangi bosqichga ko‘tarildi",
    "Bugungi futbol uchrashuvida Messi g‘alaba golini urdi",
    "Davlat budjeti va soliq siyosati yuzasidan yangi qonun qabul qilindi"
]

for text in sample_texts:
    print(f"📝: {text}")
    print(f"➡️  Category: {predict_category(text)}\n")

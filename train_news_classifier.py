import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import joblib

df = pd.read_csv("kunuz_by_category_news.csv")

df['category'] = df['category_url'].apply(lambda x: x.strip().split("/")[-1])

df = df[['content', 'category']].dropna()

X_train, X_test, y_train, y_test = train_test_split(
    df['content'], df['category'],
    test_size=0.2, random_state=42, stratify=df['category']
)

pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=5000, stop_words='english')),
    ('clf', LogisticRegression(max_iter=1000))
])

pipeline.fit(X_train, y_train)

y_pred = pipeline.predict(X_test)
print("\n📊 Classification Report:\n")
print(classification_report(y_test, y_pred))

joblib.dump(pipeline, "news_category_model.joblib")
print("✅ Model saqlandi: news_category_model.joblib")

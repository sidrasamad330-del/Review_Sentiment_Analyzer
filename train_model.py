import pandas as pd
import re
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load dataset
data = pd.read_csv("dataset.csv")

# ----------------------------
# Clean Text
# ----------------------------
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text

data["review"] = data["review"].apply(clean_text)

# Features and Labels
X = data["review"]
y = data["sentiment"]

# Better Vectorizer
vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 2),
    min_df=2,
    max_df=0.90
)

X_vectorized = vectorizer.fit_transform(X)

# Better Model
model = LogisticRegression(
    max_iter=1000,
    random_state=42
)

model.fit(X_vectorized, y)

# Save
joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("Model trained successfully!")
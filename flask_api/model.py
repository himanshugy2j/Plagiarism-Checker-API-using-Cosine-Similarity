# flask_api/model.py
import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from flask_api.utils import calculate_cosine_similarity

def create_dataset_and_train():
    # Simple synthetic dataset - expand as needed
    data = [
        ("This is the original sentence.", "This is the original sentence.", 1),
        ("The sky is blue and beautiful.", "The sky is blue.", 1),
        ("Machine learning is fun.", "I like pizza.", 0),
        ("Python is a great language.", "I use Java for backend.", 0),
        ("Neural networks are powerful.", "Neural networks are powerful and useful.", 1),
        ("I went to the market to buy apples.", "I went to market to buy apples for home.", 1),
        ("I like football and cricket.", "I love cricket and football.", 1),
        ("Coffee is great.", "I dislike coffee.", 0)
    ]

    rows = []
    for orig, sub, label in data:
        sim = calculate_cosine_similarity(orig, sub)
        rows.append([sim, label])

    df = pd.DataFrame(rows, columns=["similarity", "label"])
    df.to_csv("../plagiarism_dataset.csv", index=False)  # save at repo root for deliverable

    X = df[["similarity"]]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
    model = LogisticRegression()
    model.fit(X_train, y_train)
    print("Training accuracy:", model.score(X_test, y_test))

    joblib.dump(model, "../plagiarism_model.pkl")
    print("Saved model to ../plagiarism_model.pkl")

if __name__ == "__main__":
    create_dataset_and_train()

# flask_api/app.py
from flask import Flask, request, jsonify
from flask_api.utils import calculate_cosine_similarity, highlight_matching_text
import joblib
import os

app = Flask(__name__)
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "plagiarism_model.pkl")
model = joblib.load(MODEL_PATH)

@app.route("/check", methods=["POST"])
def check():
    if 'original' not in request.files or 'submission' not in request.files:
        return jsonify({"error": "Please send 'original' and 'submission' files"}), 400

    file1 = request.files['original']
    file2 = request.files['submission']
    try:
        text1 = file1.read().decode("utf-8")
        text2 = file2.read().decode("utf-8")
    except Exception as e:
        return jsonify({"error": "Unable to read files as utf-8", "details": str(e)}), 400

    similarity = calculate_cosine_similarity(text1, text2)
    prediction = int(model.predict([[similarity]])[0])
    prob = float(model.predict_proba([[similarity]])[0][1])
    highlight1, highlight2 = highlight_matching_text(text1, text2)

    return jsonify({
        "similarity_score": round(similarity, 4),
        "plagiarized": bool(prediction),
        "probability": round(prob, 4),
        "highlighted_original": highlight1,
        "highlighted_submission": highlight2
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)

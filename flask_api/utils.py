# flask_api/utils.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import difflib

def calculate_cosine_similarity(text1: str, text2: str) -> float:
    vectorizer = TfidfVectorizer()
    # fit on both docs to build vocabulary
    tfidf = vectorizer.fit_transform([text1, text2])
    sim_matrix = cosine_similarity(tfidf[0:1], tfidf[1:2])
    return float(sim_matrix[0][0])

def label_similarity(similarity_score: float, threshold: float = 0.8) -> int:
    return int(similarity_score >= threshold)

def highlight_matching_text(text1: str, text2: str):
    matcher = difflib.SequenceMatcher(None, text1, text2)
    blocks = matcher.get_matching_blocks()

    def highlight(text, blocks, is_text1=True):
        out = []
        last = 0
        for blk in blocks:
            start = blk.a if is_text1 else blk.b
            size = blk.size
            if size == 0:
                continue
            out.append(text[last:start])
            out.append(f"<mark>{text[start:start+size]}</mark>")
            last = start + size
        out.append(text[last:])
        return ''.join(out)

    return highlight(text1, blocks, True), highlight(text2, blocks, False)

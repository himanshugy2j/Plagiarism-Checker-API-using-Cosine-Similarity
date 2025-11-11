# streamlit_app/app.py
import streamlit as st
import requests

st.set_page_config(page_title="Plagiarism Checker", layout="wide")
st.title("📄 Plagiarism Checker (Streamlit UI)")

st.markdown("Upload original and submission text files. This frontend posts to the Flask API at http://localhost:5000/check")

col1, col2 = st.columns(2)
with col1:
    original_file = st.file_uploader("Upload Original File", type=["txt"], key="orig")
with col2:
    submission_file = st.file_uploader("Upload Submission File", type=["txt"], key="sub")

if st.button("Check Plagiarism"):
    if not original_file or not submission_file:
        st.error("Please upload both files.")
    else:
        with st.spinner("Checking..."):
            files = {
                "original": original_file,
                "submission": submission_file
            }
            try:
                resp = requests.post("http://localhost:5000/check", files=files, timeout=10)
                if resp.status_code != 200:
                    st.error(f"API error: {resp.status_code} - {resp.text}")
                else:
                    data = resp.json()
                    st.metric("Similarity Score", f"{data['similarity_score']*100:.2f}%")
                    st.metric("Plagiarism Probability", f"{data['probability']*100:.2f}%")
                    if data["plagiarized"]:
                        st.error("🔴 Likely plagiarized")
                    else:
                        st.success("🟢 Looks original")

                    st.subheader("Highlighted Original")
                    st.markdown(data["highlighted_original"], unsafe_allow_html=True)

                    st.subheader("Highlighted Submission")
                    st.markdown(data["highlighted_submission"], unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Connection failed: {e}")

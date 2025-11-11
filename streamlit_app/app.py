import streamlit as st
import requests
import json
import os

API_URL = os.getenv("API_URL", "http://flask:5000/check")

st.title("🧠 Plagiarism Checker using Cosine Similarity")

st.markdown("Upload two text files below to check for plagiarism similarity.")

col1, col2 = st.columns(2)

with col1:
    original_file = st.file_uploader("Upload Original File", type=["txt"])

with col2:
    submission_file = st.file_uploader("Upload Submission File", type=["txt"])

if st.button("Check Plagiarism"):
    if original_file and submission_file:
        files = {
            "original": original_file,
            "submission": submission_file,
        }

        with st.spinner("Analyzing..."):
            try:
                response = requests.post(API_URL, files=files)
                if response.status_code == 200:
                    result = response.json()
                    st.success(f"✅ Similarity Score: {result['similarity_score']:.3f}")
                    st.info(f"📊 Probability: {result['probability']:.3f}")
                    st.write("**Plagiarized:**", "Yes" if result["plagiarized"] else "No")

                    with st.expander("🔍 Highlighted Original Text"):
                        st.markdown(result["highlighted_original"], unsafe_allow_html=True)

                    with st.expander("🔍 Highlighted Submission Text"):
                        st.markdown(result["highlighted_submission"], unsafe_allow_html=True)
                else:
                    st.error(f"Server returned error: {response.status_code}")
                    st.json(response.json())
            except Exception as e:
                st.error(f"Request failed: {e}")
    else:
        st.warning("Please upload both files before checking.")

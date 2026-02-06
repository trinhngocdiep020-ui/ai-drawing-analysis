import streamlit as st
import google.generativeai as genai
from PIL import Image

# Lấy API Key (Sẽ cấu hình trên Streamlit Cloud sau)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("Chưa cấu hình API Key trong Secrets!")

st.set_page_config(layout="wide")
st.title("🔍 AI Document Comparison")

u_file = st.file_uploader("Chọn ảnh bản vẽ", type=['png', 'jpg', 'jpeg'])
if u_file:
    st.image(u_file, use_container_width=True)
    if st.button("🚀 Phân tích"):
        st.info("AI đang đọc dữ liệu...")
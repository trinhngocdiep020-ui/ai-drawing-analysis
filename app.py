import streamlit as st
import google.generativeai as genai
from PIL import Image

st.title("🔍 AI Drawing Analysis")

# Sử dụng tên model cơ bản nhất có khả năng tương thích cao
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Lỗi: {e}")
    st.stop()

files = st.file_uploader("Tải ảnh", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

if files:
    imgs = [Image.open(f) for f in files]
    st.image(imgs, width=300)
    
    if st.button("🚀 Phân tích"):
        try:
            # Lệnh gọi AI trực tiếp
            response = model.generate_content(["So sánh các bản vẽ này bằng tiếng Việt", *imgs])
            st.write(response.text)
        except Exception as e:
            st.error(f"Lỗi AI: {e}")

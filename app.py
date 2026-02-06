import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="AI Analysis", layout="wide")
st.title("🔍 AI Drawing Analysis")

# Kết nối API và Model
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-pro-vision")
except Exception as e:
    st.error(f"Lỗi: {e}")
    st.stop()

# Tải ảnh
files = st.file_uploader("Tải lên các bản vẽ (Ảnh)...", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if files:
    st.success(f"Đã nhận {len(files)} ảnh.")
    imgs = [Image.open(f) for f in files]
    
    # Hiển thị ảnh
    cols = st.columns(len(imgs))
    for i, img in enumerate(imgs):
        cols[i].image(img, use_container_width=True)
    
    # Nút phân tích
    if st.button("🚀 Bắt đầu Phân tích"):
        with st.spinner("AI đang so sánh..."):
            try:
                prompt = "Hãy so sánh chi tiết sự khác biệt giữa các bản vẽ này bằng tiếng Việt."
                response = model.generate_content([prompt] + imgs)
                st.markdown("### 📊 Kết quả:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Lỗi khi gọi AI: {e}")
else:
    st.info("Vui lòng tải ảnh lên để bắt đầu.")

import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="AI Drawing Analysis", layout="wide")
st.title("🔍 AI Document & Drawing Analysis")

# Thử nghiệm kết nối với tên model cơ bản nhất
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Sử dụng tên model ổn định nhất
    model = genai.GenerativeModel('gemini-1.5-flash') 
except Exception as e:
    st.error(f"Lỗi cấu hình: {e}")
    st.stop()

uploaded_files = st.file_uploader(
    "Tải lên bản vẽ (Ảnh hoặc PDF)...", 
    type=["png", "jpg", "jpeg", "pdf"], 
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"Đã nhận {len(uploaded_files)} file.")
    input_data = []
    cols = st.columns(len(uploaded_files))
    
    for i, file in enumerate(uploaded_files):
        if file.type == "application/pdf":
            st.info(f"📄 {file.name}")
            input_data.append({"mime_type": "application/pdf", "data": file.getvalue()})
        else:
            img = Image.open(file)
            cols[i].image(img, caption=file.name, use_container_width=True)
            input_data.append(img)

    if st.button("🚀 Bắt đầu Phân tích & So sánh"):
        with st.spinner("AI đang xử lý, vui lòng đợi..."):
            try:
                prompt = "Hãy phân tích chi tiết các bản vẽ này bằng tiếng Việt. So sánh chúng nếu có nhiều hơn 1 hình."
                # Gọi lệnh tạo nội dung
                response = model.generate_content([prompt] + input_data)
                st.markdown("### 📊 Kết quả:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Lỗi: {e}. Vui lòng kiểm tra lại phiên bản thư viện trong requirements.txt")
else:
    st.info("Vui lòng tải ảnh bản vẽ hoặc file PDF lên.")



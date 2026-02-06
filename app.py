import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Cấu hình giao diện
st.set_page_config(page_title="AI Drawing Analysis", layout="wide")
st.title("🔍 AI Document & Drawing Analysis")

# 2. Cấu hình API Key
try:
    # Sử dụng tên model chuẩn xác nhất hiện tại
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash-latest') 
except Exception as e:
    st.error(f"Lỗi cấu hình: {e}")
    st.stop()

# 3. Giao diện tải file
uploaded_files = st.file_uploader(
    "Tải lên bản vẽ (Ảnh hoặc PDF)...", 
    type=["png", "jpg", "jpeg", "pdf"], 
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"Đã nhận {len(uploaded_files)} file.")
    input_data = []
    
    # Hiển thị ảnh xem trước
    cols = st.columns(len(uploaded_files))
    for i, file in enumerate(uploaded_files):
        if file.type == "application/pdf":
            st.info(f"📄 {file.name}")
            input_data.append({"mime_type": "application/pdf", "data": file.getvalue()})
        else:
            img = Image.open(file)
            cols[i].image(img, caption=file.name, use_container_width=True)
            input_data.append(img)

    # 4. Nút bấm phân tích
    if st.button("🚀 Bắt đầu Phân tích & So sánh"):
        with st.spinner("AI đang làm việc..."):
            try:
                prompt = "Bạn là kỹ sư. Hãy phân tích nội dung các bản vẽ này bằng tiếng Việt. Nếu có từ 2 hình trở lên, hãy chỉ ra các điểm khác biệt cụ thể giữa chúng."
                response = model.generate_content([prompt] + input_data)
                st.markdown("### 📊 Kết quả:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Lỗi khi gọi AI: {e}")
else:
    st.info("Vui lòng tải ảnh bản vẽ hoặc file PDF lên.")


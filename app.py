import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Cấu hình giao diện ứng dụng
st.set_page_config(page_title="AI Drawing Analysis", layout="wide")

st.title("🔍 AI Document & Drawing Analysis")
st.subheader("Phân tích và So sánh Bản vẽ Kỹ thuật")

# 2. Kết nối với Gemini API qua Secrets
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    st.error("Lỗi: Chưa tìm thấy API Key trong mục Secrets của Streamlit!")
    st.stop()

# Thiết lập model Gemini 1.5 Flash (nhanh và mạnh trong việc đọc ảnh)
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. Khu vực tải file - Đã kích hoạt chọn nhiều file và PDF
uploaded_files = st.file_uploader(
    "Tải lên các bản vẽ (Ảnh hoặc PDF)...", 
    type=["png", "jpg", "jpeg", "pdf"], 
    accept_multiple_files=True  # Dòng này cho phép chọn nhiều file cùng lúc
)

if uploaded_files:
    st.success(f"Đã nhận {len(uploaded_files)} file thành công!")
    
    # Hiển thị bản xem trước (Preview)
    cols = st.columns(len(uploaded_files))
    input_data = []
    
    for i, file in enumerate(uploaded_files):
        if file.type == "application/pdf":
            st.info(f"📄 File PDF: {file.name} (AI sẽ phân tích nội dung bên trong)")
            input_data.append(file.getvalue())
        else:
            img = Image.open(file)
            cols[i].image(img, caption=file.name, use_container_width=True)
            input_data.append(img)

    # 4. Nút bấm kích hoạt AI phân tích
    if st.button("🚀 Bắt đầu Phân tích & So sánh"):
        with st.spinner("AI đang 'đọc' bản vẽ, vui lòng đợi trong giây lát..."):
            try:
                # Câu lệnh hướng dẫn AI cách làm việc
                prompt = """
                Bạn là một kỹ sư chuyên nghiệp. Hãy thực hiện các nhiệm vụ sau:
                1. Nếu chỉ có 1 bản vẽ: Hãy liệt kê các thông số kỹ thuật, kích thước và ghi chú chính.
                2. Nếu có từ 2 bản vẽ trở lên: Hãy so sánh chúng và chỉ ra các điểm khác biệt (ví dụ: thay đổi kích thước, vị trí linh kiện, hoặc nội dung sửa đổi).
                Trả lời rõ ràng bằng tiếng Việt theo định dạng danh sách.
                """
                
                # Gửi dữ liệu cho AI
                response = model.generate_content([prompt] + input_data)
                
                st.markdown("---")
                st.markdown("### 📊 Kết quả phân tích từ AI:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Đã xảy ra lỗi khi xử lý: {e}")

else:
    st.info("Vui lòng tải ảnh bản vẽ hoặc file PDF

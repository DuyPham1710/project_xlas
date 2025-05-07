import streamlit as st

def show():
    html_code = """
    <div style="font-family: Arial, sans-serif; padding: 20px;">
        <h1 style="color: #4CAF50;">Xử lý ảnh số cuối kỳ</h1>
        <p>Chào mừng bạn đến với ứng dụng nhận diện khuôn mặt thời gian thực bằng <strong>OpenCV</strong> và <strong>Streamlit</strong>.</p>
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)

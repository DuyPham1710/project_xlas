import streamlit as st

def show():
    st.title("Đồ án cuối kỳ")
    
    # st.markdown("""
    # <div style='background: rgba(255, 255, 255, 0.9); padding: 2rem; border-radius: 15px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
    # """, unsafe_allow_html=True)
    
    st.header("🎯 Sản phẩm")
    st.write("Project cuối kỳ cho môn học xử lý ảnh số.")
    st.write("Thuộc Trường Đại Học Sư Phạm Kỹ Thuật TP.HCM.")
    
    st.header("✨ 8 chức năng chính")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='functional' style='background: rgba(255, 255, 255, 0.8); padding: 1rem; border-radius: 10px; margin: 0.5rem 0;'>
            😐 Nhận dạng khuôn mặt
        </div>
        <div class='functional' style='background: rgba(255, 255, 255, 0.8); padding: 1rem; border-radius: 10px; margin: 0.5rem 0;'>
            😊 Nhận dạng biểu cảm khuôn mặt
        </div>
        <div class='functional' style='background: rgba(255, 255, 255, 0.8); padding: 1rem; border-radius: 10px; margin: 0.5rem 0;'>
            🚦 Nhận dạng biển báo đường bộ
        </div>
        <div class='functional' style='background: rgba(255, 255, 255, 0.8); padding: 1rem; border-radius: 10px; margin: 0.5rem 0;'>
            🍎 Nhận dạng 5 loại trái cây
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='functional' style='background: rgba(255, 255, 255, 0.8); padding: 1rem; border-radius: 10px; margin: 0.5rem 0;'>
            🖼️ Xử lý ảnh số (Chương 3, 4, 9)
        </div>
        <div class='functional' style='background: rgba(255, 255, 255, 0.8); padding: 1rem; border-radius: 10px; margin: 0.5rem 0;'>
            🔍 Nhận dạng biển số xe
        </div>
        <div class='functional' style='background: rgba(255, 255, 255, 0.8); padding: 1rem; border-radius: 10px; margin: 0.5rem 0;'>
            🛣️ Nhận dạng làn đường
        </div>
        <div class='functional' style='background: rgba(255, 255, 255, 0.8); padding: 1rem; border-radius: 10px; margin: 0.5rem 0;'>
            ♟️ Nhận dạng quân cờ tướng
        </div>
        """, unsafe_allow_html=True)
    
    # st.markdown("""
    # <div style='background: rgba(255, 255, 255, 0.8); padding: 2rem; border-radius: 15px; margin-top: 2rem;'>
    # """, unsafe_allow_html=True)
    
    st.header("👨‍🎓 Thông tin sinh viên thực hiện")
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("""
        <div class='functional' style='background: rgba(255, 255, 255, 0.5); padding: 1rem; border-radius: 10px;'>
            👤 **Phạm Ngọc Duy**<br>
            📝 MSSV: 22110297
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class='functional' style='background: rgba(255, 255, 255, 0.5); padding: 1rem; border-radius: 10px;'>
            👤 **Nguyễn Hữu Ngọc Lam**<br>
            📝 MSSV: 22110362
        </div>
        """, unsafe_allow_html=True)
    
    # st.markdown("</div>", unsafe_allow_html=True)

import streamlit as st
from modules import GioiThieu, Chuong3, Chuong4, Chuong9, NhanDienKhuonMat, trai_cay
import streamlit as st
import os


st.set_page_config(page_title="Ứng dụng xử lý ảnh")

# Khởi tạo trạng thái nếu chưa có
if 'selected' not in st.session_state:
    st.session_state.selected = "GioiThieu"

# Hàm xử lý sự kiện khi nhấn nút
def set_selection(choice):
    st.session_state.selected = choice

# Sidebar với các nút riêng biệt
with st.sidebar:  
    logo = "https://tracuuxettuyen.hcmute.edu.vn/assets/img/logo/ute_logo.png"
    st.image(logo, width=250)
st.sidebar.title("Menu")
st.sidebar.button("Giới thiệu", on_click=set_selection, args=("GioiThieu",))
st.sidebar.button("Chương 3", on_click=set_selection, args=("Chuong3",))
st.sidebar.button("Chương 4", on_click=set_selection, args=("Chuong4",))
st.sidebar.button("Chương 9", on_click=set_selection, args=("Chuong9",))
st.sidebar.button("Nhận diện khuôn mặt", on_click=set_selection, args=("NhanDienKhuonMat",))
st.sidebar.button("Nhận diện trái cây", on_click=set_selection, args=("TraiCay",))

# Hiển thị nội dung tương ứng
selected = st.session_state.selected

if selected == "GioiThieu":
    GioiThieu.show()
elif selected == "Chuong3":
    Chuong3.show()
elif selected == "Chuong4":
    Chuong4.show()
elif selected == "Chuong9":
    Chuong9.show()
elif selected == "NhanDienKhuonMat":
    NhanDienKhuonMat.show()
elif selected == "TraiCay":
    trai_cay.show()




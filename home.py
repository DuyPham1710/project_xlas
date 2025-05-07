import streamlit as st
from modules import GioiThieu, Chuong3, Chuong4, Chuong9, NhanDienKhuonMat, trai_cay, vehicles_counting
import streamlit as st
import os


st.set_page_config(page_title="Ứng dụng xử lý ảnh")

page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://img.meta.com.vn/Data/image/2021/09/30/background-la-gi-anh-background-dep-9.png");
    background-size: 100% 100%;
}
[data-testid="stHeader"]{
    background: rgba(0,0,0,0);
}
[data-testid="stToolbar"]{
    right:2rem;
}
[data-testid="stSidebar"] > div:first-child {
    background-image: url("");
    background-position: center;
}
[data-testid="stSidebar"] > div:first-child {
    background-image: url("https://img.meta.com.vn/Data/image/2021/09/30/background-la-gi-anh-background-dep-9.png");
    background-position: center;
}
</style>
"""
st.markdown(page_bg_img,unsafe_allow_html=True)


st.write("# Đồ án cuối kỳ")

st.markdown(
    """
    ## Sản phẩm
    Project cuối kỳ cho môn học xử lý ảnh số.
    Thuộc Trường Đại Học Sư Phạm Kỹ Thuật TP.HCM.
    ### 7 chức năng chính
    - 📖Nhận dạng khuôn mặt
    - 📖Nhận dạng cử chỉ (Chưa làm)
    - 📖Nhận dạng chữ viết tay MNIST    (Chưa làm)
    - 📖Nhận dạng 5 loại trái cây (táo, thăng long, sầu riêng, mít, xoài)
    - 📖Xử lý ảnh số (Chương 3, 4, 9)
    - 📖Nhận dạng màu sắc (Chưa làm)
    - 📖Nhận dạng phương tiện giao thông và đếm số lượng phương tiện. (Chưa làm)
    ## Thông tin sinh viên thực hiện
    - Họ tên: Phạm Ngọc Duy
    - MSSV: 22110297
    - Họ tên: Nguyễn Hữu Ngọc Lam
    - MSSV: 22110362
    """
)

# Khởi tạo trạng thái nếu chưa có
if 'selected' not in st.session_state:
    st.session_state.selected = "GioiThieu"

# Hàm xử lý sự kiện khi nhấn nút
def set_selection(choice):
    st.session_state.selected = choice

# Sidebar với các nút riêng biệt
with st.sidebar:  
    logo = "https://fit.hcmute.edu.vn/Resources/Images/SubDomain/fit/FIT-DoanHoi.png"
    st.image(logo, width=250)
st.sidebar.title("Menu")
st.sidebar.button("Giới thiệu", on_click=set_selection, args=("GioiThieu",))
st.sidebar.button("Chương 3", on_click=set_selection, args=("Chuong3",))
st.sidebar.button("Chương 4", on_click=set_selection, args=("Chuong4",))
st.sidebar.button("Chương 9", on_click=set_selection, args=("Chuong9",))
st.sidebar.button("Nhận diện khuôn mặt", on_click=set_selection, args=("NhanDienKhuonMat",))
st.sidebar.button("Nhận diện trái cây", on_click=set_selection, args=("TraiCay",))
st.sidebar.button("Nhận dạng đếm số lượng xe", on_click=set_selection, args=("vehicles_counting",))
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
elif selected == "vehicles_counting":
    vehicles_counting.show()




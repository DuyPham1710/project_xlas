import streamlit as st
from modules import GioiThieu, Chuong3, Chuong4, Chuong9, NhanDienKhuonMat, trai_cay, lane_detect, face_mesh_detect
from modules.NhanDienBienBaoDuongBo import show as show_road_signs
from modules.NhanDienCoTuong import show as show_chess
from modules.NhanDienBienSoXe import show as show_license_plate
import streamlit as st
import os

# Custom CSS for enhanced UI
st.set_page_config(
    page_title="Ứng dụng xử lý ảnh",
    page_icon="🎨",
    layout="wide"
)

# Custom CSS
custom_css = """
<style>
    /* Main container styling */
    [data-testid="stAppViewContainer"] {
        background-image: url("https://img.meta.com.vn/Data/image/2021/09/30/background-la-gi-anh-background-dep-9.png");
        background-size: 100% 100%;
    }

    /* Header styling */
    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
        padding: 1rem;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] > div:first-child {
    background-image: url("");
    background-position: center;
    }
    [data-testid="stSidebar"] > div:first-child {
        background-image: url("https://img.meta.com.vn/Data/image/2021/09/30/background-la-gi-anh-background-dep-9.png");
        background-position: center;
    }

    /* Button styling */
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background: linear-gradient(45deg, #2193b0, #6dd5ed);
        color: white;
        border: none;
        transition: all 0.3s ease;
        margin: 5px 0;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        background: linear-gradient(45deg, #6dd5ed, #2193b0);
    }

    /* Title styling */
    h1 {
        color: #2c3e50;
        font-size: 2.5em !important;
        font-weight: 700 !important;
        text-align: center;
        margin-bottom: 1em !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }

    h2 {
        color: #34495e;
        font-size: 1.8em !important;
        font-weight: 600 !important;
        margin-top: 1.5em !important;
    }

    /* Card-like containers */
    .stMarkdown {
        background: rgba(255, 255, 255, 0.9);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        animation: fadeIn 0.5s ease-out;
    }

    /* Feature list styling */
    ul {
        list-style-type: none;
        padding-left: 0;
    }

    li {
        padding: 10px 15px;
        margin: 5px 0;
        background: rgba(255, 255, 255, 0.8);
        border-radius: 8px;
        transition: all 0.3s ease;
    }

    li:hover {
        transform: translateX(10px);
        background: rgba(255, 255, 255, 0.95);
    }

    .functional:hover {
        transform: translateX(10px);
    }

    /* Student info styling */
    .student-info {
        background: rgba(255, 255, 255, 0.8);
        padding: 1.5rem;
        border-radius: 10px;
        margin-top: 2rem;
    }

    /* Animation for content */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Sidebar styling
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 1rem;'>
        <img src='https://fit.hcmute.edu.vn/Resources/Images/SubDomain/fit/FIT-DoanHoi.png' style='width: 200px; margin-bottom: 1rem;'>
        <h2 style='color: #2c3e50; margin-bottom: 1rem;'>Menu</h2>
    </div>
    """, unsafe_allow_html=True)

# Initialize session state
if 'selected' not in st.session_state:
    st.session_state.selected = "GioiThieu"

def set_selection(choice):
    st.session_state.selected = choice

# Sidebar buttons with icons
st.sidebar.button("🏠 Giới thiệu", on_click=set_selection, args=("GioiThieu",))
st.sidebar.button("📊 Chương 3", on_click=set_selection, args=("Chuong3",))
st.sidebar.button("📈 Chương 4", on_click=set_selection, args=("Chuong4",))
st.sidebar.button("📉 Chương 9", on_click=set_selection, args=("Chuong9",))
st.sidebar.button("😐 Nhận diện khuôn mặt", on_click=set_selection, args=("NhanDienKhuonMat",))
st.sidebar.button("🍎 Nhận diện trái cây", on_click=set_selection, args=("TraiCay",))
st.sidebar.button("📝 Nhận Diện Biển Số Xe", on_click=set_selection, args=("LicensePlateRecognition",))
st.sidebar.button("🚦 Nhận diện biển báo", on_click=set_selection, args=("RoadSigns",))
st.sidebar.button("♟️ Nhận diện cờ tướng", on_click=set_selection, args=("Chess",))
st.sidebar.button("🛣️ Lane Detection", on_click=set_selection, args=("LaneDetection",))
st.sidebar.button("😊 Emotion Detection", on_click=set_selection, args=("EmotionDetection",))
# Content display
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
elif selected == "RoadSigns":
    show_road_signs()
elif selected == "Chess":
    show_chess()
elif selected == "LaneDetection":
    lane_detect.show()
elif selected == "EmotionDetection":
    face_mesh_detect.show()
elif selected == "LicensePlateRecognition": 
    show_license_plate()



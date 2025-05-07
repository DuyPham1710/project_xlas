import streamlit as st
import cv2
import numpy as np
from library import Chapter9 as c9  # Module xử lý ảnh của bạn

chuong9_options = [
    "Erosion",
    "Dilation",
    "Boundary",
    "Contour",
    "Convex Hull",
    "Defect Detect",
    "Connect Components",
    "Remove Small Rice"]

def show():
    st.subheader("Chương 9")

    # --- Sidebar ---
    selected_option = st.selectbox("Chọn chức năng:", chuong9_options)

    # --- Upload ảnh ---
    uploaded_file = st.file_uploader("Chọn ảnh", type=["jpg", "jpeg", "png","tif","bmp","webp"])
    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        img_bgr = cv2.imdecode(file_bytes, 1)
        img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        st.session_state.imgin = img_gray
        st.session_state.imgin_color = img_bgr

    # --- Hiển thị ảnh gốc ---
    if "imgin" in st.session_state:
        col1, col2 = st.columns(2)
        with col1:
            st.image(st.session_state.imgin_color, caption="Ảnh gốc", use_container_width=True, channels="GRAY")

        # --- Nút xử lý ---
        if st.button("Xử lý"):
            imgin = st.session_state.imgin
            imgin_color = st.session_state.imgin_color
            imgout = None

            if selected_option == "Erosion":
                imgout = c9.Erosion(imgin)
            elif selected_option == "Dilation":
                imgout = c9.Dilation(imgin)
            elif selected_option == "Boundary":
                imgout = c9.Boundary(imgin)
            elif selected_option == "Contour":
                imgout = c9.Contour(imgin)
            elif selected_option == "Convex Hull":
                imgout = c9.ConvexHull(imgin)
            elif selected_option == "Defect Detect":
                imgout = c9.DefectDetect(imgin)
            elif selected_option == "Connect Components":
                imgout = c9.ConnectComponents(imgin)
            elif selected_option == "Remove Small Rice":
                imgout = c9.RemoveSmallRice(imgin)
            else:
                pass

            # --- Hiển thị ảnh đã xử lý ---
            if imgout is not None:
                with col2:
                    st.image(imgout, caption="Ảnh đã xử lý", use_container_width=True, channels="GRAY")

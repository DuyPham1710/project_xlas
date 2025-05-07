import streamlit as st
import cv2
import numpy as np
from library import Chapter4 as c4  # Module xử lý ảnh của bạn

chuong4_options = [
    "Spectrum",
    "Remove Moire",
    "Remove Interference",
    "Plot Motion Filter",
    "Demotion"]

def show():
    st.subheader("Chương 4")

    # --- Sidebar ---
    selected_option = st.selectbox("Chọn chức năng:", chuong4_options)

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

            if selected_option == "Spectrum":
                imgout = c4.Spectrum(imgin)
            elif selected_option == "Remove Moire":
                imgout = c4.RemoveMoire(imgin)
            elif selected_option == "Remove Interference":
                imgout = c4.RemoveInterference(imgin)
            elif selected_option == "Plot Motion Filter":
                imgout = c4.PlotMotionFilter(imgin)
            elif selected_option == "Demotion":
                imgout = c4.Demotion(imgin)
            else:
                pass

            # --- Hiển thị ảnh đã xử lý ---
            if imgout is not None:
                with col2:
                    st.image(imgout, caption="Ảnh đã xử lý", use_container_width=True, channels="GRAY")

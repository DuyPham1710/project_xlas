import streamlit as st
import cv2
import numpy as np
from library import Chapter3 as c3  # Module xử lý ảnh của bạn

chuong3_options = [
    "Negative",
    "Negative Color",
    "Logarit",
    "Power",
    "Piecewise Linear",
    "Histogram",
    "HistEqual",
    "HistEqualColor",
    "LocalHist",
    "HistStat",
    "Smooth Box",
    "Smooth Gauss",
    "Median Filter",
    "Create Impulse Noise",
    "Sharp"]

def show():
    st.subheader("Chương 3")

    # --- Sidebar ---
    selected_option = st.selectbox("Chọn chức năng:", chuong3_options)

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

            if selected_option == "Negative":
                imgout = c3.Negative(imgin)
            elif selected_option == "Negative Color":
                imgout = c3.NegativeColor(imgin_color)
            elif selected_option == "Logarit":
                imgout = c3.Logarit(imgin)
            elif selected_option == "Power":
                imgout = c3.Power(imgin) 
            elif selected_option == "Piecewise Linear":
                imgout = c3.PiececwiseLinear(imgin)
            elif selected_option == "Histogram":
                imgout = c3.Histogram(imgin)
            elif selected_option == "HistEqual":
                imgout = cv2.equalizeHist(imgin)
            elif selected_option == "HistEqualColor":
                imgout = c3.HistEqualColor(imgin_color)
            elif selected_option == "LocalHist":
                imgout = c3.LocalHist(imgin)
            elif selected_option == "HistStat":
                imgout = c3.HistStat(imgin)
            elif selected_option == "Smooth Box":
                imgout =cv2.boxFilter(imgin, cv2.CV_8UC1, (21, 21))
            elif selected_option == "Smooth Gauss":
                imgout = cv2.GaussianBlur(imgin, (43, 43), 7)
            elif selected_option == "Median Filter":
                imgout = cv2.medianBlur(imgin, 5)
            elif selected_option == "Create Impulse Noise":
                imgout = c3.CreateImpulseNoise(imgin)
            elif selected_option == "Sharp":
                imgout = c3.Sharp(imgin)

            # --- Hiển thị ảnh đã xử lý ---
            if imgout is not None:
                with col2:
                    st.image(imgout, caption="Ảnh đã xử lý", use_container_width=True, channels="GRAY")

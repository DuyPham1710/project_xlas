from library import lane
import streamlit as st
import cv2
import numpy as np

def show():
    main_title_cfg = """
        <div style="display: flex; justify-content: center; align-items: center; padding: 0; margin: 0;">
            <h1 style="
                color: #ff40b5;
                background: white;
                padding: 15px 30px;
                border-radius: 15px;
                font-size: 36px;
                font-family: 'Segoe UI', 'Archivo', sans-serif;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
                text-align: center;
                margin-top: 10px;
                margin-bottom: 0;
            ">
                🛣️ <b>Lane Detection</b>
            </h1>
        </div>
        """
    st.markdown(main_title_cfg, unsafe_allow_html=True)
    # Trạng thái session
    if 'running' not in st.session_state:
        st.session_state.running = False

    # Nút điều khiển
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ Start"):
            st.session_state.running = True
    with col2:
        if st.button("⏹ Stop"):
            st.session_state.running = False
    frame_window = st.image([])

    cap = cv2.VideoCapture("./images/lane/lane_1.mp4")

    while st.session_state.running:
        ret, frame = cap.read()
        if not ret:
            st.warning(f"Không lấy được hình từ video. Lỗi: {ret}")
            break
        _canny = lane.canny(frame)
        roi = lane.region_of_interest(_canny)
        lines = lane.detect_lines(roi)
        averaged = lane.average_slope_intercept(frame, lines)
        line_img = lane.display_lines(frame, averaged)
        combo = lane.combine_images(frame, line_img)

        frame_window.image(combo, channels="BGR")

    cap.release()

import streamlit as st
import cv2
import mediapipe as mp
import joblib
import numpy as np
import time
import os

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
                    😐 <b>Nhận diện Biểu Cảm Khuôn Mặt (Emotion Detection)</b>
                </h1>
            </div>
            """

    st.markdown(main_title_cfg, unsafe_allow_html=True)

    run = st.checkbox('Bắt đầu nhận diện biểu cảm', key='emotion_run_checkbox')

    video_source_emotion = st.selectbox(
        "Chọn nguồn video cho biểu cảm",
        ("webcam", "video"),
        key="emotion_video_source_selectbox"
    )

    video_file_emotion = None
    if video_source_emotion == "video":
        video_file_emotion = st.file_uploader("Chọn video cho biểu cảm", type=["mp4", "avi", "mov", "mkv"], key="emotion_video_uploader")

    FRAME_WINDOW_EMOTION = st.image([])

    cap = None

    if run:
        if video_source_emotion == "webcam":
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                st.error("Không thể mở webcam. Vui lòng kiểm tra camera và quyền truy cập.")
                st.stop()
        elif video_source_emotion == "video" and video_file_emotion is not None:
            temp_video_file_path = os.path.join("temp_emotion_video.mp4")
            with open(temp_video_file_path, "wb") as f:
                f.write(video_file_emotion.read())
            cap = cv2.VideoCapture(temp_video_file_path)
            if not cap.isOpened():
                st.error(f"Không thể mở file video: {video_file_emotion.name}")
                st.stop()
        elif video_source_emotion == "video" and video_file_emotion is None:
            st.warning("Vui lòng tải lên một file video để tiếp tục.")
            st.stop()
        else: 
            st.stop()

        if cap is not None and cap.isOpened():
            st.info("Đang xử lý video/webcam...")

            # Khởi tạo Mediapipe
            mp_face_mesh = mp.solutions.face_mesh
            mp_drawing = mp.solutions.drawing_utils
            mp_drawing_styles = mp.solutions.drawing_styles

            # Tải mô hình đã huấn luyện và scaler
            model_path = 'NhanDienBieuCamKhuonMat/face_expression_model.joblib' 
            try:
                model, scaler = joblib.load(model_path)
            except FileNotFoundError:
                st.error(f"Lỗi: Không tìm thấy file model '{model_path}'.")
                st.error("Hãy đảm bảo bạn đã huấn luyện và lưu mô hình vào đúng đường dẫn.")
                st.stop()
            except Exception as e:
                st.error(f"Lỗi khi tải model: {e}")
                st.stop()

            # Lấy danh sách các lớp (biểu cảm) mà mô hình đã học
            try:
                class_labels = model.classes_
                st.caption(f"Mô hình được huấn luyện để nhận diện các biểu cảm: {class_labels}")
            except AttributeError:
                st.warning("Không thể lấy `model.classes_`. Đảm bảo mô hình đã được huấn luyện đúng cách.")
                class_labels = None 

            # Biến để kiểm soát tần suất dự đoán (giảm tải CPU)
            last_prediction_time = time.time()
            prediction_interval = 0.3 # Giây, dự đoán mỗi 0.3 giây
            current_expression_display = "Dang phan tich..."

            # Số lượng landmarks kỳ vọng (478 khi refine_landmarks=True)
            EXPECTED_LANDMARKS_COUNT = 478 
            EXPECTED_FEATURES_COUNT = EXPECTED_LANDMARKS_COUNT * 3

            with mp_face_mesh.FaceMesh(
                max_num_faces=1,
                refine_landmarks=True, 
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as face_mesh:

                while run and cap.isOpened():
                    success, image = cap.read()
                    if not success:
                        if video_source_emotion == "video":
                            st.write("Đã hết video. Để xem lại, bỏ chọn 'Bắt đầu' rồi chọn lại.")
                            break 
                        else:
                            st.warning("Không thể đọc frame từ webcam.")
                            break

                    image = cv2.flip(image, 1) # Lật ảnh để giống như gương
                    
                    # Để cải thiện hiệu suất, tùy chọn đánh dấu hình ảnh là không thể ghi đè.
                    image_for_processing = image.copy() 
                    image_for_processing.flags.writeable = False
                    image_rgb = cv2.cvtColor(image_for_processing, cv2.COLOR_BGR2RGB)
                    results = face_mesh.process(image_rgb)
                    
                    image_for_processing.flags.writeable = True 
                    image_bgr_output = image

                    if results.multi_face_landmarks:
                        face_landmarks = results.multi_face_landmarks[0] # Lấy khuôn mặt đầu tiên

                        # Draw face mesh
                        mp_drawing.draw_landmarks(
                            image=image_bgr_output,
                            landmark_list=face_landmarks,
                            connections=mp_face_mesh.FACEMESH_TESSELATION,
                            landmark_drawing_spec=None,
                            connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style())
                        mp_drawing.draw_landmarks(
                            image=image_bgr_output,
                            landmark_list=face_landmarks,
                            connections=mp_face_mesh.FACEMESH_CONTOURS,
                            landmark_drawing_spec=None,
                            connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style())

                        # Chỉ thực hiện dự đoán sau một khoảng thời gian nhất định
                        current_time = time.time()
                        if current_time - last_prediction_time > prediction_interval:
                            landmarks_data = []
                            for landmark_point in face_landmarks.landmark:
                                landmarks_data.extend([landmark_point.x, landmark_point.y, landmark_point.z])

                            if len(landmarks_data) == EXPECTED_FEATURES_COUNT:
                                scaled_landmarks = scaler.transform(np.array(landmarks_data).reshape(1, -1))
                                
                                # Dự đoán biểu cảm
                                prediction_proba = model.predict_proba(scaled_landmarks)
                                prediction_index = np.argmax(prediction_proba)
                                
                                if class_labels is not None and prediction_index < len(class_labels):
                                    predicted_expression_name = class_labels[prediction_index]
                                    confidence = prediction_proba[0][prediction_index]
                                    current_expression_display = f"{predicted_expression_name} ({confidence:.2f})"
                                else:
                                    current_expression_display = f"Bieu cam: ID {prediction_index} ({np.max(prediction_proba):.2f})"
                                
                                last_prediction_time = current_time
                            else:
                                current_expression_display = f"Landmarks: {len(landmarks_data)}/{EXPECTED_FEATURES_COUNT}"
                    else:
                        current_expression_display = "Khong tim thay khuon mat"

                    # Hiển thị biểu cảm dự đoán lên ảnh
                    cv2.putText(image_bgr_output, current_expression_display, (10, 30), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

                    # Chuyển BGR -> RGB để hiển thị trong Streamlit
                    frame_to_display = cv2.cvtColor(image_bgr_output, cv2.COLOR_BGR2RGB)
                    FRAME_WINDOW_EMOTION.image(frame_to_display, channels="RGB")
                    
                    time.sleep(0.01) 

                # End of while loop
                if video_source_emotion == "video" and video_file_emotion is not None:
                    st.write("Kết thúc xử lý video.")
                elif video_source_emotion == "webcam":
                     st.write("Đã dừng webcam.")

            # Cleanup
            if cap is not None:
                cap.release()
            if video_source_emotion == "video" and video_file_emotion is not None:
                if os.path.exists(temp_video_file_path):
                    try:
                        os.remove(temp_video_file_path) # Clean up temp file
                    except Exception as e:
                        st.warning(f"Không thể xóa file tạm: {e}")
            
            if not run:
                FRAME_WINDOW_EMOTION.empty()
                st.info("Đã dừng nhận diện biểu cảm.")


    elif not run: 
        FRAME_WINDOW_EMOTION.empty()
        if cap is not None:
            cap.release()
        st.info("Nhấn 'Bắt đầu nhận diện biểu cảm' để chạy.")

if __name__ == '__main__':
    st.title("Test Nhận Diện Biểu Cảm Khuôn Mặt")
    show()

import io
from typing import Any

import cv2
import numpy as np

from ultralytics import YOLO
from ultralytics.utils import LOGGER
from ultralytics.utils.checks import check_requirements
from ultralytics.utils.downloads import GITHUB_ASSETS_STEMS


class Inference:

    def __init__(self, **kwargs: Any):
        check_requirements("streamlit>=1.29.0")
        import streamlit as st
        self.image = None
        self.st = st  
        self.source = None  
        self.enable_trk = False  
        self.conf = 0.25
        self.iou = 0.45 
        self.org_frame = None 
        self.ann_frame = None  
        self.vid_file_name = None 
        self.selected_ind = [] 
        self.model = None 

        self.temp_dict = {"model": None, **kwargs}
        self.model_path = None  # Model file path
        if self.temp_dict["model"] is not None:
            self.model_path = self.temp_dict["model"]

        LOGGER.info(f"Ultralytics Solutions: ✅ {self.temp_dict}")

    def web_ui(self):
        """Sets up the Streamlit web interface with custom HTML elements."""
        menu_style_cfg = """<style>MainMenu {visibility: hidden;}</style>"""  # Hide main menu style

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
                    🍎 <b>Nhận diện trái cây</b>
                </h1>
            </div>
            """

        self.st.markdown(main_title_cfg, unsafe_allow_html=True)

    def sidebar(self):
        """Configure the Streamlit sidebar for model and inference settings."""
        self.st.sidebar.title("User Configuration")  
        self.source = self.st.sidebar.selectbox(
            "Nguồn đầu vào",
            ("webcam", "video", "image"),
        )  
        self.enable_trk = self.st.sidebar.radio("Enable Tracking", ("Yes", "No"))
        self.conf = float(
            self.st.sidebar.slider("Confidence Threshold", 0.0, 1.0, self.conf, 0.01)
        )  
        self.iou = float(self.st.sidebar.slider("IoU Threshold", 0.0, 1.0, self.iou, 0.01))  

        col1, col2 = self.st.columns(2) 
        self.org_frame = col1.empty() 
        self.ann_frame = col2.empty()  

    def source_upload(self):
        """Handle video file uploads through the Streamlit interface."""
        self.vid_file_name = ""
        if self.source == "video":
            vid_file = self.st.sidebar.file_uploader("Upload Video File", type=["mp4", "mov", "avi", "mkv"])
            if vid_file is not None:
                g = io.BytesIO(vid_file.read()) 
                with open("ultralytics.mp4", "wb") as out:  
                    out.write(g.read())  
                self.vid_file_name = "ultralytics.mp4"
        elif self.source == "webcam":
            self.vid_file_name = 0  
        elif self.source == "image":
            image_file = self.st.sidebar.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
            if image_file is not None:
                g = io.BytesIO(image_file.read())
                file_bytes = np.asarray(bytearray(g.read()), dtype=np.uint8)
                self.image = cv2.imdecode(file_bytes, 1)
                self.vid_file_name = "image"  # Đánh dấu là đang dùng ảnh



    def configure(self):
        """Configure the model and load selected classes for inference."""

        available_models = [x.replace("yolo", "YOLO") for x in GITHUB_ASSETS_STEMS if x.startswith("yolo11")]
        if self.model_path:  
            available_models.insert(0, self.model_path.split(".pt")[0])
        selected_model = self.st.sidebar.selectbox("Model", available_models)

        with self.st.spinner("Model is downloading..."):
            self.model = YOLO(f"{selected_model.lower()}.pt")  # Load the YOLO model
            class_names = list(self.model.names.values())  
        self.st.success("Model loaded successfully!")

        selected_classes = self.st.sidebar.multiselect("Classes", class_names, default=class_names[:3])
        self.selected_ind = [class_names.index(option) for option in selected_classes]

        if not isinstance(self.selected_ind, list):  
            self.selected_ind = list(self.selected_ind)

    def inference(self):
        """Perform real-time object detection inference on video or webcam feed."""
        self.web_ui() 
        self.sidebar() 
        self.source_upload()  
        self.configure()  

        # xử lý ngay khi upload, không cần nhấn "Start"
        if self.source == "image" and self.image is not None:
            # Dự đoán
            results = self.model(self.image, conf=self.conf, iou=self.iou, classes=self.selected_ind)
            annotated_image = results[0].plot()

            # Hiển thị ảnh gốc và ảnh đã nhận diện
            self.org_frame.image(self.image, channels="BGR", caption="Ảnh gốc")
            self.ann_frame.image(annotated_image, channels="BGR", caption="Đã nhận diện")

        elif self.st.sidebar.button("Start"):
            stop_button = self.st.button("Stop")  
            cap = cv2.VideoCapture(self.vid_file_name)  
            if not cap.isOpened():
                self.st.error("Could not open webcam or video source.")
                return

            while cap.isOpened():
                success, frame = cap.read()
                if not success:
                    self.st.warning("Failed to read frame from webcam. Please verify the webcam is connected properly.")
                    break

                # Process frame with model
                if self.enable_trk == "Yes":
                    results = self.model.track(
                        frame, conf=self.conf, iou=self.iou, classes=self.selected_ind, persist=True
                    )
                else:
                    results = self.model(frame, conf=self.conf, iou=self.iou, classes=self.selected_ind)

                annotated_frame = results[0].plot() 

                if stop_button:
                    cap.release() 
                    self.st.stop()  

                self.org_frame.image(frame, channels="BGR") 
                self.ann_frame.image(annotated_frame, channels="BGR")  

            cap.release() 
        cv2.destroyAllWindows()  

def show():
    import sys
    args = len(sys.argv)
    model = "./model/best.pt" 
    inf = Inference(model=model)
    inf.inference()
import streamlit as st
from PIL import Image

try:
    from Nhan_Dien_Bien_So_Xe.Image_test import predict
except ImportError:

    st.error("Lỗi: Không thể import hàm 'predict' cho nhận diện biển số xe. Vui lòng kiểm tra cấu trúc thư mục.")
    def predict(image_input):
        st.warning("Chức năng dự đoán biển số xe chưa được cấu hình đúng cách.")
        if image_input is not None:
            return [np.zeros((100, 200, 3), dtype=np.uint8)], ["Không có kết quả"]
        return [], []

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
                📝 <b>Nhận dạng biển số xe</b>
            </h1>
        </div>
        """
    st.markdown(main_title_cfg, unsafe_allow_html=True)

    img_in = None
    
    # Tải lên hình ảnh
    uploaded_img = st.file_uploader(
        "Tải lên hình ảnh xe", 
        type=["jpg", "png", "jpeg"], 
        key="license_plate_image_uploader",
        help="Chọn một file ảnh có định dạng JPG, PNG, hoặc JPEG."
    )
    

    col1, col2 = st.columns([1, 1]) 
    
    with col1:
        st.subheader("Hình Ảnh Gốc")
        if uploaded_img is not None:
            try:
                img = Image.open(uploaded_img)
       
                frame = np.array(img)
                if frame.ndim == 2: 
                    img_in = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
                elif frame.shape[2] == 4:
                     img_in = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
                else: # RGB image
                    img_in = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                
                st.image(cv2.cvtColor(img_in, cv2.COLOR_BGR2RGB), caption='Hình ảnh đã tải lên', use_container_width=True)
            except Exception as e:
                st.error(f"Lỗi khi xử lý hình ảnh: {e}")
                img_in = None
        else:
            st.info("Vui lòng tải lên một hình ảnh.")

    with col2:
        st.subheader("Kết Quả Nhận Diện")
        if img_in is not None:
            if st.button('🔎 Bắt đầu nhận diện biển số', key="predict_license_plate_button"):
                with st.spinner('Đang xử lý...'):
                    try:
                        img_out_list, text_list = predict(img_in) 
                        
                        if not text_list and not img_out_list: 
                            st.warning("Không phát hiện hoặc nhận diện được biển số nào trong hình ảnh.")
                        else:
                            for i in range(len(text_list)):
                                st.markdown(f"**Biển số {i+1}:**")
                                if i < len(img_out_list) and isinstance(img_out_list[i], np.ndarray) and img_out_list[i].size > 0 :
              
                                    img_display_plate = cv2.cvtColor(img_out_list[i], cv2.COLOR_BGR2RGB)
                                   
                                    st.image(img_display_plate, caption=f'Ảnh cắt biển số {i+1}', use_container_width=True) 
                                
                                st.success(f"Nội dung: `{text_list[i]}`")
                    except NameError:
                         st.error("Chức năng dự đoán biển số xe chưa được cấu hình đúng cách (thiếu hàm predict).")
                    except Exception as e:
                        st.error(f"Đã xảy ra lỗi trong quá trình nhận diện: {e}")
        else:
            st.info("Chưa có hình ảnh để nhận diện. Vui lòng tải ảnh lên ở cột bên trái.")


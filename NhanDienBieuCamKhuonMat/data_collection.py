import csv
import os
import time

import cv2
import mediapipe as mp

# Khởi tạo Mediapipe
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Cấu hình webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Lỗi: Không thể mở webcam. Vui lòng kiểm tra camera.")
    exit()

# Tạo file CSV để lưu dữ liệu
file_path = 'NhanDienBieuCamKhuonMat/face_expression_data.csv'
os.makedirs(os.path.dirname(file_path), exist_ok=True)

is_empty = not os.path.exists(file_path) or os.path.getsize(file_path) == 0

# Số lượng landmarks khi refine_landmarks=True là 478
NUM_FACE_LANDMARKS = 478
EXPECTED_LANDMARK_VALUES = NUM_FACE_LANDMARKS * 3 # 478 landmarks * 3 coordinates (x,y,z)

try:
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)

        # Ghi header nếu file chưa có nội dung
        if is_empty:
            header = []
            for i in range(NUM_FACE_LANDMARKS): # Sử dụng 478 landmarks
                header.extend([f'x{i}', f'y{i}', f'z{i}'])
            header.append('label')
            writer.writerow(header)
            print(f"Đã tạo file mới và ghi header vào: {file_path}")
        else:
            print(f"Ghi tiếp dữ liệu vào file: {file_path}")


        while True:
            print("\n--------------------------------------------------")
            label = input("Nhập tên nhãn biểu cảm (VD: 'vui', 'buon', 'ngac nhien', 'tuc gian'), hoặc nhấn 'b' để thoát hoàn toàn: ")
            if label.lower() == 'b':
                print("Kết thúc phiên thu thập dữ liệu.")
                break
            
            while True:
                try:
                    duration_str = input(f"Nhập thời gian thu thập cho nhãn '{label}' (giây, ví dụ: 10, 15, 20): ")
                    COLLECTION_DURATION_PER_TAKE = int(duration_str)
                    if COLLECTION_DURATION_PER_TAKE <= 0:
                        print("Thời gian thu thập phải là một số dương.")
                        continue
                    break
                except ValueError:
                    print("Vui lòng nhập một số nguyên hợp lệ cho thời gian.")

            take_count = 0
            while True:
                take_count += 1
                print(f"\nChuẩn bị thu thập cho nhãn: '{label}', lần thứ: {take_count}")
                print(f"Thời gian thu thập: {COLLECTION_DURATION_PER_TAKE} giây.")
                print("Khi sẵn sàng, hãy nhìn vào camera và thể hiện biểu cảm.")
                
                # Đếm ngược trước khi bắt đầu
                for i in range(3, 0, -1):
                    print(f"{i}...")
                    time.sleep(1)
                print("BẮT ĐẦU THU THẬP!")

                start_time = time.time()
                frames_collected_this_take = 0
                
                # Luôn mở lại FaceMesh cho mỗi lần "take" để đảm bảo trạng thái sạch
                with mp_face_mesh.FaceMesh(
                    max_num_faces=1,
                    refine_landmarks=True, 
                    min_detection_confidence=0.5,
                    min_tracking_confidence=0.5) as face_mesh:
                    
                    while cap.isOpened():
                        # Kiểm tra xem webcam có còn hoạt động không
                        if not cap.isOpened():
                            print("Lỗi: Webcam đã bị ngắt kết nối.")
                            # Cố gắng mở lại webcam
                            cap = cv2.VideoCapture(0)
                            if not cap.isOpened():
                                print("Không thể mở lại webcam. Thoát.")
                                exit()
                            else:
                                print("Đã kết nối lại webcam.")
                        
                        success, image = cap.read()
                        if not success:
                            print("Không thể đọc frame từ webcam.")
                            time.sleep(0.1) # Đợi một chút rồi thử lại
                            continue

                        image_display = cv2.flip(image.copy(), 1) # Ảnh để hiển thị
                        image_process = cv2.flip(image.copy(), 1) # Ảnh để xử lý

                        image_process.flags.writeable = False
                        image_rgb = cv2.cvtColor(image_process, cv2.COLOR_BGR2RGB)
                        results = face_mesh.process(image_rgb)
                        image_process.flags.writeable = True
                        
                        if results.multi_face_landmarks:
                            face_landmarks = results.multi_face_landmarks[0]

                            # Vẽ lên ảnh hiển thị
                            mp_drawing.draw_landmarks(
                                image=image_display,
                                landmark_list=face_landmarks,
                                connections=mp_face_mesh.FACEMESH_TESSELATION,
                                landmark_drawing_spec=None,
                                connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style())
                            mp_drawing.draw_landmarks(
                                image=image_display,
                                landmark_list=face_landmarks,
                                connections=mp_face_mesh.FACEMESH_CONTOURS,
                                landmark_drawing_spec=None,
                                connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style())

                            landmarks_data = []
                            for landmark in face_landmarks.landmark:
                                landmarks_data.extend([landmark.x, landmark.y, landmark.z])
                            
                            if len(landmarks_data) == EXPECTED_LANDMARK_VALUES:
                                # Chỉ ghi dữ liệu nếu đang trong thời gian thu thập
                                if time.time() - start_time <= COLLECTION_DURATION_PER_TAKE:
                                    row_to_write = landmarks_data + [label] # Tạo list mới
                                    writer.writerow(row_to_write)
                                    frames_collected_this_take += 1
                            else:
                                if time.time() - start_time <= COLLECTION_DURATION_PER_TAKE:
                                     print(f"Cảnh báo: Số lượng landmarks không đúng ({len(landmarks_data)}/{EXPECTED_LANDMARK_VALUES}). Bỏ qua frame này.")
                        
                        # Hiển thị thời gian còn lại
                        time_elapsed = time.time() - start_time
                        time_remaining = max(0, COLLECTION_DURATION_PER_TAKE - time_elapsed)
                        cv2.putText(image_display, f"Time: {time_remaining:.1f}s", (10, 30), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                        cv2.putText(image_display, f"Label: {label} (Take {take_count})", (10, 60), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                        cv2.imshow('Thu Thap Du Lieu Bieu Cam Khuon Mat', image_display)

                        # Kiểm tra thời gian thu thập
                        if time_elapsed > COLLECTION_DURATION_PER_TAKE:
                            print(f"\nĐã kết thúc thu thập cho nhãn: '{label}', lần {take_count}. Thu được {frames_collected_this_take} mẫu.")
                            break 

                        key = cv2.waitKey(5) & 0xFF
                        if key == ord('q'): # Nhấn 'q' để dừng lần thu thập hiện tại và hỏi có muốn tiếp tục không
                            print("Đã dừng thu thập lần này sớm.")
                            break 
                        elif key == 27: # Nhấn ESC để thoát hoàn toàn
                            print("Kết thúc phiên thu thập dữ liệu (người dùng nhấn ESC).")
                            cap.release()
                            cv2.destroyAllWindows()
                            file.close() # Đảm bảo file được đóng
                            exit()
                
                # Đóng cửa sổ hiển thị sau mỗi lần "take"
                if cv2.getWindowProperty('Thu Thap Du Lieu Bieu Cam Khuon Mat', cv2.WND_PROP_VISIBLE) >= 1:
                    cv2.destroyWindow('Thu Thap Du Lieu Bieu Cam Khuon Mat')

                # Hỏi người dùng có muốn thu thập thêm cho nhãn này không
                continue_label = input(f"Bạn có muốn thu thập thêm cho nhãn '{label}' không? (y/n): ")
                if continue_label.lower() != 'y':
                    break # Thoát vòng lặp thu thập cho nhãn hiện tại

except IOError:
    print(f"Lỗi: Không thể mở hoặc ghi vào file {file_path}. Kiểm tra quyền truy cập.")
except Exception as e:
    print(f"Đã xảy ra lỗi không mong muốn: {e}")
finally:
    if cap.isOpened():
        cap.release()
    cv2.destroyAllWindows()
    if 'file' in locals() and not file.closed:
        file.close()
    print(f"Đã đóng camera và file. Dữ liệu được lưu tại: {file_path}")


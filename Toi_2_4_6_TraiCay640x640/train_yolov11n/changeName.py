import os
import glob

# Đường dẫn thư mục chứa các file txt (đổi lại nếu cần)
folder_path = 'E:/Dai Hoc/Nam3/HK2/Xu_ly_anh_so/CuoiKy/Toi_2_4_6_TraiCay640x640/train/labels'  # Hoặc đường dẫn tuyệt đối

# Tìm tất cả các file phù hợp với pattern
file_pattern = os.path.join(folder_path, 'ThanhLong*.txt')
files = glob.glob(file_pattern)

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Thay thế số 0 đầu dòng bằng 2
    new_lines = []
    for line in lines:
        if line.strip().startswith('0 '):
            new_line = '2' + line[1:]  # Giữ nguyên phần còn lại
        else:
            new_line = line
        new_lines.append(new_line)

    # Ghi đè lại file với nội dung mới
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)

print("Đã cập nhật xong các file.")

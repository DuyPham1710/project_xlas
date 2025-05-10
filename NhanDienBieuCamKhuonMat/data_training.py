import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import seaborn as sns # Để vẽ confusion matrix đẹp hơn
import matplotlib.pyplot as plt # Để hiển thị plot
import os

# Đọc dữ liệu từ file CSV
csv_path = 'NhanDienBieuCamKhuonMat/face_expression_data.csv'  # THAY ĐỔI: Đường dẫn file
try:
    data = pd.read_csv(csv_path)
except FileNotFoundError:
    print(f"Lỗi: Không tìm thấy file '{csv_path}'. Hãy đảm bảo bạn đã chạy script thu thập dữ liệu.")
    exit()
except pd.errors.EmptyDataError:
    print(f"Lỗi: File CSV '{csv_path}' rỗng. Không có dữ liệu để huấn luyện.")
    exit()
except Exception as e:
    print(f"Lỗi khi đọc file CSV: {e}")
    exit()

# Kiểm tra dữ liệu
if data.empty:
    print("Dữ liệu rỗng sau khi đọc file CSV. Kiểm tra lại file.")
    exit()

print(f"Đã đọc thành công dữ liệu. Số dòng: {len(data)}, Số cột: {len(data.columns)}")
print(f"Các nhãn có trong dữ liệu: {data['label'].unique()}")
print(data['label'].value_counts())


# Kiểm tra dữ liệu thiếu
if data.isnull().values.any(): # Kiểm tra toàn bộ DataFrame nhanh hơn
    print("Dữ liệu có giá trị thiếu. Đang loại bỏ các dòng có giá trị thiếu...")
    data_shape_before_dropna = data.shape
    data = data.dropna()
    if data.empty:
        print("Dữ liệu trở nên rỗng sau khi loại bỏ giá trị thiếu. Kiểm tra lại dữ liệu gốc.")
        exit()
    print(f"Đã loại bỏ {data_shape_before_dropna[0] - data.shape[0]} dòng có giá trị thiếu.")
else:
    print("Không có giá trị thiếu trong dữ liệu.")


# Tách dữ liệu thành features (X) và labels (y)
if 'label' not in data.columns:
    print("Lỗi: Không tìm thấy cột 'label' trong file CSV. Header có thể bị sai hoặc thiếu.")
    print(f"Các cột hiện có: {data.columns.tolist()}")
    exit()

X = data.drop('label', axis=1)
y = data['label']

if X.empty or y.empty:
    print("Features (X) hoặc labels (y) rỗng. Điều này không nên xảy ra nếu dữ liệu đầu vào hợp lệ.")
    exit()

# Chia dữ liệu thành tập train và test
# Sử dụng stratify=y để đảm bảo tỷ lệ các lớp được duy trì trong cả tập train và test,
# quan trọng nếu dữ liệu không cân bằng.
try:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y if len(y.unique()) > 1 else None)
except ValueError as e:
    print(f"Lỗi khi chia dữ liệu train/test (có thể do một lớp có quá ít mẫu để stratify): {e}")
    print("Thử chia lại mà không có stratify...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

print(f"Kích thước tập huấn luyện (X_train): {X_train.shape}")
print(f"Kích thước tập kiểm tra (X_test): {X_test.shape}")

# Chuẩn hóa dữ liệu (Rất quan trọng!)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Huấn luyện mô hình với Random Forest
# Bạn có thể thử nghiệm với các tham số khác hoặc các mô hình khác (SVM, MLPClassifier, ...)
# class_weight='balanced' hữu ích nếu các lớp không cân bằng
model = RandomForestClassifier(n_estimators=150, random_state=42, max_depth=20, min_samples_split=3, min_samples_leaf=2, class_weight='balanced')
print("Bắt đầu huấn luyện mô hình Random Forest...")
model.fit(X_train_scaled, y_train)
print("Huấn luyện mô hình hoàn tất.")

# Dự đoán trên tập test
y_pred = model.predict(X_test_scaled)

# Đánh giá mô hình
accuracy = accuracy_score(y_test, y_pred)
print(f"\nĐộ chính xác (Accuracy): {accuracy:.4f}")

print("\nBáo cáo phân loại (Classification Report):")
# zero_division=0 để tránh cảnh báo nếu có lớp nào đó không có trong y_pred (precision/recall=0)
print(classification_report(y_test, y_pred, zero_division=0))

print("\nMa trận nhầm lẫn (Confusion Matrix):")
cm = confusion_matrix(y_test, y_pred, labels=model.classes_) # Sử dụng model.classes_ để đảm bảo thứ tự
print(cm)

# Vẽ ma trận nhầm lẫn
plt.figure(figsize=(10, 7))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=model.classes_, yticklabels=model.classes_)
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.title('Confusion Matrix')
plt.show()


# Lưu mô hình đã huấn luyện và scaler
model_save_path = 'NhanDienBieuCamKhuonMat/face_expression_model.joblib'  # THAY ĐỔI: Tên file model
os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
joblib.dump((model, scaler), model_save_path) # Lưu cả model và scaler
print(f"Đã lưu mô hình và scaler vào '{model_save_path}'")
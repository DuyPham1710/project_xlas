import cv2
import numpy as np

def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    dst = cv2.equalizeHist(gray)
    threshold = cv2.threshold(dst, 50, 255, cv2.THRESH_BINARY)[1]
    blur = cv2.medianBlur(threshold, 15)
    canny = cv2.Canny(blur, 80, 150)
    return canny

def region_of_interest(image):
    height, width = image.shape[:2]

    # Định nghĩa polygon với 4 điểm
    p1 = (0, int(height * 0.5))
    p2 = (width, int(height * 0.5))
    p3 = (int(0.85 * width), int(height * 0.05))
    p4 = (int(0.15 * width), int(height * 0.05))
    polygon = np.array([[p1, p2, p3, p4]], dtype=np.int32)

    # Tạo mặt nạ (mask)
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygon, (255, 255, 255))

    # Áp mặt nạ
    masked_image = cv2.bitwise_and(image, mask)

    return masked_image

def detect_lines(cropped_image):
    rho = 2
    theta = np.pi / 180
    threshold = 100
    min_line_length = 40
    max_line_gap = 5

    lines = cv2.HoughLinesP(cropped_image, rho, theta, threshold,
                            minLineLength=min_line_length,
                            maxLineGap=max_line_gap)
    return lines

def make_coordinates(image, slope, intercept):
    height, width = image.shape[:2]
    y1 = height
    y2 = int(height * 0.3)

    try:
        x1 = int((y1 - intercept) / slope)
        x2 = int((y2 - intercept) / slope)
    except ZeroDivisionError:
        x1, x2 = 0, 0  # Nếu chia cho 0, set mặc định

    # Giới hạn x1 trong phạm vi chiều rộng ảnh
    if x1 < -1000:
        x1 = 0
    elif x1 > 1000:
        x1 = width - 1

    # Giới hạn x2 trong phạm vi chiều rộng ảnh
    if x2 < -1000:
        x2 = 0
    elif x2 > 1000:
        x2 = width - 1
    return [x1, y1, x2, y2]

def average_slope_intercept(image, lines):
    left_slopes = []
    left_intercepts = []
    right_slopes = []
    right_intercepts = []

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]

            if x1 == x2:  # tránh chia cho 0
                continue

            slope = (y2 - y1) / (x2 - x1)
            intercept = y1 - slope * x1

            if slope < 0:
                left_slopes.append(slope)
                left_intercepts.append(intercept)
            else:
                right_slopes.append(slope)
                right_intercepts.append(intercept)

    lines_to_draw = []

    if left_slopes:
        avg_left_slope = sum(left_slopes) / len(left_slopes)
        avg_left_intercept = sum(left_intercepts) / len(left_intercepts)
        left_line = make_coordinates(image, avg_left_slope, avg_left_intercept)
        lines_to_draw.append(left_line)

    if right_slopes:
        avg_right_slope = sum(right_slopes) / len(right_slopes)
        avg_right_intercept = sum(right_intercepts) / len(right_intercepts)
        right_line = make_coordinates(image, avg_right_slope, avg_right_intercept)
        lines_to_draw.append(right_line)

    return np.array(lines_to_draw, dtype=np.int32)

def display_lines(image, lines):
    line_image = np.zeros_like(image)
    line_color = (255, 0, 0)  # BGR: đỏ
    line_thickness = 10

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line
            cv2.line(line_image, (x1, y1), (x2, y2), line_color, line_thickness)

    return line_image

def combine_images(original_image, line_image):
    alpha = 0.8
    beta = 1.0
    gamma = 0.0
    combo_image = cv2.addWeighted(original_image, alpha, line_image, beta, gamma)
    return combo_image
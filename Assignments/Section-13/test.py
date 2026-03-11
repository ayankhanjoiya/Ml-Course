import cv2
import numpy as np
import os

os.makedirs("output", exist_ok=True)


def nothing(value):
    pass


cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Webcam not found.")
    exit()

cv2.namedWindow("Controls")
cv2.createTrackbar("Brightness", "Controls", 100, 200, nothing)   # -100 to +100
cv2.createTrackbar("Contrast", "Controls", 10, 30, nothing)       # 0.0 to 3.0
cv2.createTrackbar("Sharpness", "Controls", 0, 10, nothing)       # 0 to 10
cv2.createTrackbar("Hue", "Controls", 90, 180, nothing)           # -90 to +90
cv2.createTrackbar("Saturation", "Controls", 10, 30, nothing)     # 0.0 to 3.0

print("Press S to save the image or ESC to exit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    brightness = cv2.getTrackbarPos("Brightness", "Controls") - 100
    contrast = cv2.getTrackbarPos("Contrast", "Controls") / 10
    sharpness = cv2.getTrackbarPos("Sharpness", "Controls") / 5
    hue = cv2.getTrackbarPos("Hue", "Controls") - 90
    saturation = cv2.getTrackbarPos("Saturation", "Controls") / 10

    # Contrast (alpha) and brightness (beta)
    result = cv2.convertScaleAbs(frame, alpha=contrast, beta=brightness)

    # Sharpness using unsharp masking
    if sharpness > 0:
        blurred = cv2.GaussianBlur(result, (0, 0), 3)
        result = cv2.addWeighted(result, 1 + sharpness, blurred, -sharpness, 0)

    # Hue and saturation in the HSV colour space
    hsv = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)
    hsv[:, :, 0] = (hsv[:, :, 0].astype(int) + hue) % 180
    sat = hsv[:, :, 1].astype(float) * saturation
    hsv[:, :, 1] = np.clip(sat, 0, 255).astype(np.uint8)
    result = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    cv2.imshow("Original | Adjusted", np.hstack((frame, result)))

    key = cv2.waitKey(1) & 0xFF
    if key == ord("s"):
        cv2.imwrite("output/adjusted.jpg", result)
        print("Adjusted image saved to output/adjusted.jpg")
    elif key == 27:
        break

cap.release()
cv2.destroyAllWindows()

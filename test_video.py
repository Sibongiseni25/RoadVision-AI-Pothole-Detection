from ultralytics import YOLO
import cv2

# Load trained pothole model
model = YOLO(
    r"runs\detect\runs\pothole_detector\weights\best.pt"
)

# Input video
video_path = r"videos\road.mp4"

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

print("Starting pothole detection...")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Run pothole detection
    results = model(
        frame,
        conf=0.25,
        verbose=False
    )

    # Draw bounding boxes and labels
    annotated_frame = results[0].plot()

    # Show video
    cv2.imshow("Pothole Detection", annotated_frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

print("Pothole detection finished.")
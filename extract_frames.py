import cv2
import os

video_path = "videos/road.mp4"
output_folder = "dataset/images/all"

os.makedirs(output_folder, exist_ok=True)

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("ERROR: Could not open video.")
    exit()

frame_number = 0
saved_number = 0

# Save 1 frame every 10 frames
frame_interval = 10

while True:
    ret, frame = cap.read()

    if not ret:
        break

    if frame_number % frame_interval == 0:

        filename = os.path.join(
            output_folder,
            f"frame_{saved_number:04d}.jpg"
        )

        cv2.imwrite(filename, frame)

        saved_number += 1

    frame_number += 1

cap.release()

print("======================================")
print("Frame extraction completed.")
print(f"Original frames: {frame_number}")
print(f"Frames saved:    {saved_number}")
print(f"Saved to:        {output_folder}")
print("======================================")
from ultralytics import YOLO

# Load YOLO11 nano model
model = YOLO("yolo11n.pt")

# Train the model
results = model.train(
    data="pothole-dataset/data.yaml",
    epochs=50,
    imgsz=640,
    batch=8,
    name="pothole_detector",
    project="runs",
    patience=15,
    plots=True
)

print("\nTraining completed!")
print("Best model saved at:")
print("runs/pothole_detector/weights/best.pt")
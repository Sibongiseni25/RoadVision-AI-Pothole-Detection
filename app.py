
from flask import Flask, render_template, request, url_for
from ultralytics import YOLO
from werkzeug.utils import secure_filename
from pathlib import Path
import imageio_ffmpeg
import subprocess
import cv2
import uuid

# ==========================================
# FLASK CONFIGURATION
# ==========================================

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent

UPLOAD_FOLDER = BASE_DIR / "static" / "uploads"
RESULT_FOLDER = BASE_DIR / "static" / "results"

UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
RESULT_FOLDER.mkdir(parents=True, exist_ok=True)

app.config["MAX_CONTENT_LENGTH"] = 200 * 1024 * 1024

ALLOWED_EXTENSIONS = {"mp4", "avi", "mov", "mkv"}

# ==========================================
# LOAD TRAINED YOLO11 MODEL
# ==========================================

MODEL_PATH = BASE_DIR / "models" / "best.pt"

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"YOLO model not found: {MODEL_PATH}"
    )

model = YOLO(str(MODEL_PATH))

print("YOLO11 pothole detection model loaded!")

# ==========================================
# CHECK UPLOADED FILE
# ==========================================

def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )

# ==========================================
# PROCESS VIDEO WITH YOLO11
# ==========================================

def process_video(input_path, output_path):

    temp_path = output_path.with_name(
        output_path.stem + "_temp.mp4"
    )

    cap = cv2.VideoCapture(str(input_path))

    if not cap.isOpened():
        raise RuntimeError("Could not open uploaded video.")

    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps <= 0 or fps > 120:
        fps = 25

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if width <= 0 or height <= 0:
        cap.release()
        raise RuntimeError("Invalid video dimensions.")

    writer = cv2.VideoWriter(
        str(temp_path),
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height)
    )

    if not writer.isOpened():
        cap.release()
        raise RuntimeError("Could not create output video.")

    total_detections = 0
    total_frames = 0
    frames_with_potholes = 0

    try:
        while True:

            ret, frame = cap.read()

            if not ret:
                break

            # Detect potholes
            results = model(
                frame,
                conf=0.25,
                verbose=False
            )

            # Count detections in this frame
            detections = len(results[0].boxes)

            total_detections += detections
            total_frames += 1

            if detections > 0:
                frames_with_potholes += 1

            # Draw bounding boxes
            annotated_frame = results[0].plot()

            # Display detection count on video
            cv2.rectangle(
                annotated_frame,
                (10, 10),
                (330, 65),
                (15, 23, 42),
                -1
            )

            cv2.putText(
                annotated_frame,
                f"Potholes in frame: {detections}",
                (20, 45),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.75,
                (255, 255, 255),
                2
            )

            writer.write(annotated_frame)

    finally:
        cap.release()
        writer.release()

    if total_frames == 0:
        raise RuntimeError("No frames were read from the video.")

    # ==========================================
    # CONVERT VIDEO TO BROWSER-COMPATIBLE H.264
    # ==========================================

    print("Converting video to H.264...")

    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()

    command = [
        ffmpeg_path,
        "-y",
        "-i", str(temp_path),
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        str(output_path)
    ]

    try:
        subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True
        )

    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"FFmpeg conversion failed:\n{e.stderr[-1500:]}"
        ) from e

    finally:
        temp_path.unlink(missing_ok=True)

    print("Video conversion completed!")

    return {
        "total_detections": total_detections,
        "total_frames": total_frames,
        "frames_with_potholes": frames_with_potholes
    }


# ==========================================
# DASHBOARD ROUTE
# ==========================================

@app.route("/", methods=["GET", "POST"])
def home():

    original_video = None
    detected_video = None

    total_detections = 0
    total_frames = 0
    frames_with_potholes = 0

    error = None

    if request.method == "POST":

        file = request.files.get("video")

        if not file or not file.filename:
            error = "Please select a road video."

        elif not allowed_file(file.filename):
            error = "Unsupported video format."

        else:
            try:
                safe_name = secure_filename(file.filename)

                video_id = uuid.uuid4().hex[:12]

                extension = Path(safe_name).suffix.lower()

                input_name = f"{video_id}{extension}"
                output_name = f"{video_id}_detected.mp4"

                input_path = UPLOAD_FOLDER / input_name
                output_path = RESULT_FOLDER / output_name

                # Save uploaded video
                file.save(str(input_path))

                print("Processing uploaded video...")

                # Run YOLO detection and conversion
                stats = process_video(
                    input_path,
                    output_path
                )

                total_detections = stats["total_detections"]
                total_frames = stats["total_frames"]
                frames_with_potholes = stats["frames_with_potholes"]

                # URLs for browser playback
                original_video = url_for(
                    "static",
                    filename=f"uploads/{input_name}"
                )

                detected_video = url_for(
                    "static",
                    filename=f"results/{output_name}"
                )

                print("Processing completed successfully!")

            except Exception as e:
                error = str(e)
                print("Error:", error)

    return render_template(
        "index.html",
        original_video=original_video,
        detected_video=detected_video,
        total_detections=total_detections,
        total_frames=total_frames,
        frames_with_potholes=frames_with_potholes,
        error=error
    )


# ==========================================
# START FLASK SERVER
# ==========================================

if __name__ == "__main__":
    app.run(debug=True)

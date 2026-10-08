# 🛣️ RoadVision AI — Pothole Detection Dashboard

### AI-Powered Road Surface Monitoring Using YOLO11 and Flask

RoadVision AI is a computer vision-based pothole detection system designed to identify potholes in road videos using a custom-trained YOLO11 object detection model.

The project combines deep learning, computer vision, and web development to provide an interactive dashboard where users can upload road videos, automatically detect potholes, view annotated results, and download processed videos.

The system demonstrates how artificial intelligence can support road infrastructure monitoring and road maintenance assessment.

---

## 🚀 Key Features

- **AI-Powered Pothole Detection:** Identifies potholes using a custom-trained YOLO11 model.
- **Video Upload:** Allows users to upload road videos for analysis.
- **Bounding Box Visualization:** Highlights detected potholes with bounding boxes and confidence scores.
- **Interactive Web Dashboard:** Built using Flask, HTML, and CSS.
- **Detection Statistics:** Displays the total number of detection boxes, frames analyzed, and frames containing potholes.
- **Video Comparison:** Displays original and processed road videos.
- **Video Download:** Allows users to download annotated detection videos.
- **Browser-Compatible Playback:** Converts processed videos to H.264 using FFmpeg.

## 🧠 Model Performance

The custom YOLO11n model was trained for 50 epochs on an annotated pothole dataset.

| Metric | Validation Result |
|---|---|
| Precision | 82.9% |
| Recall | 72.9% |
| mAP@50 | 79.8% |
| mAP@50–95 | 44.4% |
| Training Epochs | 50 |
| Model Architecture | YOLO11n |

**Dataset:** 70 annotated road video frames, split into 49 training images, 14 validation images, and 7 test images.

These metrics are from the validation dataset. Because the dataset is small and derived from one road video, the results should not be interpreted as general performance on unseen roads.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development |
| Ultralytics YOLO11 | Pothole detection |
| OpenCV | Video processing and annotation |
| Flask | Backend web framework |
| HTML5 | Dashboard structure |
| CSS3 | Dashboard styling |
| FFmpeg | Browser-compatible video encoding |
| Roboflow | Dataset annotation and export |
| Git & GitHub | Version control |

## 🏗️ Project Structure

```text
pothole-detection/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── models/
│   └── best.pt
│
├── templates/
│   └── index.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── uploads/
│   └── results/
│
├── train.py
└── test_video.py
```

The `uploads` and `results` directories store video files generated during application use. Training datasets, virtual environments, and temporary experiment outputs are excluded from Git tracking.

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Sibongiseni25/RoadVision-AI-Pothole-Detection.git
cd RoadVision-AI-Pothole-Detection
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate the environment on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

### 5. Open the dashboard

Visit:

http://127.0.0.1:5000

## 📹 How to Use

1. Open the RoadVision AI dashboard.
2. Select a road video from your computer.
3. Click **Analyze Video**.
4. Wait for the YOLO11 model to process the video.
5. View the original and annotated videos side by side.
6. Review the detection statistics.
7. Download the processed video if required.

**Supported upload formats:** MP4, AVI, MOV, and MKV. MP4 is recommended for browser playback.

## 🔄 System Workflow

```text
Road Video Upload
        |
        v
Flask Web Application
        |
        v
OpenCV Video Processing
        |
        v
Custom YOLO11 Model
        |
        v
Pothole Detection
        |
        v
Bounding Box Annotation
        |
        v
H.264 Video Conversion
        |
        v
Dashboard Results and Statistics
        |
        v
Processed Video Download
```

## 📊 Detection Statistics

The dashboard provides the following measurements:

- **Detection Boxes:** Total number of pothole bounding boxes detected across all analyzed frames.
- **Frames Analyzed:** Total number of video frames processed.
- **Frames With Potholes:** Number of frames containing at least one detected pothole.

**Important:** The total detection-box count does not represent the number of unique potholes. The same pothole may be detected across multiple consecutive video frames.

## ⚠️ Current Limitations

- The model was trained using a relatively small dataset.
- Detection performance may vary with lighting, camera angle, road conditions, and video quality.
- The application processes uploaded videos synchronously, which may take time on CPU-only systems.
- The system does not yet track unique potholes across frames.
- Pothole depth and physical severity are not measured.
- The dashboard currently displays statistics for the most recently processed upload rather than maintaining a permanent history.

## 🔮 Future Improvements

- Unique pothole counting using object tracking.
- Live camera pothole detection.
- GPS-based pothole location mapping.
- Pothole severity estimation.
- Historical detection reports and analytics.
- Background video processing with progress tracking.
- Cloud deployment for remote access.

## 🎯 Project Objective

The objective of RoadVision AI is to explore how deep learning and computer vision can automate the identification of visible road surface damage, reducing the need for fully manual video inspection.

This project is a functional prototype intended for learning, experimentation, and further development.

## 👨‍💻 Developer

**Sibongiseni Nogwaja**

Computer Systems Engineering | Python Developer | Machine Learning & Computer Vision

GitHub: [Sibongiseni25](https://github.com/Sibongiseni25)

## 📄 License

No separate software license has been specified for this repository. Refer to the licenses of the included third-party software and dataset resources where applicable.

---

**RoadVision AI — Applying Artificial Intelligence to Smarter Road Monitoring.**
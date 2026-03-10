# 🚧 Road Guard – AI Powered Pothole Detection System

Road Guard is an AI-powered computer vision system designed to detect potholes and road damage in real time. The system uses a YOLOv8 object detection model to identify potholes from camera feeds or images and sends the results to a Flutter mobile application. Detection data is synchronized using Firebase for real-time monitoring and reporting.

## 📌 Project Overview

Poor road conditions are a major cause of accidents, vehicle damage, and traffic disruptions. Road inspections are still largely manual and inefficient.  

Road Guard aims to automate pothole detection using AI and provide a system that can report road damage quickly and efficiently.

The system:
- Detects potholes using a trained YOLOv8 model
- Uploads detected images to ImgBB
- Stores image URLs in Firebase
- Displays pothole reports in a Flutter mobile application

---

# 🧠 System Architecture

### Workflow

1. **Dataset Collection**
   - Road images containing potholes were collected and organized.

2. **Model Training**
   - A YOLOv8 object detection model was trained using a custom dataset.
   - The model learned to detect potholes using bounding boxes.

3. **Real-Time Detection**
   - A Python script loads the trained model.
   - The system processes live camera feed or image input using OpenCV.

4. **Detection Output**
   - Potholes are detected in real time.
   - Detected images are uploaded to ImgBB.
   - The image URL is stored in Firebase.
   - The Flutter app retrieves and displays the data.

---

# ⚙️ Technologies Used

- Python
- Ultralytics YOLOv8
- PyTorch
- OpenCV
- Flutter
- Firebase
- ImgBB Image Hosting
- CUDA GPU Acceleration

---

# 📊 Dataset Details

Dataset Source: Kaggle

| Category | Images |
|--------|--------|
| Normal Road | 412 |
| Pothole | 780 |
| **Total** | **1192** |

Bounding box annotations were used for training the detection model.

---

# 🤖 Model Training Details

| Parameter | Value |
|-----------|------|
| Model | YOLOv8m |
| GPU | RTX 4050 (Laptop) |
| Epochs | 300 |
| Batch Size | 4 |
| Optimizer | AdamW |

### Data Augmentation
- Data augmentation techniques like horizontal flip and vertical flip was used

---

# 📈 Model Performance

| Metric | Score |
|------|------|
| Precision | 65.3% |
| Recall | 66.7% |
| mAP@0.5 | 66.3% |
| mAP@0.5:0.95 | 38.3% |



---

# ☁️ ImgBB + Firebase Implementation

When a pothole is detected:

1. The detected image is uploaded to **ImgBB**
2. ImgBB generates a **public image URL**
3. Only the **URL is stored in Firebase**, reducing database storage usage
4. The Flutter app fetches the URL and displays the image

---

# 📱 Flutter Mobile Application

The Flutter application connects to Firebase and displays pothole detection reports.

Features:
- Splash Screen
- Login Page
- Fetch detected pothole images
- Display images using ImgBB URLs
- Real-time synchronization with Firebase
- Simple user interface for monitoring road damage

---

# 🖥 Deployment

The complete system was deployed on:

- **Raspberry Pi 5**
- **Webcam for live detection**


---

# 🏆 Project Achievement

Road Guard was presented at the **International Digital Fest** conducted by **Cyber Square** at the **University of Dubai**.

Among multiple projects, the system successfully demonstrated:

- Real-time pothole detection
- Cloud-based image storage
- Mobile application integration

🏅 **Road Guard secured 3rd place in the competition.**

---

# 🔮 Future Work

Future improvements may include:

- Deploying the system on public vehicles such as **auto-rickshaws**
- Automatic **GPS-based pothole location tracking**
- Integration with **government road maintenance systems**
- Creating a **centralized road monitoring dashboard**

---

## 📝 Notes

- The **Flutter mobile application source code is not included in this repository**.
- This repository mainly focuses on the **AI model training and real-time pothole detection system**.
- The **Dataset and weights are not included in this repository**.Please contact if needed
- To enable **real time visual of potholes in flutter application** firebase should be integrated manually in the code by visiting [Firebase Official site](https://firebase.google.com/)

📄 For the **complete project documentation and Flutter application images**, please refer to the file below:

👉 **Full Project Document & App Screenshots:**  
[View Full Documentation](https://github.com/rihanmhmd102/Road-Guard/blob/main/Road%20Guard%20-doc.pdf)


---


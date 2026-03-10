# Import required libraries
import cv2                               # OpenCV for image/video processing
from ultralytics import YOLO             # YOLO model for object detection
from datetime import datetime            # For timestamp creation
import requests                          # For sending HTTP requests (upload image)
import threading                         # For background uploading
import time                              # For cooldown timing
import tkinter as tk                     # GUI framework
from tkinter import filedialog           # File selection dialog
from PIL import Image, ImageTk           # Image conversion for Tkinter display
import argparse                          # For command line arguments
import os                                # File and directory operations
import glob                              # File pattern matching
import sys      
from dotenv import load_dotenv                         


load_dotenv()

# ------------------------------------------------------------
# Configuration Section
# ------------------------------------------------------------

# Path to the trained YOLO model
MODEL_PATH = (
    os.getenv("MODEL_PATH")
)

# Load the trained YOLO model
model = YOLO(MODEL_PATH)

# API key for imgbb image hosting service
API_KEY = os.getenv("API_KEY")

# API endpoint for uploading images
UPLOAD_URL = f"https://api.imgbb.com/1/upload?key={API_KEY}"

# Firebase Realtime Database URL for storing pothole detection records
FIREBASE_URL = (
    os.getenv("FIREBASE_URL")
)

# Cooldown time between uploads (seconds)
# Prevents uploading too many images when pothole detected continuously
COOLDOWN_SECONDS = 5

# Stores time of the last upload
_last_upload_time = 0


# ------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------

def _upload_image(jpg_bytes: bytes, timestamp: str) -> None:
    

    try:
        # Prepare the image file to upload
        files = {"image": ("pothole.jpg", jpg_bytes, "image/jpeg")}

        # Send POST request to imgbb API
        resp = requests.post(UPLOAD_URL, files=files)

        # If upload successful
        if resp.status_code == 200:

            # Extract image URL from response
            url = resp.json()["data"]["url"]

            # Send image URL and timestamp to Firebase database
            requests.post(
                FIREBASE_URL,
                json={
                    "timestamp": timestamp,
                    "image_url": url
                }
            )

    except Exception as err:
        # Print error if upload fails
        print("Upload failed:", err)


# ------------------------------------------------------------
# Detection Function
# ------------------------------------------------------------

def detect_and_handle(frame):


    global _last_upload_time

    # Run YOLO prediction on the frame
    result = model.predict(source=frame, imgsz=416, conf=0.25)[0]

    # Draw bounding boxes and labels on detected objects
    out = result.plot()

    # Check if any pothole was detected
    if result.boxes:

        # Add text on screen
        cv2.putText(
            out,
            "Pothole Detected",
            (40, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

        # Get current time
        now = time.time()

        # Check cooldown time before uploading
        if now - _last_upload_time > COOLDOWN_SECONDS:

            _last_upload_time = now

            # Generate timestamp
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")

            # Convert frame to JPEG
            _, buf = cv2.imencode(".jpg", frame)

            # Upload image in a separate thread
            threading.Thread(
                target=_upload_image,
                args=(buf.tobytes(), ts)
            ).start()

    # Return annotated frame
    return out


# ------------------------------------------------------------
# Image Processing
# ------------------------------------------------------------

def process_image_file(path: str):


    # Read image from file
    img = cv2.imread(path)

    if img is None:
        print(f"cant open {path}")
        return

    # Run detection
    res = detect_and_handle(img)

    # Show result window
    cv2.imshow(f"Detection - {os.path.basename(path)}", res)

    # Wait until a key is pressed
    key = cv2.waitKey(0)

    # Close the window
    cv2.destroyWindow(f"Detection - {os.path.basename(path)}")

    # Exit if 'q' pressed
    if key & 0xFF == ord("q"):
        sys.exit(0)


# ------------------------------------------------------------
# Video Processing
# ------------------------------------------------------------

def _process_video_capture(cap, title):


    while True:

        # Read frame from video
        ret, frame = cap.read()

        # Stop if video ended
        if not ret:
            break

        # Detect potholes
        annotated = detect_and_handle(frame)

        # Show processed frame
        cv2.imshow(title, annotated)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Release video resource
    cap.release()

    # Close all windows
    cv2.destroyAllWindows()


# ------------------------------------------------------------
# GUI Interface
# ------------------------------------------------------------

def run_gui():


    root = tk.Tk()
    root.title("Pothole Detection")

    # Video display area
    video_label = tk.Label(root)
    video_label.pack(side=tk.LEFT)

    # Control panel
    ctrl = tk.Frame(root)
    ctrl.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

    # --------------------------------------------------------
    # Open Photos Button
    # --------------------------------------------------------

    def open_photos():

        paths = filedialog.askopenfilenames(
            title="Select photos",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
        )

        for p in paths:
            process_image_file(p)

    # --------------------------------------------------------
    # Open Video Button
    # --------------------------------------------------------

    def open_video():

        path = filedialog.askopenfilename(
            title="Select video file",
            filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv")]
        )

        if path:
            cap = cv2.VideoCapture(path)

            _process_video_capture(
                cap,
                f"Pothole Detection - {os.path.basename(path)}"
            )

    # Buttons in GUI
    tk.Button(ctrl, text="Open Photo(s)", command=open_photos).pack(pady=5, fill=tk.X)
    tk.Button(ctrl, text="Open Video", command=open_video).pack(pady=5, fill=tk.X)

    # --------------------------------------------------------
    # Webcam Capture
    # --------------------------------------------------------

    cap_cam = cv2.VideoCapture(0)

    def update_frame():

        # Read frame from webcam
        ret, frame = cap_cam.read()

        if ret:

            # Run detection
            annotated = detect_and_handle(frame)

            # Convert image format for Tkinter
            img = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)

            im_pil = Image.fromarray(img)

            imgtk = ImageTk.PhotoImage(image=im_pil)

            # Update label image
            video_label.imgtk = imgtk
            video_label.configure(image=imgtk)

        # Repeat every 30 ms
        root.after(30, update_frame)

    update_frame()

    # --------------------------------------------------------
    # Close GUI safely
    # --------------------------------------------------------

    def on_close():
        cap_cam.release()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

    root.mainloop()


# ------------------------------------------------------------
# Main Program
# ------------------------------------------------------------

def main():


    parser = argparse.ArgumentParser(
        description="Pothole detection (camera, photo, video, or GUI)"
    )

    parser.add_argument(
        "-p",
        "--photos",
        type=str,
        help="image file or directory"
    )

    parser.add_argument(
        "-v",
        "--video",
        type=str,
        help="video file"
    )

    parser.add_argument(
        "--nogui",
        action="store_true",
        help="do not launch graphical interface"
    )

    args = parser.parse_args()

    # Launch GUI if no arguments given
    if not args.nogui and not (args.photos or args.video):
        run_gui()
        return

    # --------------------------------------------------------
    # Video mode
    # --------------------------------------------------------

    if args.video:

        if not os.path.isfile(args.video):
            print("video not found:", args.video)
            return

        cap = cv2.VideoCapture(args.video)

        if not cap.isOpened():
            print("cannot open video", args.video)
            return

        print("processing video", args.video)

        _process_video_capture(
            cap,
            f"Pothole Detection - {os.path.basename(args.video)}"
        )

        return

    # --------------------------------------------------------
    # Photo mode
    # --------------------------------------------------------

    if args.photos:

        if os.path.isdir(args.photos):

            files = []

            # Collect all images in folder
            for ext in ("*.jpg", "*.jpeg", "*.png", "*.bmp"):
                files.extend(glob.glob(os.path.join(args.photos, ext)))

            files.sort()

        else:
            files = [args.photos]

        if not files:
            print("no images found in", args.photos)
            return

        for fp in files:
            process_image_file(fp)

        print("finished photos")

        return

    # --------------------------------------------------------
    # Webcam mode
    # --------------------------------------------------------

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Unable to open webcam")
        return

    _process_video_capture(cap, "Pothole Detection")


# Run program
if __name__ == "__main__":
    main()
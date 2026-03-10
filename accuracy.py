from ultralytics import YOLO

def main():
    # Load trained model
    model = YOLO("C:\\dev\\Road Guard\\runs\\detect\\runs\\train\\road.guard_model\\weights\\best.pt")

    # Validate the model
    metrics = model.val()

    print("Precision:", metrics.box.mp)
    print("Recall:", metrics.box.mr)
    print("mAP@0.5:", metrics.box.map50)
    print("mAP@0.5:0.95:", metrics.box.map)

if __name__ == "__main__":
    main()
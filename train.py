from ultralytics import YOLO


def main():
    # Dataset and model paths
    DATASET_CONFIG = "data.yaml"
    PRETRAINED_MODEL = "yolov8m.pt" 

    # Hyperparameters
    EPOCHS = 300
    IMAGE_SIZE = 640
    BATCH_SIZE = 4
    AUGMENT = True
    FLIPLR = 0.5
    FLIPUD = 0.0
    SCALE = 0.5

    # Load model
    model = YOLO(PRETRAINED_MODEL)

    # Train the model
    model.train(
        data=DATASET_CONFIG,
        epochs=EPOCHS,
        imgsz=IMAGE_SIZE,
        batch=BATCH_SIZE,
        name='road.guard_model',
        device='0',
        patience=30,
        optimizer='AdamW',
        augment=AUGMENT,
        fliplr=FLIPLR,
        flipud=FLIPUD,
        scale=SCALE,
        val=True,
        cache='disk',
        close_mosaic=15,
        workers=2,
        project='runs/train',
        exist_ok=True,
        resume=False    )

    # Validate the model
    metrics = model.val()
    print(metrics)

if __name__ == "__main__":
    main() 
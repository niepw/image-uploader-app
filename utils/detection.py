import cv2
import numpy as np
from ultralytics import YOLO
from config import MODEL_PATH

# Load the YOLO model once at module initialization.
# This is critical to avoid reloading the model for every image.
model = YOLO(MODEL_PATH)


def detect_faces(image_bytes: bytes, conf_threshold: float = 0.5):
    """
    Detects faces in an image using a YOLO model.

    Args:
        image_bytes (bytes): The image data in bytes format.
        conf_threshold (float, optional): Confidence threshold for face detection. Defaults to 0.2.

    Returns:
        list of tuple: A list of detected face bounding boxes, each represented as a tuple (x, y, width, height),
        where (x, y) is the top-left corner of the bounding box.
    """
    # Convert the image bytes to a NumPy array then decode to an image.
    np_arr = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # Run inference using YOLO.
    results = model.predict(source=image, conf=conf_threshold)

    # Parse results: YOLO returns a list of result objects.
    detections = []
    for result in results:
        # Ensure that results are moved to CPU and converted to a NumPy array.
        # Each result.boxes.xyxy contains the coordinates [x1, y1, x2, y2].
        bx = (
            result.boxes.xyxy.cpu().numpy()
            if result.boxes.xyxy.is_cuda
            else result.boxes.xyxy.numpy()
        )
        # Optionally, you can also filter by class if the model detects multiple classes.
        for box in bx:
            x1, y1, x2, y2 = box
            # Calculate width and height.
            width = int(x2 - x1)
            height = int(y2 - y1)
            detections.append((int(x1), int(y1), width, height))
    return detections

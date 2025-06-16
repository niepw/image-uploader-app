import cv2
import numpy as np


def redact_faces(image_bytes: bytes, detections: list, method="blur"):
    """
    Redacts faces in an image using the specified method.

    Args:
        image_bytes (bytes): The input image as a byte array (e.g., JPEG-encoded).
        detections (list): A list of face bounding boxes, each as a tuple (x, y, w, h).
        method (str, optional): The redaction method to use. 
            Supported values are "blur" (default) for Gaussian blur and "pixelate" for pixelation.

    Returns:
        bytes: The redacted image encoded as JPEG bytes.

    Raises:
        ValueError: If an unsupported redaction method is specified.

    Note:
        Requires OpenCV (`cv2`) and NumPy (`np`) to be imported.
    """
    # Decode image
    np_arr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    for x, y, w, h in detections:
        roi = image[y : y + h, x : x + w]
        if method == "blur":
            # You can adjust the kernel size for a stronger blur
            roi = cv2.GaussianBlur(roi, (99, 99), 30)
        elif method == "pixelate":
            # Resize down and then up to create a pixelation effect
            temp = cv2.resize(roi, (16, 16), interpolation=cv2.INTER_LINEAR)
            roi = cv2.resize(temp, (w, h), interpolation=cv2.INTER_NEAREST)
        image[y : y + h, x : x + w] = roi

    # Encode image back to bytes
    ret, buf = cv2.imencode(".jpg", image)
    return buf.tobytes()

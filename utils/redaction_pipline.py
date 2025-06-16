from utils import detection, redaction


def detect_and_redact_image(image_bytes: bytes, conf_threshold: float = 0.5) -> bytes:
    """
    Detects faces in an image and redacts them using a specified method.

    Args:
        image_bytes (bytes): The input image in bytes format.

    Returns:
        bytes: The redacted image in bytes format, with detected faces processed according to the chosen redaction method.

    Notes:
        - Uses a YOLO-based face detection model with a confidence threshold of 0.2.
        - The default redaction method is "blur", but other methods (e.g., "pixelate") may be supported.
    """
    # Detect faces using the integrated YOLO model.
    boxes = detection.detect_faces(image_bytes, conf_threshold)

    # Redact detected faces (method could be "blur", "pixelate", etc.)
    redacted_bytes = redaction.redact_faces(image_bytes, boxes, method="blur")

    return redacted_bytes

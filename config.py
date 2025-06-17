"""
Configuration module for the image uploader app.
This module loads configuration settings from environment variables or uses
default values.

It defines the following configuration variables:

- MODEL_PATH: Path to the YOLOv11 face detection model. Can be set via the
  'MODEL_PATH' environment variable.

- REDACTED_FOLDER: Absolute path to the folder where redacted images will be
  stored, located in 'static/redacted_folder/' relative to the current working
  directory.
"""

import os
import urllib.request
from print_color import print as pc

# Ensure the current working directory is set to the script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

# Load configurations from environment variables or use defaults

MODEL_PATH = os.getenv("MODEL_PATH", "models/yolov11l-face.pt")
# Ensure the model path exists
if not os.path.exists(MODEL_PATH):
    # Download the model from akanametov/yolo-face repository if it doesn't
    # exist
    pc(f"Model not found at {MODEL_PATH}. Downloading...", color="red", format="bold")
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    url = "https://github.com/akanametov/yolo-face/releases/download/v0.0.0/yolov11l-face.pt"
    urllib.request.urlretrieve(url, MODEL_PATH)

UPLOADED_FOLDER = os.getenv("UPLOAD_FOLDER", "static/uploaded/")
# Ensure the upload folder exists
os.makedirs(os.path.dirname(UPLOADED_FOLDER), exist_ok=True)

REDACTED_FOLDER = os.getenv("REDACTED_FOLDER", "static/redacted/")
# Ensure the redacted folder exists
os.makedirs(os.path.dirname(REDACTED_FOLDER), exist_ok=True)

TEST_IMAGE_01 = os.getenv("TEST_IMAGE_01", "static/test_images/test_image_01.jpg")
# Ensure the test image folder exists
if not os.path.exists(TEST_IMAGE_01):
    # Download the test images from DSD homepage if it doesn't exist
    pc(
        f"Test image not found at {TEST_IMAGE_01}. Downloading...",
        color="green",
        format="bold",
    )
    os.makedirs(os.path.dirname(TEST_IMAGE_01), exist_ok=True)
    url = "https://www.dsd.gov.hk/uploads/page/FAYE0915.JPG"
    urllib.request.urlretrieve(url, TEST_IMAGE_01)

TEST_IMAGE_02 = os.getenv("TEST_IMAGE_02", "static/test_images/test_image_02.jpg")
# Ensure the test image folder exists
if not os.path.exists(TEST_IMAGE_02):
    # Download the test images from DSD homepage if it doesn't exist
    pc(
        f"Test image not found at {TEST_IMAGE_02}. Downloading...",
        color="yellow",
        format="bold",
    )
    os.makedirs(os.path.dirname(TEST_IMAGE_02), exist_ok=True)
    url = "https://www.dsd.gov.hk/uploads/page/FAYE0978.JPG"
    urllib.request.urlretrieve(url, TEST_IMAGE_02)

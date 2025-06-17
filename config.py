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

# Load configurations from environment variables or use defaults
MODEL_PATH = os.getenv("MODEL_PATH", "models/yolov11l-face.pt")
# Ensure the model path exists
if not os.path.exists(MODEL_PATH):
    # Download the model from http://ultralytics.com/assets/yolov11l-face.pt
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    url = "http://ultralytics.com/assets/yolov11l-face.pt"
    urllib.request.urlretrieve(url, MODEL_PATH)

UPLOADED_FOLDER = os.getenv("UPLOAD_FOLDER", "static/uploaded/")
# Ensure the upload folder exists
os.makedirs(os.path.dirname(UPLOADED_FOLDER), exist_ok=True)
REDACTED_FOLDER = os.getenv("REDACTED_FOLDER", "static/redacted/")
# Ensure the redacted folder exists
os.makedirs(os.path.dirname(REDACTED_FOLDER), exist_ok=True)

"""
Configuration module for the image uploader app.
This module loads configuration settings from environment variables or uses default values.
It defines the following configuration variables:
- MODEL_PATH: Path to the YOLOv11 face detection model. Can be set via the 'MODEL_PATH' environment variable.
- REDACTED_FOLDER: Absolute path to the folder where redacted images will be stored, located in 'static/redacted_folder/' relative to the current working directory.
Prints the resolved paths for debugging purposes.
"""
import os

# Load configurations from environment variables or use defaults
MODEL_PATH = os.getenv("MODEL_PATH", "models/yolov11l-face.pt")  # Customize as needed
print(f"Using model path: {MODEL_PATH}")
REDACTED_FOLDER = os.getenv("REDACTED_FOLDER", "static/redacted_folder/")
print(f"Redacted folder path: {REDACTED_FOLDER}")

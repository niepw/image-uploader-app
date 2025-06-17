"""
A Flask web application for uploading images, processing them for redaction,
and serving both original and redacted images.

Modules:
    os: For file and directory operations.

    flask: For web framework functionalities.

    werkzeug.utils: For securing uploaded filenames.

    utils.redaction_pipeline: For image redaction processing.

Configuration:
    UPLOAD_FOLDER: Directory to store uploaded images.

    REDACTED_FOLDER: Directory to store redacted images.

Routes:
    / (GET, POST): Main page for uploading images. Handles file upload, saves
    the original image, processes it for redaction, and saves the redacted
    image. Renders the index page with the filename if an image is uploaded.

    /uploads/<filename> (GET): Redirects to the static URL for the uploaded
    image.

Functions:
    index(): Handles image upload and redaction processing.

    uploaded_file(filename): Redirects to the static file location for the
    uploaded image.

Usage:
    Run this script to start the Flask development server. Access the web
    interface to upload and redact images.
"""

import os
from config import UPLOADED_FOLDER, REDACTED_FOLDER
from utils.redaction_pipeline import detect_and_redact_image
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Handles the main route for image uploading and redaction.

    If the request method is POST and an image file is provided, the function:
    - Secures and sanitizes the uploaded filename.
    - Reads the image file content.
    - Saves the original image to the configured upload folder.
    - Processes the image using `detect_and_redact_image` and saves the
      redacted version to the redacted folder.
    - Renders the index template with the filename of the uploaded image.

    If the request method is GET or no file is uploaded, renders the index
    template without a filename.

    Returns:
        Rendered HTML template for the index page, with or without the
        uploaded filename.
    """
    if request.method == "POST":
        file = request.files["image"]
        if file:
            # Ensure the filename is unique or sanitized if necessary
            filename = secure_filename(file.filename)
            content = file.read()
            # Save the original file to the upload folder
            with open(f"{UPLOADED_FOLDER}{filename}", "wb") as f:
                f.write(content)
            # Process the image and save the redacted version
            with open(f"{REDACTED_FOLDER}{filename}", "wb") as f:
                f.write(detect_and_redact_image(content, 0.2))
            return render_template("index.html", filename=filename)

    # If the request method is GET or if no file was uploaded, render the
    # index page without a filename
    print("No file uploaded or GET request received.")
    return render_template("index.html", filename=None)


@app.route("/uploaded/<filename>")
def uploaded_file(filename):
    """
    Redirects the client to the URL of the uploaded file in the static
    directory.

    Args:
        filename (str): The name of the uploaded file.

    Returns:
        Response: A Flask redirect response to the static file location with
        HTTP status code 301.
    """
    return redirect(url_for("static", filename=f"uploaded/{filename}"), code=301)


@app.route("/redacted/<filename>")
def redacted_file(filename):
    """
    Redirects the client to the URL of the redacted file in the static
    directory.

    Args:
        filename (str): The name of the redacted file.

    Returns:
        Response: A Flask redirect response to the static file location with
        HTTP status code 301.
    """
    return redirect(url_for("static", filename=f"redacted/{filename}"), code=301)


if __name__ == "__main__":
    app.run(debug=True)

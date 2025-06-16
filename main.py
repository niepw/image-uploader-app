from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from utils.redaction_pipline import detect_and_redact_image

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploaded/"
# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# Set the upload folder in the app configuration
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

REDACTED_FOLDER = "static/redacted/"
# Ensure the redacted folder exists
os.makedirs(REDACTED_FOLDER, exist_ok=True)
# Set the redacted folder in the app configuration
app.config["REDACTED_FOLDER"] = REDACTED_FOLDER


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["image"]
        if file:
            # Ensure the filename is unique or sanitized if necessary
            filename = file.filename
            filename = filename.replace(" ", "_")
            filename = filename.replace("/", "_")
            filename = filename.replace("\\", "_")
            filename = filename.replace(":", "_")
            filename = filename.replace("?", "_")
            filename = filename.replace("*", "_")
            filename = filename.replace("<", "_")
            filename = filename.replace(">", "_")
            filename = filename.replace("|", "_")
            filename = filename.replace('"', "_")
            filename = filename.replace("'", "_")
            filename = filename.replace(".", "_")
            content = file.read()
            # Save the original file to the upload folder
            with open(f"{app.config['UPLOAD_FOLDER']}{filename}", "wb") as f:
                f.write(content)
            # Process the image and save the redacted version
            with open(f"{app.config['REDACTED_FOLDER']}{filename}", "wb") as f:
                f.write(detect_and_redact_image(content, 0.2))
            return render_template("index.html", filename=filename)

    # If the request method is GET or if no file was uploaded, render the index page without a filename
    print("No file uploaded or GET request received.")
    return render_template("index.html", filename=None)


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return redirect(url_for("static", filename=f"uploaded/{filename}"), code=301)


if __name__ == "__main__":
    app.run(debug=True)

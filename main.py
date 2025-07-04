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
from urllib.parse import urlparse
from flask import (
    Flask,
    request,
    render_template,
    redirect,
    session,
    url_for,
    make_response,
)
from werkzeug.utils import secure_filename
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.utils import OneLogin_Saml2_Utils
from utils.redaction_pipeline import detect_and_redact_image
from config import UPLOADED_FOLDER, REDACTED_FOLDER 

app = Flask(__name__)
app.config["SECRET_KEY"] = "b613679a0814d9ec772f95d778c35fc5ff1697c493715653c6c712144292c5ad"
app.config["SAML_PATH"] = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "saml"
)


def init_saml_auth(req):
    auth = OneLogin_Saml2_Auth(req, custom_base_path=app.config["SAML_PATH"])
    return auth


# Utility to convert Flask request
def prepare_flask_request(request):
    # If server is behind proxys or balancers use the HTTP_X_FORWARDED fields
    return {
        "https": "on" if request.scheme == "https" else "off",
        "http_host": request.host,
        "script_name": request.path,
        "get_data": request.args.copy(),
        # Uncomment if using ADFS as IdP, https://github.com/onelogin/python-saml/pull/144
        'lowercase_urlencoding': True,
        "post_data": request.form.copy(),
    }


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
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    errors = []
    error_reason = None
    not_auth_warn = False
    success_slo = False
    attributes = False
    paint_logout = False

    if "sso" in request.args:
        return redirect(auth.login())
        # If AuthNRequest ID need to be stored in order to later validate it, do instead
        # sso_built_url = auth.login()
        # request.session['AuthNRequestID'] = auth.get_last_request_id()
        # return redirect(sso_built_url)
    elif "sso2" in request.args:
        return_to = "%sattrs/" % request.host_url
        return redirect(auth.login(return_to))
    elif "slo" in request.args:
        name_id = session_index = name_id_format = name_id_nq = name_id_spnq = None
        if "samlNameId" in session:
            name_id = session["samlNameId"]
        if "samlSessionIndex" in session:
            session_index = session["samlSessionIndex"]
        if "samlNameIdFormat" in session:
            name_id_format = session["samlNameIdFormat"]
        if "samlNameIdNameQualifier" in session:
            name_id_nq = session["samlNameIdNameQualifier"]
        if "samlNameIdSPNameQualifier" in session:
            name_id_spnq = session["samlNameIdSPNameQualifier"]

        return redirect(
            auth.logout(
                name_id=name_id,
                session_index=session_index,
                nq=name_id_nq,
                name_id_format=name_id_format,
                spnq=name_id_spnq,
            )
        )
    elif "acs" in request.args:
        request_id = None
        if "AuthNRequestID" in session:
            request_id = session["AuthNRequestID"]

        auth.process_response(request_id=request_id)
        errors = auth.get_errors()
        not_auth_warn = not auth.is_authenticated()
        if len(errors) == 0:
            if "AuthNRequestID" in session:
                del session["AuthNRequestID"]
            session["samlUserdata"] = auth.get_attributes()
            session["samlNameId"] = auth.get_nameid()
            session["samlNameIdFormat"] = auth.get_nameid_format()
            session["samlNameIdNameQualifier"] = auth.get_nameid_nq()
            session["samlNameIdSPNameQualifier"] = auth.get_nameid_spnq()
            session["samlSessionIndex"] = auth.get_session_index()
            self_url = OneLogin_Saml2_Utils.get_self_url(req)
            if "RelayState" in request.form and self_url != request.form["RelayState"]:
                # To avoid 'Open Redirect' attacks, before execute the redirection confirm
                # the value of the request.form['RelayState'] is a trusted URL.
                return redirect(auth.redirect_to(request.form["RelayState"]))
        elif auth.get_settings().is_debug_active():
            error_reason = auth.get_last_error_reason()
    elif "sls" in request.args:
        request_id = None
        if "LogoutRequestID" in session:
            request_id = session["LogoutRequestID"]
        
        def dscb():
            return session.clear()
        
        url = auth.process_slo(request_id=request_id, delete_session_cb=dscb())
        errors = auth.get_errors()
        if len(errors) == 0:
            if url is not None:
                # To avoid 'Open Redirect' attacks, before execute the redirection confirm
                # the value of the url is a trusted URL.
                return redirect(url)
            else:
                success_slo = True
        elif auth.get_settings().is_debug_active():
            error_reason = auth.get_last_error_reason()

    if "samlUserdata" in session:
        paint_logout = True
        if len(session["samlUserdata"]) > 0:
            attributes = session["samlUserdata"]
            print(f"Attributs: {attributes}")

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
                # return render_template("index.html", filename=filename)
                return render_template(
                    "index.html",
                    filename=filename,
                    errors=errors,
                    error_reason=error_reason,
                    not_auth_warn=not_auth_warn,
                    success_slo=success_slo,
                    attributes=attributes,
                    paint_logout=paint_logout,
                )

    # If the request method is GET or if no file was uploaded, render the
    # index page without a filename
    print("No file uploaded or GET request received.")
    # return render_template("index.html", filename=None)
    return render_template(
        "index.html",
        filename=None,
        errors=errors,
        error_reason=error_reason,
        not_auth_warn=not_auth_warn,
        success_slo=success_slo,
        attributes=attributes,
        paint_logout=paint_logout,
    )


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


@app.route('/metadata/')
def metadata():
    """
    Endpoint to serve SAML metadata for the service provider.
    """
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    settings = auth.get_settings()
    metadata = settings.get_sp_metadata()
    errors = settings.validate_metadata(metadata)

    if len(errors) == 0:
        resp = make_response(metadata, 200)
        resp.headers["Content-Type"] = "text/xml"
    else:
        resp = make_response(", ".join(errors), 500)
    return resp


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, ssl_context=('server.crt', 'server.key'))

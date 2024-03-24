import subprocess
import os
import tempfile
import base64
from google.cloud import storage  # You may need to install this

def decrypt_base64_string(encoded_string):
    """Decrypts a base64-encoded image file string and writes it to a temporary file"""

    with tempfile.NamedTemporaryFile(mode='w+b', delete=False) as f:
        image_data = base64.b64decode(encoded_string)
        f.write(image_data)
        f.flush()

    return f.name

def extract_exif_data(file_path):
    """Extracts Exif metadata using ExifTool."""
    try:
        # Check if exiftool package is installed
        import exiftool
    except ImportError:
        # Install exiftool package if not already installed
        subprocess.check_call(["pip", "install", "exiftool"])
        import exiftool

    exif_data = exiftool.process_file(image_file_name, "-DateTimeOriginal")
    return exif_data.pop(0)

def extract_image_metadata(request):  
    if request.method != "POST":
        return "Only POST requests are accepted", 405

    if not request.is_json:
        return jsonify({"error": "Request body must be JSON"}), 400

    try:
        image_file_name = request.json["image_file_name"]
    except KeyError:
        return jsonify({"error": "image_file_name is a required field"}), 400

    # Base64 decoding and temporary file handling
    try:
        image_data = base64.b64decode(image_file_name)
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(image_data)
            temp_file_name = temp_file.name
    except Exception as e:
        return jsonify({"error": "Error decoding image data: {}".format(e)}), 400

    # Extract Exif metadata
    try:
        metadata = extract_exif_data(temp_file_name)
        return jsonify(metadata), 200
    except Exception as e:
        return jsonify({"error": "Error extracting Exif data: {}".format(e)}), 500
    finally:
        os.remove(temp_file_name) 

from flask import Flask, request, jsonify, render_template
import whisper
import os
from werkzeug.utils import secure_filename
import mimetypes

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Load model Whisper
model = whisper.load_model("base")

# Create the uploads folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_audio():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Validate file type
    mime_type, _ = mimetypes.guess_type(file.filename)
    if mime_type not in ["audio/mpeg", "audio/wav"]:
        return jsonify({"error": "Unsupported file type"}), 400

    # Save the file securely
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    try:
        file.save(filepath)
    except Exception as e:
        return jsonify({"error": f"Failed to save file: {str(e)}"}), 500

    try:
        # Process the audio with Whisper
        result = model.transcribe(filepath)
        text = result.get("text", "").strip()
        if not text:
            return jsonify({"error": "No transcribable content found in the audio"}), 400
        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": f"Failed to process audio: {str(e)}"}), 500
    finally:
        # Clean up the uploaded file to save disk space
        if os.path.exists(filepath):
            os.remove(filepath)

if __name__ == "__main__":
    app.run(debug=True)
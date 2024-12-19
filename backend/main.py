import os
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import subprocess

# Tworzymy aplikację Flask
app = Flask(__name__, static_folder="build")  # build to folder z zbudowanym frontendem
CORS(app)

# Użycie zmiennej środowiskowej PORT, jeśli jest dostępna, lub domyślnie 5000
port = int(os.environ.get("PORT", 5000))

# Domyślny folder pobierania
DEFAULT_DOWNLOAD_FOLDER = str(Path.home() / "Downloads")

@app.route("/")
def serve_frontend():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def serve_static_files(path):
    return send_from_directory(app.static_folder, path)

@app.route("/download", methods=["POST"])
def download_video():
    try:
        data = request.get_json()
        video_url = data.get("videoUrl")

        if not video_url:
            return jsonify({"error": "URL jest wymagany"}), 400
        
        # Pobieranie wideo za pomocą yt-dlp
        output_file = f"{DEFAULT_DOWNLOAD_FOLDER}/%(title)s.%(ext)s"
        subprocess.run([
            "yt-dlp",
            "--no-mtime",
            "--cookies-from-browser", "opera",  
            "-o", output_file,
            video_url
        ], check=True)
        

        return jsonify({"message": "Pobieranie skończone pomyślnie!"}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Coś poszło nie tak"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True)

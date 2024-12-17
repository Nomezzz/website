import os
from pathlib import Path
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)

# Użycie zmiennej środowiskowej PORT, jeśli jest dostępna, lub domyślnie 5000
port = int(os.environ.get("PORT", 5000))

# Domyślny folder pobierania
DEFAULT_DOWNLOAD_FOLDER = str(Path.home() / "Downloads")

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
            "-o", output_file,
            video_url
        ], check=True)

        # Znalezienie pobranego pliku (dopasowanie do nazwy pliku)
        downloaded_file = next(
            (f for f in os.listdir(DEFAULT_DOWNLOAD_FOLDER) if f.startswith("downloaded_video")),
            None
        )

        if downloaded_file:
            # Wysyłanie pliku do użytkownika
            return send_file(os.path.join(DEFAULT_DOWNLOAD_FOLDER, downloaded_file), as_attachment=True)

        return jsonify({"message": "Pobieranie skończone pomyślnie!"}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Coś poszło nie tak"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True)

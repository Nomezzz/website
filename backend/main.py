import os
from pathlib import Path
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)

# Domyślny folder pobierania
DEFAULT_DOWNLOAD_FOLDER = str(Path.home() / "Downloads")

@app.route("/download", methods=["POST"])
def download_video():
    try:
        data = request.get_json()
        video_url = data.get("videoUrl")

        if not video_url:
            return jsonify({"error": "URL jest wymagany"}), 400
        
         # Tymczasowy folder na pliki
        output_file = "downloaded_video.%(ext)s"

        # Pobieranie wideo za pomocą yt-dlp
        subprocess.run([
            "yt-dlp",
            "--no-mtime",
            "-o", f"{DEFAULT_DOWNLOAD_FOLDER}/%(title)s.%(ext)s",
            video_url
        ], check=True)

        # Znalezienie pobranego pliku (możesz to dopasować do konkretnych potrzeb)
        downloaded_file = next(
            (f for f in os.listdir() if f.startswith("downloaded_video")),
            None
        )

        if downloaded_file:
            # Wysyłanie pliku do użytkownika
            return send_file(downloaded_file, as_attachment=True)
        

        


        return jsonify({"message": "Pobieranie skończone pomyślnie!"}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Coś poszło nie tak"}), 500

if __name__ == "__main__":
    app.run(debug=True)

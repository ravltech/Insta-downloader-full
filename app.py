from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__, static_folder="static")
CORS(app)

@app.route("/")
def serve_home():
    return send_from_directory("static", "index.html")

@app.route("/download", methods=["POST"])
def download():
    try:
        data = request.get_json()
        url = data["url"]

        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'extract_flat': False,
            'forcejson': True,
            'noplaylist': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({"success": True, "video": info["url"]})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

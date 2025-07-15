from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import librosa
import numpy as np
import soundfile as sf
from spleeter.separator import Separator

app = Flask(__name__, static_folder='static')
CORS(app, origins=["https://2rochi17.github.io"])  # GitHub Pages 주소

MP3_FILE = "static/iu.good_day.mp3"
OUTPUT_DIR = "output"
OUTPUT_FILE = "static/iu_mixed.wav"

@app.route('/api/mix', methods=['POST'])
def mix_audio():
    try:
        settings = request.get_json()
        gains = {
            "vocals": settings.get("voice", 0),
            "drums": settings.get("drums", 0),
            "bass": settings.get("bass", 0),
            "other": settings.get("other", 0)
        }

        separator = Separator('spleeter:4stems')
        # output 폴더가 없으면 생성
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
        
        separator.separate_to_file(MP3_FILE, OUTPUT_DIR)

        base_path = os.path.join(OUTPUT_DIR, os.path.splitext(os.path.basename(MP3_FILE))[0])
        mixed = []

        for stem in ['vocals', 'drums', 'bass', 'other']:
            stem_file = os.path.join(base_path, f"{stem}.wav")
            if not os.path.exists(stem_file):
                return jsonify({"status": "error", "message": f"{stem_file} not found"}), 404
            y, sr = librosa.load(stem_file, sr=None)
            gain = 10 ** (gains[stem] / 20)
            mixed.append(y * gain)

        final = np.sum(mixed, axis=0)
        sf.write(OUTPUT_FILE, final, sr)
        return jsonify({"status": "success", "url": "/static/iu_mixed.wav"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/static/<path:filename>')
def static_files(filename):
    # static 폴더 내 파일 제공
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

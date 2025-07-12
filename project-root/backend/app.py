import os
import sys
import subprocess

# 자동 설치 (로컬 개발용)
def install_if_needed(package):
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

for pkg in ["flask", "flask_cors", "librosa", "numpy", "soundfile", "spleeter"]:
    install_if_needed(pkg)

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import librosa
import numpy as np
import soundfile as sf
from spleeter.separator import Separator

app = Flask(__name__)
CORS(app, origins=["https://2rochi17.github.io/2025yjproject/"]) 

MP3_FILE = "static/iu.good_day.mp3"
OUTPUT_FILE = "static/iu_mixed.wav"

@app.route('/api/mix', methods=['POST'])
def mix_audio():
    try:
        settings = request.get_json()
        voice_db = settings.get("voice", 0)
        drums_db = settings.get("drums", 0)
        bass_db = settings.get("bass", 0)
        other_db = settings.get("other", 0)

        separator = Separator('spleeter:4stems')
        separator.separate_to_file(MP3_FILE, 'output')

        stem_path = os.path.join('output', os.path.splitext(MP3_FILE)[0], '')
        stems = ['vocals', 'drums', 'bass', 'other']
        stem_data = []
        for stem in stems:
            data, sr = librosa.load(os.path.join(stem_path, f"{stem}.wav"), sr=None)
            gain_db = {
                'vocals': voice_db,
                'drums': drums_db,
                'bass': bass_db,
                'other': other_db
            }[stem]
            factor = 10**(gain_db / 20)
            stem_data.append(data * factor)

        mixed = np.sum(stem_data, axis=0)
        sf.write(OUTPUT_FILE, mixed, sr)

        return jsonify({"status": "success", "url": "/" + OUTPUT_FILE})
    except Exception as e:
        print("❌ 서버 오류:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run()

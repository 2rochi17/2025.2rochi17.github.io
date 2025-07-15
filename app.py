from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import librosa
import numpy as np
import soundfile as sf
from spleeter.separator import Separator

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "https://2rochi17.github.io"}})  # CORS 정책 강화

MP3_FILE = "static/iu.good_day.mp3"
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

        # Spleeter로 분리
        separator = Separator('spleeter:4stems')
        separator.separate_to_file(MP3_FILE, 'output')

        # static/iu.good_day.mp3 → iu.good_day
        filename_without_ext = os.path.splitext(os.path.basename(MP3_FILE))[0]
        base_path = os.path.join("output", filename_without_ext)

        mixed = []

        for stem in ['vocals', 'drums', 'bass', 'other']:
            stem_file = os.path.join(base_path, f"{stem}.wav")
            if not os.path.exists(stem_file):
                raise FileNotFoundError(f"Stem not found: {stem_file}")
            y, sr = librosa.load(stem_file, sr=None)
            gain = 10 ** (gains[stem] / 20)
            mixed.append(y * gain)

        final = np.sum(mixed, axis=0)
        sf.write(OUTPUT_FILE, final, sr)
        return jsonify({"status": "success", "url": "/static/iu_mixed.wav"})

    except Exception as e:
        print("[ERROR]", str(e))  # 콘솔 출력도 함께
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/static/<path:filename>')
def static_file(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run()

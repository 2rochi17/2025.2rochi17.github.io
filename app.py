from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS, cross_origin
import os
import librosa
import numpy as np
import soundfile as sf
from spleeter.separator import Separator

app = Flask(__name__)
CORS(app, origins=["https://2rochi17.github.io"])  # 앱 전체에 적용해도 괜찮고,
# 또는 아래처럼 개별 라우트에 cross_origin 사용 가능

MP3_FILE = "static/iu.good_day.mp3"
OUTPUT_FILE = "static/iu_mixed.wav"

@app.route('/api/mix', methods=['POST', 'OPTIONS'])
@cross_origin(origin='https://2rochi17.github.io')  # ✅ CORS 강제 허용
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

        base_path = os.path.join("output", os.path.splitext(MP3_FILE)[0])
        mixed = []

        for stem in ['vocals', 'drums', 'bass', 'other']:
            stem_file = os.path.join(base_path, f"{stem}.wav")
            y, sr = librosa.load(stem_file, sr=None)
            gain = 10 ** (gains[stem] / 20)
            mixed.append(y * gain)

        final = np.sum(mixed, axis=0)
        sf.write(OUTPUT_FILE, final, sr)

        return jsonify({"status": "success", "url": "/static/iu_mixed.wav"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/static/<path:filename>')
def static_file(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run()

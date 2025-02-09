from flask import Flask, jsonify, request, send_file, render_template
import subprocess
import os

app = Flask(__name__)

SONGS_FOLDER = "songs"

@app.route('/')
def home():
    return render_template("index.html")  # This serves the index.html page

@app.route('/run-script', methods=['POST'])
def run_script():
    try:
        subprocess.Popen(["python", "main.py"])
        return jsonify({"message": "Script started successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get-audio', methods=['GET'])
def get_audio():
    files = [f for f in os.listdir(SONGS_FOLDER) if f.endswith('.mp3')]
    if files:
        return jsonify({"audio_file": f"/songs/{files[0]}"})
    return jsonify({"error": "No MP3 files found"}), 404

@app.route('/songs/<filename>')
def serve_audio(filename):
    return send_file(os.path.join(SONGS_FOLDER, filename))

if __name__ == '__main__':
    app.run(debug=True)

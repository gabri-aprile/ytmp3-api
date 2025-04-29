from flask import Flask, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download_audio():
    data = request.json
    url = data.get('url')
    file_id = str(uuid.uuid4())
    filename = f"{file_id}.mp3"

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': filename,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    response = send_file(filename, mimetype='audio/mpeg')
    os.remove(filename)  # cancella il file dopo l'invio
    return response

app.run(host='0.0.0.0', port=10000)

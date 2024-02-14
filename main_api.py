from flask import Flask, request, jsonify, send_from_directory, send_file
from werkzeug.utils import secure_filename
from datetime import timedelta
import os
import whisper
import uuid

app = Flask(__name__)

# Directorios
audio_directory = "Audio"
srt_directory = "SrtFiles"

def transcribe_audio(path):
    model = whisper.load_model("base")  # Change this to your desired model
    print("Whisper model loaded.")
    transcribe = model.transcribe(audio=path)
    segments = transcribe['segments']

    # Asegurate de que el directorio de SRT exista
    if not os.path.exists(srt_directory):
        print("Creating SrtFiles directory...")
        os.makedirs(srt_directory)

    srtId = uuid.uuid4()
    srtFilename = os.path.join(srt_directory, f"file_{srtId}.srt")
    print(f"Writing to {srtFilename}...")

    for segment in segments:
        startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
        endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
        text = segment['text']
        segmentId = segment['id']+1
        segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n"

        with open(srtFilename, 'a', encoding='utf-8') as srtFile:
            srtFile.write(segment)
    print("Done.")
    return srtFilename

@app.route('/transcribe', methods=['POST'])
def transcribe_endpoint():
    # Asegúrate de que el directorio de audio exista
    if not os.path.exists(audio_directory):
        print("Creating audio directory...")
        os.makedirs(audio_directory)
    # Obtén el archivo de audio enviado en la solicitud
    audio_file = request.files['audio']
    audio_file_path = os.path.join(audio_directory, audio_file.filename)
    audio_file.save(audio_file_path)

    # Llama a la función de transcripción con la ruta del archivo
    srt_filename = transcribe_audio(audio_file_path)

    # Devuelve el nombre del archivo SRT generado
    return jsonify({'srt_filename': srt_filename})

@app.route('/download/<filename>')
def download_file(filename):
    # Asegúrate de que el nombre del archivo es seguro
    safe_filename = secure_filename(filename)
    
    # Especifica el directorio desde el cual se enviará el archivo
    download_directory = "SrtFiles"
    
    # Comprueba si el archivo existe antes de intentar enviarlo
    if os.path.isfile(os.path.join(download_directory, safe_filename)):
        print(f"Enviando {safe_filename}...")
        return send_from_directory(download_directory, safe_filename, as_attachment=True)
    else:
        return "Archivo no encontrado",  404
    
@app.route('/read_srt/<filename>', methods=['GET'])
def read_srt(filename):
    # Asegúrate de que el nombre del archivo es seguro
    safe_filename = secure_filename(filename)
    
    # Especifica el directorio desde el cual se leerá el archivo
    srt_directory = "SrtFiles"
    
    # Concatena el directorio y el nombre del archivo
    file_path = os.path.join(srt_directory, safe_filename)
    
    # Verifica si el archivo existe antes de intentar leerlo
    if os.path.isfile(file_path):
        print(f"Enviando {safe_filename}...")
        return send_file(file_path, mimetype='text/plain')
    else:
        return "Archivo no encontrado",  404   
if __name__ == '__main__':
    app.run(debug=True)

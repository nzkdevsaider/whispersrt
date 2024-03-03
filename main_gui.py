from datetime import timedelta
import os
import whisper
import uuid
import tkinter as tk
from tkinter import filedialog, ttk
import random

def transcribe_audio(path, progress_callback):
    model = whisper.load_model("base") # Cambia esto a tu modelo deseado
    print("Modelo Whisper cargado.")
    transcribe = model.transcribe(audio=path)
    segments = transcribe['segments']

    # Asegura que el directorio SrtFiles exista
    srt_directory = "SrtFiles"
    if not os.path.exists(srt_directory):
        print("Creando directorio SrtFiles...")
        os.makedirs(srt_directory)

    srtId = uuid.uuid4()
    srtFilename = os.path.join(srt_directory, f"file_{srtId}.srt")
    print(f"Escribiendo en {srtFilename}...")

    transcription_text = ""
    for i, segment in enumerate(segments):
        startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
        endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
        text = segment['text']
        segmentId = segment['id']+1
        segment_text = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n"
        transcription_text += segment_text
        
        # Actualizar la barra de progreso
        progress_callback(i + 1, len(segments))

    with open(srtFilename, 'w', encoding='utf-8') as srtFile:
        srtFile.write(transcription_text)
    print("Hecho.")
    return srtFilename, transcription_text

def progress_callback(current, total):
    progress_value = current / total * 100
    progress_bar['value'] = progress_value
    root.update_idletasks()

def select_audio_file():
    audio_file_path = filedialog.askopenfilename(filetypes=[("Archivos de audio", "*.mp3 *.wav")])
    if audio_file_path:
        transcribe_button.config(state=tk.DISABLED)
        progress_bar.start(10) # Iniciar la animación de carga
        root.update()
        srtFilename, transcription_text = transcribe_audio(audio_file_path, progress_callback)
        transcription_text_area.delete(1.0, tk.END)
        transcription_text_area.insert(tk.END, transcription_text)
        progress_bar.stop()
        transcribe_button.config(state=tk.NORMAL)
        # Cambiar color de fondo de manera aleatoria
        root.configure(background=random.choice(['blue', 'green', 'red']))

# Crear la ventana de tkinter
root = tk.Tk()
root.title("Transcripción de Audio")

# Botón para seleccionar archivo de audio
transcribe_button = tk.Button(root, text="Seleccionar archivo de audio", command=select_audio_file, bg='blue', fg='white')
transcribe_button.pack()

# Barra de progreso determinada
progress_bar = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=200, mode='determinate')
progress_bar.pack()

# Área de texto para mostrar la letra generada
transcription_text_area = tk.Text(root, height=10, width=50)
transcription_text_area.pack()

# Ejecutar la aplicación
root.mainloop()

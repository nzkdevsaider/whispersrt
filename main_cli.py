from datetime import timedelta
import os
import whisper
import uuid

def transcribe_audio(path):
    model = whisper.load_model("base")  # Change this to your desired model
    print("Whisper model loaded.")
    transcribe = model.transcribe(audio=path)
    segments = transcribe['segments']

    # Ensure the SrtFiles directory exists
    srt_directory = "SrtFiles"
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

audio_file_path = "audio/demo.mp3"  # Change this to your audio file path
transcribe_audio(audio_file_path)

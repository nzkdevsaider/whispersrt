# WhisperSRT

WhisperSRT is a powerful transcription tool that converts your audio files into accurately timed SRT (SubRip Text) subtitle files. With WhisperSRT, you can effortlessly create well-formatted captions for your videos, making them accessible to a wider audience, including those who are deaf or hard of hearing. Whether you're a content creator, a video editor, or simply looking to enhance your media with subtitles, WhisperSRT streamlines the process, leveraging advanced speech recognition technology to ensure precise synchronization between the spoken words and their corresponding text on screen.

# API

You can run a API server if you want make HTTP request to transcibe audio files, this API is in experimental phase and is expected to receive more features in the future.

How to run API instance:
`py main_api.py`

# GUI

The GUI is experimental, you can interact with them but it can crash sometimes.

How to run GUI instance:
`py main_gui.py`

## Requirements to run
- [Download FFmepg](https://ffmpeg.org/) latest version and put it on your PATH.
- Run `pip install git+https://github.com/openai/whisper.git`
- Run `pip install flask`

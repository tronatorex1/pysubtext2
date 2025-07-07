"""
https://www.youtube.com/watch?v=-zopCT_qYn8

1. instala ffmpeg --> ffmpeg-2025-06-23-git-e6298e0759-full_build_2.tar/gzip
    1.1 crea folder en c:\ffmpeg y extrae del tar/gzip
    1.2 crea una var entorno windows user/system PATH = c:\ffmpeg\bin (dónde está descargado en tar/gzip completo)

2. descarga un video o película --> usa yt-dl.exe <url> o un mkv/avi/mp4
3. extrae su audio en mp3 o m4a --> https://www.gumlet.com/learn/ffmpeg-extract-audio/
    ej: ffmpeg -i  input.mp3  -map 0:a -acodec libmp3lame  _out_.mp4 <-- extracts and decodes with lame mp3 driver


4. con el audio, ejecutar el código abajo (sustituye variables de source audio y out format = srt/vtt)
5. test: ejecutar el vídeo y arrastra en él, el srt/vtt file creado aquí, para ver si sincroniza el audio vs subtítulo
6. ...seguir testeando...
"""


import whisper
from whisper.utils import get_writer

model = whisper.load_model("base")
audio = r"C:\Users\w10\Desktop\S01E01.mp3"    #"C:/Users/w10/Desktop/voice-sample.mp3"
res = model.transcribe(audio, fp16=False)
out = "C:/Users/w10/Desktop/"
sub_writer = get_writer("srt", output_dir=out)
sub_writer(res, audio)


# --------------

# Bueno para extraer letras de canciones en formato plano
import whisper
model = whisper.load_model("turbo")
result = model.transcribe(fp16=False, audio=r"D:\ALEX\MUSIC\Nad Sylvan\2025 - Monumentata\09 - Unkillable (Bonus Track).mp3")
print(f"All: {result["text"]}")
for i in range(len(result['segments'])):
    print(f" [{i}] - {result['segments'][i]['text']}")

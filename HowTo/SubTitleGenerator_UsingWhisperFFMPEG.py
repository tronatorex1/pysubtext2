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

# 0 Declaración de variables generales y getops
source = path = file = video = ext1 = ext2 = audio = ""


# 1 Proceso para extraer el audio de un video ya descragado localmente
import subprocess
import os
source = "C:/TMP/Python.mkv" # actual video path and file name
path = os.path.split(source)[0]
file = os.path.split(source)[1]
video = source #os.path.join(path, file)  #"C:/TMP/Mindfulness for Anxiety.mp4"
ext1 = os.path.splitext(video)[1]
ext2 = ".mp3"
audio = video.replace(os.path.splitext(video)[1], ".mp3")
# extract audio file from movie/video:
print(f" - Extracting audio (.mp3) from original video file.....Please wait.... ", end="")
res = subprocess.call(['ffmpeg','-i',video,'-map','0:a','-acodec','libmp3lame',audio], shell=True)
if (res == 0):
    print(f" [OK] ")  #print('Res:', res)


# 2 Proceso para extraer del audio el texto y guardarlo en format SRT en la misma ruta dónde yace el video--------------------------------------------------------------------------------------
import whisper
from whisper.utils import get_writer
# extract text from audio file:
print(f" - Loading base model for Whisper Lib...", end="")
model = whisper.load_model("base")

print(f" - Transcribing.....Please wait.... ", end="")
res = model.transcribe(audio, fp16=False)

print(f" - Outputting transcription.....Please wait.... ", end="")
sub_writer = get_writer("srt", output_dir=path)
sub_writer(res, audio)







# Extra --------------
# Bueno para extraer letras de canciones en formato plano
import whisper
model = whisper.load_model("turbo")
result = model.transcribe(fp16=False, audio=r"D:\ALEX\MUSIC\Nad Sylvan\2015 - Courting the Widow\01 - Carry Me Home.mp3")
print(f"All: {result["text"]}")
for i in range(len(result['segments'])):
    print(f" [{i}] - {result['segments'][i]['text']}")
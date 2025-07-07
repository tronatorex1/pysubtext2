"""
https://www.youtube.com/watch?v=-zopCT_qYn8

Pasos a tomar en cuenta:
1. instala ffmpeg --> ffmpeg-2025-06-23-git-e6298e0759-full_build_2.tar/gzip
    1.1 crea folder en c:\ffmpeg y extrae del tar/gzip
    1.2 crea una var entorno windows user/system PATH = c:\ffmpeg\bin (dónde está descargado en tar/gzip completo)

2. descarga un video o película --> usa yt-dl.exe <url> para descargar un video, o usa un mkv/avi/mp4
3. extrae su audio en mp3 o m4a --> https://www.gumlet.com/learn/ffmpeg-extract-audio/
    ej: ffmpeg -i  input.mp3  -map 0:a -acodec libmp3lame  _out_.mp4 <-- extracts and decodes with lame mp3 driver

4. con el audio, ejecutar el código abajo (sustituye variables de source audio y out format = srt/vtt)
5. test: ejecutar el vídeo y arrastra en él, el srt/vtt file creado aquí, para ver si sincroniza el audio vs subtítulo
"""
import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
import time as tm

# Create a TkinterDnD window (required for drag-and-drop)
root = TkinterDnD.Tk()
root.title("Subtitles generator - Drag and Drop File Here")
root.geometry("400x200")

# Variable to hold the file path
dropped_file_path = tk.StringVar()

# Label to display the file path
label = tk.Label(root, text="Drag and drop a file here", bg="lightgrey", width=40, height=5)
label.pack(padx=10, pady=10, expand=False)

# Status message label (bottom)
status_label = tk.Label(root, text="", bg="#f0f0f0", fg="grey", font=("Arial", 10))
status_label.pack(side="bottom", pady=10)

# Function to handle drop event
def drop(event):
    # Clean path (removes braces if present on Windows)
    path = event.data.strip("{}")
    dropped_file_path.set(path)
    label.config(text=f"File path:\n{path}")
    print(f"File path captured: {path}")  # You can use the variable here

# Bind the drop event to the label
label.drop_target_register(DND_FILES)
label.dnd_bind('<<Drop>>', drop)

# Function to run when button is clicked
def process_file():
    path = dropped_file_path.get()
    if path:
        print(f"Processing file: {path}")

        # 1 Proceso para extraer el audio de un video ya descragado localmente
        import subprocess
        import os
        source = path  # actual video path and file name
        path = os.path.split(source)[0]
        #file = os.path.split(source)[1]
        video = source  # os.path.join(path, file)  #"C:/TMP/Mindfulness for Anxiety.mp4"
        #ext1 = os.path.splitext(video)[1]
        #ext2 = ".mp3"
        audio = video.replace(os.path.splitext(video)[1],".mp3")
        # extract audio file from movie/video:
        print(f" - Extracting audio (.mp3) from original video file...Please wait...",end="")
        res = subprocess.call(['ffmpeg','-i',video,'-map','0:a','-acodec','libmp3lame',audio],shell=True)
        if (res == 0):
            print(f" - Extracting audio (.mp3) from original video file...Please wait... [OK] ")  # print('Res:', res)
            #status_label.config(text="Extracting audio (.mp3) from original video file...[OK]")

        # 2 Proceso para extraer del audio el texto y guardarlo en format SRT en la misma ruta dónde yace el video--------------------------------------------------------------------------------------
        import whisper
        from whisper.utils import get_writer
        # extract text from audio file:
        print(f" - Loading base model for Whisper Lib...Please wait...",end="")
        #status_label.config(text="Loading base model for Whisper Lib...Please wait...")
        #root.update_idletasks()
        model = whisper.load_model("base")
        print(f" [OK]")
        #status_label.config(text="Loading base model for Whisper Lib...[OK]")
        #root.update_idletasks()

        print(f" - Transcribing...Please wait...",end="")
        #status_label.config(text="Transcribing...Please wait...")
        #root.update_idletasks()
        res = model.transcribe(audio,fp16=False)
        print(f" [OK]")
        #status_label.config(text="Transcribing...Please wait...[OK]")
        #root.update_idletasks()

        print(f" - Outputting transcription...Please wait...",end="")
        #root.update_idletasks()
        #status_label.config(text="Outputting transcription...Please wait...")
        sub_writer = get_writer("srt",output_dir=path)
        sub_writer(res,audio)
        print(f" [OK]")
        #status_label.config(text="Outputting transcription...[OK]")
        #root.update_idletasks()
        tm.sleep(3)
        #status_label.config(text=f">> Subtitles extracted and saved locally! [{path}]")
        #root.update_idletasks()
    else:
        print(" X - No file selected.")

# Button to call another function
button = tk.Button(root, text="Process File", command=process_file, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), padx=100, pady=5)
button.pack(pady=1)

# Start the GUI loop
root.mainloop()


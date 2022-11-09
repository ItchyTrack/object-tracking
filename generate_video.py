import math
import os
import shutil
import sys
from tkinter import filedialog

from PIL import Image

os.mkdir('/tmp/frames')

frames = 180
print("Choose a directory to save the video to")
save_dir = filedialog.askdirectory(mustexist=True)

if not save_dir:
    print("You must select a directory to save the video to!")
    sys.exit()

for frame in range(frames):
    pos = (frame, frame)

    background = Image.new(mode='RGB', size=(224, 224), color=(255, 255, 255))
    red_square = Image.new(mode='RGB', size=(1, 1), color=(255, 0, 0))

    background.paste(red_square.resize((40, 40)), pos)
    background.save(f'/tmp/frames/frame{frame}.jpg')

os.system(f"cd /tmp/frames && ffmpeg -r 60 -i frame%d.jpg {save_dir}/red.mp4")
shutil.rmtree("/tmp/frames")
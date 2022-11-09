import math
import os
from random import randint, random
import shutil
import sys
from tkinter import filedialog

import cv2
from PIL import Image

import scanner


def create_frames():
    print("Select a video")
    video_path = "/Users/ben/Documents/GitHub/object-tracking/red.mp4"
    capture = cv2.VideoCapture(video_path)
    total_video_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"Generating frames from video: {video_path}")
    frame_number = 0
    
    while True:
        # process frames
        success, frame = capture.read()

        if frame_number % 60 == 0:
            print(f"Splitting frames... {frame_number}/{total_video_frames}")

        if success:
            cv2.imwrite(f"/tmp/frames/frame{frame_number}.jpg", frame)
        else:
            break # finish loop at the end of the video

        frame_number += 1
    
    print("Splitting frames... done")

if __name__ == "__main__":
    # temporary folder for split frames
    try:
        os.mkdir('/tmp/frames')
        create_frames()
    except FileExistsError: # use pre-processed frames
        delete_tmp_frames = input("/tmp/frames exists. Overwrite it? (y/n) ")
        if delete_tmp_frames == "y":
            shutil.rmtree('/tmp/frames')
            os.mkdir('/tmp/frames')
            create_frames()
        elif delete_tmp_frames == "n":
            print("Using frames specified in /tmp/frames.")

images = os.listdir('/tmp/frames')

point = Image.new(mode='RGB', size=(1, 1), color=(0, 255, 0))

for i in range(math.floor(len(images)/6)):
    pimage = Image.open(f'/tmp/frames/frame{i*6}.jpg')
    predicted = scanner.scanImage(pimage)
    print(predicted)
    pimage.paste(point.resize((4, 4)), predicted)
    
    pimage.save(f'/tmp/newframes/frame{i}.jpg')
    
os.system(f"cd /tmp/newframes && ffmpeg -r 10 -i frame%d.jpg /Users/ben/Downloads/predicted.mp4")

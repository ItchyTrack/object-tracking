import cv2
import os
import sys
from tkinter import filedialog
import shutil

def create_frames():
    print("Select a video")
    video_path = filedialog.askopenfilename()
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
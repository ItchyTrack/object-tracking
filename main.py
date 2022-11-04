import cv2
import os
import sys
from tkinter import filedialog

video_path = filedialog.askopenfilename()
capture = cv2.VideoCapture(video_path)
frame_number = 0
total_video_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT)) # this doesn't work

try:
    os.mkdir('/tmp/frames')
except FileExistsError:
    delete_tmp_frames = input("/tmp/frames exists. Overwrite it? (y/n)")
    if delete_tmp_frames == "y":
        os.rmdir('/tmp/frames')
    elif delete_tmp_frames == "n":
        print("Using frames specified in /tmp/frames.")

print(f"Generating frames from video: {video_path}/{total_video_frames}")

while True:
    # process frames
    success, frame = capture.read()

    if frame_number % 60 == 0:
        print(f"Splitting frames... {frame_number}/")

    if success:
        cv2.imwrite(f"/tmp/frames/frame_{frame_number}.jpg", frame)
    else:
        break # break at the end of the video

    frame_number += 1
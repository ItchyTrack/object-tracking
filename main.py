import math
import os
from random import randint, random
from re import I
import shutil
import sys
from tkinter import filedialog

import cv2
from PIL import Image

import scanner


def create_frames():
    print("Select a video")
    video_path = "./red.mp4"
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
            cv2.imwrite(f"./tmp/frames/frame{frame_number}.jpg", frame)
        else:
            break  # finish loop at the end of the video

        frame_number += 1

    print("Splitting frames... done")


if __name__ == "__main__":
    # temporary folder for split frames
    try:
        os.mkdir('./tmp/frames')
        create_frames()
    except FileExistsError:  # use pre-processed frames
        delete_tmp_frames = input("./tmp/frames, Overwrite it? (y/n) ")
        if delete_tmp_frames == "y":
            shutil.rmtree('./tmp/frames')
            os.mkdir('./tmp/frames')
            create_frames()
        elif delete_tmp_frames == "n":
            print("Using frames specified in ./tmp/frames.")


def addLine(img, x1, y1, x2, y2):
    ''' draws the line(or box) from (x1, y1) to (x2, y2) on img '''
    point = Image.new(mode='RGB', size=(1, 1), color=(0, 255, 0))

    for iy in range(y2 - y1 + 1):
        y = y1 + iy
        for ix in range(x2 - x1 + 1):
            x = x1 + ix
            img.paste(point.resize((2, 2)), [x, y])
    return img


try:
    os.mkdir('./tmp/newframes')
except FileExistsError:
    shutil.rmtree('./tmp/newframes')
    os.mkdir('./tmp/newframes')

framSkip = 1


for i in range(math.floor(len(os.listdir('./tmp/frames'))/framSkip)):
    pimage = Image.open(f'./tmp/frames/frame{i*framSkip}.jpg')
    foundArea = scanner.scanImage(pimage)
    print(i)
    pimage = addLine(
        pimage, foundArea[0][0], foundArea[0][1], foundArea[1][0], foundArea[0][1])
    pimage = addLine(
        pimage, foundArea[0][0], foundArea[1][1], foundArea[1][0], foundArea[1][1])
    pimage = addLine(
        pimage, foundArea[0][0], foundArea[0][1], foundArea[0][0], foundArea[1][1])
    pimage = addLine(
        pimage, foundArea[1][0], foundArea[0][1], foundArea[1][0], foundArea[1][1])
    pimage.save(f'./tmp/newframes/frame{i}.jpg')

os.system(
    f"cd ./tmp/newframes && ffmpeg -r {60/framSkip} -i frame%d.jpg ../../predictedVideos/predicted.mp4")

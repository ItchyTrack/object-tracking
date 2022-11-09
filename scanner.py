import math

import fastbook
import numpy as np
from fastai.vision.core import PILImage
from PIL import Image

def predict(image):
    learn = fastbook.load_learner("model.pkl")

    pred_class, pred_idx, probabilities = learn.predict(image)
    return probabilities[1]

def scanImage(img):
    size = img.size
    scanImageSize = 50
    stepSize = 10
    out = FinalOut(size)
    for yi in range(math.floor((size[1] - scanImageSize)/stepSize)):
        ypos = yi * stepSize
        for xi in range(math.floor((size[0] - scanImageSize)/stepSize)):
            xpos = xi * stepSize
            scan_image = img.crop((xpos, ypos, xpos + scanImageSize, ypos + scanImageSize))
            out.addValues(
                xpos,
                ypos,
                float(predict(PILImage(scan_image))),
                scanImageSize
            )
    return out.getHighestPos()

class FinalOut():
    def __init__(self, size):
        self.image = np.zeros((size[0], size[1]))

    def addValues(self, xpos, ypos, value, size):
        for yi in range(size):
            for xi in range(size):
                self.image[yi + ypos][xi + xpos] += value

    def getHighestPos(self):
        img = Image.fromarray(self.image, 'F')
        img.show()
        highestItem = [0, 0]
        for yi in range(len(self.image)):
            for xi in range(len(self.image[yi])):
                if self.image[yi][xi] > self.image[highestItem[1]][highestItem[0]]:
                    highestItem = [xi, yi]
        return highestItem
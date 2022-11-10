import math
from telnetlib import XASCII
from xml.etree.ElementTree import XML
from numpy import unravel_index
import fastbook
import numpy as np
from fastai.vision.core import PILImage
from PIL import Image

# import network
learn = fastbook.load_learner("model.pkl")

def predict(image):
    pred_class, pred_idx, probabilities = learn.predict(image)
    return probabilities[1]

def scanImage(img):
    size = img.size
    scanImageSize = 30
    stepSize = 15
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
        self.addedImages = np.zeros((size[0], size[1]))


    def addValues(self, xpos, ypos, value, size):
        #print(f"found {value} at x: {xpos} y: {ypos}")
        value = self.image[ypos : ypos + size, xpos : xpos + size] + (value * np.ones((size, size)))
        self.image[tuple(slice(edge, edge+i) for edge, i in zip((ypos, xpos), value.shape))] = value
        
        #for yi in range(size):
        #    for xi in range(size):
        #        #print(f"found 2 {value} at x: {xi + xpos} y: {yi + ypos}")
        #        self.image[yi + ypos][xi + xpos] += value
        #        self.addedImages[yi + ypos][xi + xpos] += 1


    def getHighestPos(self):
        #self.image = self.image / self.addedImages
        foundPoints = []
        for yi in range(len(self.image)):
            for xi in range(len(self.image[yi])):
                if abs(self.image[yi][xi] - self.image.max()) < 0.2 :
                    foundPoints.append([xi, yi])
        #math.floor(np.average(xs)), math.floor(np.average(ys))
        xL = 0
        yL = 0
        xS = len(self.image[0])
        yS = len(self.image)
        for point in foundPoints:
            if point[0] > xL:
                xL = point[0]
            if point[1] > yL:
                yL = point[1]
            if point[0] < xS:
                xS = point[0]
            if point[1] < yS:
                yS = point[1]
            
            
        return [[xS, yS], [xL, yL]]
        #print(self.image.max())
        #print(self.image[highestItem[1]][highestItem[0]])
        #print(self.addedImages[highestItem[1]][highestItem[0]])
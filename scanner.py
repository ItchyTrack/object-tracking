''' used to find objects in images '''
from email.mime import image
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
    ''' gets the probability that the object is in the image '''
    pred_class, pred_idx, probabilities = learn.predict(image)
    return probabilities[1]


def scanImage(img):
    '''
    scans a image looking for a object

    returns the 2 corners of a rectangle that surrounds the object
    [ [smallest X, smallest Y], [largest X, Largest Y] ]
    '''
    imgSize = img.size
    scaningArea = findObjectArea(img, 8)
    size = [scaningArea[2] - scaningArea[0], scaningArea[3] - scaningArea[1]]
    scanImageSize = 10
    stepSize = 4
    out = FinalOut(size)
    for yi in range(math.floor((size[1])/stepSize)):
        ypos = yi * stepSize + scaningArea[1]
        if imgSize[1] > ypos + scanImageSize:
            for xi in range(math.floor((size[0])/stepSize)):
                xpos = xi * stepSize + scaningArea[0]
                if imgSize[0] > xpos + scanImageSize:
                    scan_image = img.crop((xpos, ypos, xpos + scanImageSize, ypos + scanImageSize))
                    out.addValues(
                        xpos - scaningArea[0],
                        ypos - scaningArea[1],
                        float(predict(PILImage(scan_image))),
                        scanImageSize
                    )

    return out.getHighestPos(scaningArea[0], scaningArea[1])


def findObjectArea(image, numberOfSplit):
    '''
    find the area of the image that the object is in

    returns:
    the area that the object is in
    '''
    size = image.size
    xL = 0
    yL = 0
    xS = size[0]
    yS = size[1]
    splitSizeX = math.floor(size[0]/numberOfSplit)
    splitSizeY = math.floor(size[1]/numberOfSplit)
    out = FinalOut(size)
    for yi in range(math.floor(size[1]/splitSizeY)):
        ypos = yi * splitSizeY
        for xi in range(math.floor(size[0]/splitSizeX)):
            xpos = xi * splitSizeX
            checkImage = image.crop(
                (xpos, ypos, xpos + splitSizeX, ypos + splitSizeY))
            if (float(predict(PILImage(checkImage))) > 0.5):
                if xpos + splitSizeX > xL:
                    xL = xpos + splitSizeX
                if ypos + splitSizeY > yL:
                    yL = ypos + splitSizeY
                if xpos < xS:
                    xS = xpos
                if ypos < yS:
                    yS = ypos
    # checks if the image was reduced in size
    if (xS == 0 and yS == 0 and xL == image.size[0] and image.size[1]) or xS == image.size[0] and yS == image.size[1] and xL == 0 and yL == 0:
        return image, 0, 0
    else:
        
        return [xS, yS, xL, yL]


class FinalOut():
    def __init__(self, size):
        ''' hold and processes scan data from a image '''
        self.image = np.zeros((size[0], size[1]))
        self.addedCounter = np.zeros((size[0], size[1]))

    def addValues(self, xpos, ypos, value, size):
        '''
        adds a array (size, size) filled with value
        to self.image at [ypos][xpos]
        '''
        if self.image[ypos: ypos + size, xpos: xpos + size].shape == (size, size):
            value = self.image[ypos: ypos + size, xpos: xpos + size] + (value * np.ones((size, size)))
            self.image[tuple(slice(edge, edge+i) for edge, i in zip((ypos, xpos), value.shape))] = value

            value = self.addedCounter[ypos: ypos + size, xpos: xpos + size] + np.ones((size, size))
            self.addedCounter[tuple(slice(edge, edge+i) for edge, i in zip((ypos, xpos), value.shape))] = value

    def getHighestPos(self, xOffset, yOffset):
        ''' 
        find the hight points on the heat map

        returns the 2 corners of a rectangle that surrounds the object
        [ [smallest X, smallest Y], [largest X, Largest Y] ]
        '''
        # finds the smalest x y and largest x y
        self.addedCounter[self.addedCounter == 0] = 1
        self.image = self.image / self.addedCounter
        xL = 0
        yL = 0
        xS = len(self.image[0])
        yS = len(self.image)
        for yi in range(len(self.image)):
            for xi in range(len(self.image[yi])):
                if abs(self.image[yi][xi] - self.image.max()) < 0.001:
                    if xi > xL:
                        xL = xi
                    if yi > yL:
                        yL = yi
                    if xi < xS:
                        xS = xi
                    if yi < yS:
                        yS = yi

        return [[xS + xOffset, yS + yOffset], [xL + xOffset, yL + yOffset]]

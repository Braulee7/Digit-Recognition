import cv2 
import numpy as np

class Prepare():
    def __init__(self, img):
        #scale down image to 28 by 28 for input
        self.width = int(img.shape[1] * 0.1) 
        self.height = int(img.shape[0] * 0.1)
        self.dim = (self.width, self.height)

        self.resized = cv2.resize(img, self.dim, interpolation=cv2.INTER_AREA)

        #change pixel values to greyscale image
        self.gray = cv2.cvtColor(self.resized, cv2.COLOR_BGR2GRAY)

    def getGrayScale(self):
        self.gray = self.gray / 255.0
        return np.reshape(self.gray, (-1, 28, 28))
    
    def getDimensions(self):
        return self.width, self.height

    def getRescaled(self):
        img = self.resized / 255.0
        return np.reshape(img, (-1, 28, ))
        




import numpy as np
import cv2 as cv

class TrackObject():
    def __init__(self, image):
        super().__init__()
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0 
        self.image = image


    def get_shape(self):
        return self.image.shape


    def track(self):
        copy_image = self.image.copy()

        hsv_image = cv.cvtColor(self.image, cv.COLOR_BGR2HSV)
        lowerlimit = np.array([29, 86, 100])
        upperlimit = np.array([64, 255, 255])

        mask = cv.inRange(hsv_image, lowerlimit, upperlimit)
        mask = cv.erode(mask, None, iterations=2) 
        mask = cv.dilate(mask, None, iterations=2)

        contours, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        if contours.__len__() != 0:
            cv.drawContours(copy_image, contours, -1, 255, 3)
            max_contor = max(contours, key=cv.contourArea)
            self.x, self.y, self.w, self.h = cv.boundingRect(max_contor)
            return(self.x, self.y, self.w, self.h)
        else:
            return "Human out of range!!"


import qrcode
import cv2 as cv


class QRCodeGenerator:
    def __init__(self):
        self.done = False
        self.filename = "detail.png"
        self.data = {
            "Account Name":"Smart Shopping Cart",
            "Account Number": 123456789101112
            }
    
    def generateQR(self):
        try:
            img = qrcode.make(self.data)
            img.save(self.filename)
            self.done = True
        except Exception as e:
            print("Exception occured!!")
            print(e)
            self.done = False
        return self.done
    
    
    def getQR(self):
        image = cv.imread(self.filename)
        print(type(image))
        return image
    
    def showQR(self):
        try:
            image = cv.imread(self.filename)
            cv.imshow('qr', image)
            cv.waitKey(0)
            cv.destroyAllWindows()
            self.done = True
        except Exception as e:
            print("Exception occured!!")
            print(e)
            self.done = False
        return self.done


if __name__ == '__main__':
    generator = QRCodeGenerator()
    generator.generateQR()
    generator.getQR()
    generator.showQR()
    
    
    
    
            
            
            
            
            
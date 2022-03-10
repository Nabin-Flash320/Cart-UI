#for barcode
from sqlite3 import paramstyle
from pyzbar import pyzbar
import json
import requests
import cv2
import time

class BarcodeReader:

    def __init__(self):
        self.data_list = list()
        self.previous_data = 0
        self.datalength = 0



    def draw_barcode(decoded, image):
        # n_points = len(decoded.polygon)
        # for i in range(n_points):
        #     image = cv2.line(image, decoded.polygon[i], decoded.polygon[(i+1) % n_points], color=(0, 255, 0), thickness=5)
        image = cv2.rectangle(image, (decoded.rect.left, decoded.rect.top), 
                                (decoded.rect.left + decoded.rect.width, decoded.rect.top + decoded.rect.height),
                                color=(0, 255, 0),
                                thickness=5)
        return image


    def decode(image):
        global data_list, previous_data, datalength
        # decodes all barcodes from an image
        decoded_objects = pyzbar.decode(image)
        for obj in decoded_objects:

            # draw the barcode
            image = draw_barcode(obj, image)
            self.present_data = int(obj.data)
            self.data_list.append(self.present_data)
            self.datalength = len(self.data_list)
            if self.datalength == 20:
                if self.data_list.count(self.data_list[0]) == 20:
                    print('Barcode scanning.')
                    payload = {
                        'product_id' : '3',
                        'count':'-1'
                    }
                    r= requests.post("http://localhost:8080/shop/1/data", payload)
                    print (json.loads(r.text))
                    print('Data list=>', self.data_list)
                    print('data_list.count(data_list) ==>', self.data_list.count(self.data_list[0]))
                    print('Barcode scanned.')
                    self.data_list = []
                    time.sleep(3)
                    print('Scanner restarted.')
                elif self.data_list.count(self.data_list[0]) < 20: 
                    print('data_list.count(data_list[0]) ==>', self.data_list.count(self.data_list[0]))
                    self.data_list = []
                    print('Emptied data_list in counte not equal 20')
            elif self.datalength > 0 and self.datalength < 20:
                if self.data_list[0] != self.present_data:
                    print("datalength > 0 and datalength < 20")
                    print(self.data_list)
                    self.data_list = []

        return image


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    while True:
        # read the frame from the camera
        _, frame = cap.read()

        # decode detected barcodes & get the image
        # that is drawn
        frame = decode(frame)
        
        
        # show the image in the window
        cv2.imshow("frame", frame)
        
        if cv2.waitKey(5) & cv2.waitKey(1) == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()



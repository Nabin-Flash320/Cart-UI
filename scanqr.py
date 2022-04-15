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
        self.present_data = 0
        self.datalength = 0
        self.previous_data = 0
        self.is_scanned = bool()

    def draw_barcode(self, decoded, image):
        image = cv2.rectangle(image, (decoded.rect.left, decoded.rect.top), 
                                (decoded.rect.left + decoded.rect.width, decoded.rect.top + decoded.rect.height),
                                color=(0, 255, 0),
                                thickness=5)
        return image


    def decode(self, image):
        self.is_scanned = False
        # decodes all barcodes from an image
        decoded_objects = pyzbar.decode(image)
        for obj in decoded_objects:
            # draw the barcode
            image = self.draw_barcode(obj, image)
            self.present_data = int(obj.data)
            self.data_list.append(self.present_data)
            self.datalength = len(self.data_list)
            if self.present_data == self.previous_data:
                print('Data taken')
                self.data_list = []
                continue
            else:
                print("inside else")
                if self.datalength == 20:
                    print("inside == 20")
                    if self.data_list.count(self.data_list[0]) == 20:
                        print('Barcode scanning.')
                        payload = {
                            'product_id' : '3',
                            'count':'1'
                        }
                        r = requests.post("http://192.168.254.11:8080/shop/1/data", payload)
                        print (json.loads(r.text))
                        print('Data list=>', self.data_list)
                        print('data_list.count(data_list) ==>', self.data_list.count(self.data_list[0]))
                        self.previous_data = self.data_list[len(self.data_list) - 1]
                        self.data_list = []
                        self.is_scanned = True
                        time.sleep(1)
                        print('Scanner restarted.')
                    elif self.data_list.count(self.data_list[0]) < 20: 
                        print('data_list.count(data_list[0]) ==>', self.data_list.count(self.data_list[0]))
                        self.data_list = []
                        self.is_scanned = False 
                elif self.datalength > 0 and self.datalength < 20:
                    if self.data_list[0] != self.present_data:
                        print("datalength > 0 and datalength < 20")
                        print(self.data_list)
                        self.data_list = []

        return image, self.is_scanned



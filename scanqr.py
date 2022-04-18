#for barcode
from sqlite3 import paramstyle
from pyzbar import pyzbar
import json
import requests
import cv2
import time
import i2cCheck

class BarcodeReader:

    def __init__(self):
        self.data_list = list()
        self.present_data = 0
        self.datalength = 0
        self.previous_data = 0
        self.previous_weight_data = 0
        self.is_scanned = bool()
        print("Barcode reader initialized!!")

    def draw_barcode(self, decoded, image):
        image = cv2.rectangle(image, (decoded.rect.left, decoded.rect.top), 
                                (decoded.rect.left + decoded.rect.width, decoded.rect.top + decoded.rect.height),
                                color=(0, 255, 0),
                                thickness=5)
        return image


    def decode(self, image):
        self.is_scanned = False
        # decodes all barcodes from an image
        print("Inside decoder!!")
        decoded_objects = pyzbar.decode(image)
        for obj in decoded_objects:

            # draw the barcode
            image = self.draw_barcode(obj, image)
            self.present_data = int(obj.data)
            self.data_list.append(self.present_data)
            self.datalength = len(self.data_list)
            print(self.data_list)
            if self.present_data == self.previous_data:
                print('Data taken')
                self.data_list = []
                self.previous_data = 0
                continue
            else:
                if self.datalength == 3:
                    if self.data_list.count(self.data_list[0]) == 3:
                        print('Scanning weight...')
                        time.sleep(3)
                        present_weight_data = i2cCheck.getFromI2C()
                        print("weight data=>{}".format(present_weight_data))
                        if present_weight_data > self.previous_weight_data:
                            payload = {
                                'product_id' : '3',
                                'count':'1'
                            }
                            print("Greater")
                            self.previous_weight_data = present_weight_data
                        elif present_weight_data < self.previous_weight_data:
                            payload = {
                                'product_id' : '3',
                                'count':'-1'
                            }
                            print("Smaller")
                            self.previous_weight_data = present_weight_data
                        else:
                            payload = {
                                'product_id' : '3',
                                'count':'0'
                            }
                            self.previous_weight_data = present_weight_data
                        r = requests.post("http://192.168.43.133:8080/shop/1/data", payload)
                        print (json.loads(r.text))
                        print('Data list=>', self.data_list)
                        print('data_list.count(data_list) ==>', self.data_list.count(self.data_list[0]))
                        self.previous_data = self.data_list[len(self.data_list) - 1]
                        self.data_list = []
                        self.is_scanned = True
                        time.sleep(1)
                        print('Scanner restarted.')
                    elif self.data_list.count(self.data_list[0]) < 3: 
                        print('data_list.count(data_list[0]) ==>', self.data_list.count(self.data_list[0]))
                        self.data_list = []
                        self.is_scanned = False 
                elif self.datalength > 0 and self.datalength < 3:
                    if self.data_list[0] != self.present_data:
                        print("datalength > 0 and datalength < 10")
                        print(self.data_list)
                        self.data_list = []

        return image, self.is_scanned



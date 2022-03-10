
from itertools import count
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
import cv2 as cv
import sys
import requests
import json

class TrackObject(QThread):
    image_signal = pyqtSignal('PyQt_PyObject')
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
        lowerlimit = np.array([29, 86, 6])
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


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal('PyQt_PyObject')

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        # capture from web cam
        cap = cv.VideoCapture(0)
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()       


class TableView(QTableWidget):
    def __init__(self, data, *args):
        QTableWidget.__init__(self, *args)
        self.data = data
        self.setData()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

    def setData(self): 
        horHeaders = []
        for n, key in enumerate(self.data.keys()):
            horHeaders.append(key)
            for m, item in enumerate(self.data[key]):
                newitem = QTableWidgetItem(item)
                self.setItem(m, n, newitem)
        self.verticalHeader().setVisible(False)
        self.setHorizontalHeaderLabels(horHeaders)

class ApplyQuery():
    def __init__(self, url):
        self.url = url
        self.product_id = None

    def get_url(self):
        return self.url
    
    def query_post(self, id, flag='c', product_id=None):
        self.product_id = product_id
        if flag == 'c' and self.product_id:
            payload = {
                'product_id':str(self.product_id),
                'count':'-1'
            }
            r = requests.post(self.url+'/'+str(id)+'/data', payload)
            datas = json.loads(r.text)
            return self.parse_data(datas=datas, keys=['key', 'cart_id'])

    def query_get(self, id, flag='p'):
        if flag=='p':
            r = requests.get(self.url+'/'+str(id)+'/data')
            datas = json.loads(r.text)
            return self.parse_data(datas=datas, keys=['product_mfd', 'product_epd'])

    def completed(self, id):
        payload = {
            'completed': True
        }
        r = requests.post(self.url+'/'+str(id)+'/completed', payload)
        print(json.loads(r.text))
    
    def parse_data(self, datas, keys=None):
        data_dict = dict()
        for data in datas:
            for key, value in data.items():
                if keys!= None and key in keys:
                    continue
                if key in data_dict.keys():
                    data_dict[key].append(str(value))
                else:
                    data_dict[key] = list([str(value)])
        return data_dict


class Ui_ShoppingCart(object):
    def setupUi(self, ShoppingCart):
        ShoppingCart.setObjectName("ShoppingCart")
        ShoppingCart.resize(637, 480)

        query = ApplyQuery('http://localhost:8080/shop')


        self.centralwidget = QtWidgets.QWidget(ShoppingCart)
        self.centralwidget.setObjectName("centralwidget")

        self.linelabel = QtWidgets.QLabel(self.centralwidget)
        self.linelabel.setGeometry(QtCore.QRect(20, 10, 601, 51))
        self.linelabel.setObjectName("lineEdit")
        self.linelabel.setText('Shopping Cart (You are online...)')
        self.linelabel.setAlignment(QtCore.Qt.AlignCenter)
        self.linelabel.setStyleSheet("QFrame\n"
            "{\n"
            "    background-color: rgb(255, 255, 255);\n"
            "    \n"
            "    color: rgb(0, 0, 0);\n"
            "    border-radius:10px;\n"
            "    font-size:20px;\n"
            "}")

        self.humanlinelabel = QtWidgets.QLabel(self.centralwidget)
        self.humanlinelabel.setGeometry(QtCore.QRect(20, 70, 300, 41))
        self.humanlinelabel.setObjectName("lineEdit")
        self.humanlinelabel.setText('Human Not Detected!!')
        self.humanlinelabel.setAlignment(QtCore.Qt.AlignCenter)
        self.humanlinelabel.setStyleSheet("QFrame\n"
            "{\n"
            "    background-color: rgb(255, 255, 255);\n"
            "    \n"
            "    color: rgb(0, 0, 0);\n"
            "    border-radius:10px;\n"
            "    font-size:20px;\n"
            "}")

        self.cart_data = query.query_post(id=1, product_id=1)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 120, 300, 301))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.CartData = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.CartData.setContentsMargins(0, 0, 0, 0)
        self.CartData.setObjectName("CartData")
        self.CartDataTable = TableView(self.cart_data, len(self.cart_data[list(self.cart_data.keys())[0]]), len(list(self.cart_data.keys())), self.horizontalLayoutWidget)
        self.CartDataTable.setObjectName("CartDataTable")
        self.CartData.addWidget(self.CartDataTable)
        self.CartDataTable.setStyleSheet("QFrame\n"
            "{\n"
            "    background-color: rgb(255, 255, 255);\n"
            "    \n"
            "    color: rgb(0, 0, 0);\n"
            "    border-radius:10px;\n"
            "}")


        self.imageLabel = QtWidgets.QLabel(self.centralwidget)
        self.imageLabel.setGeometry(QtCore.QRect(335, 70, 282, 181))
        self.imageLabel.setObjectName("PiCameraView")
        self.imageLabel.setStyleSheet("QFrame\n"
            "{\n"
            "    background-color: rgb(255, 255, 255);\n"
            "    \n"
            "    color: rgb(0, 0, 0);\n"
            "    border-radius:10px;\n"
            "    font-size:20px;\n"
            "}")


        # create the video capture thread
        self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.thread.start()


        # Get the product data fromt the database...
        self.product_data = query.query_get(1, 'p')
        

        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(335, 260, 282, 211))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.AvailableProducts = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.AvailableProducts.setContentsMargins(0, 0, 0, 0)
        self.AvailableProducts.setObjectName("AvailableProducts")
        self.AvailableProductTable = TableView(self.product_data, len(self.product_data[list(self.product_data.keys())[0]]), len(list(self.product_data.keys())), self.horizontalLayoutWidget)
        self.AvailableProductTable.setObjectName("AvailableProductTable")
        self.AvailableProducts.addWidget(self.AvailableProductTable)


        self.SubmitButton = QtWidgets.QPushButton(self.centralwidget)
        self.SubmitButton.setGeometry(QtCore.QRect(20, 430, 300, 41))
        self.SubmitButton.setObjectName("SubmitButton")


        ShoppingCart.setCentralWidget(self.centralwidget)

        self.retranslateUi(ShoppingCart)
        QtCore.QMetaObject.connectSlotsByName(ShoppingCart)


    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.imageLabel.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv.cvtColor(cv_img, cv.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(282, 211, QtCore.Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


    def closeEvent(self, event):
        self.thread.stop()
        event.accept()


    def retranslateUi(self, ShoppingCart):
        _translate = QtCore.QCoreApplication.translate
        ShoppingCart.setWindowTitle(_translate("ShoppingCart", "Shopping Cart"))
        self.SubmitButton.setText(_translate("ShoppingCart", "Completed"))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    cart = Ui_ShoppingCart()
    cart.setupUi(main_window)
    main_window.show()
    sys.exit(app.exec_())

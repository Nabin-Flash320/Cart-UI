
from itertools import count
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QImage, QPixmap
import cv2 as cv
import sys
import numpy as np
from TrackObject import TrackObject
from scanqr import BarcodeReader
import time
from ApplyQuery import ApplyQuery


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
        self.done = False
        self.setData()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

    def setData(self, data=None): 
        if data != None:
            self.data = data
        horHeaders = []
        for n, key in enumerate(self.data.keys()):
            horHeaders.append(key)
            for m, item in enumerate(self.data[key]):
                newitem = QTableWidgetItem(item)
                self.setItem(m, n, newitem)
        self.verticalHeader().setVisible(False)
        self.setHorizontalHeaderLabels(horHeaders)


    def update(self, data):
        try:
            self.setData(data)
            self.done = True
        except Exception as e:
            self.done = False
        finally:
            return self.done




class Ui_ShoppingCart(object):
    def __init__(self):
        self.reader = BarcodeReader()
        self.scanned = False 
        self.query = ApplyQuery('http://192.168.254.11:8080/shop')


    def setupUi(self, ShoppingCart):
        ShoppingCart.setObjectName("ShoppingCart")
        ShoppingCart.resize(637, 480)



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

        # self.humanlinelabel = QtWidgets.QLabel(self.centralwidget)
        # self.humanlinelabel.setGeometry(QtCore.QRect(20, 70, 300, 41))
        # self.humanlinelabel.setObjectName("lineEdit")
        # self.humanlinelabel.setText('Human Not Detected!!')
        # self.humanlinelabel.setAlignment(QtCore.Qt.AlignCenter)
        # self.humanlinelabel.setStyleSheet("QFrame\n"
        #     "{\n"
        #     "    background-color: rgb(255, 255, 255);\n"
        #     "    \n"
        #     "    color: rgb(0, 0, 0);\n"
        #     "    border-radius:10px;\n"
        #     "    font-size:20px;\n"
        #     "}")

        self.imageLabel_2 = QtWidgets.QLabel(self.centralwidget)
        self.imageLabel_2.setGeometry(QtCore.QRect(20, 70, 282, 181))
        self.imageLabel_2.setObjectName("PiCameraView")
        self.imageLabel_2.setStyleSheet("QFrame\n"
            "{\n"
            "    background-color: rgb(255, 255, 255);\n"
            "    \n"
            "    color: rgb(0, 0, 0);\n"
            "    border-radius:10px;\n"
            "    font-size:20px;\n"
            "}")

        self.cart_data = self.query.query_get(id=1, flag='c')
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        # self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 120, 300, 301))
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 260, 300, 211))
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


        self.imageLabel_1 = QtWidgets.QLabel(self.centralwidget)
        self.imageLabel_1.setGeometry(QtCore.QRect(335, 70, 282, 181))
        self.imageLabel_1.setObjectName("PiCameraView")
        self.imageLabel_1.setStyleSheet("QFrame\n"
            "{\n"
            "    background-color: rgb(255, 255, 255);\n"
            "    \n"
            "    color: rgb(0, 0, 0);\n"
            "    border-radius:10px;\n"
            "    font-size:20px;\n"
            "}")


        # create the video capture thread
        self.video_thread = VideoThread()
        # connect its signal to the update_image slot
        self.video_thread.change_pixmap_signal.connect(self.update_image)
        # start the thread
        self.video_thread.start()


        # Get the product data fromt the database...
        self.product_data = self.query.query_get(1, 'p')

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
        self.SubmitButton.setText('Completed')
        self.SubmitButton.setObjectName("SubmitButton")
        self.SubmitButton.clicked.connect(self.completed)


        #Setting timer that updates the product and cart data at every two seconds.
        self.update_widget_timer = QTimer()
        self.update_widget_timer.timeout.connect(self.update_widget)
        self.update_widget_timer.setInterval(2000)
        self.update_widget_timer.start()



        ShoppingCart.setCentralWidget(self.centralwidget)

        self.retranslateUi(ShoppingCart)
        QtCore.QMetaObject.connectSlotsByName(ShoppingCart)


    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img_1 = self.convert_cv_qt(self.detectObj(cv_img.copy()))
        qt_img_2 = self.convert_cv_qt(self.detectQR(cv_img))
        self.imageLabel_1.setPixmap(qt_img_2)
        self.imageLabel_2.setPixmap(qt_img_1)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv.cvtColor(cv_img, cv.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(282, 211, QtCore.Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def update_widget(self):
        cart_data = self.query.query_get(id=1, flag='c')
        product_data = self.query.query_get(1, 'p')
        self.CartDataTable.update(cart_data)
        self.AvailableProductTable.update(product_data)

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    def detectObj(self, image):
        track_object = TrackObject(image)
        obj = track_object.track()

        if isinstance(obj, str):
            cv.putText(image, text=obj[:len(obj)-2], org=(20, 55), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 0, 0),thickness=2)
        else:
            x, y, w, h = obj

            if (w*h) >= 900:
                cv.rectangle(image, (x, y), (x+w, y+h), (255, 0, 255), 3)
                cv.putText(image, text="Human within range", org=(20, 55), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 0, 0),thickness=2)
            if x < 48:
                cv.putText(image, text="Human within range(Right)", org=(20, 55), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 0, 0),thickness=2)
            elif x+w > 600:
                cv.putText(image, text="Human within range(Left)", org=(20, 55), fontFace=cv.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 0, 0),thickness=2)

        return image

    def detectQR(self, image):
        frame, is_scanned = self.reader.decode(image)
        return cv.flip(frame, 1)

    def completed(self):
        self.query.completed(id=1)

    def retranslateUi(self, ShoppingCart):
        _translate = QtCore.QCoreApplication.translate
        ShoppingCart.setWindowTitle(_translate("ShoppingCart", "Shopping Cart"))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    cart = Ui_ShoppingCart()
    cart.setupUi(main_window)
    main_window.show()
    sys.exit(app.exec_())

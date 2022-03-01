# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ShoppingCart.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
import sys
import requests
import json

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

    def get_url(self):
        return self.url

    def query_get(self, id, flag='p'):
        if flag=='p':
            r = requests.get(self.get_url()+'/'+str(id)+'/data')
            datas = json.loads(r.text)
            data_dict = dict()
            for data in datas:
                for key, value in data.items():
                    if key == 'product_mfd' or key == 'product_epd':
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

        query = ApplyQuery('http://192.168.2.72:8080/shop')


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


        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 70, 361, 351))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.CartData = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.CartData.setContentsMargins(0, 0, 0, 0)
        self.CartData.setObjectName("CartData")
        # self.CartDataTable = TableView(self.product_data, len(self.product_data[list(self.product_data.keys())[0]]), len(list(self.product_data.keys())), self.horizontalLayoutWidget)
        self.CartDataTable = QtWidgets.QTableView(self.horizontalLayoutWidget)
        self.CartDataTable.setObjectName("CartDataTable")
        self.CartData.addWidget(self.CartDataTable)
        self.CartDataTable.setStyleSheet("QFrame\n"
            "{\n"
            "    background-color: rgb(255, 255, 255);\n"
            "    \n"
            "    color: rgb(0, 0, 0);\n"
            "    border-radius:10px;\n"
            "}")



        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(390, 70, 231, 141))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.Images = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.Images.setContentsMargins(0, 0, 0, 0)
        self.Images.setObjectName("Images")
        self.PiCameraView = QtWidgets.QGraphicsView(self.horizontalLayoutWidget_2)
        self.PiCameraView.setObjectName("PiCameraView")
        self.Images.addWidget(self.PiCameraView)
        self.PiCameraView.setStyleSheet("QFrame\n"
            "{\n"
            "    background-color: rgb(255, 255, 255);\n"
            "    \n"
            "    color: rgb(0, 0, 0);\n"
            "    border-radius:10px;\n"
            "}")

        # Get the product data fromt the database...
        self.product_data = query.query_get(1, 'p')

        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(390, 220, 231, 251))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.AvailableProducts = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.AvailableProducts.setContentsMargins(0, 0, 0, 0)
        self.AvailableProducts.setObjectName("AvailableProducts")
        self.AvailableProductTable = TableView(self.product_data, len(self.product_data[list(self.product_data.keys())[0]]), len(list(self.product_data.keys())), self.horizontalLayoutWidget)
        self.AvailableProductTable.setObjectName("AvailableProductTable")
        self.AvailableProducts.addWidget(self.AvailableProductTable)
        self.AvailableProductTable.setStyleSheet("QFrame\n"
            "{\n"
            "    background-color: rgb(255, 255, 255);\n"
            "    \n"
            "    color: rgb(0, 0, 0);\n"
            "    border-radius:10px;\n"
            "}")

        self.SubmitButton = QtWidgets.QPushButton(self.centralwidget)
        self.SubmitButton.setGeometry(QtCore.QRect(20, 430, 361, 41))
        self.SubmitButton.setObjectName("SubmitButton")


        ShoppingCart.setCentralWidget(self.centralwidget)

        self.retranslateUi(ShoppingCart)
        QtCore.QMetaObject.connectSlotsByName(ShoppingCart)

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

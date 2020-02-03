from colordescriptor import ColorDescriptor
import argparse
import glob
from PyQt5 import QtCore, QtGui, QtWidgets
from searcher import Searcher
import cv2


class Ui_window_2(object):
    def setupUi(self, window_2):
        window_2.setObjectName("window_2")
        window_2.resize(632, 525)
        self.centralwidget = QtWidgets.QWidget(window_2)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 210, 121, 41))
        self.pushButton.setObjectName("pushButton")
        self.imageLbl = QtWidgets.QLabel(self.centralwidget)
        self.imageLbl.setGeometry(QtCore.QRect(230, 30, 361, 421))
        self.imageLbl.setAlignment(QtCore.Qt.AlignCenter)
        self.imageLbl.setObjectName("imageLbl")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 140, 121, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(150, 140, 51, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(150, 210, 51, 41))
        self.pushButton_4.setObjectName("pushButton_4")
        window_2.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(window_2)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 632, 21))
        self.menubar.setObjectName("menubar")
        self.menuSearching = QtWidgets.QMenu(self.menubar)
        self.menuSearching.setObjectName("menuSearching")
        window_2.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(window_2)
        self.statusbar.setObjectName("statusbar")
        window_2.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuSearching.menuAction())

        self.retranslateUi(window_2)
        QtCore.QMetaObject.connectSlotsByName(window_2)
        self.pushButton.clicked.connect(self.cut_)
        self.pushButton_2.clicked.connect(self.un_cut)
        self.pushButton_3.clicked.connect(self.search_uncut)
        self.pushButton_4.clicked.connect(self.search_cut)      

    def retranslateUi(self, window_2):
        _translate = QtCore.QCoreApplication.translate
        window_2.setWindowTitle(_translate("window_2", "Color Description"))
        self.pushButton.setText(_translate("window_2", "Cut?"))
        self.imageLbl.setText(_translate("window_2", "image query"))
        self.pushButton_2.setText(_translate("window_2", "Not Cut?"))
        self.pushButton_3.setText(_translate("window_2", "Search!"))
        self.pushButton_4.setText(_translate("window_2", "Search!"))
        self.menuSearching.setTitle(_translate("window_2", "Searching..."))

    def cut_(self):
        fileName = "out.jpg"
        # Setup pixmap with the provided image 1
        pixmap = QtGui.QPixmap(fileName)
        pixmap = pixmap.scaled(self.imageLbl.width(), self.imageLbl.height(
        ), QtCore.Qt.KeepAspectRatio)  # Scale pixmap
        self.imageLbl.setPixmap(pixmap)  # Set the pixmap onto the label
        # Align the label to center
        self.imageLbl.setAlignment(QtCore.Qt.AlignCenter)

    def un_cut(self):
        # load the query image and describe it
        fp = open("image_name.txt", "r")
        data = fp.read()
        query = cv2.imread(data)

        # Setup pixmap with the provided image 1
        pixmap = QtGui.QPixmap(data)
        pixmap = pixmap.scaled(self.imageLbl.width(), self.imageLbl.height(
        ), QtCore.Qt.KeepAspectRatio)  # Scale pixmap
        self.imageLbl.setPixmap(pixmap)  # Set the pixmap onto the label
        # Align the label to center
        self.imageLbl.setAlignment(QtCore.Qt.AlignCenter)

    def search_uncut(self):
        # initialize the image descriptor
        cd = ColorDescriptor((8, 12, 3))
        fp = open ("image_name.txt" , "r")
        data = fp.read()
        # load the query image and describe it
        query = cv2.imread(data)
        features = cd.describe(query)

        # perform the search
        searcher = Searcher("index.csv")
        results = searcher.search(features)

        # loop over the results
        for (score, resultID) in results:
            # load the result image and display it
            result = cv2.imread(resultID)
            cv2.imshow("Result", result)
            cv2.waitKey(0)
    def search_cut(self):
        # initialize the image descriptor
        cd = ColorDescriptor((8, 12, 3))

        # load the query image and describe it
        query = cv2.imread("out.jpg")
        features = cd.describe(query)

        # perform the search
        searcher = Searcher("index.csv")
        results = searcher.search(features)

        # loop over the results
        for (score, resultID) in results:
            # load the result image and display it
            result = cv2.imread(resultID)
            cv2.imshow("Result", result)
            cv2.waitKey(0)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window_2 = QtWidgets.QMainWindow()
    ui = Ui_window_2()
    ui.setupUi(window_2)
    window_2.show()
    sys.exit(app.exec_())

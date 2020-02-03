from colordescriptor import ColorDescriptor
import argparse
import glob
from PyQt5 import QtCore, QtGui, QtWidgets
from searcher import Searcher
import cv2


class Ui_window_3(object):
    def setupUi(self, window_3):
        window_3.setObjectName("window_3")
        window_3.resize(632, 525)
        self.centralwidget = QtWidgets.QWidget(window_3)
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
        window_3.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(window_3)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 632, 21))
        self.menubar.setObjectName("menubar")
        self.menuSearching = QtWidgets.QMenu(self.menubar)
        self.menuSearching.setObjectName("menuSearching")
        window_3.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(window_3)
        self.statusbar.setObjectName("statusbar")
        window_3.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuSearching.menuAction())

        self.retranslateUi(window_3)
        QtCore.QMetaObject.connectSlotsByName(window_3)
        self.pushButton.clicked.connect(self.cut_)
        self.pushButton_2.clicked.connect(self.un_cut)
        self.pushButton_3.clicked.connect(self.search_uncut)
        self.pushButton_4.clicked.connect(self.search_cut)      


    def retranslateUi(self, window_3):
        _translate = QtCore.QCoreApplication.translate
        window_3.setWindowTitle(_translate("window_3", "KAZE feature extract"))
        self.pushButton.setText(_translate("window_3", "Cut?"))
        self.imageLbl.setText(_translate("window_3", "image query"))
        self.pushButton_2.setText(_translate("window_3", "Not Cut?"))
        self.pushButton_3.setText(_translate("window_3", "Search!"))
        self.pushButton_4.setText(_translate("window_3", "Search!"))
        self.menuSearching.setTitle(_translate("window_3", "Searching..."))

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

        fp = open ("image_name.txt" , "r")
        data = fp.read()
        # load the query image and describe it
        query = cv2.imread(data)
        features = extract_features(query)

        # perform the search
        searcher = Searcher("index6.csv")
        results = searcher.search(features)

        # loop over the results
        for (score, resultID) in results:
            # load the result image and display it
            result = cv2.imread("dataset" + "/" + resultID)
            cv2.imshow("Result", result)
            cv2.waitKey(0)
    def search_cut(self):

        # load the query image and describe it
        query = cv2.imread("out.jpg")
        features = extract_features(query)

        # perform the search
        searcher = Searcher("index6.csv")
        results = searcher.search(features)

        # loop over the results
        for (score, resultID) in results:
            # load the result image and display it
            result = cv2.imread("dataset" + "/" + resultID)
            cv2.imshow("Result", result)
            cv2.waitKey(0)
# Feature extractor


def extract_features(image, vector_size=32):
    try:
        # Using KAZE, cause SIFT, ORB and other was moved to additional module
        # which is adding addtional pain during install
        alg = cv2.KAZE_create()
        # Dinding image keypoints
        kps = alg.detect(image)
        # Getting first 32 of them.
        # Number of keypoints is varies depend on image size and color pallet
        # Sorting them based on keypoint response value(bigger is better)
        #kps = sorted(kps, key=lambda x: -x.response)[:vector_size]
        # computing descriptors vector
        kps, dsc = alg.compute(image, kps)
        # Flatten all of them in one big vector - our feature vector
        dsc = dsc.flatten()

        # Making descriptor of same size
        # Descriptor vector size is 64
        needed_size = (vector_size * 64)
        if dsc.size < needed_size:
            # if we have less the 32 descriptors then just adding zeros at the
            # end of our feature vector
            dsc = np.concatenate([dsc, np.zeros(needed_size - dsc.size)])
    except cv2.error as e:
        print('Error: ', e)
        return None

    return dsc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window_3 = QtWidgets.QMainWindow()
    ui = Ui_window_3()
    ui.setupUi(window_3)
    window_3.show()
    sys.exit(app.exec_())

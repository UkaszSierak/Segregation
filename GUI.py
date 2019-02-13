from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot
import sys

class GuiLogic(QtWidgets.QMainWindow):

    def __init__(self):
        super(GuiLogic,self).__init__()
        loadUi('GUI.ui',self)

        self.pushButton_12.clicked.connect(connect)

        """
        self.pushButton.clicked.connect()
        self.pushButton_2.clicked.connect()
        self.pushButton_3.clicked.connect()
        self.pushButton_4.clicked.connect()
        self.pushButton_5.clicked.connect()
        self.pushButton_6.clicked.connect()
        self.pushButton_7.clicked.connect()
        self.pushButton_8.clicked.connect()
        self.pushButton_9.clicked.connect()
        self.pushButton_10.clicked.connect()
        self.pushButton_11.clicked.connect()
        self.pushButton_13.clicked.connect()
        self.pushButton_14.clicked.connect()
        self.pushButton_15.clicked.connect()
        self.pushButton_16.clicked.connect()
        self.pushButton_17.clicked.connect()
        self.pushButton_18.clicked.connect()
        self.pushButton_19.clicked.connect()
        self.pushButton_20.clicked.connect()
        self.pushButton_21.clicked.connect()
        self.pushButton_22.clicked.connect()
        self.pushButton_23.clicked.connect()
        self.pushButton_24.clicked.connect()
        self.pushButton_25.clicked.connect()
        self.pushButton_26.clicked.connect()
        self.pushButton_27.clicked.connect()
        self.horizontalSlider.valueChanged.connect()
        self.start_vis.clicked.connect()
        self.stop_vis.clicked.connect()
        self.start_process.clicked.connect()
        self.pushButton.setAutoRepeat(True)
        self.pushButton_2.setAutoRepeat(True)
        self.pushButton_3.setAutoRepeat(True)
        self.pushButton_4.setAutoRepeat(True)
        self.pushButton_5.setAutoRepeat(True)
        self.pushButton_6.setAutoRepeat(True)
        self.pushButton_7.setAutoRepeat(True)
        self.pushButton_8.setAutoRepeat(True)
        self.pushButton_9.setAutoRepeat(True)
        self.pushButton_10.setAutoRepeat(True)
        self.pushButton_11.setAutoRepeat(True)
        self.pushButton_14.setAutoRepeat(True)
        self.pushButton_15.setAutoRepeat(True)
        self.pushButton_16.setAutoRepeat(True)
        self.pushButton_17.setAutoRepeat(True)
        self.pushButton_18.setAutoRepeat(True)
        self.start_vis.setEnabled(True)
        self.clear.clicked.connect()
"""
@pyqtSlot()
def connect():
    print('')

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = GuiLogic()
    MainWindow.show()
    sys.exit(app.exec_())
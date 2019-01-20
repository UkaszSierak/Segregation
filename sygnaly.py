from PyQt5.QtCore import QObject, pyqtSignal
import numpy as np


class Signals(QObject):

    signal = pyqtSignal(np.ndarray)

    def connect_signal(self,variable):

        self.signal.connect(variable)

    def emit_signal(self,obiekt):
        self.signal.emit(obiekt)

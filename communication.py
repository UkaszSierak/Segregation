import serial


class COM:

    def __init__(self):
        self.ser = serial.Serial()
        self.ser.baudrate
        self.ser.port
        self.ser.bytesize
        self.ser.parity
        self.ser.stopbits


    def openCOM(self, baudrate, port, bytesize, parity, stopbits):

        self.ser = serial.Serial()
        self.ser.baudrate = baudrate
        self.ser.port = port
        self.ser.bytesize = bytesize
        self.ser.parity = parity
        self.ser.stopbits = stopbits

        self.ser.open()


    def write(self, string):

        if (self.ser.is_open):
            self.ser.write(string.encode())

    def readBuffor(self):

        if (self.ser.is_open):
            odp = self.ser.read()
            wiadomosc = odp
            while odp != b'\r':
                odp = self.ser.read()
                wiadomosc += odp

            return wiadomosc.decode('utf-8')

    def closCOM(self):

        if (self.ser.is_open):
            self.ser.close()

    def comIsOpen(self):
        if self.ser.is_open:
            return True
        else:
            False

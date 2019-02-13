"""
    Communication module, is responsible for communication between robot and PC through serial port.

    Class attributes are necessary serial connection parameters such as baudrate port number itp.

    Class methods:
                    write() - write  input command for robot control device, and received output through serial port
                    _readBuffer() - reads serial port buffer
                    _getParam() - assign serial library variables to parameters according to input data

"""

import serial

class COM:
    def __init__(self, baudrate,port,databits,parity,stopbits):
        self.serial = serial.Serial()
        self.serial.baudrate = self._getParam(baudrate)
        self.serial.port = self._getParam(port)
        self.serial.bytesize = self._getParam(databits)
        self.serial.parity = self._getParam(parity)
        self.serial.stopbits = self._getParam(stopbits)

    def _getParam(self, parameter):
        dict = {
            'Even': serial.PARITY_EVEN,
            'None': serial.PARITY_NONE,
            'Odd': serial.PARITY_ODD,
            'Mark': serial.PARITY_MARK,
            'Space': serial.PARITY_SPACE,
            5: serial.FIVEBITS,
            6: serial.SIXBITS,
            7: serial.SEVENBITS,
            8: serial.EIGHTBITS,
            1: serial.STOPBITS_ONE,
            1.5: serial.STOPBITS_ONE_POINT_FIVE,
            2: serial.STOPBITS_TWO,
        }
        return dict[parameter]

    def _readBuffer(self):
        message = ''

        while self.serial.read() != b'\r':
            message += self.serial.read()

        return message.decode('utf-8')

    def write(self, string):

        try:
            self.serial.open()

        except Exception as e:
            print(e)

        else:
            self.serial.write(string.encode())
            output_msg = self._readBuffer()
            self.serial.close()

            return output_msg



if __name__ == '__main__':
    port = 'asdaaf'
    parity = 'Even'
    baudrate = 9600
    databits = 8
    stopbits = 2

    communication = COM(baudrate,port,databits,parity,stopbits)
    communication.write('no elo')
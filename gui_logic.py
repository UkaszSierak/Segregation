from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.uic import loadUi
from matplotlib import pyplot as plt
import time
import cv2 as cv
import sys
from objects import *
#from recognition import*
from new_recog import*
import serial
from communication import*
import objects
import re
import numpy as np
import math
import time
import testowanie #plik z testowymi funkcjami




class GuiLogic(QtWidgets.QMainWindow):


    def __init__(self):
        super(GuiLogic,self).__init__()
        loadUi('finallGUI.ui',self)

        self.image = None
        self.corners = []
        self.klocki = []
        self.com = COM()
        self.recogThread = None


        self.pushButton_12.clicked.connect(self.connect_device)
        self.pushButton_13.clicked.connect(self.DisConnect)

        self.pushButton.clicked.connect(self.CallAction)
        self.pushButton_2.clicked.connect(self.CallAction)
        self.pushButton_3.clicked.connect(self.CallAction)
        self.pushButton_4.clicked.connect(self.CallAction)
        self.pushButton_5.clicked.connect(self.CallAction)
        self.pushButton_6.clicked.connect(self.CallAction)
        self.pushButton_7.clicked.connect(self.CallAction)
        self.pushButton_8.clicked.connect(self.CallAction)
        self.pushButton_9.clicked.connect(self.CallAction)
        self.pushButton_10.clicked.connect(self.CallAction)
        self.pushButton_11.clicked.connect(self.CallAction)
        self.pushButton_14.clicked.connect(self.CallAction)
        self.pushButton_15.clicked.connect(self.CallAction)
        self.pushButton_16.clicked.connect(self.CallAction)
        self.pushButton_17.clicked.connect(self.CallAction)
        self.pushButton_18.clicked.connect(self.CallAction)
        self.pushButton_19.clicked.connect(self.SerwosOn)
        self.pushButton_20.clicked.connect(self.SerwosOff)
        #self.pushButton_21.clicked.connect(self.testMovs)#zmienic na kasowanie errorów
        self.pushButton_22.clicked.connect(self.GripClose)
        self.pushButton_23.clicked.connect(self.GripOpen)
        self.pushButton_24.clicked.connect(self.ConfSpeed)

        self.horizontalSlider.valueChanged.connect(self.Speed)

        self.start_vis.clicked.connect(self.start_view)
        self.stop_vis.clicked.connect(self.end_view)
        self.start_process.clicked.connect(self.SortOne)# zmienić nazwię przycisku na pushButton25 i resztę przesunąć o jeen w górę
        self.pushButton_25.clicked.connect(self.SortTwo)
        self.pushButton_26.clicked.connect(self.SortThree)
        #self.pushButton_27.clicked.connect(self.weryfie) #napisać funkcję która stopuje wykonywanie programów

        #self.Vision_wind.mousePressEvent = self.getPixel
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
        #self.clear.clicked.connect(self.ClearVision)

        cams = objects.CamCount()
        for i in range(0, len(cams)):
            name = 'Cam ' + str(cams[i])
            self.comboBox_6.addItem(name)

    def setKlocki(self, param):
        self.klocki = param

    def SortOne(self):

        image = self.capture
        self.recogThread = SortOneThread()
        self.recogThread.SetImage(image)
        self.recogThread.SetCom(self.com)
        self.recogThread.start()

    def SortTwo(self):

        image = self.capture
        self.recogThread = SortTwoThread()
        self.recogThread.SetImage(image)
        self.recogThread.SetCom(self.com)
        self.recogThread.start()

    def SortThree(self):

        image = self.capture
        self.recogThread = SortThreeThread()
        self.recogThread.SetImage(image)
        self.recogThread.SetCom(self.com)
        self.recogThread.start()

    def weryfie(self):

        self.klocki = Recognition(self.image)

        if (self.com.comIsOpen()):

            i = 5  # numer pozycji
            j = 110  # numer linijki kodu

            list1 = ['X', 'Y', 'Z', 'A', 'B', 'C','L1']  # stringi po których sprawdzana jest współrzędna i umieszczana pod takim samym indeksem ale w list2
            list2 = []
            string = []  # lista na linijki kodu

            # odczytywanie bierzacej pozycji robota
            self.com.write('1;1;PPOSF' + '\r\n')
            odp = self.com.readBuffor()
            string.append('1;1;LOAD=100' + '\r\n')
            string.append('1;1;ECLR' + '\r\n')
            string.append('1;1;EDATA10 GETM 1' + '\r\n')
            string.append('1;1;EDATA20 DEF POS P01' + '\r\n')
            string.append('1;1;EDATA30 P01=(298.6117,0.00,280.00,0.00,178.7203,0.00)(0,0)' + '\r\n')  # referencyjna
            string.append('1;1;EDATA40 DEF POS P02' + '\r\n')
            string.append('1;1;EDATA50 P02=(327.6703,-252.0321,125.6951,0.00,178.7204,0.0000)(0,0)' + '\r\n')  # pierwsza kategoria
            string.append('1;1;EDATA60 DEF POS P03' + '\r\n')
            string.append('1;1;EDATA70 P03=(237.3889,-252.0321,125.6951,0.00,178.7204,0.0000)(0,0)' + '\r\n')  # druga kategoria
            string.append('1;1;EDATA80 DEF POS P04' + '\r\n')
            string.append('1;1;EDATA90 P04=(155.1510,-252.0321,125.6951,0.00,178.7204,0.0000)(0,0)' + '\r\n')  # trzecia kategoria
            string.append('1;1;EDATA100 DEF INTE M01' + '\r\n')
            string.append('1;1;EDATA110 M01=0' + '\r\n')


            for klocek in self.klocki:  # pętla iterująca po kazdym obiekcie

                if i < 9:  # warunek numerowania pozycji wzgledem zmiennej i
                    pozycja = '0' + str(i)
                else:
                    pozycja = str(i)

                center = klocek.getCenter()  # zmienne środka
                angle = klocek.getAngle()  # zmienne kąta obrotu

                x_delta = (240.0 - center[1]) * 0.4  # róznica od środka obrazu po X pomnożona przez wpółczynnik odpowiadający ile pix mieści się w mm
                y_delta = (320.0 - center[0]) * 0.4  # to samo co wyżej ale po Y

                for cell in list1:  # iteracja po zmiennych w liście l1 umożliwiająca wydobycie danych
                    list2.append(getPos(odp, cell))

                # modyfikacja listy zmiennych, tak by możliwy był podjazd kamery do kontynuowania identyfikacja klocka

                x = list2[0] + round(x_delta, 4)
                y = list2[1] - round(y_delta, 4)
                z = 160.00
                theta = list2[3]

                list2[0] += round((x_delta + 57), 4)  # wspolzedna X
                list2[1] -= round(y_delta, 4)  # wspolzedna Y
                list2[2] = 117.00  # wspolzedna Z
                list2[3] = round(angle, 4)  # wspolzedna A

                string.append('1;1;EDATA' + str(j + 10) + ' DEF POS P' + pozycja + '\r\n')
                string.append('1;1;EDATA' + str(j + 20) + ' P' + pozycja + '=(' + str(x) + ',' + str(y) + ',' + str(z) + ',' + str(theta) + ',' + str(list2[4]) + ',' + str(list2[5]) + ')(0,0)' + '\r\n')
                string.append('1;1;EDATA' + str(j + 30) + ' MVS P' + pozycja + '\r\n')
                string.append('1;1;EDATA' + str(j + 40) + ' OPEN "COM1:" AS#1' + '\r\n')
                string.append('1;1;EDATA' + str(j + 50) + ' PRINT #1,"HEHE"' + '\r\n')
                string.append('1;1;EDATA' + str(j + 60) + ' CLOSE #1' + '\r\n')
                string.append('1;1;EDATA' + str(j + 70) + ' *L' + pozycja + '\r\n')
                string.append('1;1;EDATA' + str(j + 80) + ' If M01=0 Then GoTo *L' + pozycja + '\r\n')
                string.append('1;1;EDATA' + str(j + 90) + ' P' + pozycja + '=(' + str(list2[0]) + ',' + str(list2[1]) + ',' + str(list2[2]) + ',' + str(list2[3]) + ',' + str(list2[4]) + ',' + str(list2[5]) + ')(0,0)' + '\r\n'
                )
                string.append('1;1;EDATA' + str(j + 100) + ' MVS P' + pozycja + '\r\n')

                string.append('1;1;EDATA' + str(j + 110) + ' HCLOSE 1' + '\r\n')
                string.append('1;1;EDATA' + str(j + 120) + ' MVS P01' + '\r\n')

                string.append('1;1;EDATA' + str(j + 130) + ' If M01=1 Then GoTo ' + str(j + 160) + '\r\n')
                string.append('1;1;EDATA' + str(j + 140) + ' If M01=2 Then GoTo ' + str(j + 180) + '\r\n')
                string.append('1;1;EDATA' + str(j + 150) + ' If M01=3 Then GoTo ' + str(j + 200) + '\r\n')
                string.append('1;1;EDATA' + str(j + 160) + ' MVS P02' + '\r\n')
                string.append('1;1;EDATA' + str(j + 170) + ' GoTo ' + str(j + 210) + '\r\n')

                string.append('1;1;EDATA' + str(j + 180) + ' MVS P04' + '\r\n')
                string.append('1;1;EDATA' + str(j + 190) + ' GoTo ' + str(j + 210) + '\r\n')

                string.append('1;1;EDATA' + str(j + 200) + ' MVS P03' + '\r\n')
                string.append('1;1;EDATA' + str(j + 210) + ' M01=0' + '\r\n')
                string.append('1;1;EDATA' + str(j + 220) + ' HOPEN 1' + '\r\n')
                string.append('1;1;EDATA' + str(j + 230) + ' MVS P01' + '\r\n')

                i += 2
                j += 230

            string.append('1;1;EDATA' + str(j + 10) + ' RELM' +'\r\n')
            string.append('1;1;SAVE' + '\r\n')
            string.append('1;3;RUN100;1' + '\r\n')

            for cell in string:  # wykonaj i załaduj program
                self.com.write(cell)
                msng = self.com.readBuffor()
                #print(cell + ' ' + msng)
                #self.label_17.setText(msng)


            #print('1;4;VAL=M_00=1' + '' + msng)

            iteracje = len(self.klocki)
            k = 0
            while 1:

                    msng = self.com.readBuffor()
                    if "HEHE" in msng:
                        obj = Recognition(self.image)
                        if '4block' in obj[0].getClass():
                           self.com.write('1;1;HOT100;M01=1'+ '\r\n')
                           msng = self.com.readBuffor()
                           #print('1;1;EXEC XRUN 4,"105",1'+''+msng)
                           k += 1

                        else:
                            if '3block' in obj[0].getClass():
                                self.com.write('1;1;HOT100;M01=2'+ '\r\n')
                                msng = self.com.readBuffor()
                                #print('1;1;HOT100;M01=2' + '' + msng)
                                k += 1
                            else:
                                self.com.write('1;1;HOT100;M01=3'+ '\r\n')
                                msng = self.com.readBuffor()
                                #print('1;1;HOT100;M01=3' + '' + msng)
                                k += 1
                    if k == iteracje:
                        break



    def ClearVision(self):

        self.corners = []
        self.klocki = []



    def getPixel(self, event):
        x = event.pos().x()-5
        y = event.pos().y()

        if len(self.corners) < 2:
            self.corners.append([x,y])
        else :
            del self.corners[:]
            self.corners.append([x,y])


    def GripClose(self):



            string1 = '1;1;HNDON1'+'\r\n'
            self.com.write(string1)
            msng = self.com.readBuffor()
            self.label_17.setText(msng)

            self.pushButton_23.setEnabled(True)
            self.pushButton_22.setEnabled(False)

    def GripOpen(self):

            string1 = '1;1;HNDOFF1'+'\r\n'
            self.com.write(string1)
            msng = self.com.readBuffor()
            self.label_17.setText(msng)

            self.pushButton_22.setEnabled(True)
            self.pushButton_23.setEnabled(False)

    def Speed(self):
        val = self.horizontalSlider.value()
        print(val)
        self.label_15.setNum(val)

    def ConfSpeed(self):

            val= str(self.horizontalSlider.value())
            string1 = '1;1;OVRD=' + val + '\r\n'

            self.com.write(string1)
            msng = self.com.readBuffor()
            self.label_17.setText(msng)


    def DisConnect(self):

        if(self.com.comIsOpen()):
            self.tab_cntrl.setEnabled(False)
            #self.tab_srt.setEnabled(False)
            self.pushButton_12.setEnabled(True)
            self.pushButton_13.setEnabled(False)

            string1 = '1;1;SRVOFF'+'\r\n'
            string2 = '1;1;OVRD=0'+'\r\n'

            self.com.write(string1)
            msng = self.com.readBuffor()
            self.label_17.setText(msng)

            self.com.closCOM()

    def SerwosOn(self):


        string1 = '1;1;SRVON'+'\r\n'
        self.com.write(string1)
        msng = self.com.readBuffor()
        self.label_17.setText(msng)

        self.pushButton_20.setEnabled(True)
        self.pushButton_19.setEnabled(False)

    def SerwosOff(self):

        string1 = '1;1;SRVOFF'+'\r\n'

        self.com.write(string1)
        msng = self.com.readBuffor()
        self.label_17.setText(msng)

        self.pushButton_20.setEnabled(False)
        self.pushButton_19.setEnabled(True)

    def CallAction(self):
        trigger = self.sender()
        polecenie = objects.ActionOne(trigger.objectName())

        self.com.write(polecenie)
        msng = self.com.readBuffor()
        self.label_17.setText(msng)


    def CallAction1(self):

        polecenie = '1;1;JOG01;00;00;04;00/r/n'+'\r\n'

        self.com.write(polecenie)
        msng = self.com.readBuffor()
        self.label_17.setText(msng)



    def CallAction2(self):

        polecenie = '1;1;JOG01;00;04;00;00/r/n'+'\r\n'
        self.com.write(polecenie)
        msng = self.com.readBuffor()
        self.label_17.setText(msng)

    def connect_device(self):

        baudrate = int(self.comboBox_2.currentText())
        port = '/dev/ttyUSB0'  # nazwa_portu komunikacyjnego
        bytesize = objects.ConnParam(str(self.comboBox_3.currentText()))  # number of bits per bytes
        parity = objects.ConnParam(str(self.comboBox_5.currentText()))  # set parity check: no parity
        stopbits = objects.ConnParam(str(self.comboBox_4.currentText()))  # number of stop bits

        try:
            self.com.openCOM(baudrate, port, bytesize, parity, stopbits)

            string = ['1;1;OPEN=/dev/ttyUSB0'+'\r\n']
            string.append('1;1;CNTLON'+'\r\n')
            string.append('1;1;CYCLETIME101' + '\r\n')
            string.append('1;1;CYCLETIME100' + '\r\n')
            string.append('1;1;SRVON'+'\r\n')
            string.append('1;1;OVRD=20' + '\r\n')
            string.append('1;1;LOAD=101' + '\r\n')
            string.append('1;1;ECLR' + '\r\n')
            string.append('1;1;EDATA10 DEF POS P01' + '\r\n')
            string.append('1;1;EDATA20 P01=(298.6117,0.00,339.8730,0.00,178.7203,0.00)(0,0)' + '\r\n')
            string.append('1;1;EDATA30 MVS P01' + '\r\n')
            string.append('1;1;EDATA40 HOPEN 1' + '\r\n')
            string.append('1;1;EDATA50 RELM' + '\r\n')
            string.append('1;1;SAVE' + '\r\n')
            string.append('1;1;SLOTINIT' + '\r\n')
            string.append('1;1;PRGLOAD=101' + '\r\n')
            string.append('1;1;RUN101;1' + '\r\n')
            string.append('1;1;SLOTINIT' + '\r\n')
            string.append('1;1;OVRD=0' + '\r\n')
            string.append('1;1;SRVOFF' + '\r\n')
            string.append('1;1;RELM' + '\r\n')



            for cell in string:
                self.com.write(cell)
                msng = self.com.readBuffor()
                print(cell + ' ' + msng)
                self.label_17.setText(msng)
                if 'SRVON' in cell or 'RUN101' in cell:
                    time.sleep(2)


        except Exception as e:
            print("error open serial port: " + str(e))
            exit()


        self.tab_cntrl.setEnabled(True)
        #self.tab_srt.setEnabled(True)
        self.pushButton_12.setEnabled(False)
        self.pushButton_13.setEnabled(True)


    def detect(self):
        t = time.process_time()

        self.klocki = Recognition(self.image)

        if (self.com.comIsOpen()):

            self.com.write('1;1;PPOSF' + '\r\n')
            odp = self.com.readBuffor()

            i = 5
            j = 110

            string =  []
            string.append('1;1;LOAD=100' + '\r\n')
            string.append('1;1;ECLR' + '\r\n')
            string.append('1;1;EDATA10 GETM 1' + '\r\n')
            string.append('1;1;EDATA20 DEF POS P01' + '\r\n')
            string.append('1;1;EDATA30 P01=(298.6117,0.00,280.00,0.00,178.7203,0.00)(0,0)' + '\r\n')  # referencyjna
            string.append('1;1;EDATA40 DEF POS P02' + '\r\n')
            string.append('1;1;EDATA50 P02=(327.6703,-252.0321,125.6951,0.00,178.7204,0.0000)(0,0)' + '\r\n')  # pierwsza kategoria
            string.append('1;1;EDATA60 DEF POS P03' + '\r\n')
            string.append('1;1;EDATA70 P03=(237.3889,-252.0321,125.6951,0.00,178.7204,0.0000)(0,0)' + '\r\n')  # druga kategoria
            string.append('1;1;EDATA80 DEF POS P04' + '\r\n')
            string.append('1;1;EDATA90 P04=(155.1510,-252.0321,125.6951,0.00,178.7204,0.0000)(0,0)' + '\r\n')  # trzecia kategoria
            string.append('1;1;EDATA100 DEF INTE M01' + '\r\n')
            string.append('1;1;EDATA110 M01=0' + '\r\n')

            for klocek in self.klocki:

                if i < 9:
                    pozycja = '0'+ str(i)

                else:
                    pozycja = str(i)


                center = klocek.getCenter()
                angle = klocek.getAngle()

                x_delta = (240.0 - center[1])*0.4
                y_delta = (320.0 - center[0])*0.4

                list1 = ['X','Y','Z','A','B','C','L1']
                list2 = []
                for cell in list1:

                      list2.append(getPos(odp, cell))

                x = list2[0] + round(x_delta,4)
                y = list2[1] - round(y_delta, 4)
                z = 160.00
                theta = list2[3]

                list2[0] += round((x_delta + 57),4)# wspolzedna X
                list2[1] -= round(y_delta, 4)# wspolzedna Y
                list2[2] = 117.00# wspolzedna Z
                list2[3] = round(angle, 4)# wspolzedna A
                string.append('1;1;EDATA' + str(j + 10) + ' DEF POS P' + pozycja + '\r\n')
                string.append('1;1;EDATA' + str(j + 20) + ' P' + pozycja + '=(' + str(x) + ',' + str(y) + ',' + str(z) + ',' + str(theta) + ',' + str(list2[4]) + ',' + str(list2[5]) + ')(6,0)' + '\r\n')
                string.append('1;1;EDATA' + str(j + 30) + ' MVS P' + pozycja + '\r\n')
                string.append('1;1;EDATA' + str(j + 40) + ' OPEN "COM1:" AS#1' + '\r\n')
                string.append('1;1;EDATA' + str(j + 50) + ' PRINT #1,"HEHE"' + '\r\n')
                string.append('1;1;EDATA' + str(j + 60) + ' CLOSE #1' + '\r\n')
                string.append('1;1;EDATA' + str(j + 70) + ' *L' + pozycja + '\r\n')
                string.append('1;1;EDATA' + str(j + 80) + ' If M01=0 Then GoTo *L' + pozycja + '\r\n')
                string.append('1;1;EDATA' + str(j + 90) + ' P' + pozycja + '=(' + str(list2[0]) + ',' + str(list2[1]) + ',' + str(list2[2]) + ',' + str(list2[3]) + ',' + str(list2[4]) + ',' + str(list2[5]) + ')(6,0)' + '\r\n')
                string.append('1;1;EDATA' + str(j + 100) + ' MVS P' + pozycja + '\r\n')

                string.append('1;1;EDATA' + str(j + 110) + ' HCLOSE 1' + '\r\n')
                string.append('1;1;EDATA' + str(j + 120) + ' MVS P01' + '\r\n')

                string.append('1;1;EDATA' + str(j + 130) + ' If M01=1 Then GoTo ' + str(j + 160) + '\r\n')
                string.append('1;1;EDATA' + str(j + 140) + ' If M01=2 Then GoTo ' + str(j + 180) + '\r\n')
                string.append('1;1;EDATA' + str(j + 150) + ' If M01=3 Then GoTo ' + str(j + 200) + '\r\n')
                string.append('1;1;EDATA' + str(j + 160) + ' MVS P02' + '\r\n')
                string.append('1;1;EDATA' + str(j + 170) + ' GoTo ' + str(j + 210) + '\r\n')

                string.append('1;1;EDATA' + str(j + 180) + ' MVS P04' + '\r\n')
                string.append('1;1;EDATA' + str(j + 190) + ' GoTo ' + str(j + 210) + '\r\n')

                string.append('1;1;EDATA' + str(j + 200) + ' MVS P03' + '\r\n')
                string.append('1;1;EDATA' + str(j + 210) + ' M01=0' + '\r\n')
                string.append('1;1;EDATA' + str(j + 220) + ' HOPEN 1' + '\r\n')
                string.append('1;1;EDATA' + str(j + 230) + ' MVS P01' + '\r\n')

                i += 1
                j += 230

            string.append('1;1;EDATA' + str(j + 10) + ' RELM' + '\r\n')
            string.append('1;1;SAVE' + '\r\n')
            string.append('1;3;RUN100;1' + '\r\n')

            for cell in string:
                self.com.write(cell)
                msng = self.com.readBuffor()
                print(cell + ' ' + msng)
                self.label_17.setText(msng)

            iteracje = len(self.klocki)
            k = 0
            while 1:

                msng = self.com.readBuffor()
                if "HEHE" in msng:
                    obj = Recognition(self.image)
                    if '4block' in obj[0].getClass():
                        self.com.write('1;1;HOT100;M01=1' + '\r\n')
                        msng = self.com.readBuffor()
                        # print('1;1;EXEC XRUN 4,"105",1'+''+msng)
                        k += 1

                    else:
                        if '3block' in obj[0].getClass():
                            self.com.write('1;1;HOT100;M01=2' + '\r\n')
                            msng = self.com.readBuffor()
                            # print('1;1;HOT100;M01=2' + '' + msng)
                            k += 1
                        else:
                            self.com.write('1;1;HOT100;M01=3' + '\r\n')
                            msng = self.com.readBuffor()
                            # print('1;1;HOT100;M01=3' + '' + msng)
                            k += 1
                if k == iteracje:
                    break
        elapsed_time = time.process_time() - t

        print('Czas operacji: ' + str(elapsed_time))

    def start_view(self):


        indx = str(self.comboBox_6.currentText())


        indxa = re.findall('\d*', indx)

        for i in indxa:
            if i != '': cam = int(i)


        #self.capture = cv.VideoCapture(cam)


        #ret, self.image = self.capture.read()
        #h, w = self.image.shape[:2]


        #self.capture.set(cv.CAP_PROP_FRAME_WIDTH,640)
        #self.capture.set(cv.CAP_PROP_FRAME_HEIGHT,480)

        self.capture = cv.imread('my_photo-11.jpg', 1)

        self.image = self.capture

        self.timer=QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(5)

    def update_frame(self):
        #ret, self.image = self.capture.read()
        #self.image = cv.flip(self.image, 1)


        self.image = self.capture

        if self.klocki:
            for row in self.klocki:
                row.drawOnImg(self.image)

        if self.corners:
            if len(self.corners) == 2:
                cv.rectangle(self.image, tuple(self.corners[0]), tuple(self.corners[1]),(0,0,255), 2)

                x_diff = math.fabs(self.corners[0][0] - self.corners[1][0])
                y_diff = math.fabs(self.corners[0][1] - self.corners[1][1])

                print(x_diff)
                print(y_diff)

                if self.corners[0][0] < self.corners[1][0]:
                    region_center= [(self.corners[0][0] + (x_diff/2))]
                else:
                    region_center = [(self.corners[1][0] + (x_diff/2))]

                if self.corners[0][1] < self.corners[1][1]:
                   region_center.append(self.corners[0][1]+(y_diff/2))
                else:
                    region_center.append(self.corners[1][1] + (y_diff/2))

                print(region_center)

                print(tuple(region_center))
                cv.circle(self.image, (int(region_center[0]),int(region_center[1])), 10, (0,0,255))


        self.displayImage(self.image, 1)

    def displayImage(self,img,window=1):
        qformat=QImage.Format_Indexed8
        if len(img.shape)==3:
            if img.shape[2]==4:
                qformat=QImage.Format_RGBA8888
            else:
                qformat=QImage.Format_RGB888

        outImage=QImage(img,img.shape[1],img.shape[0],img.strides[0],qformat)
        outImage=outImage.rgbSwapped()

        if window==1:
            convertFormat = QPixmap.fromImage(outImage)
            convertFormat = convertFormat.scaled(640, 480, QtCore.Qt.KeepAspectRatio)
            self.Sort_vision.setPixmap(convertFormat)

    def end_view(self):

        self.capture.release()
        self.timer.stop()
        self.Sort_vision.clear()

    def closeEvent(self, event):

        string1 = '1;1;SRVOFF' + '\r\n'
        string2 = '1;1;OVRD=0' + '\r\n'
        string3 = '1;1;EXEC CLR 0' + '\r\n'
        string4 = '1;1;CLOSE' + '\r\n'
        self.com.write(string1)  # wyłaczenie serwa
        self.com.write(string2)  # ustawienie prędkości 0
        self.com.write(string3)  # ustawienie prędkości 0
        self.com.write(string4)  # ustawienie prędkości 0

        self.com.closCOM()


class SortOneThread(QThread):

    def __init__(self, parent=None):
        self.image = None
        self.com = None
        super(SortOneThread, self).__init__(parent)

    def SetImage(self,image):
        self.image = image

    def SetCom(self,com):
        self.com = com

    def run(self):
        t = time.process_time()
        th, frame = self.image.read()
        klocki = Recognition(frame, 'all')

        if (self.com.comIsOpen()):

            self.com.write('1;1;PPOSF' + '\r\n')
            odp = self.com.readBuffor()

            i = 5
            j = 110

            string = []
            string.append('1;1;SLOTINIT' + '\r\n')
            string.append('1;1;LOAD=100' + '\r\n')
            string.append('1;1;ECLR' + '\r\n')
            string.append('1;1;EDATA10 GETM 1' + '\r\n')
            string.append('1;1;EDATA10 DEF POS P01' + '\r\n')
            string.append('1;1;EDATA20 P01=(298.6117,0.00,339.8730,0.00,178.7203,0.00(0,0)' + '\r\n')
            string.append('1;1;EDATA40 DEF POS P02' + '\r\n')
            string.append('1;1;EDATA50 P02=(327.6703,-252.0321,125.6951,0.00,178.7204,0.0000)(0,0)' + '\r\n')  # pierwsza kategoria
            string.append('1;1;EDATA60 DEF POS P03' + '\r\n')
            string.append('1;1;EDATA70 P03=(237.3889,-252.0321,125.6951,0.00,178.7204,0.0000)(0,0)' + '\r\n')  # druga kategoria
            string.append('1;1;EDATA80 DEF POS P04' + '\r\n')
            string.append('1;1;EDATA90 P04=(155.1510,-252.0321,125.6951,0.00,178.7204,0.0000)(0,0)' + '\r\n')  # trzecia kategoria
            string.append('1;1;EDATA100 DEF INTE M01' + '\r\n')
            string.append('1;1;EDATA110 M01=0' + '\r\n')

            for klocek in klocki:

                if i < 9:
                    pozycja = '0' + str(i)

                else:
                    pozycja = str(i)

                center = klocek.getCenter()
                angle = klocek.getAngle()

                x_delta = (240.0 - center[1]) * 0.4
                y_delta = (320.0 - center[0]) * 0.4

                list1 = ['X', 'Y', 'Z', 'A', 'B', 'C', 'L1']
                list2 = []
                for cell in list1:
                    list2.append(getPos(odp, cell))

                x = list2[0] + round(x_delta, 4)
                y = list2[1] + round(y_delta, 4)
                z = 165.00
                theta = list2[3]

                list2[0] += round((x_delta + 57), 4)  # wspolzedna X
                list2[1] += round(y_delta, 4)  # wspolzedna Y
                list2[2] = 117.00  # wspolzedna Z
                list2[3] = round(angle, 4)  # wspolzedna A
                string.append('1;1;EDATA' + str(j + 10) + ' DEF POS P' + pozycja + '\r\n')
                string.append('1;1;EDATA' + str(j + 20) + ' P' + pozycja + '=(' + str(x) + ',' + str(y) + ',' + str(z) + ',' + str(theta) + ',' + str(list2[4]) + ',' + str(list2[5])+')(0,0)' + '\r\n')
                string.append('1;1;EDATA' + str(j + 30) + ' MVS P' + pozycja + '\r\n')
                string.append('1;1;EDATA' + str(j + 40) + ' DLY 0.1' + '\r\n')
                string.append('1;1;EDATA' + str(j + 50) + ' OPEN "COM1:" AS#1' + '\r\n')
                string.append('1;1;EDATA' + str(j + 60) + ' PRINT #1,"HEHE"' + '\r\n')
                string.append('1;1;EDATA' + str(j + 70) + ' CLOSE #1' + '\r\n')
                string.append('1;1;EDATA' + str(j + 80) + ' *L' + pozycja + '\r\n')
                string.append('1;1;EDATA' + str(j + 90) + ' If M01=0 Then GoTo *L' + pozycja + '\r\n')
                string.append('1;1;EDATA' + str(j + 100) + ' P' + pozycja + '=(' + str(list2[0]) + ',' + str(list2[1]) + ',' + str(list2[2]) + ',' + str(list2[3]) + ',' + str(list2[4]) + ',' + str(list2[5]) + ')(0,0)' + '\r\n')
                string.append('1;1;EDATA' + str(j + 110) + ' MVS P' + pozycja + '\r\n')

                #string.append('1;1;EDATA' + str(j + 110) + ' HCLOSE 1' + '\r\n')
                string.append('1;1;EDATA' + str(j + 120) + ' MVS P01' + '\r\n')

                string.append('1;1;EDATA' + str(j + 130) + ' If M01=1 Then GoTo ' + str(j + 160) + '\r\n')
                string.append('1;1;EDATA' + str(j + 140) + ' If M01=2 Then GoTo ' + str(j + 180) + '\r\n')
                string.append('1;1;EDATA' + str(j + 150) + ' If M01=3 Then GoTo ' + str(j + 2000) + '\r\n')
                string.append('1;1;EDATA' + str(j + 160) + ' MVS P02' + '\r\n')
                string.append('1;1;EDATA' + str(j + 170) + ' GoTo ' + str(j + 210) + '\r\n')

                string.append('1;1;EDATA' + str(j + 180) + ' MVS P04' + '\r\n')
                string.append('1;1;EDATA' + str(j + 190) + ' GoTo ' + str(j + 210) + '\r\n')

                string.append('1;1;EDATA' + str(j + 200) + ' MVS P03' + '\r\n')
                string.append('1;1;EDATA' + str(j + 210) + ' M01=0' + '\r\n')
                #string.append('1;1;EDATA' + str(j + 220) + ' HOPEN 1' + '\r\n')
                string.append('1;1;EDATA' + str(j + 220) + ' MVS P01' + '\r\n')

                i += 1
                j += 220

            string.append('1;1;EDATA' + str(j + 10) + ' RELM' + '\r\n')
            string.append('1;1;SAVE' + '\r\n')
            string.append('1;1;RUN100;1' + '\r\n')

            for cell in string:
                self.com.write(cell)
                msng = self.com.readBuffor()

            iteracje = len(klocki)
            k = 0
            while 1:

                msng = self.com.readBuffor()
                if "HEHE" in msng:
                    print("odczytano")
                    th1, frame1 = self.image.read()
                    obj = Recognition(frame1, str(k))
                    klasa = obj[0].getClass()
                    ratio = obj[0].getRatio()
                    print(klasa)
                    print(ratio)
                    if '4block' in klasa:
                        self.com.write('1;3;HOT100;M01=1' + '\r\n')
                        msng = self.com.readBuffor()

                        k += 1

                    else:
                        if '3block' in klasa:
                            self.com.write('1;3;HOT100;M01=2' + '\r\n')
                            msng = self.com.readBuffor()

                            k += 1
                        else:
                            self.com.write('1;3;HOT100;M01=3' + '\r\n')
                            msng = self.com.readBuffor()

                            k += 1
                if k == iteracje:
                    break
        elapsed_time = time.process_time() - t

        print('Czas operacji: ' + str(elapsed_time))


class SortTwoThread(QThread):

    def __init__(self, parent=None):
        self.image = None
        self.com = None
        super(SortTwoThread, self).__init__(parent)

    def SetImage(self,image):
        self.image = image

    def SetCom(self,com):
        self.com = com

    def run(self):
        t = time.process_time()
        th, frame = self.image.read()
        #frame = self.image
        klocki = Recognition(frame, 'all')

        if (self.com.comIsOpen()):

            self.com.write('1;1;PPOSF' + '\r\n')
            odp = self.com.readBuffor()

            i = 5
            j = 80

            string =  []
            string.append('1;1;SLOTINIT' + '\r\n')
            string.append('1;1;LOAD=100' + '\r\n')
            string.append('1;1;ECLR' + '\r\n')
            string.append('1;1;EDATA10 DEF POS P01' + '\r\n')
            string.append('1;1;EDATA20 P01=(298.6117,0.00,339.8730,0.00,178.7203,0.00)(0,0)' + '\r\n')
            string.append('1;1;EDATA30 DEF POS P02' + '\r\n')
            string.append('1;1;EDATA40 P02=(327.6703,-252.0321,125.6951,0.00,178.7204,0.0000)(0,0)' + '\r\n')#pierwsza kategoria
            string.append('1;1;EDATA50 DEF POS P03' + '\r\n')
            string.append('1;1;EDATA60 P03=(237.3889,-252.0321,125.6951,0.00,178.7204,0.0000)(0,0)' + '\r\n')#druga kategoria
            string.append('1;1;EDATA70 DEF POS P04' + '\r\n')
            string.append('1;1;EDATA80 P04=(155.1510,-252.0321,125.6951,0.00,178.7204,0.0000)(0,0)' + '\r\n')#trzecia kategoria

            for klocek in klocki:

                if i < 9:
                    pozycja = '0'+ str(i)

                else:
                    pozycja = str(i)


                center = klocek.getCenter()
                angle = klocek.getAngle()

                x_delta = (240.0 - center[1])*0.4
                y_delta = (320.0 - center[0])*0.4

                list1 = ['X','Y','Z','A','B','C','L1']
                list2 = []
                for cell in list1:

                      list2.append(getPos(odp, cell))

                list2[0] += round((x_delta + 57),4)# wspolzedna X
                list2[1] += round(y_delta, 4)# wspolzedna Y
                list2[2] = 117.00# wspolzedna Z
                list2[3] = round(angle, 4)# wspolzedna A


                string.append('1;1;EDATA' + str(j + 10) + ' DEF POS P'+ pozycja + '\r\n')
                string.append('1;1;EDATA' + str(j + 20) + ' P' + pozycja + '=(' + str(list2[0]) + ',' + str(list2[1]) + ',' + str(list2[2]) + ',' + str(list2[3]) + ',' + str(list2[4]) + ',' + str(list2[5]) + ')(0,0)' + '\r\n')
                string.append('1;1;EDATA' + str(j + 30) + ' MVS P' + pozycja + '\r\n')
                #string.append('1;1;EDATA' + str(j + 40) + ' HCLOSE 1' + '\r\n')

                string.append('1;1;EDATA' + str(j + 40) + ' MVS P01' + '\r\n')
                if '4block' in klocek.getClass():
                    string.append('1;1;EDATA' + str(j + 50) + ' MVS P02' + '\r\n')
                else:
                    if '3block' in klocek.getClass():
                        string.append('1;1;EDATA' + str(j + 50) + ' MVS P04' + '\r\n')
                    else:
                        if '2block' in klocek.getClass():
                            string.append('1;1;EDATA' + str(j + 50) + ' MVS P03' + '\r\n')


                #string.append('1;1;EDATA' + str(j + 70) + ' HOPEN 1' + '\r\n')
                string.append('1;1;EDATA' + str(j + 60) + ' MVS P01' + '\r\n')

                i += 1
                j += 60
            string.append('1;1;EDATA' + str(j + 10) + ' RELM' + '\r\n')
            string.append('1;1;SAVE' + '\r\n')
            string.append('1;1;PRGLOAD=100' + '\r\n')
            string.append('1;1;RUN100;1' + '\r\n')
            string.append('1;1;SLOTINIT' + '\r\n')



            for cell in string:
                self.com.write(cell)
                msng = self.com.readBuffor()
                print(cell + ' ' + msng )
        elapsed_time = time.process_time() - t

        print('Czas operacji: ' + str(elapsed_time))

class SortThreeThread(QThread):

    def __init__(self, parent=None):
         self.image = None
         self.com = None
         super(SortThreeThread, self).__init__(parent)

    def SetImage(self, image):
        self.image = image

    def SetCom(self, com):
        self.com = com

    def run(self):
        t = time.process_time()
        th, frame = self.image.read()
        klocki = Recognition(frame, 'all')

        if (self.com.comIsOpen()):

            self.com.write('1;1;PPOSF' + '\r\n')
            odp = self.com.readBuffor()

            i = 5
            j = 80

            string = []
            string.append('1;1;SLOTINIT' + '\r\n')
            string.append('1;1;LOAD=100' + '\r\n')
            string.append('1;1;ECLR' + '\r\n')
            string.append('1;1;EDATA10 DEF POS P01' + '\r\n')
            string.append('1;1;EDATA20 P01=(298.6117,0.00,339.8730,0.00,178.7203,0.00)(0,0)' + '\r\n') #ostatnia współrzędna na L1 to było 713.00
            string.append('1;1;EDATA30 DEF POS P02' + '\r\n')
            string.append('1;1;EDATA40 P02=(327.6703,-252.0321,125.6951,0.00,178.7204,0.0000)(0,0)' + '\r\n')  # pierwsza kategoria
            string.append('1;1;EDATA50 DEF POS P03' + '\r\n')
            string.append('1;1;EDATA60 P03=(237.3889,-252.0321,125.6951,0.00,178.7204,0.0000)(0,0)' + '\r\n')  # druga kategoria
            string.append('1;1;EDATA70 DEF POS P04' + '\r\n')
            string.append('1;1;EDATA80 P04=(155.1510,-252.0321,125.6951,0.00,178.7204,0.0000)(0,0)' + '\r\n')  # trzecia kategoria

            for klocek in klocki:

                if i < 9:
                    pozycja = '0' + str(i)

                else:
                    pozycja = str(i)

                center = klocek.getCenter()
                angle = klocek.getAngle()

                x_delta = (240.0 - center[1]) * 0.4
                y_delta = (320.0 - center[0]) * 0.4

                list1 = ['X', 'Y', 'Z', 'A', 'B', 'C', 'L1']
                list2 = []
                for cell in list1:
                    list2.append(getPos(odp, cell))

                list2[0] += round((x_delta + 57), 4)  # wspolzedna X
                list2[1] += round(y_delta, 4)  # wspolzedna Y
                list2[2] = 117.00  # wspolzedna Z
                list2[3] = round(angle, 4)  # wspolzedna A

                string.append('1;1;EDATA' + str(j + 10) + ' DEF POS P' + pozycja + '\r\n')
                string.append('1;1;EDATA' + str(j + 20) + ' P' + pozycja + '=(' + str(list2[0]) + ',' + str(list2[1]) + ',' + str(list2[2]) + ',' + str(list2[3]) + ',' + str(list2[4]) + ',' + str(list2[5]) + ')(0,0)' + '\r\n')
                string.append('1;1;EDATA' + str(j + 30) + ' MVS P' + pozycja + '\r\n')
                #string.append('1;1;EDATA' + str(j + 40) + ' HCLOSE 1' + '\r\n')

                string.append('1;1;EDATA' + str(j + 40) + ' MVS P01' + '\r\n')
                if '4block' in klocek.getClass():
                    string.append('1;1;EDATA' + str(j + 50) + ' MVS P02' + '\r\n')
                else:
                    if '3block' in klocek.getClass():
                        string.append('1;1;EDATA' + str(j + 50) + ' MVS P04' + '\r\n')
                    else:
                        if '2block' in klocek.getClass():
                            string.append('1;1;EDATA' + str(j + 50) + ' MVS P03' + '\r\n')

                #string.append('1;1;EDATA' + str(j + 70) + ' HOPEN 1' + '\r\n')
                string.append('1;1;EDATA' + str(j + 60) + ' MVS P01' + '\r\n')

                i += 1
                j += 60
            string.append('1;1;EDATA' + str(j + 10) + ' RELM' + '\r\n')
            string.append('1;1;SAVE' + '\r\n')
            string.append('1;1;PRGLOAD=100' + '\r\n')
            string.append('1;1;RUN100;1' + '\r\n')
            string.append('1;1;SLOTINIT' + '\r\n')

            for cell in string:
                self.com.write(cell)
                msng = self.com.readBuffor()

        elapsed_time = time.process_time() - t

        print('Czas operacji: ' + str(elapsed_time))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = GuiLogic()
    MainWindow.show()
    sys.exit(app.exec_())
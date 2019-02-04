
def DefPos(message: list):
    message.extend(
        '1;1;LOAD=100\r\n',
        '1;1;ECLR\r\n',
        '1;1;EDATA10 GETM 1\r\n',
        '1;1;EDATA20 DEF POS P01\r\n',
        '1;1;EDATA30 P01=(298.6117,0.00,280.00,0.00,178.7203,0.00)(0,0)\r\n',
        '1;1;EDATA40 DEF POS P02\r\n',
        '1;1;EDATA50 P02=(327.6703,-252.0321,125.6951,0.00,178.7204,0.0000)(0,0)\r\n',
        '1;1;EDATA60 DEF POS P03\r\n',
        '1;1;EDATA70 P03=(237.3889,-252.0321,125.6951,0.00,178.7204,0.0000)(0,0)\r\n',
        '1;1;EDATA80 DEF POS P04\r\n',
        '1;1;EDATA90 P04=(155.1510,-252.0321,125.6951,0.00,178.7204,0.0000)(0,0)\r\n',
        '1;1;EDATA100 DEF INTE M01\r\n',
        '1;1;EDATA110 M01=0\r\n',
    )
    return message

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
            string.append('1;1;LOAD=100\r\n')
            string.append('1;1;ECLR\r\n')
            string.append('1;1;EDATA10 GETM 1\r\n')
            string.append('1;1;EDATA20 DEF POS P01\r\n')
            string.append('1;1;EDATA30 P01=(298.6117,0.00,280.00,0.00,178.7203,0.00)(0,0)\r\n')  # referencyjna
            string.append('1;1;EDATA40 DEF POS P02\r\n')
            string.append('1;1;EDATA50 P02=(327.6703,-252.0321,125.6951,0.00,178.7204,0.0000)(0,0)\r\n')  # pierwsza kategoria
            string.append('1;1;EDATA60 DEF POS P03\r\n')
            string.append('1;1;EDATA70 P03=(237.3889,-252.0321,125.6951,0.00,178.7204,0.0000)(0,0)\r\n')  # druga kategoria
            string.append('1;1;EDATA80 DEF POS P04\r\n')
            string.append('1;1;EDATA90 P04=(155.1510,-252.0321,125.6951,0.00,178.7204,0.0000)(0,0)\r\n')  # trzecia kategoria
            string.append('1;1;EDATA100 DEF INTE M01\r\n')
            string.append('1;1;EDATA110 M01=0\r\n')


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




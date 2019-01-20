self.klocki = Recognition(self.image)

if(self.com.comIsOpen()):

    i = 5 #numer pozycji
    j = 80 #numer linijki kodu

    list1 = ['X', 'Y', 'Z', 'A', 'B', 'C', 'L1']    #stringi po których sprawdzana jest współrzędna i umieszczana pod takim samym indeksem ale w list2
    list2 = []
    string = []                                     # lista na linijki kodu


    #odczytywanie bierzacej pozycji robota
    self.com.write('1;1;PPOSF' + '\r\n')
    odp = self.com.readBuffor()

    string.append('1;1;LOAD=100' + '\r\n')
    string.append('1;1;ECLR' + '\r\n')
    string.append('1;1;EDATA10 DEF POS P01' + '\r\n')
    string.append('1;1;EDATA20 P01=(298.6117,0.00,280.00,0.00,178.7203,0.00,713)(6,1)' + '\r\n')                # referencyjna
    string.append('1;1;EDATA30 DEF POS P02' + '\r\n')
    string.append('1;1;EDATA40 P02=(327.6703,-252.0321,125.6951,0.00,178.7204,0.0000,713.00)(6,1)' + '\r\n')    # pierwsza kategoria
    string.append('1;1;EDATA50 DEF POS P03' + '\r\n')
    string.append('1;1;EDATA60 P03=(237.3889,-252.0321,125.6951,0.00,178.7204,0.0000,713.00)(6,1)' + '\r\n')    # druga kategoria
    string.append('1;1;EDATA70 DEF POS P04' + '\r\n')
    string.append('1;1;EDATA80 P04=(155.1510,-252.0321,125.6951,0.00,178.7204,0.0000,713.00)(6,1)' + '\r\n')    # trzecia kategoria

    for klocek in self.klocki:                           #pętla iterująca po kazdym obiekcie

        if i < 9:                                        #warunek numerowania pozycji wzgledem zmiennej i
            pozycja = '0' + str(i)
        else:
            pozycja = str(i)


        center = klocek.getCenter()                     #zmienne środka
        angle = klocek.getAngle()                       #zmienne kąta obrotu

        x_delta = (240.0 - center[1]) * 0.4             #róznica od środka obrazu po X pomnożona przez wpółczynnik odpowiadający ile pix mieści się w mm
        y_delta = (320.0 - center[0]) * 0.4             #to samo co wyżej ale po Y


        for cell in list1:                              #iteracja po zmiennych w liście l1 umożliwiająca wydobycie danych
            list2.append(getPos(odp, cell))

        #modyfikacja listy zmiennych, tak by możliwy był podjazd kamery do kontynuowania identyfikacja klocka

        list2[0] += round(x_delta, 4)                   # wspolzedna X
        list2[1] -= round(y_delta, 4)                   # wspolzedna Y
        list2[2] = 160.00                               # wspolzedna Z

        string.append('1;1;EDATA' + str(j + 10) + ' DEF POS P' + pozycja + '\r\n')
        string.append('1;1;EDATA' + str(j + 20) + ' P' + pozycja + '=(' + str(list2[0]) + ',' + str(list2[1]) + ',' + str(list2[2]) + ',' + str(list2[3]) + ',' + str(list2[4]) + ',' + str(list2[5]) + ')(6,0)' + '\r\n')
        string.append('1;1;EDATA' + str(j + 30) + ' MVS P' + pozycja + '\r\n')
        string.append('1:1;EDATA' + str(j + 30) + ' Open"COM1:"AS #1' + '\r\n')
        string.append('1:1;EDATA' + str(j + 30) + ' Print#1,"Gotowe"' + '\r\n')
        string.append('1:1;EDATA' + str(j + 30) + ' Close #1' + '\r\n')
        string.append('1;1;EDATA' + str(j + 40) + ' *L' + pozycja + '\r\n')
        string.append('1;1;EDATA' + str(j + 50) + ' If M_00=0 Then GoTo *L' + pozycja + '\r\n')
        string.append('1;1;EDATA' + str(j + 60) + ' P' + pozycja + '=(' + str(list2[0] + 57) + ',' + str(list2[1]) + ',' + str(117) + ',' + str(round(angle, 4)) + ',' + str(list2[4]) + ',' + str(list2[5]) + ')(6,0)' + '\r\n')
        string.append('1;1;EDATA' + str(j + 70) + ' MVS P' + pozycja + '\r\n')

        string.append('1;1;EDATA' + str(j + 80) + ' HCLOSE 1' + '\r\n')
        string.append('1;1;EDATA' + str(j + 90) + ' MVS P01' + '\r\n')

        string.append('1;1;EDATA' + str(j + 100) + ' If M_00=1 Then GoTo ' + str(j + 130) + '\r\n')
        string.append('1;1;EDATA' + str(j + 110) + ' If M_00=2 Then GoTo ' + str(j + 150) + '\r\n')
        string.append('1;1;EDATA' + str(j + 120) + ' If M_00=3 Then GoTo ' + str(j + 170) + '\r\n')

        string.append('1;1;EDATA' + str(j + 130) + ' MVS P02' + '\r\n')
        string.append('1;1;EDATA' + str(j + 140) + ' GoTo ' + str(j + 180) + '\r\n')

        string.append('1;1;EDATA' + str(j + 150) + ' MVS P04' + '\r\n')
        string.append('1;1;EDATA' + str(j + 160) + ' GoTo ' + str(j + 180) + '\r\n')

        string.append('1;1;EDATA' + str(j + 170) + ' MVS P03' + '\r\n')
        string.append('1;1;EDATA' + str(j + 180) + ' HOPEN 1' + '\r\n')
        string.append('1;1;EDATA' + str(j + 190) + ' MVS P01' + '\r\n')
        string.append('1;1;EDATA' + str(j + 200) + '\r\n')

        i += 1
        j += 200

    string.append('1;1;SAVE' + '\r\n')
    string.append('1;1;LOAD=100' + '\r\n')
    string.append('1;1;RUN100;1' + '\r\n')



    for cell in string:                             # wykonaj i załaduj program
        self.com.write(cell)
        msng = self.com.readBuffor()
        print(cell + ' ' + msng)
        self.label_17.setText(msng)

    ieracje = len(self.klocki)
    k = 0
    while 1 :

        if self.com.readBuffor():

            obj = Recognition(self.image)
            if '4block' in obj[0].getClass():
                self.com.write('1;9;VAL=M_00=1')
            else:
                if '3block' in obj[0].getClass():
                    self.com.write('1;9;VAL=M_00=2')
                else:
                    self.com.write('1;9;VAL=M_00=3')
            k += 0
        if k == iteracje:
            break




 def detect(self):
        t = time.process_time()

        self.klocki = Recognition(self.image)

        if (self.com.comIsOpen()):

            self.com.write('1;1;PPOSF' + '\r\n')
            odp = self.com.readBuffor()

            i = 5
            j = 80

            string =  []
            string.append('1;1;LOAD=100' + '\r\n')
            string.append('1;1;ECLR' + '\r\n')
            string.append('1;1;EDATA10 DEF POS P01' + '\r\n')
            string.append('1;1;EDATA20 P01=(298.6117,0.00,280.00,0.00,178.7203,0.00,713)(6,1)' + '\r\n')#referencyjna
            string.append('1;1;EDATA30 DEF POS P02' + '\r\n')
            string.append('1;1;EDATA40 P02=(327.6703,-252.0321,125.6951,0.00,178.7204,0.0000,713.00)(6,1)' + '\r\n')#pierwsza kategoria
            string.append('1;1;EDATA50 DEF POS P03' + '\r\n')
            string.append('1;1;EDATA60 P03=(237.3889,-252.0321,125.6951,0.00,178.7204,0.0000,713.00)(6,1)' + '\r\n')#druga kategoria
            string.append('1;1;EDATA70 DEF POS P04' + '\r\n')
            string.append('1;1;EDATA80 P04=(155.1510,-252.0321,125.6951,0.00,178.7204,0.0000,713.00)(6,1)' + '\r\n')#trzecia kategoria

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




                string.append('1;1;EDATA' + str(j + 10) + ' DEF POS P'+ pozycja + '\r\n')
                string.append('1;1;EDATA' + str(j + 20) + ' P'+ pozycja + '=('+ str(x) +','+ str(y) +','+ str(z) +','+ str(theta) +','+ str(list2[4]) +','+ str(list2[5]) +')(6,0)' + '\r\n')
                string.append('1;1;EDATA' + str(j + 30) + ' MVS P'+ pozycja + '\r\n')
                string.append('1;1;EDATA' + str(j + 40) + ' P' + pozycja + '=(' + str(list2[0]) + ',' + str(list2[1]) + ',' + str(list2[2]) + ',' + str(list2[3]) + ',' + str(list2[4]) + ',' + str(list2[5]) + ')(6,0)' + '\r\n')
                string.append('1;1;EDATA' + str(j + 50) + ' MVS P' + pozycja + '\r\n')
                string.append('1;1;EDATA' + str(j + 60) + ' HCLOSE 1' + '\r\n')

                string.append('1;1;EDATA' + str(j + 70) + ' MVS P01' + '\r\n')
                if '4block' in klocek.getClass():
                    string.append('1;1;EDATA' + str(j + 80) + ' MVS P02' + '\r\n')
                else:
                    if '3block' in klocek.getClass():
                        string.append('1;1;EDATA' + str(j + 80) + ' MVS P04' + '\r\n')
                    else:
                        if '2block' in klocek.getClass():
                            string.append('1;1;EDATA' + str(j + 80) + ' MVS P03' + '\r\n')


                string.append('1;1;EDATA' + str(j + 90) + ' HOPEN 1' + '\r\n')
                string.append('1;1;EDATA' + str(j + 100) + ' MVS P01' + '\r\n')

                i += 1
                j += 100

            string.append('1;1;SAVE' + '\r\n')
            string.append('1;1;PRGLOAD=100' + '\r\n')
            string.append('1;1;RUN100;1' + '\r\n')
            string.append('1;1;SLOTINIT' + '\r\n')



            for cell in string:
                self.com.write(cell)
                msng = self.com.readBuffor()
                print(cell + ' ' + msng)
                self.label_17.setText(msng)

        elapsed_time = time.process_time() - t

        print('Czas operacji: ' + str(elapsed_time))
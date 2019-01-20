# obecna metoda

t = time.process_time()

self.klocki = Recognition(self.image)

if (self.com.comIsOpen()):

    self.com.write('1;1;PPOSF' + '\r\n')
    odp = self.com.readBuffor()

    i = 5
    j = 80

    string = []
    string.append('1;1;LOAD=100' + '\r\n')
    string.append('1;1;ECLR' + '\r\n')
    string.append('1;1;EDATA10 DEF POS P01' + '\r\n')
    string.append('1;1;EDATA20 P01=(298.6117,0.00,280.00,0.00,178.7203,0.00,713)(6,1)' + '\r\n')  # referencyjna
    string.append('1;1;EDATA30 DEF POS P02' + '\r\n')
    string.append(
        '1;1;EDATA40 P02=(327.6703,-252.0321,125.6951,0.00,178.7204,0.0000,713.00)(6,1)' + '\r\n')  # pierwsza kategoria
    string.append('1;1;EDATA50 DEF POS P03' + '\r\n')
    string.append(
        '1;1;EDATA60 P03=(237.3889,-252.0321,125.6951,0.00,178.7204,0.0000,713.00)(6,1)' + '\r\n')  # druga kategoria
    string.append('1;1;EDATA70 DEF POS P04' + '\r\n')
    string.append(
        '1;1;EDATA80 P04=(155.1510,-252.0321,125.6951,0.00,178.7204,0.0000,713.00)(6,1)' + '\r\n')  # trzecia kategoria

    for klocek in self.klocki:

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
        list2[1] -= round(y_delta, 4)  # wspolzedna Y
        list2[2] = 117.00  # wspolzedna Z
        list2[3] = round(angle, 4)  # wspolzedna A

        string.append('1;1;EDATA' + str(j + 10) + ' DEF POS P' + pozycja + '\r\n')
        string.append(
            '1;1;EDATA' + str(j + 20) + ' P' + pozycja + '=(' + str(list2[0]) + ',' + str(list2[1]) + ',' + str(
                list2[2]) + ',' + str(list2[3]) + ',' + str(list2[4]) + ',' + str(list2[5]) + ')(6,0)' + '\r\n')
        string.append('1;1;EDATA' + str(j + 30) + ' MVS P' + pozycja + '\r\n')

        string.append('1;1;EDATA' + str(j + 40) + ' HCLOSE 1' + '\r\n')

        string.append('1;1;EDATA' + str(j + 50) + ' MVS P01' + '\r\n')
        if '4block' in klocek.getClass():
            string.append('1;1;EDATA' + str(j + 60) + ' MVS P02' + '\r\n')
        else:
            if '3block' in klocek.getClass():
                string.append('1;1;EDATA' + str(j + 60) + ' MVS P04' + '\r\n')
            else:
                if '2block' in klocek.getClass():
                    string.append('1;1;EDATA' + str(j + 60) + ' MVS P03' + '\r\n')

        string.append('1;1;EDATA' + str(j + 70) + ' HOPEN 1' + '\r\n')
        string.append('1;1;EDATA' + str(j + 80) + ' MVS P01' + '\r\n')

        i += 1
        j += 80

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


# metoda z podjazdem do każdego klocka i klasyfikacją



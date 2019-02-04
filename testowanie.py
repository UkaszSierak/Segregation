"""
Cały plik służy do testowania poprawionych funkcji i ich działania
funkcje zdaten do implementacji zostają opatrzone odpowiednim komentarzem

Przydatne:
            DefPOS

Zmiany do wprowadzenia:

    - otwierać i zamykać port tylko przy okazji potrzeby komunikacji z urządzeniem
"""

import sys
import re
from collections import defaultdict

def concat_position(pos_list: list, container_list: dict, message: str):

    def extract_header(offset):
        return '1;1;EDATA{}'.format(offset)

    def defin_position(position):
        return ' DEF POS P{}'.format(position)

    def declare_position(position, value):
         return ' P{}={}(0,0)'.format(position, value)

    def define_flag(position):
        return  ' DEF INTE M{}'.format(position)

    def declare_flag(position):
        return  ' M{}=0'.format(position)

    def finish_record():
        return '\r\n'

    containers = []

    for i, item in enumerate(pos_list):

        position = i +1
        value = item.get('location')
        container = item.get('container')
        if container not in containers:
            containers.append(container)

        offset = 10 * (i * 2 + 1)
        next_offset = 10 * (i * 2 + 2)

        message += extract_header(offset) + defin_position(position) + finish_record()
        message += extract_header(next_offset) + declare_position(position, value) + finish_record()

    for i, item in enumerate(containers):

        offset = 10 * (position * 2 + 1)
        next_offset = 10 * (position * 2 + 2)

        position  = position + 1
        value = container_list.get(item)

        message += extract_header(offset) + defin_position(position) + finish_record()
        message += extract_header(next_offset) + declare_position(position, value) + finish_record()

    for i, item in enumerate(containers):

        offset = 10 * (position * 2 + 1)
        next_offset = 10 * (position * 2 + 2)

        position -= 1

        value = container_list.get(item)

        message += extract_header(offset) + define_flag(position) + finish_record()
        message += extract_header(next_offset) + declare_flag(position) + finish_record()

        position += 2

    return  message






def DefPos(message: list, positions):

#    message.extend(
#        ['1;1;LOAD=100\r\n',
#         '1;1;ECLR\r\n',
#         '1;1;EDATA10 GETM 1\r\n',
#         '1;1;EDATA20 DEF POS P01\r\n',
#         '1;1;EDATA30 P01=(298.6117,0.00,280.00,0.00,178.7203,0.00)(0,0)\r\n',
#         '1;1;EDATA40 DEF POS P02\r\n',
#         '1;1;EDATA50 P02=(327.6703,-252.0321,125.6951,0.00,178.7204,0.0000)(0,0)\r\n',
#         '1;1;EDATA60 DEF POS P03\r\n',
#         '1;1;EDATA70 P03=(237.3889,-252.0321,125.6951,0.00,178.7204,0.0000)(0,0)\r\n',
#         '1;1;EDATA80 DEF POS P04\r\n',
#         '1;1;EDATA90 P04=(155.1510,-252.0321,125.6951,0.00,178.7204,0.0000)(0,0)\r\n',
#         '1;1;EDATA100 DEF INTE M01\r\n',
#         '1;1;EDATA110 M01=0\r\n']
 #   )
    return message
"""
Funkcja odpowiedzialna za cięcie treści programu sterującego robotem na bloki po max 255 byte
wstawić w miejsce funkcji chopp_message() w klasie RobotControlProgram.
"""

def chop_string(message: str):

    chopped_message = []
    end_indx = None
    start_indx = 0

    pattern = r'\r\n'
    regex = re.compile(pattern, re.IGNORECASE)
    end_of_lines = regex.finditer(message)
    end_indx = end_of_lines.__next__().start() + 2
    chopped_message.append(message[start_indx:end_indx])

    for match in end_of_lines:

        if sys.getsizeof(message[start_indx:int(match.start() + 2)]) < 255:
            chopped_message.pop()
            end_indx = match.start() + 2
            chopped_message.append(message[start_indx:end_indx])
        else:
            try :
                start_indx = end_indx
                end_indx = end_of_lines.__next__().start() + 2
                chopped_message.append(message[start_indx:end_indx])
            except:
                pass
    return chopped_message


dupa = '1;1;EDATA10 DEF POS P01\r\n' \
       '1;1;EDATA20 P02=(327.6703,-252.0321,125.6951,0.00,178.7204,0.0000)(0,0)\r\n' \
       '1;1;EDATA30 OPEN "COM1:" AS#1\r\n' \
       '1;1;EDATA40 PRINT #1,"HEHE"\r\n' \
       '1;1;EDATA50 CLOSE #1\r\n' \
       '1;1;EDATA10 *L01\r\n' \
       '1;1;EDATA60 If M01=0 Then GoTo *L01\r\n' \
       '1;1;EDATA70 P02=(327.6703,-252.0321,125.6951,0.00,178.7204,0.0000)(0,0)\r\n' \
       '1;1;EDATA80 MVS P01\r\n' \
       '1;1;EDATA90 HCLOSE 1\r\n' \
       '1;1;EDATA100 MVS P01\r\n' \
       '1;1;EDATA110 If M01=1 Then GoTo 160\r\n' \
       '1;1;EDATA120 If M01=2 Then GoTo 180\r\n' \
       '1;1;EDATA130 If M01=3 Then GoTo 200\r\n' \
       '1;1;EDATA140 MVS P02\r\n' \
       '1;1;EDATA150 GoTo 210\r\n' \
       '1;1;EDATA160 MVS P04\r\n' \
       '1;1;EDATA170 GoTo 210\r\n' \
       '1;1;EDATA180 MVS P03\r\n' \
       '1;1;EDATA190 M01=0\r\n' \
       '1;1;EDATA200 HOPEN 1\r\n' \
       '1;1;EDATA210 MVS P01\r\n'

dropp_locations = {'small': [124.34, 546.23, 675.45, 432.34, 675.45, 234.34],
                   'medium': [224.34, 546.23, 675.45, 432.34, 675.45, 234.34],
                   'large': [324.34, 546.23, 675.45, 432.34, 675.45, 234.34]}
blocks = {'block01':{'location': [327.6703,-252.0321,125.6951,0.00,178.7204,0.0000], 'container': 'small'},
          'block02':{'location': [627.6703,-252.0321,125.6951,0.00,178.7204,0.0000], 'container': 'medium'}}


blocks2 = [{'location': (327.6703,-252.0321,125.6951,0.00,178.7204,0.0000), 'container': 'small'},
           {'location': (627.6703,-252.0321,125.6951,0.00,178.7204,0.0000), 'container': 'medium'}]

containers = {'small': (727.6703,-252.0321,125.6951,0.00,178.7204,0.0000),
              'medium': (827.6703,-252.0321,125.6951,0.00,178.7204,0.0000),
              'large': (927.6703,-252.0321,125.6951,0.00,178.7204,0.0000)}

message = ''

message = concat_position(blocks2, containers, message)

print(message)
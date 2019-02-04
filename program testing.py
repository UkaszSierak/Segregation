
            '1;1;PPOSF\r\n'
            '1;1;LOAD=100\r\n'
            '1;1;ECLR\r\n'
            '1;1;EDATA10 GETM 1\r\n'
            '1;1;EDATA20 DEF POS P01\r\n'
            '1;1;EDATA30 P01=(298.6117,0.00,280.00,0.00,178.7203,0.00)(0,0)\r\n'
            '1;1;EDATA40 DEF POS P02\r\n'
            '1;1;EDATA50 P02=(327.6703,-252.0321,125.6951,0.00,178.7204,0.0000)(0,0)\r\n'
            '1;1;EDATA60 DEF POS P03\r\n'
            '1;1;EDATA70 P03=(237.3889,-252.0321,125.6951,0.00,178.7204,0.0000)(0,0)\r\n'
            '1;1;EDATA80 DEF POS P04\r\n'
            '1;1;EDATA90 P04=(155.1510,-252.0321,125.6951,0.00,178.7204,0.0000)(0,0)\r\n'
            '1;1;EDATA100 DEF INTE M01\r\n'
            '1;1;EDATA110 M01=0\r\n'
            '1;1;EDATA30 MVS P01\r\n'
            '1;1;EDATA40 OPEN "COM1:" AS#1\r\n'
            '1;1;EDATA50 PRINT #1,"HEHE"\r\n'
            '1;1;EDATA60 CLOSE #1\r\n'
            '1;1;EDATA70 *L01\r\n'
            '1;1;EDATA80 If M01=0 Then GoTo *L01\r\n'
            '1;1;EDATA110 HCLOSE 1\r\n'
            '1;1;EDATA130 If M01=1 Then GoTo 160\r\n'
            '1;1;EDATA170 GoTo  210\r\n'
            '1;1;EDATA220 HOPEN 1\r\n'
            '1;1;EDATA10 RELM\r\n'
            '1;1;SAVE\r\n'
            '1;3;RUN100;1\r\n'
            '1;1;HOT100;M01=1\r\n'

            def write_variable(program_number, variable):
                return 'HOT{};{}'.format(program_number, variable)

            def open_hand(hand_number):
                return 'HOPEN {}'.format(hand_number)

            def close_hand(hand_number):
                return 'HCLOSE {}'.format(hand_number)

            def save():
                return 'SAVE'

            def run_program(program_number, mode):
                return 'RUN{};{}'.format(program_number,mode)


            def open_communication(line_number, file_number):
                return 'OPEN "COM{}:" AS#{}'.format(line_number, file_number)

            def output_data(file_number, message):
                return 'PRINT #{}, "{}"'.format(file_number, message)

            def clos_comunication(file_number):
                return 'CLOSE #{}'.format(file_number)

            def label_line(indx):
                return '*L{}'.format(indx)

            def if_statnment(condition, action):
                return 'If {} Then {}'

            def jump_to_line(line_nmbr):
                return 'GoTo {}'.format(line_nmbr)

            def load_program(program_number):
                return 'LOAD={}'.format(program_number)

            def clear_program():
                return 'ECLR'

            def read_current_position():
                return 'PPOSF'

            def move_to_position(idx):
                return 'MVS P{}'.format(idx)

            def extract_header(device_number, slot_number):
                return '{};{};'.format(device_number, slot_number)


            def edit_line(offset, action):
                return 'EDATA{} {}'.format(offset, action)

            def defin_position(position):
                return 'DEF POS P{}'.format(position)


            def declare_position(position, value):
                return 'P{}={}(0,0)'.format(position, value)


            def define_flag(position):
                return 'DEF INTE M{}'.format(position)


            def declare_flag(position):
                return 'M{}=0'.format(position)


            def finish_record():
                return '\r\n'
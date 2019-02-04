

def open_hand(hand_number):
    return 'HOPEN {}'.format(hand_number)

def close_hand(hand_number = 1):
    return 'HCLOSE {}'.format(hand_number)

def output_data(file_number, message):
    return 'PRINT #{}, "{}"'.format(file_number, message)

def clos_comunication(file_number):
    return 'CLOSE #{}'.format(file_number)

def label_line(indx):
    return '*L{}'.format(indx)

def if_statnment(condition, action):
    return 'If {} Then {}'.format(condition, action)

def jump_to_line(line_nmbr):
    return 'GoTo {}'.format(line_nmbr)

def move_to_position(idx):
    return 'MVS P{}'.format(idx)

def defin_position(position):
    return 'DEF POS P{}'.format(position)

def declare_position(position, value):
    return 'P{}={}(0,0)'.format(position, value)

def define_flag(position):
    return 'DEF INTE M{}'.format(position)

def declare_flag(position, value):
    return 'M{}={}'.format(position, value)
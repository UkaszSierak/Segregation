import melfa_IV
"""
Trzeba pomyslec ktre instrukcje wjada ze zmian dziaanai na slotach 

"""


class RobotControl(object):

    def __init__(self,communication_port: str,* , device_number = None, slot_number = None):

        self.communication_port = communication_port
        if device_number == None:
            self.device_number = 1
        else:
            self.device_number = device_number
        if slot_number == None:
            self.slot_number = 1
        else:
            self.slot_number = slot_number

    def __extract_header(self, slot) -> str:
        return '{};{};'.format(self.device_number, slot)

    def __finish_line(self) -> str:
        return '\r\n'

    def __make_command(self, action, slot = None) -> str:
        if slot == None:
            slot = self.slot_number
        else:
            pass
        return self.__extract_header(slot) + action + self.__finish_line()

    def open_port(self):
        action = 'OPEN={}'.format(self.communication_port)
        return self.__make_command(action)

    def enable_control(self, value: str):
        action = 'CNTL{}'.format(value)
        return self.__make_command(action)

    def turn_servo(self, value: str):
        action = 'SRV{}'.format(value)
        return self.__make_command(action)

    def change_override(self, value):
        action = 'OVRD={}'.format(value)
        return self.__make_command(action)

    def open_grip(self, grip_number=1):
        action = 'HNDON{}'.format(grip_number)
        return self.__make_command(action)

    def close_grip(self, grip_number=1):
        action = 'HNDOFF{}'.format(grip_number)
        return self.__make_command(action)

    def read_current_position(self):
        action = 'PPOSF'
        return self.__make_command(action)

    def close_port(self):
        action = 'CLOSE'
        return self.__make_command(action)

    def save(self):
        action = 'SAVE'
        return self.__make_command(action)

    def run_program(self, program_number, mode):
        action = 'RUN{};{}'.format(program_number, mode)
        return self.__make_command(action)

    def jog_operation(self, jog_mode, direction, inching=0):
        action = 'JOG{};00;{};{}'.format(jog_mode, direction, inching)
        return self.__make_command(action)

    def edit_line(self, offset, command):
        action = 'EDATA{} {}'.format(offset, command)
        return self.__make_command(action)



if __name__ == '__main__':

    c = RobotControl('USB')
    print(c.open_port())



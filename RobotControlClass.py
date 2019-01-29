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


    def __extract_header(self) -> str:
        return '{};{};'.format(self.device_number, self.slot_number)

    def __finish_record(self) -> str:
        return '\r\n'

    def open_port(self) -> str:
        return 'OPEN={}'.format(self.communication_port)

    def enable_control(self, value: str) -> str:
        return 'CNTL{}'.format(value)

    def turn_servo(self, value: str) -> str:
        return 'SRV{}'.format(value)

    def change_override(self, value) -> str:
        return 'OVRD={}'.format(value)

    def open_grip(self, grip_number = 1) -> str:
        return 'HNDON{}'.format(grip_number)

    def close_grip(self, grip_number = 1) -> str:
        return 'HNDOFF{}'.format(grip_number)

    def read_current_position(self) -> str:
        return 'PPOSF'

    def close_port(self) -> str:
        return 'CLOSE'

    def make_command(self, action) -> str:

        command = self.__extract_header() + action + self.__finish_record()

        return command






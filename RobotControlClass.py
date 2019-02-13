"""
    RobotControl class methods allows to create a commands described by R3 protocol, released by Mitsubishi.

    Syntax of command :
                        [<Robot No.>];[<Slot No>];<Command><Argument>

                                <Robot No.> -The robot number to be operated is specified. (0, 1, 2 or 3)
                                  <Slot No> -The slot number to be operated is specified. (0, 1 - 33)
                        <Command><Argument> - It differs in each command, and refer to the explanation of each command

                        Example:
                                1;1;CNTLON

    All commands and options are described in R3 Protocol by Mitsubishi

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

    def openPort(self):
        action = 'OPEN={}'.format(self.communication_port)
        return self.__make_command(action)

    def enableControl(self, value: str):
        action = 'CNTL{}'.format(value)
        return self.__make_command(action)

    def turnServo(self, value: str):
        action = 'SRV{}'.format(value)
        return self.__make_command(action)

    def changeOverride(self, value):
        action = 'OVRD={}'.format(value)
        return self.__make_command(action)

    def openGrip(self, grip_number=1):
        action = 'HNDON{}'.format(grip_number)
        return self.__make_command(action)

    def closeGrip(self, grip_number=1):
        action = 'HNDOFF{}'.format(grip_number)
        return self.__make_command(action)

    def readPosition(self):
        action = 'PPOSF'
        return self.__make_command(action)

    def closePort(self):
        action = 'CLOSE'
        return self.__make_command(action)

    def save(self):
        action = 'SAVE'
        return self.__make_command(action)

    def runProgram(self, program_number, mode):
        action = 'RUN{};{}'.format(program_number, mode)
        return self.__make_command(action)

    def jogOperation(self, jog_mode, direction, inching=0):
        action = 'JOG{};00;{};{}'.format(jog_mode, direction, inching)
        return self.__make_command(action)

    def editLine(self, offset, command):
        action = 'EDATA{} {}'.format(offset, command)
        return self.__make_command(action)






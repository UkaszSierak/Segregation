"""
    Module that held robot control generate program.

    Class attributes:
                        _points    - list of trajectory points in dictionary
                        _relations - dictionary of relations between trajectory points
                        _program - list of control program lines
                        _line - index of last program line
                        _program_slot - slot in  robot control device memory where program is stored
                        _message - list of all message strings

    Class methods:

                    generate() - generate control program
                    chop() - chop program line list ino parts that are  255 bytes max

"""

import sys
import RobotControlClass
import melfa_IV

class RobotControlProgram(RobotControlClass.RobotControl):

    def __init__(self, points: dict, relations: dict , communication_port: str):
        super().__init__(communication_port)
        self._points = points
        self._relations = relations
        self._program = []
        self._program_slot = '100'
        self._line = 0
        self._message = []

    def _newLine(self):
        self._line += 10
        return self._line

    def _editNewLine(self, content):
        self._program.append(self.editLine(self._newLine(),content))

    def _definePoints(self):

        for i, item in enumerate(self._points):

            define = melfa_IV.defin_position(self._points[item])
            declare = melfa_IV.declare_position(self._points[item], item)

            self._editNewLine(define)
            self._editNewLine(declare)

    def _defineTrajectory(self):
        for item in self._relations:

            self._editNewLine(melfa_IV.move_to_position(item, retraction = -50))
            self._editNewLine(melfa_IV.move_to_position(item))
            self._editNewLine(melfa_IV.close_hand())
            self._editNewLine(melfa_IV.move_to_position(retraction = -50))
            self._editNewLine(melfa_IV.move_to_position(self._relations[item], retraction= -50))
            self._editNewLine(melfa_IV.move_to_position(self._relations[item]))
            self._editNewLine(melfa_IV.open_hand())
            self._editNewLine(melfa_IV.move_to_position(retraction= -50))


    def generate(self):
        self._definePoints()
        self._defineTrajectory()

    def chopp(self):

        iterator = self._program.__iter__()
        container = ''

        while True:
            try:

                if sys.getsizeof(container) <= 255:
                    container += iterator.__next__()
                else:
                    self._message.append(container)
                    container = ''

            except StopIteration:
                break

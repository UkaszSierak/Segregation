import re, sys
import RobotControlClass
import ObjectClass
import melfa_IV


class RobotControlProgram(RobotControlClass.RobotControl):

    def __init__(self, points: dict, relations: dict , communication_port: str):
        super().__init__(communication_port)
        self._points = points
        self._relations = relations
        self._program = []
        self._programslot = '100'
        self._line = 0
        self._message = []

    def _newLine(self):
        self._line += 10
        return self._line

    def _DefinePoints(self):

        for i, item in enumerate(self._points):

            define = melfa_IV.defin_position(self._points[item])
            declare = melfa_IV.declare_position(self._points[item], item)

            self._program.append(self.edit_line(self._newLine(), define))
            self._program.append(self.edit_line(self._newLine(), declare))

    def _DefineTrajectory(self):
        for item in self._relations:
            self._program.append(self.edit_line(self._newLine(), melfa_IV.move_to_position(item, retraction = -50)))
            self._program.append(self.edit_line(self._newLine(), melfa_IV.move_to_position(item)))
            self._program.append(self.edit_line(self._newLine(), melfa_IV.close_hand()))
            self._program.append(self.edit_line(self._newLine(), melfa_IV.move_to_position(retraction = -50)))
            self._program.append(self.edit_line(self._newLine(), melfa_IV.move_to_position(self._relations[item], retraction= -50)))
            self._program.append(self.edit_line(self._newLine(), melfa_IV.move_to_position(self._relations[item])))
            self._program.append(self.edit_line(self._newLine(), melfa_IV.open_hand()))
            self._program.append(self.edit_line(self._newLine(), melfa_IV.move_to_position(retraction= -50)))

    def Generate(self):
        self._DefinePoints()
        self._DefineTrajectory()

    def Chopp(self):

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






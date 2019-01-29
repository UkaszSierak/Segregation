import re, sys

class RobotControlProgram:

    def __init__(self, object_locations: list, object_containers_location: dict):
        self.objects_locations = object_locations
        self.objects_containters_location = object_containers_location
        self.message_string = None
        self.programslot = '100'

    def _points_definition(self):


    def _add_pre_part(self):

        self.message_string += '1;1;LOAD={}\r\n'.format(self.programslot)
        self.message_string += '1;1;ECLR\r\n'

    def add_main_part(self):

    def add_closing(self):

    def generate_program(self):

        self._add_pre_part()
        self._add_main_part()
        self._add_closing()

    def chopp(self):

        pattern = r'\r\n'
        regex = re.compile(pattern, re.IGNORECASE)
        end_of_lines = regex.finditer(self.message_string)
        end_indx = end_of_lines.__next__().start() + 2
        start_indx = 0
        chopped_message = []
        chopped_message.append(self.message_string[start_indx:end_indx])

        for match in end_of_lines:
            if sys.getsizeof(self.message_string[start_indx:int(match.start() + 2)]) < 255:
                chopped_message.pop()
                end_indx = match.start() + 2
                chopped_message.append(self.message_string[start_indx:end_indx])
            else:
                try:
                    start_indx = end_indx
                    end_indx = end_of_lines.__next__().start() + 2
                    chopped_message.append(self.message_string[start_indx:end_indx])
                except:
                    pass
        return chopped_message

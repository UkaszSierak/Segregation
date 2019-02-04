import re, sys
import RobotControlClass

class RobotControlProgram(RobotControlClass.RobotControl):

    def __init__(self, objects, object_containers_location, communication_port: str):
        super().__init__(communication_port)
        self.objects_locations = object_locations
        self.objects_containters_location = object_containers_location
        self.message_string = None
        self.programslot = '100'



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

c = RobotControlClass.RobotControl('dupeczki')

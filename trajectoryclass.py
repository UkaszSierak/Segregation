from collections import OrderedDict

class Trajectory:
    def __init__(self):
        self._point_list = OrderedDict()
        self._point_relations = OrderedDict()

    def AddNewPoint(self, location):
        idx = len(self._point_list) + 1

        self._point_list[location] = idx

    def AddRelation(self,object_location, container_location):
        object_idx = self._point_list[object_location]
        container_idx = self._point_list[container_location]

        self._point_relations[object_idx] = container_idx

    @property
    def point_list(self):
        return self._point_list
    @property
    def point_relations(self):
        return self._point_relations

#if __name__ == '__main__':



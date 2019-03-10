"""
    Trajectory module contains class definition which describes robot trajectory by:

        - _point_list:
                        list of trajectory points in dictionary:
                        __________________________
                        |    keys     :   values  |
                        ---------------------------
                        | coordinates :  point id |
                        |             .           |
                        |             .           |

        - _point_relations:
                            relations between points in dictionary:
                            _________________________________________
                            |      keys       :        values       |
                            -----------------------------------------
                            | object point id :  container point id |
                            |                 .                     |
                            |                 .                     |

    Class contains method such as:

        addPoint - adding point to trajectory with its parameters as id and location
        addRelation - adding relation between described trajectory points
"""

from collections import OrderedDict

class Trajectory:
    def __init__(self):
        self._point_list = OrderedDict()
        self._point_relations = OrderedDict()

    def addPoint(self, location):
        idx = len(self._point_list) + 1

        self._point_list[location] = idx

    def addRelation(self,object_location, container_location):
        object_idx = self._point_list[object_location]
        container_idx = self._point_list[container_location]

        self._point_relations[object_idx] = container_idx

    @property
    def point_list(self):
        return self._point_list
    @property
    def point_relations(self):
        return self._point_relations



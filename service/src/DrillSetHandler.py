#
#  DrillSetHandler Class keeps a copy of drills.json in memory
#  Allows CRU(D) operations on the data in drills.json
#
#
import json
from uuid import uuid4


class DrillSetHandler():
    """
    Docstring?
    """

    def __init__(self, pathname):
        self.pathname = pathname
        with open(self.pathname, 'r', encoding="UTF-8") as f_in:
            self.drill_data = json.loads(f_in.read())

    def get_drill_sets(self):
        return [{"id": id, "name": self.drill_data[id]["name"]} for id in self.drill_data]

    def get_drill_set(self, id):
        return self.drill_data[id]

    def get_sentence(self, id, index):
        return self.drill_data[id]["sentences"][index]

    def add_drill_set(self, new_drill_set):
        self.drill_data[uuid4()] = new_drill_set
        with open(self.pathname, 'w', encoding="UTF-8") as f_out:
            f_out.write(json.dumps(self.drill_data))

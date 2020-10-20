from .cage import Cage


class CageList(object):
    def __init__(self, cages, client):
        self.client = client
        self.cages = self.__build_cages(cages)

    def __build_cages(self, cages):
        cage_dict = {}
        for cage in cages:
            cage_obj = Cage(cage["name"], cage["uuid"], self.client)
            cage_dict[cage["name"]] = cage_obj
        return cage_dict

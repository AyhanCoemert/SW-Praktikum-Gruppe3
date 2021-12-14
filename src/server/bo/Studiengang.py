from src.server.bo import BusinessObject as bo


# Group Invitation Klasse
class Studiengang(bo.BusinessObject):

    def __init__(self):
        super().__init__()
        self._ID = 0
        self._module = 0
        self._semester = 0
        self._name = 0


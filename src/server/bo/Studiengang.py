from src.server.bo import BusinessObject as bo


# Group Invitation Klasse
class Studiengang(bo.BusinessObject):

    def __init__(self):
        super().__init__()
        self._ID = 0
        self._module = 0
        self._semester = 0
        self._name = 0

    def get_ID(self):
        return self._ID

    def set_ID(self, ID):
        self.ID = ID

    def get_module(self):
        return self._module

    def set_module(self, module):
        self._module = module

    def get_semester(self):
        return self._semester

    def set_semester(self, semester):
        self._semester = semester

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    # Erstellung von Studiengang mit Dictionary
    @staticmethod
    def from_dict(dictionary=dict()):
        obj = Modul()
        obj.set_id(dictionary["id"])
        obj.set_creation_date(dictionary["creation_date"])
        obj.set_ID(dictionary["ID"])
        obj.set_module(dictionary["module"])
        obj.set_semester(dictionary["semester"])
        obj.set_name(dictionary["name"])
        return obj                          # nochmal kontrollieren
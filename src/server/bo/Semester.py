from src.server.bo import BusinessObject as bo


# Group Invitation Klasse
class Semester(bo.BusinessObject):

    def __init__(self):
        super().__init__()
        self._ID = 0
        self._semesteranzahl = 0


    def get_ID(self):
        return self._ID

    def set_ID(self, ID):
        self.ID = ID

    def get_semesteranzahl(self):
        return self._semesteranzahl

    def set_semesteranzahl(self, semesteranzahl):
        self._semesteranzahl = semesteranzahl


    # Erstellung von Semester mit Dictionary
    @staticmethod
    def from_dict(dictionary=dict()):
        obj = Semester()
        obj.set_ID(dictionary["ID"])
        obj.set_creation_date(dictionary["creation_date"])
        obj.set_semesteranzahl(dictionary["semesteranzahl"])
        return obj                          # nochmal kontrollieren
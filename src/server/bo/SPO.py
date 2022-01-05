from src.server.bo import BusinessObject as bo


# Group Invitation Klasse
class SPO(bo.BusinessObject):

    def __init__(self):
        super().__init__()
        self._ID = 0
        self._beginn = 0
        self._studiengang = 0

    def get_ID(self):
        return self._ID

    def set_ID(self, ID):
        self.ID = ID

    def get_beginn(self):
        return self._beginn

    def set_beginn(self, beginn):
        self._beginn = beginn

    def get_studiengang(self):
        return self._studiengang

    def set_studiengang(self, studiengang):
        self._studiengang = studiengang

    # Erstellung von SPO mit Dictionary
    @staticmethod
    def from_dict(dictionary=dict()):
        obj = SPO()
        obj.set_id(dictionary["id"])
        obj.set_creation_date(dictionary["creation_date"])
        obj.set_beginn(dictionary["beginn"])
        obj.set_studiengang(dictionary["studiengang"])
        return obj                          # nochmal kontrollieren
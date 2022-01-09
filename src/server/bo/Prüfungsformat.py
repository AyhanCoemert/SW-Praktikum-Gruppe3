from src.server.bo import BusinessObject as bo


# Group Invitation Klasse
class Prüfungsformat(bo.BusinessObject):

    def __init__(self):
        super().__init__()
        self._ID = 0
        self._benennung = 0
        self._leistung = 0

    def get_ID(self):
        return self._ID

    def set_ID(self, ID):
        self.ID = ID

    def get_benennung(self):
        return self._benennung

    def set_benennung(self, benennung):
        self._benennung = benennung

    def get_leistung(self):
        return self._leistung

    def set_leistung(self, leistung):
        self._leistung = leistung


    # Erstellung von Prüfungsformat mit Dictionary
    @staticmethod
    def from_dict(dictionary=dict()):
        obj = Prüfungsformat()
        obj.set_ID(dictionary["ID"])
        obj.set_creation_date(dictionary["creation_date"])
        obj.set_benennung(dictionary["benennung"])
        obj.set_leistung(dictionary["leistung"])
        return obj                          # nochmal kontrollieren
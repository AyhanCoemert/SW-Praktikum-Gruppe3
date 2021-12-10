from src.server.bo import BusinessObject as bo


# Group Invitation Klasse
class Modul(bo.BusinessObject):

    def __init__(self):
        super().__init__()
        self._sws = False
        self._ects = 0
        self._literatur = 0
        self._verantwortlicher = 0
        self._edv_nummer = 0

    def get_sws(self):
        return self._sws

    def set_sws(self, sws):
        self.sws = sws

    def get_ects(self):
        return self._ects

    def set_ects(self, ects):
        self._ects = ects

    def get_literatur(self):
        return self._literatur

    def set_literatur(self, literatur):
        self._literatur = literatur

    def get_verantwortlicher(self):
        return self._verantwortlicher

    def set_verantwortlicher(self, verantwortlicher):
        self._verantwortlicher = verantwortlicher

    def get_edv_nummer(self):
        return self._edv_nummer

    def set_edv_nummer(self, edv_nummer):
        self._edv_nummer = edv_nummer

    # Erstellung von Modul mit Dictionary
    @staticmethod
    def from_dict(dictionary=dict()):
        obj = Modul()
        obj.set_id(dictionary["id"])
        obj.set_creation_date(dictionary["creation_date"])
        obj.set_sws(dictionary["sws"])
        obj.set_ects(dictionary["ects"])
        obj.set_literatur(dictionary["literatur"])
        obj.set_verantwortlicher(dictionary["verantwortlicher"])
        obj.set_edv_nummer(dictionary["edv_nummer"])
        return obj
from src.server.bo import BusinessObject as bo


# Group Invitation Klasse
class Student(bo.BusinessObject):

    def __init__(self):
        super().__init__()
        self._ID = False
        self._google_user_id = 0
        self._name = 0
        self._vorname = 0
        self._mail_adresse = 0
        self._semester = 0
        self._studiengang = 0
        self._matrikelnummer = 0

    def get_ID(self):
        return self._ID

    def set_ID(self, ID):
        self.ID = ID

    def get_google_use_id(self):
        return self._google_user_id

    def set_google_user_id(self, google_user_id):
        self._google_user_id = google_user_id

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_vorname(self):
        return self._vorname

    def set_veorname(self, vorname):
        self._vorname = vorname

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

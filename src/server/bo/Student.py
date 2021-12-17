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

    def set_vorname(self, vorname):
        self._vorname = vorname

    def get_mail_adresse(self):
        return self._mail_adresse

    def set_mail_adresse(self, mail_adresse):
        self._mail_adresse = mail_adresse

    def get_semester(self):
        return self._semester

    def set_semester(self, semester):
        self._semester = semester

    def get_studiengang(self):
        return self._studiengang

    def set_studiengang(self, studiengang):
        self._studiengang = studiengang

    def get_matrikelnummer(self):
        return self._matrikelnummer

    def set_matrikelnummer(self, matrikelnummer):
        self._matrikelnummer = matrikelnummer

    # Erstellung von Student mit Dictionary
    @staticmethod
    def from_dict(dictionary=dict()):
        obj = Student()
        obj.set_id(dictionary["id"])
        obj.set_creation_date(dictionary["creation_date"])
        obj.set_ID(dictionary["ID"])
        obj.set_google_user_id(dictionary["google_user_id"])
        obj.set_name(dictionary["name"])
        obj.set_vorname(dictionary["vorname"])
        obj.set_mail_adresse(dictionary["mail_adresse"])
        obj.set_semester(dictionary["semester"])
        obj.set_studiengang(dictionary["studiengang"])
        obj.set_matrikelnummer(dictionary["matrikelnummer"])
        return obj                                   # nochmal kontrollieren

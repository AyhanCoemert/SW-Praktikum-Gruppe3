from src.server.bo import BusinessObject as bo


# Group Invitation Klasse
class Verwaltungsmitarbeiter(bo.BusinessObject):

    def __init__(self):
        super().__init__()
        self._ID = False
        self._name = 0
        self._vorname = 0
        self._email = 0
        self._passwort = 0

    def get_ID(self):
        return self._ID

    def set_ID(self, ID):
        self.ID = ID

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_vorname(self):
        return self._vorname

    def set_vorname(self, vorname):
        self._vorname = vorname

    def get_email(self):
        return self._email

    def set_email(self, email):
        self._email = email

    def get_passwort(self):
        return self._passwort

    def set_passwort(self, passwort):
        self._passwort = passwort


    # Erstellung von Verwaltungsmitarbeiter mit Dictionary
    @staticmethod
    def from_dict(dictionary=dict()):
        obj = Verwaltungsmitarbeiter()
        obj.set_creation_date(dictionary["creation_date"])
        obj.set_ID(dictionary["ID"])
        obj.set_name(dictionary["name"])
        obj.set_vorname(dictionary["vorname"])
        obj.set_email(dictionary["email"])
        obj.set_passwort(dictionary["passwort"])
        return obj                                   # nochmal kontrollieren
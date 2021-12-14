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
        self._name = 0
        self._vorname = 0
        self._mail_adresse = 0 #test

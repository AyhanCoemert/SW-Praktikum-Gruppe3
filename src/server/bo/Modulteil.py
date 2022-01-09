from src.server.bo import BusinessObject as bo


# Group Invitation Klasse
class Modulteil(bo.BusinessObject):

    def __init__(self):
        super().__init__()
        self._ID = 0


    def get_ID(self):
        return self._ID

    def set_ID(self, ID):
        self.ID = ID



    # Erstellung von Modulteil mit Dictionary
    @staticmethod
    def from_dict(dictionary=dict()):
        obj = Modulteil()
        obj.set_ID(dictionary["ID"])
        obj.set_creation_date(dictionary["creation_date"])
        return obj                          # nochmal kontrollieren
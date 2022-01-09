from abc import ABC, abstractmethod
from datetime import datetime


# BusinessObject Klasse
class BusinessObject(ABC):

    def __init__(self):
        self._ID = 0
        self._creation_date = datetime.now().isoformat()

    def get_ID(self):
        return self._ID

    def set_ID(self, value):
        self._ID = value

    def get_creation_date(self):
        return self._creation_date

    def set_creation_date(self, new_date):
        self._creation_date = new_date

    # Datumsformat bei Bedarf anpassen (Manchmal muss "Z" entfernt werden damit die Datenbank es akzeptiert)
    @staticmethod
    def date_format(date_string):
        if date_string is not None:
            return datetime.fromisoformat(date_string.replace("Z", ""))
        return None
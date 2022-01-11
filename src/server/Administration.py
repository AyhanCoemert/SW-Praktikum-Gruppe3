from .bo.Modul import Modul
from .bo.Modulteil import Modulteil
from .bo.Prüfungsformat import Prüfungsformat
from .bo.Semester import Semester
from .bo.SPO import SPO
from .bo.Student import Student
from .bo.Studiengang import Studiengang
from .bo.Verwaltungsmitarbeiter import Verwaltungsmitarbeiter

from .db.ModulMapper import *
from .db.ModulteilMapper import *
from .db.PrüfungsformatMapper import *
from .db.SemesterMapper import *
from .db.SPOMapper import *
from .db.StudentMapper import *
from .db.StudiengangMapper import *
from .db.VerwaltungsmitarbeiterMapper import *


class Administration(object):
    """Diese Klasse aggregiert nahezu sämtliche Applikationslogik (engl. Business Logic).
    Sie ist wie eine Spinne, die sämtliche Zusammenhänge in ihrem Netz (in unserem
    Fall die Daten der Applikation) überblickt und für einen geordneten Ablauf und
    dauerhafte Konsistenz der Daten und Abläufe sorgt.
    Die Applikationslogik findet sich in den Methoden dieser Klasse. Jede dieser
    Methoden kann als *Transaction Script* bezeichnet werden. Dieser Name
    lässt schon vermuten, dass hier analog zu Datenbanktransaktion pro
    Transaktion gleiche mehrere Teilaktionen durchgeführt werden, die das System
    von einem konsistenten Zustand in einen anderen, auch wieder konsistenten
    Zustand überführen. Wenn dies zwischenzeitig scheitern sollte, dann ist das
    jeweilige Transaction Script dafür verwantwortlich, eine Fehlerbehandlung
    durchzuführen.
    Diese Klasse steht mit einer Reihe weiterer Datentypen in Verbindung. Diese
    sind:
    - die Klassen BusinessObject und deren Subklassen,
    - die Mapper-Klassen für den DB-Zugriff."""

    def __init__(self):
        pass

 def create_modul (self, name, englischer Titel, creation_date, sws, ects, literatur, verantwortlicher, edv_nummer):
        """Modul wird erstellt"""

        modul = Modul()
        modul.set_name(name)
        modul.set_creation_date(creation_date)
        modul.set_sws(sws)
        modul.set_ects(ects)
        modul.set_literatur(literatur)
        modul.set_verantwortlicher(verantwortlicher)
        modul.set_edv_nummer(edv_nummer)


        with MOdulMapper() as mapper:
            return mapper.insert(Modul)




    def get_modul_by_name(self, name):
        with ModulMapper() as mapper:
             return mapper.find_by_name(name)

    def get_Modul_by_id(self, id):
        """Modul mit gegebener ID Auslesen"""

        with ModulMapper() as mapper:
            return mapper.find_by_id(id)


    def get_all_Modul(self):
        """Auslesen aller StudyGroups in unserem System"""

        with ModulMapper() as mapper:
            return mapper.find_all()

    def save_Modul(self, Modul):
        """Das gegebene Modul speichern."""

        with ModulMapper() as mapper:
            mapper.update(Modul)

    def delete_Modul(self, Modul):
        """Das gegebene Modul aus unserem System löschen."""

        with ModulMapper() as mapper:
            mapper.delete(Modul)
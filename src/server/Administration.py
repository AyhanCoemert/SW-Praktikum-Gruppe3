from .bo.User import User
from .bo.Chat import Chat
from .bo.ChatInvitation import ChatInvitation
from .bo.ChatMessage import ChatMessage
from .bo.LearningprofileGroup import LearningProfileGroup
from .bo.LearningProfileUser import LearningProfileUser
from .bo.StudyGroup import StudyGroup
from .bo.GroupInvitation import GroupInvitation

from .db.UserMapper import *
from .db.ChatMapper import *
from .db.ChatInvitationMapper import *
from .db.ChatMessageMapper import *
from .db.LearningProfileGroupMapper import *
from .db.LearningProfileUserMapper import *
from .db.StudyGroupMapper import *
from .db.GroupInvitationMapper import *


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

 def create_modul (self, name, englischer Titel, Alle Atribute rein):
        """Modul wird erstellt"""

        modul = Modul()
        studygroup.set_name(name)
        chat = self.create_chat(name)
        studygroup.set_chat_id(chat.get_id())
        studygroup.set_id(1)

        with StudyGroupMapper() as mapper:
            return mapper.insert(studygroup)




    def get_studygroup_by_name(self, name):
        """Den StudyGroup über den gegebenen Namen Auslesen"""

        with StudyGroupMapper() as mapper:
            return mapper.find_by_group_name(name)

    def get_studygroup_by_id(self, id):
        """StudyGroup mit gegebener ID Auslesen"""

        with StudyGroupMapper() as mapper:
            return mapper.find_by_id(id)


    def get_all_studygroups(self):
        """Auslesen aller StudyGroups in unserem System"""

        with StudyGroupMapper() as mapper:
            return mapper.find_all()

    def save_studygroup(self, studygroup):
        """Die gegebene StudyGroup speichern."""

        with StudyGroupMapper() as mapper:
            mapper.update(studygroup)

    def delete_studygroup(self, studygroup):
        """Die gegebene StudyGroup aus unserem System löschen."""

        with StudyGroupMapper() as mapper:
            mapper.delete(studygroup)
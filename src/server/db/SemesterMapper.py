from src.server.db.Mapper import Mapper
from src.server.bo.Semester import Semester


class SemesterMapper(Mapper):
    """Mapper-Klasse, die Chat-Objekte auf eine relationale
    Datenbank abbildet. Hierzu wird eine Reihe von Methoden zur Verfügung
    gestellt, mit deren Hilfe z.B. Objekte gesucht, erzeugt, modifiziert und
    gelöscht werden können. Das Mapping ist bidirektional. D.h., Objekte können
    in DB-Strukturen und DB-Strukturen in Objekte umgewandelt werden.
    """

    def __init__(self):
        super().__init__()

    def build_bo(self, tuples):
        """BO wird aufgebaut und in späteren Methoden aufgegriffen.
        So spart man sich das immer wieder aufbauen des BOs später"""

        result = []

        if len(tuples) == 1:
            "Baue nur einen"

            for (id, name, semesteranzahl ) in tuples:
                semester = Semester()
                semester.set_id(id)
                semester.set_name(name)
                semester.set_semesteranzahl(semesteranzahl)
                result = semester

        else:
            "Baue mehrere"

            for (id, name, semesteranzahl) in tuples:
                semester = Semester()
                semester.set_id(id)
                semester.set_name(name)
                semester.set_semesteranzahl(semesteranzahl)
                result = semester

        return result

    def find_all(self):
        """Auslesen aller Semester in unserem System.
        :return Eine Sammlung mit Semester-Objekten.
        """

        result = []

        cursor = self._cnx.cursor()
        command = "SELECT * FROM chat"
        cursor.execute(command)
        tuples = cursor.fetchall()

        result = self.build_bo(tuples)

        self._cnx.commit()
        cursor.close()

        return result

    def find_by_id(self, id):
        """Suchen eines Semesters mit vorgegebener ID. Da diese eindeutig ist,
        wird genau ein Objekt zurückgegeben.
        :param id Primärschlüsselattribut (->DB)
        :return Semester-Objekt, das dem übergebenen Schlüssel entspricht, None bei
                nicht vorhandenem DB-Tupel.
        """

        result = None

        cursor = self._cnx.cursor()
        command = "SELECT id, name, semesteranzahl FROM semester " \
                  "WHERE id LIKE '{}' ".format(id)
        cursor.execute(command)
        tuples = cursor.fetchall()

        try:
            result = self.build_bo(tuples)

        except IndexError:
            """Der IndexError wird oben beim Zugriff auf self.build_bo(tuples) auftreten, wenn der vorherige SELECT-Aufruf
            keine Tupel liefert, sondern tuples = cursor.fetchall() eine leere Sequenz zurück gibt."""

            result = None

        self._cnx.commit()
        cursor.close()

        return result

    def find_by_name(self, name):
        """Auslesen aller Semester anhand des Semester-Namens.
        :param name Name des zugehörigen Semesters.
        :return Eine Sammlung mit Semester-Objekten, die sämtliche Semester
            mit dem gewünschten Namen enthält.
        """

        result = None

        cursor = self._cnx.cursor()
        command = "SELECT id, name, semesteranzahl FROM chat " \
                  "WHERE name LIKE '{}' ".format(name)
        cursor.execute(command)
        tuples = cursor.fetchall()

        try:
            result = self.build_bo(tuples)

        except IndexError:
            """Der IndexError wird oben beim Zugriff auf self.build_bo(tuples) auftreten, wenn der vorherige SELECT-Aufruf
            keine Tupel liefert, sondern tuples = cursor.fetchall() eine leere Sequenz zurück gibt."""

            result = None

        self._cnx.commit()
        cursor.close()

        return result

    def insert(self, chat):
        """Einfügen eines Semester-Objekts in die Datenbank.
        Dabei wird auch der Primärschlüssel des übergebenen Objekts geprüft und ggf.
        berichtigt.
        :param chat das zu speichernde Objekt
        :return das bereits übergebene Objekt, jedoch mit ggf. korrigierter ID.
        """

        cursor = self._cnx.cursor()
        cursor.execute("SELECT MAX(id) as maxid from chat")
        tuples = cursor.fetchall()

        for (maxid) in tuples:
            if maxid[0] is None:
                """Wenn wir KEINE maximale ID feststellen konnten, dann gehen wir
                davon aus, dass die Tabelle leer ist und wir mit der ID 1 beginnen können."""

                chat.set_id(1)

            else:
                """Wenn wir eine maximale ID festellen konnten, zählen wir diese
                um 1 hoch und weisen diesen Wert als ID dem Participation-Objekt zu."""

                chat.set_id(maxid[0] + 1)

        command = "INSERT INTO chat (id, name, semesteranzahl) VALUES " \
                  "('{}','{}','{}')".format(semester.get_id(), semester.get_name(), semester.get_semesteranzahl()() )
        cursor.execute(command)

        self._cnx.commit()
        cursor.close()

        return chat

    def update(self, chat):
        """Wiederholtes Schreiben eines Objekts in die Datenbank.
        :param Semester ist das Objekt, das in die DB geschrieben werden soll
        """

        cursor = self._cnx.cursor()
        command = "UPDATE chat SET name = ('{}'), creation_date = ('{}') WHERE id = ('{}')" \
            .format(chat.get_name(), chat.get_creation_date(), chat.get_id())
        cursor.execute(command)

        self._cnx.commit()
        cursor.close()

    def delete(self, chat):
        """Löschen der Daten eines Semester-Objekts aus der Datenbank.
        :param Semester ist das aus der DB zu löschende "Objekt"
        """

        cursor = self._cnx.cursor()

        command = "DELETE FROM semester WHERE id={}".format(semester.get_id())
        cursor.execute(command)

        self._cnx.commit()
        cursor.close()
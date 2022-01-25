from flask import Flask
# Auf Flask aufbauend nutzen wir RestX
from flask_restx import Api, Resource, fields
# Wir benutzen noch eine Flask-Erweiterung für Cross-Origin Resource Sharing
from flask_cors import CORS

from src.server.Administration import Administration
from src.server.bo.Modul import Modul
"""test Commit"""
"""test"""

#fehlt etwas?

"""
A. Konventionen für dieses Module:
    A.1. HTTP response status codes:
        Folgende Codes werden verwendet:
        200 OK           :      bei erfolgreichen requests. Af die Verwendung von
                                weiter differenzierenden Statusmeldungen wie etwa
                                '204 No Content' für erfolgreiche requests, die
                                außer evtl. im Header keine weiteren Daten zurückliefern,
                                wird in dieser Fallstudye auch aus Gründen einer
                                möglichst einfachen Umsetzung verzichtet.
        401 Unauthorized :      falls der User sich nicht gegenüber dem System
                                authentisiert hat und daher keinen Zugriff erhält.
        404 Not Found    :      falls eine angefragte Resource nicht verfügbar ist
        500 Internal Server Error : falls der Server einen Fehler erkennt,
                                diesen aber nicht genauer zu bearbeiten weiß.
    A.2. Name des Moduls:
        Der Name dieses Moduls lautet main.py. Grund hierfür ist, dass Google
        App Engine, diesen Namen bevorzugt und sich dadurch das Deployment
        einfacher gestaltet. Natürlich wären auch andere Namen möglich. Dies
        wäre aber mit zusätzlichem Konfigurationsaufwand in der Datei app.yaml
        verbunden.
"""

app = Flask(__name__)
"""
Instanzieren von Flask. Am Ende dieser Datei erfolgt dann erst der 'Start' von Flask.
"""

CORS(app, resources=r'/Spotch/*')


"""
Alle Ressourcen mit dem Präfix /Spotch für **Cross-Origin Resource Sharing** (CORS) freigeben.
Diese eine Zeile setzt die Installation des Package flask-cors voraus. 
"""

"""
In dem folgenden Abschnitt bauen wir ein Modell auf, das die Datenstruktur beschreibt, 
auf deren Basis Clients und Server Daten austauschen. Grundlage hierfür ist das Package flask-restx.
"""
api = Api(app, version='1.0', title='Spotch API',
          description='Eine App um die zutreffende SPO zu finden.') #passt das so?

"""Anlegen eines Namespace
Namespaces erlauben uns die Strukturierung von APIs. In diesem Fall fasst dieser Namespace alle
Spotch-relevanten Operationen unter dem Präfix /Spotch zusammen."""

Spotch = api.namespace('Spotch', description='Funktionen des Spotch')


bo = api.model('BusinessObject', {
    'id': fields.Integer(attribute='_id', description='Der Unique Identifier eines BusinessObject'),
    'creation_date': fields.DateTime(attribute='_creation_date', description='Das Erstellungsdatum eines bo',
                                     dt_format='iso8601')
})

nbo = api.inherit('NamedBusinessObject', bo, {
    'name': fields.String(attribute='_name', description='Name eines NamedBusinessObjects')
})

Modul = api.inherit('Modul', bo, {
    'sws': fields.Integer(attribute='_sws', description='sws eines moduls'),
    'ects': fields.Integer(attribute='_ects', description='ects eines moduls'),
    'literatur': fields.Integer(attribute='_literatur ', description='literatur eines moduls'),
    'verantwortlicher': fields.Integer(attribute='_verantwortlicher', description='verantwortlicher eines moduls'),
    'edv_nummer': fields.Integer(attribute='_edv_nummer', description='edv_nummer eines moduls') #muss das nicht für jeden einzeln?
})


# ----- Modul -----


@spotch.route('/modul')
@spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
class ModulListOperations(Resource):
    """Auslesen aller modul-Objekte.
    Sollten keine modul-Objekte verfügbar sein, so wird eine leere Sequenz zurückgegeben."""

    @spotch.marshal_list_with(modul)
    @secured
    def get(self):
        adm = Administration()
        modul = adm.get_all_modul()
        return modul

    @spotch.marshal_with(modul, code=200)
    @spotch.expect(modul)
    @secured
    def post(self):
        """Anlegen eines neuen Modul-Objekts.
        **ACHTUNG:** Wir fassen die vom Client gesendeten Daten als Vorschlag auf.
        So ist zum Beispiel die Vergabe der ID nicht Aufgabe des Clients.
        Selbst wenn der Client eine ID in dem Proposal vergeben sollte, so
        liegt es an der Administration (Businesslogik), eine korrekte ID
        zu vergeben. *Das korrigierte Objekt wird schließlich zurückgegeben.*""" #kann man Client hier lassen?

        adm = Administration()
        prpl = Modul.from_dict(api.payload)
        """RATSCHLAG: Prüfen Sie stets die Referenzen auf valide Werte, bevor Sie diese verwenden!"""

        if prpl is not None:
            """ Das serverseitig erzeugte Objekt ist das maßgebliche und 
            wird auch dem Client zurückgegeben."""

            s = adm.create_modul(prpl.get_creation_date(),
                                 prpl.get_sws(),
                                 prpl.get_ects(),
                                 prpl.get_literatur(),
                                 prpl.get_verantwortlicher(),
                                 prpl.get_edv_nummer())

            return s, 200

        else:
            ''' Wenn irgendetwas schiefgeht, dann geben wir nichts zurück und werfen einen Server-Fehler.'''

            return '', 500


@spotch.route('/modul/<int:id>')
@spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
class ModulOperations(Resource):
    @spotch.marshal_with(modul)
    @secured
    @secured
    def get(self, id):
        """Auslesen eines bestimmten Modul-Objekts.
        Das auszulesende Objekt wird durch die ```id``` in dem URI bestimmt."""

        adm = Administration()
        single_modul = adm.get_modul_by_id(id)
        return single_modul

    @spotch.marshal_with(modul)
    @spotch.expect(modul, validate=True)
    @secured
    def put(self, id):
        """Update eines bestimmten Modul-Objekts.
        **ACHTUNG:** Relevante id ist die id, die mittels URI bereitgestellt und somit als Methodenparameter
        verwendet wird. Dieser Parameter überschreibt das ID-Attribut des im Payload der Anfrage übermittelten
        Modul-Objekts."""

        adm = Administration()
        modul = Modul.from_dict(api.payload)
        print('main aufruf')

        if modul is not None:
            """Hierdurch wird die id des zu überschreibenden (vgl. Update) Modul-Objekts gesetzt."""

            modul.set_id(id)
            adm.save_modul(modul)
            return '', 200

        else:
            return '', 500

    @secured
    def delete(self, id):
        """Löschen eines bestimmten Modul-Objekts.
        Das zu löschende Objekt wird durch die ```id``` in dem URI bestimmt."""

        adm = Administration()
        single_modul = adm.get_modul_by_id(id)
        adm.delete_modul(single_modul)
        return '', 200


    @spotch.route('/modul-by-name/<string:name>')
    @spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
    class ModulNameOperations(Resource):
        @spotch.marshal_list_with(modul)
        @secured
        def get(self, name):
            """ Auslesen von Modul-Objekten, die durch ihren Namen bestimmt werden.
            Die auszulesenden Objekte werden durch ```name``` in dem URI bestimmt."""

            adm = Administration()
            modul = adm.get_modul_by_name(name)
            return modul  #brauchen wir Name?


    @spotch.route('/modul-by-sws/<string:sws>')
    @spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
    class ModulSwsOperations(Resource):
        @spotch.marshal_list_with(modul)
        @secured
        def get(self, name):
            """ Auslesen von Modul-Objekten, die durch ihren Namen bestimmt werden.
            Die auszulesenden Objekte werden durch ```name``` in dem URI bestimmt."""

            adm = Administration()
            modul = adm.get_modul_by_sws(sws)
            return modul


    @spotch.route('/modul-by-ects/<string:ects>')
    @spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
    class ModulEctsOperations(Resource):
        @spotch.marshal_list_with(modul)
        @secured
        def get(self, name):
            """ Auslesen von Modul-Objekten, die durch ihren Namen bestimmt werden.
            Die auszulesenden Objekte werden durch ```name``` in dem URI bestimmt."""

            adm = Administration()
            modul = adm.get_modul_by_ects(ects)
            return modul


    @spotch.route('/modul-by-literatur/<string:literatur>')
    @spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
    class ModulLiteraturOperations(Resource):
        @spotch.marshal_list_with(modul)
        @secured
        def get(self, name):
            """ Auslesen von Modul-Objekten, die durch ihren Namen bestimmt werden.
            Die auszulesenden Objekte werden durch ```name``` in dem URI bestimmt."""

            adm = Administration()
            modul = adm.get_modul_by_literatur(literatur)
            return modul


    @spotch.route('/modul-by-verantwortlicher/<string:verantwortlicher>')
    @spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
    class ModulVerantwortlicherOperations(Resource):
        @spotch.marshal_list_with(modul)
        @secured
        def get(self, name):
            """ Auslesen von Modul-Objekten, die durch ihren Namen bestimmt werden.
            Die auszulesenden Objekte werden durch ```name``` in dem URI bestimmt."""

            adm = Administration()
            modul = adm.get_modul_by_verantwortlicher(verantwortlicher)
            return modul

    @spotch.route('/modul-by-edv-nummer/<string:edv_nummer>')
    @spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
    class ModulEdvNummerOperations(Resource):
        @spotch.marshal_list_with(modul)
        @secured
        def get(self, name):
            """ Auslesen von Modul-Objekten, die durch ihren Namen bestimmt werden.
            Die auszulesenden Objekte werden durch ```name``` in dem URI bestimmt."""

            adm = Administration()
            modul = adm.get_modul_by_edv_nummer(edv_nummer)
            return modul

# ----- Modulteil -----


@spotch.route('/Modulteil')
@spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
class ModulteilListOperations(Resource):
    """Auslesen aller Modulteil-Objekte.
    Sollten keine Modulteil-Objekte verfügbar sein, so wird eine leere Sequenz zurückgegeben."""

    @spotch.marshal_list_with(modulteil)
    @secured
    def get(self):
        adm = Administration()
        modulteile = adm.get_all_modulteile()
        return modulteile

    @spotch.marshal_with(modulteil, code=200)
    @spotch.expect(modulteil)

    def post(self):
        """Anlegen eines neuen Modulteil-Objekts.
        **ACHTUNG:** Wir fassen die vom Client gesendeten Daten als Vorschlag auf.
        So ist zum Beispiel die Vergabe der ID nicht Aufgabe des Clients.
        Selbst wenn der Client eine ID in dem Proposal vergeben sollte, so
        liegt es an der Administration (Businesslogik), eine korrekte ID
        zu vergeben. *Das korrigierte Objekt wird schließlich zurückgegeben.*
        """

        adm = Administration()
        print(api.payload)
        prpl = Modulteil.from_dict(api.payload)

        """RATSCHLAG: Prüfen Sie stets die Referenzen auf valide Werte, bevor Sie diese verwenden!"""

        if prpl is not None:
            """ Das serverseitig erzeugte Objekt ist das maßgebliche und 
            wird auch dem Client zurückgegeben. 
            """

            s = adm.create_modulteil(prpl.get_ID(),
                                          )
            return s, 200

        else:
            return '', 500


@spotch.route('/modulteil/<int:id>')
@spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
class ModulteilOperations(Resource):
    @spotch.marshal_with(Modulteil)
    @secured
    def get(self, id):
        """Auslesen eines bestimmten Modulteil-Objekts.
        Das auszulesende Objekt wird durch die ```id``` in dem URI bestimmt.
        """

        adm = Administration()
        single_modulteil = adm.get_modulteil_by_id(id)
        return single_modulteil

    @secured
    def delete(self, id):
        """Löschen eines bestimmten Modulteil-Objekts.
        Das zu löschende Objekt wird durch die ```id``` in dem URI bestimmt."""

        adm = Administration()
        modulteil = adm.get_modulteil_by_id(id)

        if modulteil is not None:

            adm.delete_modulteil(modulteil)
            return '', 200

        else:
            return '', 500

    @spotch.marshal_with(modulteil)
    @spotch.expect(modulteil, validate=True)  #Wir erwarten ein Modulteil-Objekt von Client-Seite.

    def put(self, id):
        """Update eines bestimmten Modulteil-Objekts.
        **ACHTUNG:** Relevante id ist die id, die mittels URI bereitgestellt und somit als Methodenparameter
        verwendet wird. Dieser Parameter überschreibt das ID-Attribut des im Payload der Anfrage übermittelten
        Modulteil-Objekts."""

        adm = Administration()
        modulteil = Modulteil.from_dict(api.payload)
        print('main aufruf')

        if modulteil is not None:
            """Hierdurch wird die id des zu überschreibenden (vgl. Update) Modulteil-Objekts gesetzt."""

            modulteil.set_id(id)
            adm.save_modulteil(modulteil)
            return '', 200

        else:
            return '', 500


# ----- Prüfungsformat -----


@spotch.route('/prüfungsformat')
@spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
class PrüfungsformatListOperations(Resource):
    """Auslesen aller Prüfungsformat-Objekte.
    Sollten keine Prüfungsformat-Objekte verfügbar sein, so wird eine leere Sequenz zurückgegeben."""

    @spotch.marshal_list_with(prüfungsformat)
    @secured
    def get(self):
        adm = Administration()
        prüfungsformat = adm.get_all_prüfungsformat()
        return prüfungsformat

    @spotch.marshal_with(prüfungsformat, code=200)
    @spotch.expect(prüfungsformat)
    @secured
    def post(self):
        """Anlegen eines neuen Prüfungsformat-Objekts.
        **ACHTUNG:** Wir fassen die vom Client gesendeten Daten als Vorschlag auf.
        So ist zum Beispiel die Vergabe der ID nicht Aufgabe des Clients.
        Selbst wenn der Client eine ID in dem Proposal vergeben sollte, so
        liegt es an der Administration (Businesslogik), eine korrekte ID
        zu vergeben. *Das korrigierte Objekt wird schließlich zurückgegeben.*""" #kann man Client hier lassen?

        adm = Administration()
        prpl = Prüfungsformat.from_dict(api.payload)
        """RATSCHLAG: Prüfen Sie stets die Referenzen auf valide Werte, bevor Sie diese verwenden!"""

        if prpl is not None:
            """ Das serverseitig erzeugte Objekt ist das maßgebliche und 
            wird auch dem Client zurückgegeben."""

            s = adm.create_prüfungsformat(prpl.get_ID(),
                                          prpl.get_benennung(),
                                          prpl.get_leistung())

            return s, 200

        else:
            ''' Wenn irgendetwas schiefgeht, dann geben wir nichts zurück und werfen einen Server-Fehler.'''

            return '', 500


@spotch.route('/prüfungsformat/<int:id>')
@spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
class PrüfungsformatOperations(Resource):
    @spotch.marshal_with(prüfungsformat)
    @secured
    @secured
    def get(self, id):
        """Auslesen eines bestimmten Prüfungsformat-Objekts.
        Das auszulesende Objekt wird durch die ```id``` in dem URI bestimmt."""

        adm = Administration()
        single_prüfungsformat = adm.get_prüfungsformat_by_id(id)
        return single_prüfungsformat

    @spotch.marshal_with(prüfungsformat)
    @spotch.expect(prüfungsformat, validate=True)
    @secured
    def put(self, id):
        """Update eines bestimmten Prüfungsformat-Objekts.
        **ACHTUNG:** Relevante id ist die id, die mittels URI bereitgestellt und somit als Methodenparameter
        verwendet wird. Dieser Parameter überschreibt das ID-Attribut des im Payload der Anfrage übermittelten
        Prüfungsformat-Objekts."""

        adm = Administration()
        prüfungsformat = Prüfungsformat.from_dict(api.payload)
        print('main aufruf')

        if prüfungsformat is not None:
            """Hierdurch wird die id des zu überschreibenden (vgl. Update) Prüfungsformat-Objekts gesetzt."""

            prüfungsformat.set_id(id)
            adm.save_prüfungsformat(prüfungsformat)
            return '', 200

        else:
            return '', 500

    @secured
    def delete(self, id):
        """Löschen eines bestimmten Prüfungsformat-Objekts.
        Das zu löschende Objekt wird durch die ```id``` in dem URI bestimmt."""

        adm = Administration()
        single_prüfungsformat = adm.get_prüfungsformat_by_id(id)
        adm.delete_prüfungsformat(single_prüfungsformat)
        return '', 200


    @spotch.route('/prüfungsformat-benennung/<string:benennung>')
    @spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
    class PrüfungsformatBenennungOperations(Resource):
        @spotch.marshal_list_with(prüfungsformat)
        @secured
        def get(self, benennung):
            """ Auslesen von Prüfungsformat-Objekten, die durch ihren Namen bestimmt werden.
            Die auszulesenden Objekte werden durch ```name``` in dem URI bestimmt."""

            adm = Administration()
            prüfungsformat = adm.get_prüfungsformat_benennung(benennung)
            return prüfungsformat


    @spotch.route('/prüfungsformat_leistung/<string:leistung>')
    @spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
    class PrüfungsformatLeistungOperations(Resource):
        @spotch.marshal_list_with(prüfungsformat)
        @secured
        def get(self, name):
            """ Auslesen von Prüfungsformat-Objekten, die durch ihren Namen bestimmt werden.
            Die auszulesenden Objekte werden durch ```name``` in dem URI bestimmt."""

            adm = Administration()
            prüfungsformat = adm.get_prüfungsformat_by_leistung(leistung)
            return prüfungsformat


# ------ Semester -----


@spotch.route('/semester')
@spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
class SemesterListOperations(Resource):
    """Auslesen aller Semester-Objekte.
    Sollten keine Semester-Objekte verfügbar sein, so wird eine leere Sequenz zurückgegeben."""

    @spotch.marshal_list_with(semester)
    @secured
    def get(self):
        adm = Administration()
        semester = adm.get_all_semester()
        return semester

    @spotch.marshal_with(semester, code=200)
    @spotch.expect(semester)
    @secured
    def post(self):
        """Anlegen eines neuen Semester-Objekts.
        **ACHTUNG:** Wir fassen die vom Client gesendeten Daten als Vorschlag auf.
        So ist zum Beispiel die Vergabe der ID nicht Aufgabe des Clients.
        Selbst wenn der Client eine ID in dem Proposal vergeben sollte, so
        liegt es an der Administration (Businesslogik), eine korrekte ID
        zu vergeben. *Das korrigierte Objekt wird schließlich zurückgegeben.*""" #kann man Client hier lassen?

        adm = Administration()
        prpl = Semester.from_dict(api.payload)
        """RATSCHLAG: Prüfen Sie stets die Referenzen auf valide Werte, bevor Sie diese verwenden!"""

        if prpl is not None:
            """ Das serverseitig erzeugte Objekt ist das maßgebliche und 
            wird auch dem Client zurückgegeben."""

            s = adm.create_semester(prpl.get_ID(),
                                    prpl.get_semesteranzahl())

            return s, 200

        else:
            ''' Wenn irgendetwas schiefgeht, dann geben wir nichts zurück und werfen einen Server-Fehler.'''

            return '', 500


@spotch.route('/semester/<int:id>')
@spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
class SemesteratOperations(Resource):
    @spotch.marshal_with(semester)
    @secured
    @secured
    def get(self, id):
        """Auslesen eines bestimmten Semester-Objekts.
        Das auszulesende Objekt wird durch die ```id``` in dem URI bestimmt."""

        adm = Administration()
        single_semester = adm.get_semester_by_id(id)
        return single_semester

    @spotch.marshal_with(semester)
    @spotch.expect(semester, validate=True)
    @secured
    def put(self, id):
        """Update eines bestimmten Semester-Objekts.
        **ACHTUNG:** Relevante id ist die id, die mittels URI bereitgestellt und somit als Methodenparameter
        verwendet wird. Dieser Parameter überschreibt das ID-Attribut des im Payload der Anfrage übermittelten
        Semester-Objekts."""

        adm = Administration()
        semester = Semester.from_dict(api.payload)
        print('main aufruf')

        if semester is not None:
            """Hierdurch wird die id des zu überschreibenden (vgl. Update) Semester-Objekts gesetzt."""

            semester.set_id(id)
            adm.save_semester(semester)
            return '', 200

        else:
            return '', 500

    @secured
    def delete(self, id):
        """Löschen eines bestimmten Semester-Objekts.
        Das zu löschende Objekt wird durch die ```id``` in dem URI bestimmt."""

        adm = Administration()
        single_semester = adm.get_semester_by_id(id)
        adm.delete_semester(single_semester)
        return '', 200


    @spotch.route('/semester-semesteranzahl/<string:semesteranzahl>')
    @spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
    class SemesterSemesteranzahlOperations(Resource):
        @spotch.marshal_list_with(semester)
        @secured
        def get(self, semesteranzahl):
            """ Auslesen von Semester-Objekten, die durch ihren Namen bestimmt werden.
            Die auszulesenden Objekte werden durch ```name``` in dem URI bestimmt."""

            adm = Administration()
            semester = adm.get_semester_by_semesteranzahl(semesteranzahl)
            return semester


# ----- SPO -----


@spotch.route('/spo')
@spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
class SPOListOperations(Resource):
    """Auslesen aller SPO-Objekte.
    Sollten keine SPO-Objekte verfügbar sein, so wird eine leere Sequenz zurückgegeben."""

    @spotch.marshal_list_with(spo)
    @secured
    def get(self):
        adm = Administration()
        spo = adm.get_all_spo()
        return spo

    @spotch.marshal_with(spo, code=200)
    @spotch.expect(spo)
    @secured
    def post(self):
        """Anlegen eines neuen SPO-Objekts.
        **ACHTUNG:** Wir fassen die vom Client gesendeten Daten als Vorschlag auf.
        So ist zum Beispiel die Vergabe der ID nicht Aufgabe des Clients.
        Selbst wenn der Client eine ID in dem Proposal vergeben sollte, so
        liegt es an der Administration (Businesslogik), eine korrekte ID
        zu vergeben. *Das korrigierte Objekt wird schließlich zurückgegeben.*""" #kann man Client hier lassen?

        adm = Administration()
        prpl = SPO.from_dict(api.payload)
        """RATSCHLAG: Prüfen Sie stets die Referenzen auf valide Werte, bevor Sie diese verwenden!"""

        if prpl is not None:
            """ Das serverseitig erzeugte Objekt ist das maßgebliche und 
            wird auch dem Client zurückgegeben."""

            s = adm.create_spo(prpl.get_ID(),
                               prpl.get_beginn(),
                               prpl.get_studiengang())

            return s, 200

        else:
            ''' Wenn irgendetwas schiefgeht, dann geben wir nichts zurück und werfen einen Server-Fehler.'''

            return '', 500


@spotch.route('/spo/<int:id>')
@spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
class SPOatOperations(Resource):
    @spotch.marshal_with(spo)
    @secured
    @secured
    def get(self, id):
        """Auslesen eines bestimmten SPO-Objekts.
        Das auszulesende Objekt wird durch die ```id``` in dem URI bestimmt."""

        adm = Administration()
        single_spo = adm.get_spo_by_id(id)
        return single_spo

    @spotch.marshal_with(spo)
    @spotch.expect(spo, validate=True)
    @secured
    def put(self, id):
        """Update eines bestimmten SPO-Objekts.
        **ACHTUNG:** Relevante id ist die id, die mittels URI bereitgestellt und somit als Methodenparameter
        verwendet wird. Dieser Parameter überschreibt das ID-Attribut des im Payload der Anfrage übermittelten
        SPO-Objekts."""

        adm = Administration()
        spo = SPO.from_dict(api.payload)
        print('main aufruf')

        if spo is not None:
            """Hierdurch wird die id des zu überschreibenden (vgl. Update) Semester-Objekts gesetzt."""

            spo.set_id(id)
            adm.save_spo(spo)
            return '', 200

        else:
            return '', 500

    @secured
    def delete(self, id):
        """Löschen eines bestimmten SPO-Objekts.
        Das zu löschende Objekt wird durch die ```id``` in dem URI bestimmt."""

        adm = Administration()
        single_spo = adm.get_spo(id)
        adm.delete_spo(single_spo)
        return '', 200


    @spotch.route('/spo-beginn/<string:beginn>')
    @spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
    class SPOBeginnOperations(Resource):
        @spotch.marshal_list_with(spo)
        @secured
        def get(self, beginn):
            """ Auslesen von SPO-Objekten, die durch ihren Namen bestimmt werden.
            Die auszulesenden Objekte werden durch ```name``` in dem URI bestimmt."""

            adm = Administration()
            spo = adm.get_spo_by_beginn(beginn)
            return spo


    @spotch.route('/spo-studiengang/<string:studiengang>')
    @spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
    class SPOStudiengangOperations(Resource):
        @spotch.marshal_list_with(spo)
        @secured
        def get(self, studiengang):
            """ Auslesen von SPO-Objekten, die durch ihren Namen bestimmt werden.
            Die auszulesenden Objekte werden durch ```name``` in dem URI bestimmt."""

            adm = Administration()
            spo = adm.get_spo_by_studiengang(studiengang)
            return spo


# ----- Student -----



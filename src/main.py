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
            return modul


    @spotch.route('/modul-by-sws/<string:sws>')
    @spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
    class ModulSwsOperations(Resource):
        @spotch.marshal_list_with(modul)
        @secured
        def get(self, sws):
            """ Auslesen von Modul-Objekten, die durch ihre SWS bestimmt werden.
            Die auszulesenden Objekte werden durch ```sws``` in dem URI bestimmt."""

            adm = Administration()
            modul = adm.get_modul_by_sws(sws)
            return modul


    @spotch.route('/modul-by-ects/<string:ects>')
    @spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
    class ModulEctsOperations(Resource):
        @spotch.marshal_list_with(modul)
        @secured
        def get(self, ects):
            """ Auslesen von Modul-Objekten, die durch ihre Ects bestimmt werden.
            Die auszulesenden Objekte werden durch ```ects``` in dem URI bestimmt."""

            adm = Administration()
            modul = adm.get_modul_by_ects(ects)
            return modul


    @spotch.route('/modul-by-literatur/<string:literatur>')
    @spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
    class ModulLiteraturOperations(Resource):
        @spotch.marshal_list_with(modul)
        @secured
        def get(self, literatur):
            """ Auslesen von Modul-Objekten, die durch ihre Literatur bestimmt werden.
            Die auszulesenden Objekte werden durch ```literatur``` in dem URI bestimmt."""

            adm = Administration()
            modul = adm.get_modul_by_literatur(literatur)
            return modul


    @spotch.route('/modul-by-verantwortlicher/<string:verantwortlicher>')
    @spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
    class ModulVerantwortlicherOperations(Resource):
        @spotch.marshal_list_with(modul)
        @secured
        def get(self, verantwortlicher):
            """ Auslesen von Modul-Objekten, die durch ihren Verantwortlichen bestimmt werden.
            Die auszulesenden Objekte werden durch ```verantwortlicher``` in dem URI bestimmt."""

            adm = Administration()
            modul = adm.get_modul_by_verantwortlicher(verantwortlicher)
            return modul

    @spotch.route('/modul-by-edv-nummer/<string:edv_nummer>')
    @spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
    class ModulEdvNummerOperations(Resource):
        @spotch.marshal_list_with(modul)
        @secured
        def get(self, edv_nummer):
            """ Auslesen von Modul-Objekten, die durch ihre EDV-Nummer bestimmt werden.
            Die auszulesenden Objekte werden durch ```edv_nummer``` in dem URI bestimmt."""

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


    @spotch.route('/prüfungsformat-by-benennung/<string:benennung>')
    @spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
    class PrüfungsformatBenennungOperations(Resource):
        @spotch.marshal_list_with(prüfungsformat)
        @secured
        def get(self, benennung):
            """ Auslesen von Prüfungsformat-Objekten, die durch ihre Benennung bestimmt werden.
            Die auszulesenden Objekte werden durch ```benennung``` in dem URI bestimmt."""

            adm = Administration()
            prüfungsformat = adm.get_prüfungsformat_benennung(benennung)
            return prüfungsformat


    @spotch.route('/prüfungsformat-by-leistung/<string:leistung>')
    @spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
    class PrüfungsformatLeistungOperations(Resource):
        @spotch.marshal_list_with(prüfungsformat)
        @secured
        def get(self, leistung):
            """ Auslesen von Prüfungsformat-Objekten, die durch ihre Leistung bestimmt werden.
            Die auszulesenden Objekte werden durch ```leistung``` in dem URI bestimmt."""

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


    @spotch.route('/semester-by-semesteranzahl/<string:semesteranzahl>')
    @spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
    class SemesterSemesteranzahlOperations(Resource):
        @spotch.marshal_list_with(semester)
        @secured
        def get(self, semesteranzahl):
            """ Auslesen von Semester-Objekten, die durch ihre Semesteranzahl bestimmt werden.
            Die auszulesenden Objekte werden durch ```semesteranzahl``` in dem URI bestimmt."""

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
            """Hierdurch wird die id des zu überschreibenden (vgl. Update) SPO-Objekts gesetzt."""

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


    @spotch.route('/spo-by-beginn/<string:beginn>')
    @spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
    class SPOBeginnOperations(Resource):
        @spotch.marshal_list_with(spo)
        @secured
        def get(self, beginn):
            """ Auslesen von SPO-Objekten, die durch ihren Beginn bestimmt werden.
            Die auszulesenden Objekte werden durch ```beginn``` in dem URI bestimmt."""

            adm = Administration()
            spo = adm.get_spo_by_beginn(beginn)
            return spo


    @spotch.route('/spo-by-studiengang/<string:studiengang>')
    @spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
    class SPOStudiengangOperations(Resource):
        @spotch.marshal_list_with(spo)
        @secured
        def get(self, studiengang):
            """ Auslesen von SPO-Objekten, die durch ihren Studiengang bestimmt werden.
            Die auszulesenden Objekte werden durch ```studiengang``` in dem URI bestimmt."""

            adm = Administration()
            spo = adm.get_spo_by_studiengang(studiengang)
            return spo


# ----- Student -----


@spotch.route('/student')
@spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
class StudentListOperations(Resource):
    """Auslesen aller Student-Objekte.
    Sollten keine Student-Objekte verfügbar sein, so wird eine leere Sequenz zurückgegeben."""

    @spotch.marshal_list_with(student)
    @secured
    def get(self):
        adm = Administration()
        student = adm.get_all_student()
        return student

    @spotch.marshal_with(student, code=200)
    @spotch.expect(student)
    @secured
    def post(self):
        """Anlegen eines neuen Student-Objekts.
        **ACHTUNG:** Wir fassen die vom Client gesendeten Daten als Vorschlag auf.
        So ist zum Beispiel die Vergabe der ID nicht Aufgabe des Clients.
        Selbst wenn der Client eine ID in dem Proposal vergeben sollte, so
        liegt es an der Administration (Businesslogik), eine korrekte ID
        zu vergeben. *Das korrigierte Objekt wird schließlich zurückgegeben.*""" #kann man Client hier lassen?

        adm = Administration()
        prpl = Student.from_dict(api.payload)
        """RATSCHLAG: Prüfen Sie stets die Referenzen auf valide Werte, bevor Sie diese verwenden!"""

        if prpl is not None:
            """ Das serverseitig erzeugte Objekt ist das maßgebliche und 
            wird auch dem Client zurückgegeben."""

            s = adm.create_student(prpl.get_ID(),
                                   prpl.get_google_user_id(),
                                   prpl.get_name(),
                                   prpl.get_vorname(),
                                   prpl.get_mail_adresse(),
                                   prpl.semester(),
                                   prpl.get_studiengang(),
                                   prpl.matrikelnummer()
                                   )

            return s, 200

        else:
            ''' Wenn irgendetwas schiefgeht, dann geben wir nichts zurück und werfen einen Server-Fehler.'''

            return '', 500


@spotch.route('/student/<int:id>')
@spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
class StudentatOperations(Resource):
    @spotch.marshal_with(student)
    @secured
    @secured
    def get(self, id):
        """Auslesen eines bestimmten Student-Objekts.
        Das auszulesende Objekt wird durch die ```id``` in dem URI bestimmt."""

        adm = Administration()
        single_student = adm.get_student_by_id(id)
        return single_student

    @spotch.marshal_with(student)
    @spotch.expect(student, validate=True)
    @secured
    def put(self, id):
        """Update eines bestimmten Student-Objekts.
        **ACHTUNG:** Relevante id ist die id, die mittels URI bereitgestellt und somit als Methodenparameter
        verwendet wird. Dieser Parameter überschreibt das ID-Attribut des im Payload der Anfrage übermittelten
        Student-Objekts."""

        adm = Administration()
        student = Student.from_dict(api.payload)
        print('main aufruf')

        if student is not None:
            """Hierdurch wird die id des zu überschreibenden (vgl. Update) Student-Objekts gesetzt."""

            student.set_id(id)
            adm.save_student(student)
            return '', 200

        else:
            return '', 500

    @secured
    def delete(self, id):
        """Löschen eines bestimmten Student-Objekts.
        Das zu löschende Objekt wird durch die ```id``` in dem URI bestimmt."""

        adm = Administration()
        single_student = adm.get_student(id)
        adm.delete_student(single_student)
        return '', 200


    @spotch.route('/student-by-google-user-id/<string:google_user_id>')
    @spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
    class StudentGoogleUserIdOperations(Resource):
        @spotch.marshal_list_with(student)
        @secured
        def get(self, google_user_id):
            """ Auslesen von Student-Objekten, die durch ihre Google-User-ID bestimmt werden.
            Die auszulesenden Objekte werden durch ```google_user_id``` in dem URI bestimmt."""

            adm = Administration()
            student = adm.get_student_by_google_user_id(google_user_id)
            return student


    @spotch.route('/student-by-name/<string:name>')
    @spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
    class StudentByNameOperations(Resource):
        @spotch.marshal_list_with(student)
        @secured
        def get(self, name):
            """ Auslesen von Student-Objekten, die durch ihren Namen bestimmt werden.
            Die auszulesenden Objekte werden durch ```name``` in dem URI bestimmt."""

            adm = Administration()
            student = adm.get_student_by_name(name)
            return student


    @spotch.route('/student-by-vorname/<string:vorname>')
    @spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
    class StudentByVornameOperations(Resource):
        @spotch.marshal_list_with(student)
        @secured
        def get(self, vorname):
            """ Auslesen von Student-Objekten, die durch ihren Vornamen bestimmt werden.
            Die auszulesenden Objekte werden durch ```vorname``` in dem URI bestimmt."""

            adm = Administration()
            student = adm.get_student_by_vorname(vorname)
            return student


    @spotch.route('/student-by-mail-adresse/<string:mail_adresse>')
    @spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
    class StudentByMailAdresseOperations(Resource):
        @spotch.marshal_list_with(student)
        @secured
        def get(self, mail_adresse):
            """ Auslesen von Student-Objekten, die durch ihre Mail-Adresse bestimmt werden.
            Die auszulesenden Objekte werden durch ```mail_adresse``` in dem URI bestimmt."""

            adm = Administration()
            student = adm.get_student_by_mail_adresse(mail_adresse)
            return student


    @spotch.route('/student-by-semester/<string:semester>')
    @spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
    class StudentBySemesterOperations(Resource):
        @spotch.marshal_list_with(student)
        @secured
        def get(self, semester):
            """ Auslesen von Student-Objekten, die durch ihr Semester bestimmt werden.
            Die auszulesenden Objekte werden durch ```semester``` in dem URI bestimmt."""

            adm = Administration()
            student = adm.get_student_by_semester(semester)
            return student


    @spotch.route('/student-by-studiengang/<string:studiengang>')
    @spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
    class StudentByStudiengang(Resource):
        @spotch.marshal_list_with(student)
        @secured
        def get(self, studiengang):
            """ Auslesen von Student-Objekten, die durch ihren Studiengang bestimmt werden.
            Die auszulesenden Objekte werden durch ```studiengang``` in dem URI bestimmt."""

            adm = Administration()
            student = adm.get_student_by_studiengang(studiengang)
            return student

    @spotch.route('/student-by-matrikelnummer/<string:matrikelnummer>')
    @spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
    class StudentByMatrikelnummerOperations(Resource):
        @spotch.marshal_list_with(student)
        @secured
        def get(self, matrikelnummer):
            """ Auslesen von Student-Objekten, die durch ihre Matrikelnummer bestimmt werden.
            Die auszulesenden Objekte werden durch ```matrikelnummer``` in dem URI bestimmt."""

            adm = Administration()
            student = adm.get_student_by_matrikelnummer(matrikelnummer)
            return student


# ----- Studiengang -----


@spotch.route('/studiengang')
@spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
class StudiengangListOperations(Resource):
    """Auslesen aller Studiengang-Objekte.
    Sollten keine Studiengang-Objekte verfügbar sein, so wird eine leere Sequenz zurückgegeben."""

    @spotch.marshal_list_with(studiengang)
    @secured
    def get(self):
        adm = Administration()
        studiengang = adm.get_all_studiengang()
        return studiengang

    @spotch.marshal_with(studiengang, code=200)
    @spotch.expect(studiengang)
    @secured
    def post(self):
        """Anlegen eines neuen Studiengang-Objekts.
        **ACHTUNG:** Wir fassen die vom Client gesendeten Daten als Vorschlag auf.
        So ist zum Beispiel die Vergabe der ID nicht Aufgabe des Clients.
        Selbst wenn der Client eine ID in dem Proposal vergeben sollte, so
        liegt es an der Administration (Businesslogik), eine korrekte ID
        zu vergeben. *Das korrigierte Objekt wird schließlich zurückgegeben.*""" #kann man Client hier lassen?

        adm = Administration()
        prpl = Studiengang.from_dict(api.payload)
        """RATSCHLAG: Prüfen Sie stets die Referenzen auf valide Werte, bevor Sie diese verwenden!"""

        if prpl is not None:
            """ Das serverseitig erzeugte Objekt ist das maßgebliche und 
            wird auch dem Client zurückgegeben."""

            s = adm.create_studiengang(prpl.get_ID(),
                                       prpl.get_module(),
                                       prpl.get_semester(),
                                       prpl.get_name())

            return s, 200

        else:
            ''' Wenn irgendetwas schiefgeht, dann geben wir nichts zurück und werfen einen Server-Fehler.'''

            return '', 500


@spotch.route('/studiengang/<int:id>')
@spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
class StudiengangatOperations(Resource):
    @spotch.marshal_with(studiengang)
    @secured
    @secured
    def get(self, id):
        """Auslesen eines bestimmten Studiengang-Objekts.
        Das auszulesende Objekt wird durch die ```id``` in dem URI bestimmt."""

        adm = Administration()
        single_studiengang = adm.get_studiengang_by_id(id)
        return single_studiengang

    @spotch.marshal_with(studiengang)
    @spotch.expect(studiengang, validate=True)
    @secured
    def put(self, id):
        """Update eines bestimmten Studiengang-Objekts.
        **ACHTUNG:** Relevante id ist die id, die mittels URI bereitgestellt und somit als Methodenparameter
        verwendet wird. Dieser Parameter überschreibt das ID-Attribut des im Payload der Anfrage übermittelten
        Studiengang-Objekts."""

        adm = Administration()
        studiengang = Studiengang.from_dict(api.payload)
        print('main aufruf')

        if studiengang is not None:
            """Hierdurch wird die id des zu überschreibenden (vgl. Update) Studiengang-Objekts gesetzt."""

            studiengang.set_id(id)
            adm.save_studiengang(studiengang)
            return '', 200

        else:
            return '', 500

    @secured
    def delete(self, id):
        """Löschen eines bestimmten Studiengang-Objekts.
        Das zu löschende Objekt wird durch die ```id``` in dem URI bestimmt."""

        adm = Administration()
        single_studiengang = adm.get_studiengang(id)
        adm.delete_studiengang(single_studiengang)
        return '', 200


    @spotch.route('/studiengang-by-module/<string:module>')
    @spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
    class StudiengangModuleOperations(Resource):
        @spotch.marshal_list_with(studiengang)
        @secured
        def get(self, module):
            """ Auslesen von Studiengang-Objekten, die durch ihre Module bestimmt werden.
            Die auszulesenden Objekte werden durch ```module``` in dem URI bestimmt."""

            adm = Administration()
            studiengang = adm.get_studiengang_by_module(module)
            return studiengang


    @spotch.route('/studiengang-by-semester/<string:semester>')
    @spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
    class StudiengangSemesterOperations(Resource):
        @spotch.marshal_list_with(studiengang)
        @secured
        def get(self, semester):
            """ Auslesen von Studiengang-Objekten, die durch ihr Semester bestimmt werden.
            Die auszulesenden Objekte werden durch ```semester``` in dem URI bestimmt."""

            adm = Administration()
            studiengang = adm.get_studiengang_by_semester(semester)
            return studiengang

    @spotch.route('/studiengang-by-name/<string:name>')
    @spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
    class StudiengangModuleOperations(Resource):
        @spotch.marshal_list_with(studiengang)
        @secured
        def get(self, name):
            """ Auslesen von Studiengang-Objekten, die durch ihren Namen bestimmt werden.
            Die auszulesenden Objekte werden durch ```name``` in dem URI bestimmt."""

            adm = Administration()
            studiengang = adm.get_studiengang_by_name(name)
            return studiengang


# ----- Verwaltungsmitarbeiter -----


@spotch.route('/verwaltungsmitarbeiter')
@spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
class VerwaltungsmitarbeiterListOperations(Resource):
    """Auslesen aller Verwaltungsmitarbeiter-Objekte.
    Sollten keine Verwaltungsmitarbeiter-Objekte verfügbar sein, so wird eine leere Sequenz zurückgegeben."""

    @spotch.marshal_list_with(verwaltungsmitarbeiter)
    @secured
    def get(self):
        adm = Administration()
        verwaltungsmitarbeiter = adm.get_all_verwaltungsmitarbeiter()
        return verwaltungsmitarbeiter

    @spotch.marshal_with(verwaltungsmitarbeiter, code=200)
    @spotch.expect(verwaltungsmitarbeiter)
    @secured
    def post(self):
        """Anlegen eines neuen Verwaltungsmitarbeiter-Objekts.
        **ACHTUNG:** Wir fassen die vom Client gesendeten Daten als Vorschlag auf.
        So ist zum Beispiel die Vergabe der ID nicht Aufgabe des Clients.
        Selbst wenn der Client eine ID in dem Proposal vergeben sollte, so
        liegt es an der Administration (Businesslogik), eine korrekte ID
        zu vergeben. *Das korrigierte Objekt wird schließlich zurückgegeben.*""" #kann man Client hier lassen?

        adm = Administration()
        prpl = Verwaltungsmitarbeiter.from_dict(api.payload)
        """RATSCHLAG: Prüfen Sie stets die Referenzen auf valide Werte, bevor Sie diese verwenden!"""

        if prpl is not None:
            """ Das serverseitig erzeugte Objekt ist das maßgebliche und 
            wird auch dem Client zurückgegeben."""

            s = adm.create_verwaltungsmitarbeiter(prpl.get_ID(),
                                                  prpl.get_name(),
                                                  prpl.get_vorname(),
                                                  prpl.get_email(),
                                                  prpl.get_passwort())

            return s, 200

        else:
            ''' Wenn irgendetwas schiefgeht, dann geben wir nichts zurück und werfen einen Server-Fehler.'''

            return '', 500


@spotch.route('/verwaltungsmitarbeiter/<int:id>')
@spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
class VerwaltungsmitarbeiteratOperations(Resource):
    @spotch.marshal_with(verwaltungsmitarbeiter)
    @secured
    @secured
    def get(self, id):
        """Auslesen eines bestimmten Verwaltungsmitarbeiter-Objekts.
        Das auszulesende Objekt wird durch die ```id``` in dem URI bestimmt."""

        adm = Administration()
        single_verwaltungsmitarbeiter = adm.get_verwaltungsmitarbeiter_by_id(id)
        return single_verwaltungsmitarbeiter

    @spotch.marshal_with(verwaltungsmitarbeiter)
    @spotch.expect(verwaltungsmitarbeiter, validate=True)
    @secured
    def put(self, id):
        """Update eines bestimmten Verwaltungsmitarbeiter-Objekts.
        **ACHTUNG:** Relevante id ist die id, die mittels URI bereitgestellt und somit als Methodenparameter
        verwendet wird. Dieser Parameter überschreibt das ID-Attribut des im Payload der Anfrage übermittelten
        Verwaltungsmitarbeiter-Objekts."""

        adm = Administration()
        verwaltungsmitarbeiter = Verwaltungsmitarbeiter.from_dict(api.payload)
        print('main aufruf')

        if verwaltungsmitarbeiter is not None:
            """Hierdurch wird die id des zu überschreibenden (vgl. Update) Verwaltungsmitarbeiter-Objekts gesetzt."""

            verwaltungsmitarbeiter.set_id(id)
            adm.save_verwaltungsmitarbeiter(verwaltungsmitarbeiter)
            return '', 200

        else:
            return '', 500

    @secured
    def delete(self, id):
        """Löschen eines bestimmten Verwaltungsmitarbeiter-Objekts.
        Das zu löschende Objekt wird durch die ```id``` in dem URI bestimmt."""

        adm = Administration()
        single_verwaltungsmitarbeiter = adm.get_verwaltungsmitarbeiter(id)
        adm.delete_verwaltungsmitarbeiter(single_verwaltungsmitarbeiter)
        return '', 200


    @spotch.route('/verwaltungsmitarbeiter-by-name/<string:name>')
    @spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
    class VerwaltungsmitarbeiterNameOperations(Resource):
        @spotch.marshal_list_with(verwaltungsmitarbeiter)
        @secured
        def get(self, name):
            """ Auslesen von Verwaltungsmitarbeiter-Objekten, die durch ihren Namen bestimmt werden.
            Die auszulesenden Objekte werden durch ```name``` in dem URI bestimmt."""

            adm = Administration()
            verwaltungsmitarbeiter = adm.get_verwaltungsmitarbeiter_by_name(name)
            return verwaltungsmitarbeiter


    @spotch.route('/verwaltungsmitarbeiter-by-vorname/<string:vorname>')
    @spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
    class VerwaltungsmitarbeiterVornameOperations(Resource):
        @spotch.marshal_list_with(verwaltungsmitarbeiter)
        @secured
        def get(self, vorname):
            """ Auslesen von Verwaltungsmitarbeiter-Objekten, die durch ihren Vornamen bestimmt werden.
            Die auszulesenden Objekte werden durch ```vorname``` in dem URI bestimmt."""

            adm = Administration()
            verwaltungsmitarbeiter = adm.get_verwaltungsmitarbeiter_by_vorname(vorname)
            return verwaltungsmitarbeiter


    @spotch.route('/verwaltungsmitarbeiter-by-email/<string:email>')
    @spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
    class VerwaltungsmitarbeiterEmailOperations(Resource):
        @spotch.marshal_list_with(verwaltungsmitarbeiter)
        @secured
        def get(self, email):
            """ Auslesen von Verwaltungsmitarbeiter-Objekten, die durch ihre Email bestimmt werden.
            Die auszulesenden Objekte werden durch ```email``` in dem URI bestimmt."""

            adm = Administration()
            verwaltungsmitarbeiter = adm.get_verwaltungsmitarbeiter_by_email(email)
            return verwaltungsmitarbeiter


    @spotch.route('/verwaltungsmitarbeiter-by-passwort/<string:passwort>')
    @spotch.response(500, 'Wenn ein Server-seitiger Fehler aufkommt')
    class VerwaltungsmitarbeiterPasswortOperations(Resource):
        @spotch.marshal_list_with(verwaltungsmitarbeiter)
        @secured
        def get(self, passwort):
            """ Auslesen von Verwaltungsmitarbeiter-Objekten, die durch ihr Passwort bestimmt werden.
            Die auszulesenden Objekte werden durch ```passwort``` in dem URI bestimmt."""

            adm = Administration()
            verwaltungsmitarbeiter = adm.get_verwaltungsmitarbeiter_by_passwort(passwort)
            return verwaltungsmitarbeiter

if __name__ == '__main__':
    app.run(debug=True)

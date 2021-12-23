from flask import Flask
# Auf Flask aufbauend nutzen wir RestX
from flask_restx import Api, Resource, fields
# Wir benutzen noch eine Flask-Erweiterung für Cross-Origin Resource Sharing
from flask_cors import CORS

from src.server.Administration import Administration
from src.server.bo.Modul import Modul
"""test Commit"""



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
          description='Eine App zum auffinden von Lernpartnern und Lerngruppen.')

"""Anlegen eines Namespace
Namespaces erlauben uns die Strukturierung von APIs. In diesem Fall fasst dieser Namespace alle
studyFix-relevanten Operationen unter dem Präfix /studyfix zusammen."""

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
    'edv_nummer': fields.Integer(attribute='_edv_nummer', description='edv_nummer eines moduls')
})
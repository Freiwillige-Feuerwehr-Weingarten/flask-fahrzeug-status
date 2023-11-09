from flask import Flask, render_template
from datetime import datetime
import psycopg2
import json

app = Flask(__name__)
app.config.from_file('config.json', load=json.load)


def get_vehicle_status(vehicle):
    connection = psycopg2.connect(database=app.config['DB_NAME'],
                                  host=app.config['DB_HOST'],
                                  user=app.config['DB_USER'],
                                  password=app.config['DB_PASSWORD'],
                                  port=app.config['DB_PORT'])
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT fahrzeug_status.status FROM fahrzeug_status, fahrzeuge WHERE fahrzeug_status.issi = fahrzeuge.issi AND fahrzeuge.funkrufname = '%s' ORDER BY timestamp DESC LIMIT 1" %vehicle)
    except (Exception, psycopg2.DatabaseError) as error:
        return "Nicht bekannt"
    records = cursor.fetchone()
    cursor.close()
    connection.close()
    if not records:
        return "Nicht bekannt"
    else: 
        return records[0]

@app.route('/')
def index():
    return render_template("index.html",
                           status10=get_vehicle_status(10),
                           status11=get_vehicle_status(11),
                           status23=get_vehicle_status(23),
                           status33=get_vehicle_status(33),
                           status441=get_vehicle_status(441),
                           status442=get_vehicle_status(442),
                           status50=get_vehicle_status(50),
                           status52=get_vehicle_status(52),
                           status56=get_vehicle_status(56),
                           status591=get_vehicle_status(591),
                           status73=get_vehicle_status(73),
                           status191=get_vehicle_status(191),
                           status192=get_vehicle_status(192))


@app.route('/status/<vehicle>')
def status(vehicle):
    connection = psycopg2.connect(database=app.config['DB_NAME'],
                        host=app.config['DB_HOST'],
                        user=app.config['DB_USER'],
                        password=app.config['DB_PASSWORD'],
                        port=app.config['DB_PORT'])
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM fahrzeug_status, fahrzeuge WHERE fahrzeug_status.issi = fahrzeuge.issi AND fahrzeuge.funkrufname = '%s' ORDER BY timestamp DESC" %vehicle)
    records = cursor.fetchall()
    cursor.close()
    connection.close()
    # records = {}
    return render_template("fahrzeug.html", vehicle=vehicle, records=records)

if __name__ == "__main__":
    app.run(host='0.0.0.0, port=5000')
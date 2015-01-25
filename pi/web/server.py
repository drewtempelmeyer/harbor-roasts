from datetime import datetime
from flask import (Flask, redirect, render_template, request, make_response,
    jsonify, url_for)
from flask.ext.sqlalchemy import SQLAlchemy
from temperature_client import TemperatureClient

###
# Configuration
###
# Temperature server (see pi/temp-server/server.py)
TEMP_SERVER_HOST = '127.0.0.1'
TEMP_SERVER_PORT = 8888

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///roasts.db'
db = SQLAlchemy(app)
temperature_client = TemperatureClient(TEMP_SERVER_HOST, TEMP_SERVER_PORT)

###
# Models
###
class Roast(db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    beans        = db.Column(db.String(100))
    weight       = db.Column(db.Integer)
    roaster      = db.Column(db.String(50))
    duration     = db.Column(db.Numeric(5, 2))
    start_at     = db.Column(db.DateTime(True))
    end_at       = db.Column(db.DateTime(True))
    first_crack  = db.Column(db.DateTime(True))
    second_crack = db.Column(db.DateTime(True))
    synced       = db.Column(db.Boolean)

    def __init__(self, beans, weight, roaster, duration):
        self.beans    = beans
        self.weight   = weight
        self.roaster  = roaster
        self.duration = duration
        self.start_at = datetime.utcnow()
        self.synced   = False

class TemperatureReading(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    farenheight = db.Column(db.Numeric(6, 2))
    log_date    = db.Column(db.DateTime(True))
    roast_id    = db.Column(db.Integer, db.ForeignKey('roast.id'))

    roast = db.relationship('Roast',
        backref=db.backref('temperature_readings', lazy='dynamic'))

    def __init__(self, roast_id, farenheight):
        self.roast_id    = roast_id
        self.farenheight = farenheight

@app.route('/')
def new_roast():
    """Prompt for beans, roaster's name, and weight"""
    return render_template('new_roast.html')

@app.route('/', methods=['POST'])
def create_roast():
    form  = request.form
    roast = Roast(form.get('beans'), form.get('weight'), form.get('roaster'),
            form.get('duration'))

    # Add the Roast to the database
    db.session.add(roast)
    db.session.commit()

    # Redirect to the current roast
    return redirect(url_for('.current_roast'))

@app.route('/current')
def current_roast():
    roast = Roast.query.filter(Roast.end_at == None).first()

    if roast == None:
        return redirect(url_for('.new_roast'))

    return render_template('current.html', roast=roast)

@app.route('/current-temperature')
def current_temperature():
    reading = temperature_client.get()
    return make_response(jsonify(reading))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

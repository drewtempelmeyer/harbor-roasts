from datetime import datetime
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

###
# Configuration
###
# Temperature server (see pi/temp-server/server.py)
TEMP_SERVER_HOST = '127.0.0.1'
TEMP_SERVER_PORT = 8888

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://roasts.db'
db = SQLAlchemy(app)

###
# Models
###
class Roast(db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    beans        = db.Column(db.String(100))
    weight       = db.Column(db.Integer)
    roaster      = db.Column(db.String(50))
    start_at     = db.Column(db.DateTime(True))
    end_at       = db.Column(db.DateTime(True))
    first_crack  = db.Column(db.DateTime(True))
    second_crack = db.Column(db.DateTime(True))
    synced       = db.Column(db.Boolean)

    def __init__(self, beans, weight, roaster):
        self.beans    = beans
        self.weight   = weight
        self.roaster  = roaster
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
def bean_prompt():
    """Prompt for beans, roaster's name, and weight"""
    return 'sleeping'

@app.route('/current')
def current_roast():
    """Display information regarding the current roast"""
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

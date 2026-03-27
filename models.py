from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class RideRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    passenger_name = db.Column(db.String(100))
    pickup_location = db.Column(db.String(200))
    destination = db.Column(db.String(200))
    status = db.Column(db.String(20), default='Pending') # Pending, Accepted, Completed
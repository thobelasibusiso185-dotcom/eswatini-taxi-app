from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# Replace this with your actual database connection string if you have one
app.config['SQLALCHEMY_DATABASE_DATABASE_URI'] = 'sqlite:///sureride.db' 
db = SQLAlchemy(app)

# --- STEP 1: THE USER MODEL ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(10), default='passenger') # passenger or driver

    # This hashes the password for security
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

# This line actually creates the table in your database file
with app.app_context():
    db.create_all()
# ------------------------------

@app.route('/')
def home():
    return jsonify({"message": "SureRide API is Online"})

if __name__ == '__main__':
    app.run(debug=True)

class RideRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    passenger_name = db.Column(db.String(100))
    pickup_location = db.Column(db.String(200))
    destination = db.Column(db.String(200))
    status = db.Column(db.String(20), default='Pending') # Pending, Accepted, Completed

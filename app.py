from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)

# --- CONFIGURATION ---
# Use an environment variable for the database URL if available (better for production)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///sureride.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- MODELS ---

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(10), default='passenger') # passenger or driver
    
    # Relationship to link rides to users
    rides = db.relationship('Ride', backref='passenger', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Ride(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    passenger_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pickup_address = db.Column(db.String(255), nullable=False)
    dropoff_address = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), default='requested') # requested, accepted, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Initialize the database
with app.app_context():
    db.create_all()

# --- ROUTES ---

@app.route('/')
def home():
    return jsonify({"status": "online", "message": "SureRide Eswatini API is active"})

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or 'phone_number' not in data or 'password' not in data:
        return jsonify({"status": "error", "message": "Missing fields"}), 400

    if User.query.filter_by(phone_number=data['phone_number']).first():
        return jsonify({"status": "error", "message": "Phone number already exists"}), 400

    new_user = User(
        full_name=data.get('full_name', 'Anonymous'),
        phone_number=data['phone_number']
    )
    new_user.set_password(data['password'])
    
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"status": "success", "message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(phone_number=data.get('phone_number')).first()

    if user and user.check_password(data.get('password')):
        return jsonify({
            "status": "success",
            "message": f"Welcome, {user.full_name}",
            "user": {
                "id": user.id,
                "full_name": user.full_name,
                "user_type": user.user_type
            }
        }), 200
    return jsonify({"status": "error", "message": "Invalid credentials"}), 401

@app.route('/request-ride', methods=['POST'])
def request_ride():
    data = request.get_json()
    try:
        new_ride = Ride(
            passenger_id=data['user_id'],
            pickup_address=data['pickup_address'],
            dropoff_address=data.get('dropoff_address', 'Not Specified')
        )
        db.session.add(new_ride)
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": "Ride request received!",
            "ride_id": new_ride.id
        }), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Use port from environment (Render requirement)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

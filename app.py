from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# --- FIX: Ensure the key is exactly SQLALCHEMY_DATABASE_URI ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sureride.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- STEP 1: THE USER MODEL ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(10), default='passenger')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Create tables
with app.app_context():
    db.create_all()

# --- STEP 2: THE ROUTES ---
@app.route('/')
def home():
    return jsonify({"message": "SureRide API is Online"})

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validation
    if not data or 'phone_number' not in data or 'password' not in data:
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    if User.query.filter_by(phone_number=data['phone_number']).first():
        return jsonify({"status": "error", "message": "Phone number already registered"}), 400

    try:
        new_user = User(
            full_name=data.get('full_name', 'Unnamed User'),
            phone_number=data['phone_number']
        )
        new_user.set_password(data['password'])

        db.session.add(new_user)
        db.session.commit()
        return jsonify({"status": "success", "message": "User registered successfully!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

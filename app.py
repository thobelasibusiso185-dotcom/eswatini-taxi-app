from flask import Flask, request, jsonify
from models import db, RideRequest

app = Flask(__name__)
@app.route('/')
def home():
    return "<h1>SureRide API is Online</h1><p>The backend is working perfectly!</p>"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sureride.db' # This creates a local database file
db.init_app(app)

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/book', methods=['POST'])
def book_ride():
    data = request.json
    new_ride = RideRequest(
        passenger_name=data['name'],
        pickup_location=data['pickup'],
        destination=data['destination']
    )
    db.session.add(new_ride)
    db.session.commit()
    return jsonify({"message": "Ride booked successfully!", "ride_id": new_ride.id})
    @app.route('/register', methods=['POST'])
def register():
    # 1. Get the JSON data from the request
    data = request.get_json()
    
    # 2. Extract the info (name, phone, password)
    full_name = data.get('name')
    phone = data.get('phone')
    password = data.get('password')

    # 3. Basic Validation
    if not full_name or not phone or not password:
        return jsonify({"error": "Missing required fields"}), 400

    # 4. Check if the phone number already exists in the DB
    existing_user = User.query.filter_by(phone_number=phone).first()
    if existing_user:
        return jsonify({"error": "This phone number is already registered"}), 409

    # 5. Create the new User object
    new_user = User(
        full_name=full_name,
        phone_number=phone
    )
    
    # 6. Hash the password (never store it as plain text!)
    new_user.set_password(password)

    # 7. Save to the database
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            "message": "Registration successful!",
            "user_id": new_user.id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Database error, please try again later"}), 500

if __name__ == "__main__":
    app.run(debug=True)

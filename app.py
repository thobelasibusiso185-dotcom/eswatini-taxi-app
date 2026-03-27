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

if __name__ == "__main__":
    app.run(debug=True)

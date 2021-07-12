from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import phonenumbers
from sqlalchemy_utils import PhoneNumberType
from sqlalchemy.orm import relationship

class TimestampMixin(object):
    created_timestamp = db.Column(
        db.DateTime, default=datetime.utcnow)

# Create our database model
class User(db.Model, TimestampMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(PhoneNumberType(), unique=True, nullable=False)
    first_name = db.Column(db.String(18), nullable=False)
    last_name = db.Column(db.String(18), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_driver = db.Column(db.Boolean)

    def __init__(self, phone_number, first_name, last_name, email, is_driver):
        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_driver = is_driver

    # Create password hashing function
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class PickUpLocations(db.Model, TimestampMixin):

    __tablename__ = 'pickup_locations'
    id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(120), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def __init__(self, location_name):
        self.location_name = location_name

class DropOffLocations(db.Model, TimestampMixin):

    __tablename__ = 'dropoff_locations'
    id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(120), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def __init__(self, location_name):
        self.location_name = location_name


class Trips(db.Model, TimestampMixin):
    __tablename__ = 'trips'
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column('driver_id', db.Integer, db.ForeignKey('users.id'), nullable = False)
    car_id = db.Column('car_id', db.Integer, db.ForeignKey('cars.id'), unique = True, nullable = False)
    time_started = db.Column(db.DateTime(timezone=True))
    pickup = db.Column(db.String(120), nullable=False)
    destination = db.Column(db.String(120), nullable=False)
    qr_string = db.Column(db.String(18), nullable=False)
    session_id = db.Column(db.String(20), nullable=False)
    passenger = relationship("Passengers", cascade="all, delete")
    active = db.Column(db.Boolean, nullable=False)

    def __init__(self, driver_id, car_id, pickup, destination, qr_string, session_id):
        self.driver_id = driver_id
        self.car_id = car_id
        self.time_started = datetime.now()
        self.pickup = pickup
        self.destination = destination
        self.qr_string = qr_string
        self.session_id = session_id
        self.active = False;

class TripHistory(db.Model, TimestampMixin):
    __tablename__ = 'trip_history'
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column('driver_id', db.Integer, nullable = False)
    car_id = db.Column('car_id', db.Integer, nullable = False)
    time_started = db.Column(db.DateTime(timezone=True))
    time_ended = db.Column(db.DateTime(timezone=True))
    pickup = db.Column(db.String(120), nullable=False)
    destination = db.Column(db.String(120), nullable=False)
    active = active = db.Column(db.Boolean, nullable=False)

    def __init__(self, driver_id, car_id, pickup, destination, time_started, active):
        self.driver_id = driver_id
        self.car_id = car_id
        self.time_started = time_started
        self.time_ended = datetime.now()
        self.pickup = pickup
        self.destination = destination
        self.active = active

class Passengers(db.Model, TimestampMixin):
    __tablename__ = 'passengers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False, unique = True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable = False)

    def __init__(self, passenger_id, trip_id):
        self.user_id = passenger_id
        self.trip_id = trip_id

class PassengerHistory(db.Model, TimestampMixin):
    __tablename__ = 'passenger_history'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable = False)
    trip_id = db.Column(db.Integer, nullable = False)

    def __init__(self, passenger_id, trip_id):
        self.user_id = passenger_id
        self.trip_id = trip_id

class Cars(db.Model, TimestampMixin):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True)
    qr_string = db.Column(db.String(18), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    car_make = db.Column(db.String(18), nullable=False)
    car_year = db.Column(db.Integer, nullable=False)
    license_plate = db.Column(db.String(8), nullable=False)
    ezpass_tag = db.Column(db.String(18), nullable=False)


    def __init__(self, qr_string, owner_id, car_make, car_year, license_plate, ezpass_tag):
        self.qr_string = qr_string
        self.owner_id = owner_id
        self.car_make = car_make
        self.car_year = car_year
        self.license_plate = license_plate
        self.ezpass_tag = ezpass_tag

from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import phonenumbers
from sqlalchemy_utils import PhoneNumberType

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

    __tablename__ = 'pickuplocations'
    id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(120), nullable=False)

    def __init__(self, location_name):
        self.location_name = location_name

    def get_list(self):


class DropOffLocations(db.Model, TimestampMixin):

    __tablename__ = 'dropofflocations'
    id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(120), nullable=False)

    def __init__(self, location_name):
        self.location_name = location_name

    def get_list(self):


class Trips(db.Model, TimestampMixin):
    __tablename__ = 'trips'
    id = db.Column(db.Integer, primary_key=True)
    time_ended = db.Column(db.DateTime(timezone=True))
    rider = db.Column('user_id', db.Integer, db.ForeignKey('users.id'), nullable = False)
    car = db.Column('car_id', db.Integer, db.ForeignKey('cars.id'), nullable = False)

    def __init__(self, time_ended, rider, car):
        self.time_ended = time_ended
        self.rider = rider
        self.car = car

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

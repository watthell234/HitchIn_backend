from app import db
from datetime import datetime

# carpools = db.Table('carpool',
#     db.Column('car_id', db.Integer, db.ForeignKey('cars.id'), primary_key=True),
#     db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
# )

class TimestampMixin(object):
    created_timestamp = db.Column(
        db.DateTime, default=datetime.utcnow)

# Create our database model
class User(db.Model, TimestampMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.Integer, unique=True, nullable=False)
    first_name = db.Column(db.String(18), nullable=False)
    last_name = db.Column(db.String(18), nullable=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(64), unique=False)
    is_driver = db.Column(db.Boolean)

    def __init__(self, phone_number, first_name, last_name, email, password):
        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password


class Trips(db.Model, TimestampMixin):
    __tablename__ = 'trips'
    id = db.Column(db.Integer, primary_key=True)
    time_ended = db.Column(db.DateTime(timezone=True))
    rider = db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
    # carpools = db.relationship('Cars', secondary=carpools, backref=db.backref('carpool', lazy=True))
    car = db.Column('car_id', db.Integer, db.ForeignKey('cars.id'), primary_key=True)

    def __init__(self, id, time_ended,):
        self.id = id
        self.time_ended = time_ended

class Cars(db.Model, TimestampMixin):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True)
    qr_string = db.Column(db.String(18), nullable=False)
    # owner_id = db.Column(db.String(18), db.ForeignKey('users.email'))
    # car_make = db.Column(db.String(18), nullable=False)
    # car_year = db.Column(db.Integer, nullable=False)


    def __init__(self, id, qr_string):
        self.id = id
        self.qr_string = qr_string

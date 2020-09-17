from flask import Flask, request, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random
import string

from flask_heroku import Heroku

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/hitchin'
heroku = Heroku(app)
db = SQLAlchemy(app)

from models import *

@app.route("/")
def index():
    return "<h1>Welcome to HitchIn</h1>"


@app.route("/sign-up", methods=['POST'])
def sign_up():
    phone_number = request.json.get('phoneNumber', None)
    first_name = request.json.get('firstName', None)
    last_name = request.json.get('lastName', None)
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    is_driver = request.json.get('checked', None)

    if not db.session.query(User).filter(User.phone_number == phone_number).first():
        new_user = User(phone_number, first_name, last_name, email, is_driver)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        created_id = db.session.query(User).order_by(User.created_timestamp.desc()).first()
        return jsonify({
            'status': '200',
            'message': 'Successfully Signed Up',
            'id': str(created_id.id)
        })
    else:
        abort(401)


@app.route("/login", methods=['POST'])
def login():
    phone_number = request.json.get('phoneNumber', None)
    password = request.json.get('password', None)
    user = db.session.query(User).filter(User.phone_number == phone_number).first()
    print(user.id)
    if user and user.check_password(password):
        return jsonify({
            'status': '200',
            'message': 'Successfully Logged in',
            'id': str(user.id)
        })
    else:
        abort(403)


@app.route("/car", methods=['POST'])
def create_car():
    owner_id = request.json.get('userId', None)
    letters = string.ascii_letters
    qr_string = ''.join(random.choice(letters) for i in range(18))
    car_make = request.json.get('carMake', None)
    car_year = request.json.get('carYear', None)
    license_plate = request.json.get('licensePlate', None)
    ezpass_tag = request.json.get('ezpassTag', None)

    car = Cars(qr_string, owner_id, car_make, car_year, license_plate, ezpass_tag)
    db.session.add(car)
    db.session.commit()
    created_car_id = db.session.query(Cars).order_by(Cars.created_timestamp.desc()).first()
    return jsonify({
        'status': '200',
        'message': 'Successfully registered car',
        'id': str(created_car_id.id),
        'qr_id': qr_string
    })


@app.route("/checkin", methods=['POST'])
def checkin():
    car_qr = request.json.get('carQr', None)
    # try:
    logged_car = db.session.query(Cars).filter(Cars.qr_string == car_qr).first()
    print(logged_car.id)
    checkin = Trips(time_ended == null, rider == 19, car == car.id)
    db.session.add(checkin)
    db.session.commit()
    return jsonify({
        'status': '200',
        'message': 'Successfully sluggin'
    })
    # except:
    #     abort(404)


@app.route("/cartrips/<int:car_id>", methods=['GET', 'PUT'])
def pool_count(car_id):

    if request.method == 'GET':

        passng_checked = (db.session.query(Trips).filter(Trips.car == car_id, Trips.time_ended == None)
                 .all())
        passenger_count = len(passng_checked)
        return jsonify({
            'status': '200',
            'car_id': car_id,
            'slugs': passenger_count
        })
    # if request.method == 'PUT':
    #     slugs = db.session.query(Slug).filter(Slug.slug_id == slug_id, Slug.time_ended == None).all(
    #     ).update().values({Slug.time_ended: datetime.utcnow})
    #     db.session.commit()
    #     return jsonify({
    #         'status': '200'
    #     })


if __name__ == '__main__':
    app.debug = True
    app.run()

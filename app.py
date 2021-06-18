from datetime import datetime
import random
import string
import requests

from flask import Flask, request, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt import JWT, jwt_required, current_identity
from flask_socketio import SocketIO, send, emit, join_room, leave_room, close_room, rooms, disconnect
from flask_heroku import Heroku

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://127.0.0.1/hitchin'
heroku = Heroku(app)
db = SQLAlchemy(app)

from models import *

# Authentication
def authenticate(phoneNumber, password):

    user = db.session.query(User).filter(User.phone_number == phoneNumber).first()
    if user and user.check_password(password):
        return user

def identity(payload):
    user_id = payload['identity']
    return db.session.query(User).filter(User.id == user_id).scalar()

jwt = JWT(app, authenticate, identity)

#Socket
socketio = SocketIO(app)

# HTTP Routes
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

    if not (email_exists(email) or phone_number_exists(phone_number)):

        new_user = User(phone_number, first_name, last_name, email, is_driver)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        created_user = db.session.query(User).filter(User.phone_number == phone_number).scalar()
        request_token = requests.post('https://hitchin-server.herokuapp.com/auth',
                    json={"username": str(phone_number), "password": password})
        # request_token = requests.post('http://127.0.0.1:5000/auth',
        #             json={"username": str(phone_number), "password": password})

        return jsonify({
            'status': '200',
            'message': 'Successfully Signed Up',
            'id': str(created_user.id),
            'auth_token': request_token.json()['access_token']
        })
    else:
        abort(401)

def email_exists(email):

    exists = False
    email_exists = db.session.query(User).filter(User.email == email).scalar()

    if email_exists:
        exists = True

    return exists

def phone_number_exists(phone_number):

    exists = False
    phone_number_exists = db.session.query(User).filter(User.phone_number == phone_number).scalar()

    if phone_number_exists:
        exists = True

    return exists

#return pickup spots and dropoff spots in two lists in json
@app.route("/routes", methods=['GET'])
def get_routes():
    pickup_list = []
    dropoff_list = []
    pickup_rows = db.session.query(PickUpLocations).all()
    dropoff_rows = db.session.query(DropOffLocations).all()

    for pickup in pickup_rows:
        pickup_list.append(pickup.location_name)

    for dropoff in dropoff_rows:
        dropoff_list.append(dropoff.location_name)

    return jsonify({
        'status': '200',
        'pickup_list': pickup_list,
        'dropoff_list': dropoff_list
    })

@app.route("/car_list", methods=['POST'])
def get_car_list():

    owner_id = request.json.get('userID', None)

    car_list = []
    car_rows = db.session.query(Cars).filter(Cars.owner_id == owner_id).all()

    #only returns license plate for now
    for car in car_rows:
        car_list.append({"car_id": car.id, "license_plate": car.license_plate})

    return jsonify({
        'status': '200',
        'car_list': car_list
    })


@app.route("/login", methods=['POST'])
def login():
    phone_number = request.json.get('phoneNumber', None)
    password = request.json.get('password', None)
    #Check if the phone number exists first.
    if phone_number_exists(phone_number):
        #Now authenticate.
        logged_user = authenticate(phone_number, password)

        request_token = requests.post('https://hitchin-server.herokuapp.com/auth',
            json={"username": str(phone_number), "password": password})

        # request_token = requests.post('http://127.0.0.1:5000/auth',
        #     json={"username": str(phone_number), "password": password})

        if logged_user:
            return jsonify({
                'status': '200',
                'message': 'Successfully Logged in',
                'id': logged_user.id,
                'auth_token': request_token.json()['access_token']
            })
        #if authentication fails, abort with 403.
        else:
            abort(403)
    #if phone_number doesn't exist, abort with 401.
    else:
        abort(401)


@app.route("/create_car", methods=['POST'])
@jwt_required()
def create_car():

    letters = string.ascii_letters
    qr_string = ''.join(random.choice(letters) for i in range(18))
    owner_id = request.json.get('userID', None)
    car_maker = request.json.get('car_maker', None)
    car_year = request.json.get('car_year', None)
    license_plate = request.json.get('car_plate', None)
    ezpass_tag = request.json.get('ezpass_tag', None)

    #check if the license plate already exists.
    #If not, proceed.
    if not car_exists(license_plate):
        car = Cars(qr_string, owner_id, car_maker, car_year, license_plate, ezpass_tag)
        db.session.add(car)
        db.session.commit()
        created_car_id = db.session.query(Cars).filter(Cars.license_plate == license_plate).scalar()

        return jsonify({
            'status': '200',
            'message': 'Successfully registered car',
            'car_id': str(created_car_id.id),
            'qr_id': qr_string
        })

    #if it does, abort with 401.
    else:
        abort(401)

def car_exists(car_plate):

    exists = False
    car_plate_exists = db.session.query(Cars).filter(Cars.license_plate == car_plate).scalar()

    if car_plate_exists:
        exists = True

    return exists

@app.route("/checkin", methods=['POST'])
@jwt_required()
def checkin():
    car_qr = request.json.get('carQr', None)
    user_id = request.json.get('userId', None)
    try:
        logged_car = db.session.query(Cars).filter(Cars.qr_string == car_qr).first()
        checkin = Trips(None, 2, logged_car.id)
        db.session.add(checkin)
        db.session.commit()
        return jsonify({
            'status': '200',
            'message': 'Successfully sluggin'
        })
    except:
        abort(404)


@app.route("/pooltrips/<int:car_id>", methods=['GET', 'PUT'])
@jwt_required()
def pool_trips(car_id):

    if request.method == 'GET':

        passng_checked = (db.session.query(Trips).filter(Trips.car == car_id, Trips.time_ended == None).all())
        passenger_count = len(passng_checked)
        return jsonify({
            'status': '200',
            'car_id': car_id,
            'slugs': passenger_count
        })
    if request.method == 'PUT':
        end_trip = db.session.query(Trips).filter(Trips.car == car_id, Trips.time_ended == None).all().update().values({Trips.time_ended: datetime.utcnow})
        db.session.commit()
        return jsonify({
            'status': '200'
        })


# Socket Route
@socketio.on('event')
def test_message(message):
    print("Button was pressed")
    json = {'data': message + " from server"}
    emit('events', json)

#DRIVER
@socketio.on('register_trip')
def handle_register_trip(data):
    userID = data['userID']
    carID = data['carID']
    pickup = data['pickup']
    destination = data['dropoff']
    car_list = []

    print(datetime.now())
    print(userID)
    print(carID)
    trip = Trips(userID, carID, pickup, destination)
    db.session.add(trip)
    db.session.commit()

    trip_rows = db.session.query(Trips).filter(Trips.pickup == pickup).all()

    #ASSUME EVERY TRIP'S CAR IS UNIQUE FOR NOW.
    for trip in trip_rows:
        car = db.session.query(Cars).filter(Cars.id == trip.car_id).scalar()
        car_list.append(car.id)

    pickup = pickup.replace(" ", "_")
    print(car_list)
    print(pickup)

    emit('trip_id', {'trip_id': trip.id})
    emit('updated_car_list' + pickup, {'car_list': car_list})

@socketio.on('delete_trip')
def handle_delete_trip(data):
    tripID = data['tripID']

    print(tripID)
    trip = db.session.query(Trips).filter(Trips.id == tripID).scalar()

    db.session.delete(trip)
    db.session.commit()

@socketio.on('init_ride')
def handle_init_ride(data):
    pickup = data['pickup']
    destination = data['dropoff']

    print(pickup)
    print(destination)

    car_list = []
    trip_rows = db.session.query(Trips).filter(Trips.pickup == pickup).all()

    for trip in trip_rows:
        car = db.session.query(Cars).filter(Cars.id == trip.car_id).scalar()
        car_list.append(car.id)

    print(car_list)
    pickup = pickup.replace(" ", "_")

    emit('car_list' + pickup, {'car_list': car_list})

# This is used to add people into carpool trip
@socketio.on('join')
def on_join(data):

    send("received: " + data)
    # username = data['username']
    # pool_id = data['pool_id']
    # join_room(pool_id)
    # get_car_id = db.session.query(Cars).filter(Cars.qr_string == pool_id).first()
    # passng_checked = (db.session.query(Trips)
    #                 .filter(Trips.car == get_car_id.id, Trips.time_ended == None)
    #                 .all())
    # passenger_count = len(passng_checked)
    # data = {'data': username + ' has joined the carpool: ' + str(pool_id)
    #             + '. There are: ' + str(passenger_count) + ' in carpool'}
    # print(data)
    # emit('roomjoin', data, to=pool_id)

# This is used to have people exit the carpool trip
@socketio.on('leave')
def on_leave(data):
    pool_id = data['pool_id']
    get_car_id = db.session.query(Cars).filter(Cars.qr_string == pool_id).first()
    end_trip = db.session.query(Trips).filter(Trips.car == get_car_id.id, Trips.time_ended == None).all().update().values({Trips.time_ended: datetime.utcnow})
    db.session.commit()
    data = {'data': 'All users have left carpool: ' + str(pool_id)}
    emit('endtrip', data, to=pool_id)
    leave_room(pool_id)
    print(data)

# Closes the carpool room created
@socketio.on('close')
def on_leave(data):
    pool_id = data['pool_id']
    data = {'data': 'carpool: ' + str(pool_id) + ' is now over'}
    emit('completetrip', data, to=pool_id)
    close_room(pool_id)
    print(data)

@socketio.on('connect')
def handle_connect():
    json = {
    'sid': request.sid
    }
    emit('room_ID', json)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    app.debug = True
    # app.run()
    socketio.run(app)

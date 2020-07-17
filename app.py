from flask import Flask, request, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from flask_heroku import Heroku

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/hitchin'
# heroku = Heroku(app)
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

    if not db.session.query(User).filter(User.phone_number == phone_number).first():
        new_user = User(phone_number, first_name, last_name, email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            'status': '200',
            'message': 'Successfully Signed Up'
        })
    else:
        abort(401)


@app.route("/login", methods=['POST'])
def login():
    phone_number = request.json.get('phoneNumber', None)
    password = request.json.get('password', None)
    if db.session.query(User).filter(User.phone_number == phone_number, User.password == password).first():
        return jsonify({
            'status': '200',
            'message': 'Successfully Logged in'
        })
    else:
        abort(403)

@app.route("/slug", methods=['POST'])
def slug_checkin():
    slug_id = request.json.get('qrString', None)
    try:
        new_slug = Car(qr_string = qr_string)
        db.session.add(new_slug)
        db.session.commit()
        return jsonify({
            'status': '200',
            'message': 'Successfully sluggin'
        })
    except:
        abort(401)

@app.route("/slug/<int:slug_id>", methods=['GET', 'PUT'])
def pool_count(slug_id):

    if request.method == 'GET':
        slugs = (db.session.query(Trips).filter(Trips.car == car, Trips.time_ended == None)
                          .all())
        slug_count = len(slugs)
        return jsonify({
                    'status': '200',
                    'slug_id': slug_id,
                    'slugs': slug_count
        })
    if request.method == 'PUT':
        slugs = db.session.query(Slug).filter(Slug.slug_id == slug_id, Slug.time_ended == None).all().update().values({Slug.time_ended: datetime.utcnow})
        db.session.commit()
        return jsonify({
            'status': '200'
        })




if __name__ == '__main__':
    app.debug = True
    app.run()

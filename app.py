from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy

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
    phone_number = request.json.get('phone_number', None)
    first_name = request.json.get('first_name', None)
    last_name = request.json.get('last_name', None)
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if not db.session.query(User).filter(User.phone_number == phone_number).first():
        new_user = User(phone_number, first_name, last_name, email, password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            'status': '200',
            'message': 'Successfully Signed Up'
        })
    else:
        abort(401)

if __name__ == '__main__':
    app.debug = True
    app.run()

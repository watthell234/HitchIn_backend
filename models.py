from app import db

# Create our database model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.Integer, unique=True)
    first_name = db.Column(db.String(18), nullable=False)
    last_name = db.Column(db.String(18), nullable=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(64), unique=False)

    def __init__(self, phone_number, first_name, last_name, email, password):
        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

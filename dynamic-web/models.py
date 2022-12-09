from main import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date

class User(db.Model):
    __tablename__= 'userregister'
    id=db.Column(db.Integer, primary_key=True)
    firstname=db.Column(db.String(20), unique=False, nullable=False)
    lastname = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(256), unique=False, nullable=False)

    # represent the object when it is queried for
    def __repr__(self):
        return '<Register {}>'.format(self.id)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), unique=False, nullable=False)
    name = db.Column(db.String(20), unique=False, nullable=False)
    description = db.Column(db.Text, unique=False, nullable=True)
    weight = db.Column(db.Float, unique=False, nullable=False)
    price_per_unit = db.Column(db.Float, unique=False, nullable=False)
    quantity = db.Column(db.String(20), unique=False, nullable=False)
    product_inception_date = db.Column(db.Date, nullable=False, default=date.today())

    # represent the object when it is queried for

    def __repr__(self):
        return '<Product {}>'.format(self.id)

class Customer(db.Model):
    __tablename__ = 'Customer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(30), unique=False, nullable=False)
    Phone_number = db.Column(db.String(15), unique=False, nullable=False)
    address = db.Column(db.String(40), unique=False, nullable=False)


    def __repr__(self):
        return '<Customer {}>'.format(self.id)
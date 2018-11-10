from ParkingLotClient import db
from passlib.hash import argon2


class Users(db.Model):

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    verified = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, email, password, first_name, last_name):
        self.email = email
        self.password = argon2.hash(password)
        self.first_name = first_name
        self.last_name = last_name

    def authenticate(self, password):
        return argon2.verify(password, self.password)

    def change_password(self, old_password, new_password):
        if not argon2.verify(old_password, self.password):
            return False
        self.password = argon2.hash(new_password)
        self.save()
        return True


class Restaurant(db.model):
    __tablename__ = "Restaurant"

    rest_id =  db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255),  nullable=False)
    location = db.Column(db.String(255),  nullable=False)
    contact = db.Column(db.String(255),  nullable=False)
    open_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time,nullable=True)

    @property
    def json(self):
        return to_json(self, self.__class__)


class FoodItem(db.Model):
    __tablename__ = "product"

    item_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer , nullable=False)
    description = db.Column(db.Unicode(500), index=True, unique=True)
    image_url = db.Column(db.Unicode(128))
    rest_id = db.Column(db.Integer, db.ForeignKey('Restaurant.rest_id'))

    #https://github.com/psthomas/crud-restaurant/blob/master/database_setup.py

    @property
    def json(self):
        return to_json(self, self.__class__)



class Cart(db.model):
    __tablename__ = 'cart'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.rest_id'))
    product_id = db.Column(db.Integer, db.ForeignKey('FoodItem.item_id'))
    quantity = db.Column(db.Integer)

    @property
    def json(self):
        return to_json(self, self.__class__)

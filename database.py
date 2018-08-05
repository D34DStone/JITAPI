# pylint: disable=E1101
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from crypto import random_string

db = SQLAlchemy()
print("[SQLAlchemy] Database initialized (__name__ = {}).".format(__name__))

# ====== Database variables ====== # IN DEVELOPMENT

_UNKNOWN_PHOTO_PATH = "unknown.png"
_DEFAULT_STRING_SIZE = 127
_TOKEN_SIZE = 16
_SECRET_SIZE = 16

def token_gen():
    return random_string(_TOKEN_SIZE)

def secret_gen():
    return random_string(_SECRET_SIZE)

# ====== Database models ====== # IN DEVELOPMENT

class Employee(db.Model): # Cafe employee

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(_DEFAULT_STRING_SIZE), nullable=False)
    login = db.Column(db.String(_DEFAULT_STRING_SIZE), unique=True, nullable=False)
    password = db.Column(db.String(_DEFAULT_STRING_SIZE), nullable=False)
    token = db.Column(db.String(_DEFAULT_STRING_SIZE), unique=True, default=token_gen)
    permission = db.Column(db.Integer, default=0, nullable=False) 
    registered = db.Column(db.DateTime, default=datetime.now)
    photo = db.Column(db.String, default=_UNKNOWN_PHOTO_PATH)
    cafe_id = db.Column(db.Integer, db.ForeignKey("cafe.id"), default=-1)
    cafe = db.relationship('Cafe', backref=db.backref('employees', lazy=True))

    @classmethod
    def load(cls, employee):
        try:
            return Employee(**employee)
        except Exception as err:
            raise err


class Client(db.Model): # Client app

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(_DEFAULT_STRING_SIZE), nullable=False)
    secret = db.Column(db.String(_DEFAULT_STRING_SIZE), default=secret_gen, nullable=False)


class Customer(db.Model): # Orders' adress
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(_DEFAULT_STRING_SIZE), nullable=False)
    address = db.Column(db.String(_DEFAULT_STRING_SIZE), nullable=False)
    #wishes = backref to their wishes


class Cafe(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    #employees = backref to its employees

    # @classmethod
    # def load(cls, cafe):
    #     try:
    #         return Cafe(**cafe)
    #     except Exception as err:
    #         raise err


class Ingredient(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(_DEFAULT_STRING_SIZE), nullable=False)
    expiry = db.Column(db.Interval, nullable=False)

    # def jsonify(self):
    #     return {
    #         "id": self.id,
    #         "title": self.title,
    #         "expiry" : "TODO: write timedelta to string conversation"
    #     }

    # @classmethod
    # def load(cls, ingredient):
    #     try:
    #         ingredient["expiry"] = convert_timedelta(ingredient.get("expiry"))
    #         return Ingredient(**ingredient)
    #     except Exception as err:
    #         return err


class Dish(db.Model): # They form our menu

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(_DEFAULT_STRING_SIZE), nullable=False)
    mass = db.Column(db.Float, default=0, nullable=False)
    is_visible = db.Column(db.Boolean, default=True, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    describe = db.Column(db.String(_DEFAULT_STRING_SIZE), default="", nullable=False)
    photo = db.Column(db.String(_DEFAULT_STRING_SIZE), default=_UNKNOWN_PHOTO_PATH, nullable=False)
    tags = db.Column(db.String(_DEFAULT_STRING_SIZE), default="[]", nullable=False)
    ingredients = db.Column(db.String(_DEFAULT_STRING_SIZE), default="[]", nullable=False)

    # def jsonify(self):
    #     return {
    #         "id": self.id,
    #         "title": self.title,
    #         "mass": self.mass,
    #         "is_visible": self.is_visible,
    #         "cost": self.cost,
    #         "describe": self.describe,
    #         "photo_path": self.photo_path,
    #         "tags": self.tags,
    #         "ingredients": self.ingredients
    #     }

    # When uncommenting, don't forget to import dumps at the beginning of the file
    # @classmethod
    # def load(cls, dish):
    #     try:
    #         dish["tags"] = dumps(dish.get("tags"))
    #         dish["ingredients"] = dumps(dish.get("ingredients"))
    #         return Dish(**dish)
    #     except Exception as err:
    #         raise err
      

class Wish(db.Model): # An order of Dish from Customer

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(_DEFAULT_STRING_SIZE), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    customer = db.relationship('Customer', backref=db.backref('orders', lazy=True))
from flask_bcrypt import Bcrypt
from flask import Flask, current_app
from datetime import datetime, timedelta
import jwt

from app import db


class User(db.Model):
    """This class represents the bucketlist table."""

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, index=True, unique=True)
    password = db.Column(db.String(120), nullable=False)
    bucketlists = db.relationship(
        'Bucketlist', order_by='Bucketlist.id', cascade="all, delete-orphan", lazy="dynamic")

    def __init__(self, email, first_name, last_name, username, password):
        """Initialize the user with an email and a password."""
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()

    def password_is_valid(self, password):
        """
        Validate user's password matches hashed password
        """
        return Bcrypt().check_password_hash(self.password, password)

    def save(self):
        """Save a user to the database.
        This includes creating a new user and editing one.
        """
        db.session.add(self)
        db.session.commit()
    
    def generate_token(self, user_id):
        """ Generates the access token"""

        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=30),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET'),
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)
    @staticmethod
    def decode_token(token):
        """Decodes the access token from the header."""
        try:
            payload = jwt.decode(token, current_app.config.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # the token is expired, return an error string
            return "Token has expired. Please login again"
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string
            return "Invalid token. Please register or try again"

    def __repr__(self):
        return "<User: {}>".format(self.name)

class Bucketlist(db.Model):
    """This class represents the bucketlist table."""

    __tablename__ = 'bucketlists'

    id = db.Column(db.Integer, primary_key=True)
    bucket_name = db.Column(db.String(100), nullable=False, unique=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    belongs_to = db.Column(db.Integer, db.ForeignKey(User.id))

    def __init__(self, bucket_name):
        """Initialize with bucket_name."""
        self.bucket_name = bucket_name

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(user_id):
        """Return buckets belonging to a user."""
        return Bucketlist.query.filter_by(belongs_to=user_id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """Representation of a bucketlist instance."""
        return "<Bucketlist: {}>".format(self.name)

from app import db
from flask_bcrypt import Bcrypt

# Local imports
from app import db


class User(db.Model):

    __tablename__ = 'users'
    # Define the columns of the User table
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, index=True, unique=True)
    password = db.Column(db.String(120), nullable=False)
    bucketlists = db.relationship(
        'Bucketlist', backref="users", cascade="all, delete-orphan", lazy="dynamic")

    def __init__(self, email, password):
        """Initialize the user with an email and a password."""
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

    def __repr__(self):
        return "<User: {}>".format(self.name)


class Bucketlist(db.Model):

    __tablename__ = 'bucketlists'
    # Define the columns of the Bucketlist table
    id = db.Column(db.Integer, primary_key=True)
    bucket_name = db.Column(db.String(120), nullable=False, unique=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    items = db.relationship('Item', backref="bucketlists",
                            cascade="all, delete-orphan", lazy="dynamic")

    def __init__(bucket_name, user_id):
        """Initialize the Bucket."""
        self.bucket_name = bucket_name
        self.user_id = user_id

    def save(self):
        """Save a Bucket to the database.
        This includes creating a new user and editing one.
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    """Gets all buckets by a specific user"""
    @staticmethod
    def get_all(user_id):
        return Bucketlist.query.filter_by(user_id=user_id)

    def __repr__(self):
        return "<Bucketlist: {}>".format(self.name)


class Item(db.Model):

    __tablename__ = 'items'
    # Define the columns of the Items table
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(120), nullable=False, unique=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    bucket_id = db.Column(db.Integer, db.ForeignKey(
        'bucketlists.id'), nullable=False)

    def __init__(item_name, bucket_id):
        """Initialize the Item."""
        self.item_name = item_name
        self.bucket_id = bucket_id

    def save(self):
        """Save an Item to the database."""
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return "<Item: {}>".format(self.name)

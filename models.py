from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


""" creating an instance of SQLAlchemy  """
db = SQLAlchemy()


class User(db.Model):
    """ schema for user table using 1 to many relationship """

    __tablename__ = "user"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    full_name = db.Column(db.String(256), nullable=False)
    username = db.Column(db.String(256), nullable=False, unique=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    created_by = db.Column(db.DateTime(), default=datetime.utcnow)
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    contacts = db.relationship("Contact", backref="user", lazy="dynamic")



class Contact(db.Model):
    """ schema for contact table using many to 1 relationship """

    __tablename__ = "contact"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    phone_number = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256))
    state = db.Column(db.String(256))
    city = db.Column(db.String(256))
    country = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


    
def shutdown_session(exception=None):
    """ A function to close the database at the end of each db.session.commit """
    db.session.remove()




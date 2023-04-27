from flask_sqlalchemy import SQLAlchemy
import datetime



db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    full_name = db.Column(db.String(256), nullable=False)
    username = db.Column(db.String(256), nullable=False, unique=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    created_by = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    contact = db.relationship("Contact", backref="user", lazy="dynamic")






class Contact(db.Model):
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
    db.session.remove()




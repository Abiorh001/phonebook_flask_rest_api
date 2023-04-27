from flask import Flask, request
from flask_restx import Resource, Api, fields, marshal_with
from ..models import Contact, db
from flask import Blueprint
from flask_jwt_extended import jwt_required,  get_jwt_identity
contact_api = Blueprint("contact_api", __name__, url_prefix="/api/v1")





api = Api(contact_api, title="A Phonebook Record Api", version="1.0.0", description="The Api To Add New Contact, List All Contacts, List Each Contact, Update Each Conatct, Delete Each Contact")



contact_model = api.model(
    'Contact', {
        'id': fields.Integer(),
        'name': fields.String(),
        'phone_number': fields.String(),
        'email': fields.String(),
        'state': fields.String(),
        'city': fields.String(),
        'country': fields.String(),
        'user_id': fields.Integer()
    })




@api.route('/contacts')
@api.doc(description="List all contacts in user's record")
class Contacts(Resource):
    @api.marshal_with(contact_model, code=200, envelope="Contacts")
    @jwt_required(refresh=True)
    def get(self):
        user_id = get_jwt_identity()
        contacts = Contact.query.filter_by(user_id=user_id).all()
        return contacts, 200

@api.route('/contact')
class ContactResource(Resource):

    @api.marshal_with(contact_model, code=200, envelope="Contact")
    @api.expect(description="List each contact using their phone number")
    @jwt_required(refresh=True)
    def get(self):
        data = request.get_json()
        phone_number = data.get("phone_number")
        contact = Contact.query.filter_by(phone_number=phone_number).first()
        return contact, 200



    @api.marshal_with(contact_model, code=201, envelope= "New Contact")
    @jwt_required(refresh=True)
    @api.expect(contact_model)
    def post(self):
        data = request.get_json()
        user_id = get_jwt_identity()
        name = data.get("name")
        phone_number = data.get("phone_number")
        email = data.get("email")
        state = data.get("state")
        city = data.get("city")
        country = data.get("country")
        
        new_contact = Contact(name=name, phone_number=phone_number, email=email, state=state, city=city, country=country, user_id=user_id)

        db.session.add(new_contact)
        db.session.commit()

        return new_contact, 201

    @api.marshal_with(contact_model, code=200, envelope="Updated Contact")
    @jwt_required(refresh=True)
    @api.expect(description="Update each contact using their phone number")
    @api.expect(contact_model)
    def put(self):
        data = request.get_json()
        phone_number = data.get("phone_number")
        contact = Contact.query.filter_by(phone_number=phone_number).first_or_404()
    
        if data.get("name"):
            contact.name = data.get("name")
        contact.email = data.get("email")
        contact.state = data.get("state")
        contact.city = data.get("city")
        contact.country = data.get("country")
        db.session.commit()
        return contact, 200

    @api.marshal_with(contact_model, code=200, envelope="Contact deleted")
    @api.expect(description="delete each contact using their phone number")
    @jwt_required(refresh=True)
    def delete(self):
        data = request.get_json()
        phone_number = data.get("phone_number")
        contact = Contact.query.filter_by(phone_number=phone_number).first()
        db.session.delete(contact)
        db.session.commit()
        return contact, 200
    

@api.route('/contact/<int:id>')
class Each_contact(Resource):
    @jwt_required(refresh=True)
    @api.marshal_with(contact_model, code=200)
    @api.expect(description="List each contact using their contact id")
    def get(self, id):
        contact = Contact.query.filter_by(id=id).first_or_404()
        return contact, 200




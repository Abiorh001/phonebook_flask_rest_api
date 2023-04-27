from flask import Blueprint, request, jsonify
from flask_restx import Api, Resource, fields, marshal_with
from ..models import User, db
from jwt.exceptions import ExpiredSignatureError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required,  get_jwt_identity

user_api = Blueprint("user_api", __name__, url_prefix = "/auth/api/v1/")



api = Api(user_api, version='1.0.0', title='A PhoneBoook Record Api', description='The Api For User To Signup, Login, View  All Users, And Individual User Registered')








signup_model = api.model (
      'NewUser',
    {
        'id' : fields.Integer(),
        'full_name' : fields.String(required=True, description="Full Name"),
        'username' : fields.String(required=True, description="Username"),
        'email' : fields.String(required=True, description="Email Addess"),
        'password' : fields.String(required=True, description="Password"),
        'location' : fields.String(description="User Location"),
        'about_me' : fields.String(description="About User")
    })
  


@api.route("/signup")
class UserClass(Resource):
    @api.marshal_with(signup_model, code=201, envelope="New User")
    @api.expect(signup_model)
    @api.doc(description="Create a new user")
    def post(self):
        data = request.get_json()
        full_name = data.get("full_name")
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        location = data.get("location")
        about_me = data.get("about_me")
        
        new_user = User(full_name=full_name, username=username, email=email, password=generate_password_hash(password, method='sha256'), location=location, about_me=about_me)
        db.session.add(new_user)
        db.session.commit()
        return new_user, 201


user_model = api.model (
       'user',
       {
            'id' : fields.Integer(),
            'full_name' : fields.String(required=True, description="Full Name"),
            'username' : fields.String(required=True, description="Username"),
            'email' : fields.String(required=True, description="Email Addess"),
            'location' : fields.String(description="User Location"),
            'about_me' : fields.String(description="About User"),

        })

users_model = api.model (
       'User',
       {
            'full_name' : fields.String(required=True, description="Full Name"),
            'email' : fields.String(required=True, description="Email Addess"),

        })

@api.route("/users")
class Users(Resource):

    @api.marshal_with(users_model, code=200, envelope="All users")
    @api.doc(description="List all user registered to get their names and email. use only for marketing afliated and educational purposes")
    @jwt_required(refresh=True)
    def get(self):
        users = User.query.all()
        return users, 200



@api.route("/user/<int:id>")
class Each_user(Resource):
    @api.marshal_with(users_model, code=200, envelope="User")
    @api.doc(description="List single user using their id that is registered to get their name and email. use only for marketing afliated and educational purposes")
    @jwt_required(refresh=True)
    def get(self, id):
        user = User.query.filter_by(id=id).first_or_404()
        return user,200




@api.route("/user")
class UserModel(Resource):

    @api.marshal_with(user_model, code=200, envelope="user")
    @api.doc(description="View your all your details while logged ")
    @jwt_required(refresh=True)
    def get(self):
        id = get_jwt_identity()
        user = User.query.get_or_404(id)
        return user, 200


    @api.marshal_with(user_model, code=201, envelope="User Updated")
    @api.expect(user_model )
    @api.doc(description="update logged in user details")
    @jwt_required(refresh=True)
    def put(self):
        id = get_jwt_identity()
        user = User.query.get_or_404(id)
        data = request.get_json()
        user.full_name = data.get("full_name")
        user.username = data.get("username")
        user.email = data.get("email")
        user.location = data.get("location")
        user.about_me = data.get("about_me")

        db.session.commit()
        return user, 201


    @api.marshal_with(user_model, code=200, envelope="Contact Deleted")
    @jwt_required(refresh=True)
    @api.doc(description="delete logged in user")
    def delete(self):
        id = get_jwt_identity()
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return user, 200


login_model = api.model (
    "Login",
    {
    "email" : fields.String(required=True, describtion=" User email address"),
    "password" : fields.String(required=True, description="User Password")
})


@api.route("/login")
class Login(Resource):

    @api.expect(login_model)
    @api.doc(description="user login")
    def post(self):
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                access_token = create_access_token(identity=user.id)
                refresh_token = create_refresh_token(identity=user.id)
                return {'access_token': access_token, 'refresh_token': refresh_token}, 200

            else:
                return {"message": "User not found."}, 404



@api.route("/refreshtoken")
class RefreshToken(Resource):
    
    @jwt_required(refresh=True)
    @api.doc(description="user generate new token")
    def post(self):

        id = get_jwt_identity()
        user = User.query.filter_by(id=id).first()
        
        refresh_token = create_refresh_token(identity=id)

        return {'refresh_token': refresh_token}, 200
    
 

    
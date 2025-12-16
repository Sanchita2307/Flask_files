from flask import request
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from providers.user_providers import UserProvider
from schemas.user_schema import UserSchema

auth_bp = Namespace("auth", description="Authentication Endpoints")

user_schema = UserSchema()

# Swagger models
register_model = auth_bp.model("Register", {
    "name": fields.String(required=True),
    "email": fields.String(required=True),
    "mobile": fields.Integer(required=True),
    "salary": fields.Float(required=True),
    "password": fields.String(required=True)
})

login_model = auth_bp.model("Login", {
    "email": fields.String(required=True),
    "password": fields.String(required=True)
})

# ----- REGISTER -----
@auth_bp.route("/register")
class Register(Resource):
    @auth_bp.expect(register_model)
    def post(self):
        data = request.get_json()
        user = UserProvider.register_user_pr(data)
        return user_schema.dump(user), 201

# ----- LOGIN -----
@auth_bp.route("/login")
class Login(Resource):
    @auth_bp.expect(login_model)
    def post(self):
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        user = UserProvider.authenticate_user_pr(email, password)
        if not user:
            return {"message": "Invalid email or password"}, 401
        # create JWT access token
        access_token = create_access_token(identity=str(user.id))
        return {"access_token": access_token}, 200

# ----- PROTECTED ROUTE -----
@auth_bp.route("/protected")
class Protected(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        return {"message": f"Hello user {current_user_id}, you are logged in!"}, 200

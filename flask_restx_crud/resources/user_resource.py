from flask_restx import Resource, Namespace, fields
# from providers.user_providers import UserProvider
# from schemas.user_schema import UserSchema
# from schemas.user_schema import UserSchema
from schemas.user_schema import UserSchema
from flask import request # will be used in marshmallow schema method
from flask_jwt_extended import jwt_required
from providers.user_providers import UserProvider
import pandas as pd
from flask_restx import Resource, Namespace, fields, reqparse
from flask import Response
from werkzeug.datastructures import FileStorage

# proivder methods call in this file

api = Namespace("users", description="User CRUD Operation") 

user_schema = UserSchema()
users_schema = UserSchema(many= True)

# swagger
user_model = api.model("User", {
   "id": fields.Integer(readOnly = True), 
   "name": fields.String(50), 
   "email": fields.String(100) , 
   "mobile":fields.Integer, 
   "salary":fields.Float, 
   "is_deleted": fields.Boolean})

# http://127.0.0.1:5000/users

# @api.route("/")
# class UserListCreate(Resource):
    
    # @api.marshal_list_with(user_model) # swagger documentation
    # def get(self):
    #     return [user.to_dict() for user in UserProvider.get_users_pr()] #json return

     
    # @api.expect(user_model, validata = True)
    # @api.marshal_with(user_model)
    # def post(self):
    #     data = api.payload
    #     user = UserProvider.create_user_pr(data)
    #     return user.to_dict(), 201

# @api.route("/<int:user_id>")
# class UserGetUpdateDelete(Resource):

#     @api.marshal_with(user_model)
#     def get(self, user_id):
#         user = UserProvider.get_user_by_id_pr(user_id)
#         if not user:
#             api.abort(404, "user not found")
#         return user.to_dict()
     
#     @api.expect(user_model) #validation is not true in all cases as sometimes data might or might not come
#     @api.marshal_with(user_model)
#     def put(self, user_id):
#         data = api.payload
#         updated_user = UserProvider.update_user_pr(user_id,data)
#         return updated_user.to_dict(), 200

#     # def patch(self, user_id):
#     #     pass

#     def delete(self, user_id):
#         UserProvider.delete_user_pr(user_id)
#         return None, 204


# # # marshmallow method # # #

@api.route("/")
class UserListCreate(Resource):
    
    @jwt_required()
    @api.marshal_list_with(user_model) # swagger documentation
    def get(self):
        users = UserProvider.get_user_pr()
        # serialize SQLAlchemy objects to JSON using Marshmallow
        return users_schema.dump(users), 200
     
    @jwt_required()
    @api.expect(user_model, validate = True)
    @api.marshal_with(user_model)
    def post(self):
        data = request.get_json()
        user = user_schema.load(data)
        UserProvider.create_user_pr(user)
        return user_schema.dump(user), 201

@api.route("/<int:user_id>")
class UserGetUpdateDelete(Resource):
    
    @jwt_required()
    @api.marshal_with(user_model)
    def get(self, user_id):
        user = UserProvider.get_user_by_id_pr(user_id)
        if not user:
            api.abort(404, "User not found")
        return user_schema.dump(user)
    
    @jwt_required()
    @api.expect(user_model) 
    @api.marshal_with(user_model)
    def put(self, user_id):
        user = UserProvider.get_user_by_id_pr(user_id)
        if not user:
            api.abort(404, "User not found")
    
        data = request.get_json()
    
        updated_user = UserProvider.update_user_pr(user_id, data)
    
        return user_schema.dump(updated_user), 200
    
    @jwt_required()
    @api.marshal_with(user_model)
    def delete(self, user_id):
        success = UserProvider.delete_user_pr(user_id)
        if not success:
            api.abort(404, "User not found")
        return None, 204
 
@api.route("/soft/<int:user_id>")    
class SoftDeleteUser(Resource):

    @jwt_required()
    @api.marshal_with(user_model)
    def delete(self, user_id):
        deleted_user = UserProvider.soft_delete_user_pr(user_id)
        if not deleted_user:
            api.abort(404, "User not found or already deleted")
        
        return user_schema.dump(deleted_user), 200
        

@api.route('/deleted')
class DeletedUsers(Resource):

    @jwt_required()
    @api.marshal_list_with(user_model)
    @api.doc(description="Get all soft-deleted users (is_deleted=True)")
    def get(self):
        """
        Returns a list of users who have been soft-deleted.
        """
        return UserProvider.list_deleted_users()

#### CSV UPLOAD DOWNLOAD ####
# ---------- Swagger file upload parser ----------
upload_parser = reqparse.RequestParser()
upload_parser.add_argument(
    'file',
    type=FileStorage,
    location='files',
    required=True,
    help='CSV file containing users'
)

# ---------- CSV Upload ----------
@api.route("/upload")
class UserUpload(Resource):
    @jwt_required()
    @api.expect(upload_parser)
    def post(self):
        args = upload_parser.parse_args()
        csv_file = args['file']

        if not csv_file.filename.endswith('.csv'):
            return {"msg": "File is not a CSV"}, 400

        try:
            # Read CSV using pandas
            df = pd.read_csv(csv_file)

            # Required columns
            required_cols = ['name', 'email', 'mobile', 'salary', 'password']
            if not all(col in df.columns for col in required_cols):
                return {"msg": "Invalid CSV columns"}, 400

            # Convert dataframe rows to user dicts
            users = []
            for _, row in df.iterrows():
                user_data = {
                    "name": row['name'],
                    "email": row['email'],
                    "mobile": int(row['mobile']),
                    "salary": float(row['salary']),
                    "password": row['password']  # will be hashed in provider
                }
                user = UserProvider.register_user_pr(user_data)
                users.append(user)

            return {"msg": f"{len(users)} users uploaded successfully"}, 201

        except Exception as e:
            return {"msg": str(e)}, 500

# ---------- CSV Download ----------
@api.route("/download")
class UserDownload(Resource):
    @jwt_required()
    def get(self):
        # Fetch all users
        users = UserProvider.get_user_pr()

        # Convert to pandas DataFrame
        data = [
            {
                "id": u.id,
                "name": u.name,
                "email": u.email,
                "mobile": u.mobile,
                "salary": u.salary,
                "is_deleted": u.is_deleted
            }
            for u in users
        ]
        df = pd.DataFrame(data)

        # Create CSV response
        response = Response(
            df.to_csv(index=False),
            mimetype="text/csv",
        )
        response.headers["Content-Disposition"] = "attachment; filename=users.csv"
        return response
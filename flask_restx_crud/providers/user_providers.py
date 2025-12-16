# business logic / dao layer's methods call
from dao.user_dao import UserDAO
from models.user_models import User # to get user details

class UserProvider:
    
    # @staticmethod
    # def create_user_pr(data):
    #     name = data.get("name")
    #     email = data.get("email")
    #     mobile = data.get("mobile")
    #     salary = data.get("salary")
    #     is_deleted = data.get("is_deleted")

    #     return UserDAO.create_user(name, email, mobile, salary, is_deleted) # == return user from Dao create method

    # @staticmethod
    # def get_users_pr():
    #     return UserDAO.get_all_users()  
    
    # @staticmethod
    # def get_user_by_id_pr(user_id):
    #     return UserDAO.get_user_by_id(user_id)  
    
    # @staticmethod
    # def update_user_pr(user_id, data):
    #     name = data.get("name")
    #     email = data.get("email")
    #     mobile = data.get("mobile")
    #     salary = data.get("salary")
    #     is_deleted = data.get("is_deleted")
    #     return UserDAO.update_user(user_id, name, email, mobile, salary, is_deleted)
    
    # @staticmethod
    # def delete_user_pr(user_id):
    #     return UserDAO.delete_user(user_id)

# add register and authenticate methods
    @staticmethod
    def register_user_pr(data):
        """Create a user with hashed password"""
        user = User(
            name=data.get("name"),
            email=data.get("email"),
            mobile=data.get("mobile"),
            salary=data.get("salary")
        )
        user.set_password(data.get("password"))  # hash password
        return UserDAO.create_user(user)

    @staticmethod
    def authenticate_user_pr(email, password):
        """Verify user credentials"""
        user = UserDAO.get_user_by_email(email)
        if user and user.check_password(password):
            return user
        return None

 # # marshmallow method # #
    @staticmethod
    def create_user_pr(user_obj):
        """
        Accepts a User object (deserialized by Marshmallow),
        and passes it to the DAO to save in the DB.
        """
        return UserDAO.create_user(user_obj)  # return the user object from DAO    
    
    @staticmethod
    def get_user_pr():
        return UserDAO.get_users()
    
    @staticmethod
    def get_user_by_id_pr(user_id):
        return UserDAO.get_user_by_id(user_id)
    
    @staticmethod
    def update_user_pr(user_id, data):
        user = UserDAO.get_user_by_id(user_id)
        if not user:
            return None
        
        updated_user = UserDAO.update_user(user, data)
        return updated_user
    
    @staticmethod
    def delete_user_pr(user_id):
        user = UserDAO.get_user_by_id(user_id)
        if not user:
            return None
        UserDAO.delete_user(user)
        return True
    
    @staticmethod
    def soft_delete_user_pr(user_id):
        user = UserDAO.get_user_by_id(user_id)
        if not user or user.is_deleted:
            return None
        return UserDAO.soft_delete_user(user)
    
    @staticmethod
    def list_deleted_users():
        # Returns all users with is_deleted=True
        return UserDAO.get_deleted_users()
    


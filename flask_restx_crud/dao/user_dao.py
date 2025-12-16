from models.user_models import User
from extensions.db import db

class UserDAO: # database access object (get, update,delete db operations)

    # @staticmethod
    # def create_user(name, email, mobile, salary, is_deleted):
    #     user = User(name = name, email = email, mobile = mobile,
    #                  salary = salary, is_deleted = is_deleted)
    #     db.session.add(user)
    #     db.session.commit()
    #     return user

    # @staticmethod
    # def get_all_users():
    #     return User.query.all()

    # @staticmethod
    # def get_user_by_id(user_id):
    #     return User.query.get(user_id)

    # @staticmethod
    # def update_user(user_id, name, email, mobile, salary, is_deleted):
    #     user = UserDAO.get_user_by_id(user_id)
    #     user.name = name
    #     user.email = email
    #     user.mobile = mobile
    #     user.salary = salary
    #     user.is_deleted = is_deleted
    #     db.session.commit()
    #     return user


    # @staticmethod
    # def delete_user(user_id):
    #     user = UserDAO.get_user_by_id(user_id)
    #     db.session.delete(user)
    #     db.session.commit()
    #     return True # as we can'tretrun the user it has been deleted

    @staticmethod
    def get_user_by_email(email):
        """Fetch a user by email for authentication"""
        return User.query.filter_by(email=email).first()

# # marshmallow method # # 
    @staticmethod
    def create_user(user_obj):
        db.session.add(user_obj)
        db.session.commit()
        return user_obj
    
    @staticmethod
    def get_users():
        return User.query.all()
    
    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)
    
    @staticmethod
    def update_user(user, data):
        for key, value in data.items():
            setattr(user, key, value)

        db.session.commit()
        return user
    
    @staticmethod
    def delete_user(user):
        db.session.delete(user)
        db.session.commit()
        return True

    
    @staticmethod
    def soft_delete_user(user):
        user.is_deleted = True
        if not user:
            return None
        db.session.commit()
        return user
    
    # restore softdeleted users
    @staticmethod
    def get_deleted_users():
        # Fetch only users with is_deleted=True
        return User.query.filter_by(is_deleted=True).all()
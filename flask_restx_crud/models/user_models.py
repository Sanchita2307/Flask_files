from extensions.db import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable= False)
    email = db.Column(db.String(100), nullable= False)
    mobile = db.Column(db.BigInteger, nullable= False)
    salary = db.Column(db.Float, nullable = False)
    password = db.Column(db.String(200), nullable=True) 
    is_deleted = db.Column(db.Boolean, default = False )

    def to_dict(self):
        return {"id":self.id, "name":self.name, "email":self.email, 
                "mobile":self.mobile, "salary":self.salary, "is_deleted":self.is_deleted}

    def __repr__(self):
        return f"<User {self.name}>"
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def soft_delete(self):
        self.is_deleted = True
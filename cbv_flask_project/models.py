from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() 

class Employee(db.Model):
    __tablename__ = "employees"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    mobile = db.Column(db.Integer, nullable= False)
    address = db.Column(db.String(100), nullable= False)
    salary = db.Column(db.Float, nullable = False)
    is_deleted = db.Column(db.Boolean, default = False)

    def __repr__(self):
        return f"<Employee {self.name}>"
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# create app , file name will be passed
app = Flask(__name__) 

# create db though string
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/b14_flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# pass your app to sqlalchemy
db = SQLAlchemy(app) #connection b/w app and sqlalchemy

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable= False)
    department = db.Column(db.String(100), nullable= False)
    salary = db.Column(db.Float, nullable = False)
    # is_deleted = db.Column(db.Boolean, default = False )

    def to_dict(self):
        return{
            "id":self.id,
            "name":self.name,
            "department":self.department,
            "salary":self.salary
        }
    
# create table
with app.app_context():
    db.create_all()

@app.route('/employees', methods = ["POST"])
def create_employee():
    data = request.get_json()    #json to python dictionary  
    print(data)
    name = data.get("name")
    department = data.get("department")
    salary = data.get("salary")
    if not all([name,department,salary]): # if not any
        return jsonify({"error":"Missing fields"}), 400 # client error
    new_emp = Employee(name=name, department=department ,salary=salary) #202 rec created #emp object creation
    db.session.add(new_emp)
    db.session.commit()
    return jsonify(new_emp.to_dict()), 201

@app.route('/employees', methods = ["GET"])
def get_employees():
    all_data = Employee.query.all()
    # return jsonify({"a":all_data}) # wont work as all_data is obj of each employee
    return jsonify([emp.to_dict() for emp in all_data])

@app.route('/employees/<int:id>',methods = ["GET"])
def get_employee(id):
    emp = Employee.query.get(id)
    if not emp:
        return jsonify({"error":"Employee doesn't exist"})
    return jsonify(emp.to_dict()) # single employee so no need of list as above

@app.route('/employees/<int:id>', methods = ["PUT"]) # will work as both PUT and PATCH
def update_employee(id):
    emp = Employee.query.get(id)
    if not emp:
        return jsonify({"error":"Employee doesn't exists"})
    data = request.get_json() #json to python dict

    emp.name = data.get("name", emp.name)
    emp.department = data.get("department", emp.department)
    emp.salary = data.get("salary", emp.salary)

    db.session.commit()
    return jsonify(emp.to_dict()), 201

@app.route('/employees/<int:id>', methods = ["DELETE"])
def delete_employee(id):
    emp = Employee.query.get(id)
    if not emp:
        return jsonify({"error": "Employee doesn't exist"})
    db.session.delete(emp)
    db.session.commit()
    return jsonify({"message":"Employee deleted"}),200

# def soft_delete(id):
#     emp = Employee.query.get(id)
#     emp.


if __name__ == "__main__":
    app.run(debug=True)
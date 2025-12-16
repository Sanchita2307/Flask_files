from flask import Flask,request
from flask_restx import Api,Resource, fields
from models import db, Employee
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

api = Api(app, version='1.0', title="Employee App",
          description='A Simple Employee CRUD API using Flask-RESTx')

namespace = api.namespace('employees', description = 'Employee operations')

# Define API model for swagger
employee_model = api.model('Employee', {
    'id': fields.Integer(readOnly=True, description='The employee unique identifier'),
    'name': fields.String(required = True, description = 'Employee name'),
    'mobile':fields.Integer(required = True, description = 'Employee mobile'),
    'address':fields.String(required = True, description = 'Employee address'),
    'salary':fields.Float(required = True, description = 'Employee salary'),
    'is_deleted':fields.Boolean(required = True, description = 'Employee is deleted')
})

# http://127.0.0.1:5000/employees

@namespace.route("/")
class EmployeeList(Resource):
    """Shows a list of all employees and lets you POST to add new ones"""

    @namespace.doc("list_employees")
    @namespace.marshal_list_with(employee_model)
    def get(self):
        """List all employees"""
        employees= Employee.query.all()
        return employees

    @namespace.doc("create_employees")
    @namespace.marshal_with(employee_model)    
    def post(self):
        """Create new employee"""
        data = request.get_json()
        new_emp = Employee(name=data['name'], mobile=data['mobile'], address = data['address'],
                           salary = data['salary'], is_deleted = data['is_deleted'])
        db.session().add(new_emp)
        db.session.commit()
        return new_emp, 201
    
@namespace.route("/<int:id>")
class EmployeeResource(Resource):

    @namespace.doc("get_employee")
    @namespace.marshal_with(employee_model)
    def get(self,id):
        """Fetch an employee given its identifier"""
        emp = Employee.query.get_or_404(id)
        return emp
    
    @namespace.doc("delete_employee")
    @namespace.marshal_with(employee_model)
    def delete(self,id):
        """Delete an employee given its indetifier"""
        emp = Employee.query.get_or_404(id)
        db.session.delete(emp)
        db.session.commit()
        return '',204
    
    @namespace.doc("update_employee")
    # @namespace.marshal_list_with(employee_model)
    def put(self,id):
        """Update"""
        emp = Employee.query.get_or_404(id)
        data = request.get_json()
        emp.name = data.get('name', emp.name)
        emp.mobile = data.get('mobile', emp.mobile)
        emp.address = data.get('address',emp.address)
        emp.salary = data.get('salary', emp.salary)
        emp.is_deleted = data.get('is_deleted', emp.is_deleted)
        db.session.commit()
        return emp
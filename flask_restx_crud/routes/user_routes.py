# from flask_restx import Api
# from resources.user_resource import api as user_ns
# from flask import Flask
# from resources.user_resource import api as user_api
# from routes.auth_routes import auth_bp as auth_api


# def register_routes(app):
#     api = Api(app, version="1.0", title="Flask Restx User CRUD API")
#     api.add_namespace(user_ns, path="/users") # apis could be single or multiple so it to be added in namespace

# def register_routes(app: Flask):

#     api = Api(app)
#     api.add_namespace(user_api, path="/users")
#     api.add_namespace(auth_api, path="/auth")


from flask_restx import Api
from flask import Flask
from resources.user_resource import api as user_api
from routes.auth_routes import auth_bp as auth_api

def register_routes(app: Flask):

    # JWT Bearer token setup for Swagger
    authorizations = {
        'Bearer Auth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    }

    api = Api(
        app,
        version="1.0",
        title="Flask Restx User CRUD API",
        authorizations=authorizations,
        security='Bearer Auth'  # applies JWT to all endpoints unless overridden
    )

    api.add_namespace(user_api, path="/users")
    api.add_namespace(auth_api, path="/auth")
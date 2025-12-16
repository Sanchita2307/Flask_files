# class Config:
#     Debug = True
#     SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/flask_restx_crud_operation'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

#     # # initialize JWT
#     JWT_SECRET_KEY = "64dc2cd6f1816cb4e62893969ea886c1be24fac83199d8612dc8cc71e0e8e859"
#     JWT_ACCESS_TOKEN_EXPIRES = 3600  


import secrets

class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://root:root@localhost/flask_restx_crud_operation"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'ab961159091f07d20bef0e02799f6ff6'  # Flask session key
    JWT_SECRET_KEY = '6caf18ddef666847c4c6f2e1c0a2dcd926a7619801d124f9d8aa6573d508571d'  # JWT signing key
    JWT_ACCESS_TOKEN_EXPIRES = 3600
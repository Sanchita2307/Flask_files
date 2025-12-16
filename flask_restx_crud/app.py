from flask import Flask
from config import Config
from routes.user_routes import register_routes
from extensions.db import db
from flask_jwt_extended import JWTManager  


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    jwt = JWTManager(app)

    # creates tables in db
    with app.app_context():
        # db.drop_all() # i added passowrd col later so needed this, later on added mobile as big int
        db.create_all()

    register_routes(app)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True) # this is flase in case of prod but we're taking True
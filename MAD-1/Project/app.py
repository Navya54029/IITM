# Om Ganeshaya Namah

import os
from flask import Flask
from application.config import LocalDevelopmentConfig
from application.database import db
from flask_login import LoginManager
from application.models import User

app = None


def create_app():
    app = Flask(__name__, template_folder="templates")
    if os.getenv('ENV', "development") == "production":
      app.logger.info("Currently no production config is setup.")
      raise Exception("Currently no production config is setup.")
    else:
      app.logger.info("Staring Local Development.")
      print("Staring Local Development")
      app.config.from_object(LocalDevelopmentConfig)
      app.config['SECRET_KEY'] = 'lkjhgasdfg'
    db.init_app(app)
    app.app_context().push()

    login_manager = LoginManager()
    login_manager.login_view = 'application.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        print(user_id)
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))
    app.logger.info("App setup complete")
    return app

app = create_app()

# Import all the controllers so they are loaded
from application.controllers import *

if __name__ == '__main__':
  # Run the Flask app
  app.run()

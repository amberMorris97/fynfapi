from flask import Flask
from dotenv import dotenv_values

app_secret = dotenv_values(".env")['SECRET_KEY']

def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = app_secret

  from routes import api

  app.register_blueprint(api, url_prefix='/')

  return app

app = create_app()

if __name__ == "__main__":
  app.run(debug=True)
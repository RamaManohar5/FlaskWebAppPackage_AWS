from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'api_key'

from .views import application

# register the resources of the API to the flask object
app.register_blueprint(application, url_prefix= '/')
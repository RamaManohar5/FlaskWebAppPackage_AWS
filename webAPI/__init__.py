from flask import Flask

application = Flask(__name__)
application.config['SECRET_KEY'] = 'api_key'

from .views import views

# register the resources of the API to the flask object
application.register_blueprint(views, url_prefix= '/')
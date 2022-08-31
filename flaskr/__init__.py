# Basic blog app called Flaskr. 
# Users will be able to: register, log in, create posts and edit or delete their own posts. 
# It'll be able to package and install the app on other computers. 

'''
A Flask app is an instance of the Flask class: everything about the app, such as
configuration and URLs, will be registered with this class. 

The most straightforward way to create a Flask app is to create a global Flask isntance 
directly at the top of the code. While this is simple and useful in some cases, it can cause some tricky issues as the project grows.

So, instead of creating a Flask instance globally, better create it inside a function.
This function is known as "Application factory" --- > Any configuration, registration and other setup the app needs
will happen inside the function, then the app will be returned. 
'''

import os 
from flask import Flask

# app factory
def create_app(test_config = None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent = True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)
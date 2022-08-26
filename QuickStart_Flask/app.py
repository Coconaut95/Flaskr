'''
source: https://flask.palletsprojects.com/en/2.2.x/quickstart/#
'''
# from flask import methods
from flask import Flask
from flask import url_for
from flask import request  # http methods
from flask import render_template

# When returning HTML, any user-provided values rendered in the output must be escaped to protect from injection attacks.
# HTML rendered with Jinja will do this automatically.
# Injection attacks: Proporcionar info no confiable a un programa ---> Robo de datos, pérdida de datos, denegación de servicio y el compromiso total del sistema.
# La razón principan de las vulnerabilidades de inyección suele ser una validación insuficiente de la entrada del usuario.
from markupsafe import escape

# Create an instance of class Flask
# This argument is needed so that Flask knows where to look for resources such as templates and static files.
app = Flask(__name__)
# app.app_context().push()

# flask --app [name] run
# default response type in Flask: HTML

## Debug Mode: By enabling debug mode, the server will automatically reload if code changes,
# and will show an interactive debugger in the browser if an error occurs durings a request.
# Do not run the development server or debugger in a production environment, cause
# the debugger allows executing arbitrary python code from the browser.
# flask --app [name] --debug run

@app.route('/')
def index():
    return 'Index Page'


@app.route('/login')
def login():
    return 'login'

# Variable Rules: Can be add variable sections to a URL by marking sections with <variable_name>
# The function then receives the <variable_name> as a keyword argument.
# Optionally, you can use a converter to specify the type of the argument like <converter:variable_name>


@app.route('/user/<username>')  # decorator route() bind a function to a URL.
def show_user_profile(username):
    # show the user profile for that user
    return f"User {username}\s profile!"


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post{post_id}'


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'

# URL Builiding: To build a URL to a specific function, use url_for().
# This function accepts the name of the function as its first argument and any number of keyword arguments,
# each corresponding to a variable part of the URL rule. Unknown variable parts are appended to the URL as query parameters.


# test_request_context() tells Flask to behave as though it's handling a request even while we use Python shell.
with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('show_user_profile', username='Jonh', lastname='Salchichon'))
    print(url_for('show_post', post_id=10))

# @app.route('/projects/') Si termina con /, es similiar a apuntar a un directorio
# def projects():
#     return 'The project page'

# @app.route('/about') Como no termina con /, es similar a apuntar a un archivo.
# def about():
#     return 'The about page'

## HTTP Methods: 
# Web app use different HTTP methods when accessing URLs.
## Accessing Request Data
# For web app it's crucial to react to the data a client sends to the server.
# In Flask this info es provided by the blogal 'request' object
# By default, a route only answers to GET requests
# One can use the methods argument of the route() decorator to handle different HTTP methods

# 1) The request object
'''
The example below keeps all methods for the route within one function, 
which can be useful if each part uses some common data. 

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    return render_template('login.html', error=error)
'''

'''
It can also be done by different functions.

@app.get('/login')
def login_get():
    return show_the_login_form()

@app.post('/post')
def login_post():
    return do_the_login()
'''
# 2) File Uploads
# You can handle uploaded fileswith Flask easily. 
# Just make sure not to foret to set the: enctype = "multipart/form-data" attribute on your HTML form,
# otherwise the browser will not transmit your files at all.  
# Uploaded files are stored in memory or at a temporary location on the filesystem.
# You can access those files by looking at the "files" attribute on the request object.
# Each uploaded file is stored in that dictionary. 
# It behaves just like a standard Python 'file object', but it also has a 'save()' method
# that allows you to store that file on the filesystem of the server
'''
    @app.route('/upload', methods=['GET', 'POST'])
    def upload_file():
        if request.method == 'POST':
            f = request.files['the_file']
            f.save('/var/www/uploads/uploaded_file.txt')

    ---> To keep the name of the file before it was uploaded, use filename attribute.
    ---> But never trust that value for secure reason, use: secure_filename()
    from werkzeug.utils import secure_filename

    @app.route('/upload', methods=['GET', 'POST'])
    def upload_file():
        if request.method == 'POST':
            file = request.files['the_file']
            file.save(f"/var/www/uploads/{secure_filename(file.filename)}")

'''

## Cookies
# To access cookies use 'cookies' attribute. It's a dictionary with all the cookies the client transmits.
# To set cookies use 'set_cookie' method of response objects.
# If you want to use sessions, don't use the cookies directly but instead use the 'Sessions' in Flask that add some security on top of cookies for you.

'''
Reading cookies:

    from flask import request

    @app.route('/')
    def index():
        username = request.cookies.get('username')
        # use cookies.get(key) instead of cookies[key] to not get a
        # KeyError if the cookie is missing.
'''
'''
Storing cookies:

    @app.route('/')
    def index():
        resp = make_response(render_template(...))
        resp.set_cookie('username', 'the username')
        return resp
'''
## Static files
# url_for('static', filenmae='style.css') # generate URL for static file

## Rendering Templates
# Flask configures Jinja2 template engine for HTML files.
# To render a template you can use "render_template()"

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

## APIs with JSON
# Common response format when writing an API is JSON. 
# If you return a dict or list from a view, it'll be converted to a JSON response.

'''

@app.route("/me")
def me_api():
    user = get_current_user()
    return {
        "username": user.username,
        "theme": user.theme,
        "image": url_for("user_image", filename=user.image),
    }

@app.route("/users")
def users_api():
    users = get_all_users()
    return [user.to_json() for user in users]

'''
## Sessions
# Object called 'session' allows to store info specific to a user from one request to the next. 

# from flask import session

# # Set the secret key to some random bytes. Keep this really secret!
# app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# @app.route('/')
# def index():
#     if 'username' in session:
#         return f'Logged in as {session["username"]}'
#     return 'You are not logged in'

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         session['username'] = request.form['username']
#         return redirect(url_for('index'))
#     return '''
#         <form method="post">
#             <p><input type=text name=username>
#             <p><input type=submit value=Login>
#         </form>
#     '''

# @app.route('/logout')
# def logout():
#     # remove the username from the session if it's there
#     session.pop('username', None)
#     return redirect(url_for('index'))


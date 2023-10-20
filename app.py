from flask import Flask
from middleware import init_app as init_socket, start_app
from routes import init_app as init_routes

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'my_secret_key123@_456'

app.group = {}
app.generator = {}
app.gg = {}


if __name__ == "__main__":
    init_routes(app)
    init_socket(app)
    start_app(app)
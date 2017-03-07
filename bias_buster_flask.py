from flask import Flask, request
from os import urandom

app = Flask(__name__)

from views import *
# @app.route('/')
# def hello_world():
#     return 'Hello World!'
app.config["WTF_CSRF_ENABLED"] = True
app.config["SECRET_KEY"] = urandom(24)

# @app.before_request
# def print_stuff():
#     print(request.headers)
#     print(request.path)
#     print(request.url)
#     # print(request.routing_exception())


if __name__ == '__main__':
    app.run(port=5001)

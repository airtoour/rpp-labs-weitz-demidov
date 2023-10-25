from flask import Flask

from api.add import add
from api.fetch import fetch
from api.update import update

app = Flask(__name__)

dict = {}

if __name__ == '__main__':
    app.run(debug = True)
    app.register_blueprint(add)
    app.register_blueprint(fetch)
    app.register_blueprint(update)

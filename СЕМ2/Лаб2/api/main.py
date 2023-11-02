from flask  import Flask

from add    import add
from fetch  import fetch
from update import update

app = Flask(__name__)

app.register_blueprint(add)
app.register_blueprint(fetch)
app.register_blueprint(update)

if __name__ == '__main__':
    app.run(debug = True)

from flask import Flask
from routes import login

app = Flask(__name__)

app.register_blueprint(login)

if __name__ == "__main__":
    app.run(debug=True)

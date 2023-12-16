from signup import signup
from login import login
from config import app

app.register_blueprint(signup)
app.register_blueprint(login)


if __name__ == '__main__':
    app.run(debug=True)

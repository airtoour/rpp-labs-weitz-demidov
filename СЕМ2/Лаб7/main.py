from config import app
from routes import lab

app.register_blueprint(lab, url_prefix='/lab')

if __name__ == '__main__':
    app.run(debug=True)

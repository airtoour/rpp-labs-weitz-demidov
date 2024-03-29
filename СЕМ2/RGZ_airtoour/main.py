from config import app, db
from routes import operation

app.register_blueprint(operation, url_prefix='/operation')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
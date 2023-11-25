from flask import Flask

app = Flask(__name__, template_folder='templates')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/SEM2LR4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

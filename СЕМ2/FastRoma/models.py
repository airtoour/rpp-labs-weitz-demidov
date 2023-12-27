from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired
from config import db

class Operations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    sum = db.Column(db.Numeric, nullable=False)

class OperationsForm(FlaskForm):
    id = IntegerField('Номер операции', validators=[DataRequired()])
    submit = SubmitField('Найти описание')
from flask_wtf import FlaskForm
from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from wtforms import StringField, SubmitField, BooleanField, PasswordField, EmailField
from wtforms.validators import DataRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_required, login_user, current_user, logout_user
from limit import limiter

login = Blueprint('login', __name__)




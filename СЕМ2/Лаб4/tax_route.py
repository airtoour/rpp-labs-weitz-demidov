from flask import Blueprint, render_template

tax = Blueprint("tax", __name__)

@tax.route("/v1/car/tax/calc", methods=["GET"])
def calculate_tax():
    # Логика расчета налога на автомобиль
    return "Расчет налога выполнен успешно"

@tax.route("/")
def index():
    return render_template("index.html")
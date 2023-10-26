from flask           import Flask
from region_routes   import region
from tax_param_route import tax_param
from tax_route       import tax

app = Flask(__name__)

# Инициализация Blueprint
app.register_blueprint(region, url_prefix = '/v1/region')
app.register_blueprint(tax_param, url_prefix = '/v1/car/tax-param')
app.register_blueprint(tax, url_prefix = '/v1/car/tax')

if __name__ == '__main__':
    app.run(debug = True)

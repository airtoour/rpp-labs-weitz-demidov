from region_routes   import region
from tax_param_route import tax_param
from tax_route       import tax
from config          import app
from models          import db

# Инициализация Blueprint
app.register_blueprint(region, url_prefix='/region')
app.register_blueprint(tax_param, url_prefix = '/car/tax-param')
app.register_blueprint(tax, url_prefix = '/car/tax')

db.init_app(app)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug = True)
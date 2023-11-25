from region_routes   import region
from tax_param_route import tax_param
from tax_route       import tax
from config          import app

app.register_blueprint(region,    url_prefix='/region')
app.register_blueprint(tax_param, url_prefix='/tax_param')
app.register_blueprint(tax,       url_prefix='/tax')


if __name__ == '__main__':
    app.run(debug=True)
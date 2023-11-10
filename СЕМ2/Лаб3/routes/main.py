from flask        import Flask
from region_route import region
from car_route    import cars
from area_route   import area_route

app = Flask(__name__)

# Регистрация Blueprint
app.register_blueprint(region)
app.register_blueprint(cars)
app.register_blueprint(area_route)

if __name__ == '__main__':
    app.run(debug = True)
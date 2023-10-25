from Config import app

from routes.region_route import regions
from routes.car_route import cars
from routes.area_route import area_route

app.register_blueprint(regions)
app.register_blueprint(cars)
app.register_blueprint(area_route)


if __name__ == '__main__':
    app.run(debug=True)
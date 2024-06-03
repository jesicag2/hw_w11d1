# HW: REST API Design Patterns

from flask import Flask
from database import db
from schemas import ma
from limiter import limiter
from caching import cache


from routes.employeeBP import employee_blueprint
from routes.productBP import product_blueprint
from routes.orderBP import order_blueprint
from routes.customerBP import customer_blueprint
from routes.productionBP import production_blueprint


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(f'config.{config_name}')

    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)

    return app

def blueprint_config(app):
    app.register_blueprint(employee_blueprint, url_prefix='/employees')
    app.register_blueprint(product_blueprint, url_prefix='/products')
    app.register_blueprint(order_blueprint, url_prefix='/orders')
    app.register_blueprint(customer_blueprint, url_prefix='/customers')
    app.register_blueprint(production_blueprint, url_prefix='/productions')

def config_rate_limit():
    limiter.limit("10 per hour")(employee_blueprint)
    limiter.limit("10 per hour")(product_blueprint)
    limiter.limit("10 per hour")(order_blueprint)
    limiter.limit("10 per hour")(customer_blueprint)
    limiter.limit("10 per hour")(production_blueprint)

if __name__ == "__main__":
    app = create_app('DevelopmentConfig')

    blueprint_config(app)
    config_rate_limit()

    with app.app_context():
        db.drop_all()
        db.create_all()

    app.run(debug=True)
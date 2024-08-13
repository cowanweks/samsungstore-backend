import os
from flask import Flask, send_from_directory, current_app
from app.config import ProductionConfig, DevelopmentConfig, TestingConfig
from .extensions import cors, db, sess, vite, folder_setup
from app.routes import (
    index_route,
    cart_route,
    user_route,
    role_route,
    product_route,
    payment_route,
    order_route
)  # Routes
from app.utils.app_utils import app_setup
from app.utils import bcolors


@app_setup
def create_app() -> Flask:
    """Create flask app"""

    app = Flask(__name__)

    # # Prevent redirects in blueprints
    app.url_map.strict_slashes = False

    # Set the application configuration
    if os.getenv("ENV") == "production":
        app.config.from_object(ProductionConfig)

    elif os.getenv("ENV") == "development":
        app.config.from_object(DevelopmentConfig)

    else:
        app.config.from_object(TestingConfig)

    # Register blueprints
    app.register_blueprint(index_route)
    app.register_blueprint(cart_route)
    app.register_blueprint(user_route)
    app.register_blueprint(role_route)
    app.register_blueprint(product_route)
    app.register_blueprint(payment_route)
    app.register_blueprint(order_route)

    db.init_app(app)
    cors.init_app(app)
    sess.init_app(app)
    vite.init_app(app)
    folder_setup.init_app(app)  # Set the templates and static directories

    with app.app_context():
        db.create_all()

    print(
        bcolors.OKGREEN
        + f"""[*] - You are running {app.config.get('APP_NAME')} in {app.config.get(
            'ENV')} on HOST {app.config.get("HOST")} on PORT {app.config.get("PORT")} with {app.config.get("SQLALCHEMY_DATABASE_URI")} as database URI !"""
    )

    return app

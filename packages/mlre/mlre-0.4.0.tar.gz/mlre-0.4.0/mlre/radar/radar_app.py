"""Entry point for hosting the radar app with API and frontend."""
from flask import Flask

from mlre.radar import radar_api_server, radar_database, radar_frontend


def create_default_app() -> Flask:
    """Creates an app instance with the default configuration."""
    database = radar_database.RadarDatabase()
    app = Flask(__name__)
    app.register_blueprint(
        radar_api_server.create_api_server_blueprint(database))
    app.register_blueprint(radar_frontend.create_frontend_blueprint(database))
    return app


__all__ = ["create_default_app"]

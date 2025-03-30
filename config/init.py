# config/init.py

from .settings import API_KEY, DATABASE_URL, DEBUG, SECRET_KEY

# Additional configuration options


class Config:
    @staticmethod
    def init_app(app):
        # Register blueprints
        from . import blueprints

        app.register_blueprint(blueprints.crypto_bp)
        app.register_blueprint(blueprints.data_bp)

        # Configure logging
        if not app.debug:
            import logging
            from logging.handlers import RotatingFileHandler

            file_handler = RotatingFileHandler(
                "app.log", maxBytes=10240, backupCount=10
            )
            file_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
                )
            )
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

            app.logger.setLevel(logging.INFO)
            app.logger.info("Application startup")

        return None

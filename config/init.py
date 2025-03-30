import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from .settings import API_KEY, DATABASE_URL, DEBUG, SECRET_KEY

# Additional configuration options
class Config:
    @staticmethod
    def init_app(app: Flask) -> None:
        """Initialize the application with the given configuration."""
        # Register blueprints
        from . import blueprints

        try:
            app.register_blueprint(blueprints.crypto_bp)
            app.register_blueprint(blueprints.data_bp)
            app.logger.info("Blueprints registered successfully.")
        except Exception as e:
            app.logger.error(f"Error registering blueprints: {e}")

        # Configure logging
        if not app.debug:
            log_file = os.environ.get('LOG_FILE', 'app.log')
            max_bytes = int(os.environ.get('LOG_MAX_BYTES', 10240))
            backup_count = int(os.environ.get('LOG_BACKUP_COUNT', 10))

            file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
            file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

            app.logger.setLevel(logging.INFO)
            app.logger.info("Application startup")

        # Log configuration details
        app.logger.info("Configuration loaded:")
        app.logger.info(f"API_KEY: {API_KEY}")
        app.logger.info(f"DATABASE_URL: {DATABASE_URL}")
        app.logger.info(f"DEBUG: {DEBUG}")
        app.logger.info(f"SECRET_KEY: {SECRET_KEY}")

        return None

# tests/api_endpoints/test_api_endpoints.py

import pytest
from unittest.mock import MagicMock, patch
from flask import Flask
from api_endpoints import crypto_bp, data_bp

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(crypto_bp)
    app.register_blueprint(data_bp)
    return app

def test_crypto_route(app):
    # Arrange
    with app.test_client() as client:
        # Act
        response = client.get("/crypto/BTC")

        # Assert
        assert response.status_code == 200
        assert response.json == {"BTC": {"price": "10000"}}

def test_data_route(app):
    # Arrange
    with app.test_client() as client:
        # Act
        response = client.get("/data")

        # Assert
        assert response.status_code == 200
        assert response.json == {"BTC": {"price": "10000"}}

@patch("crypto_connector.CryptoConnector.get_crypto_data")
def test_crypto_route_exception(mock_get_crypto_data, app):
    # Arrange
    mock_get_crypto_data.side_effect = Exception("Test exception")

    with app.test_client() as client:
        # Act and Assert
        response = client.get("/crypto/BTC")

        assert response.status_code == 500

@patch("data_processor.DataProcessor.process_data")
def test_data_route_exception(mock_process_data, app):
    # Arrange
    mock_process_data.side_effect = Exception("Test exception")

    with app.test_client() as client:
        # Act and Assert
        response = client.get("/data")

        assert response.status_code == 500

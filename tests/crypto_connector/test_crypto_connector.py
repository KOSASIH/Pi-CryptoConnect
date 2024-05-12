# tests/crypto_connector/test_crypto_connector.py

from unittest.mock import MagicMock, patch

import pytest
from crypto_connector import CryptoConnector


@pytest.fixture
def crypto_connector():
    return CryptoConnector()


def test_get_crypto_data(crypto_connector):
    # Arrange
    mock_response = MagicMock()
    mock_response.json.return_value = {"BTC": {"price": "10000"}}
    mock_get = MagicMock(return_value=mock_response)

    with patch("requests.get", mock_get):
        # Act
        result = crypto_connector.get_crypto_data("BTC")

        # Assert
        assert result == {"BTC": {"price": "10000"}}
        mock_get.assert_called_once_with("https://api.example.com/crypto/BTC")


def test_get_crypto_data_exception(crypto_connector):
    # Arrange
    mock_get = MagicMock(side_effect=Exception("Test exception"))

    with patch("requests.get", mock_get):
        # Act and Assert
        with pytest.raises(Exception):
            crypto_connector.get_crypto_data("BTC")

        mock_get.assert_called_once_with("https://api.example.com/crypto/BTC")

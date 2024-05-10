# tests/data_processor/test_data_processor.py

import pytest
from unittest.mock import MagicMock
from data_processor import DataProcessor

@pytest.fixture
def data_processor():
    return DataProcessor()

def test_process_data(data_processor):
    # Arrange
    mock_crypto_data = {"BTC": {"price": "10000"}}
    mock_data_processor = MagicMock()

    data_processor.get_crypto_data = mock_data_processor
    mock_data_processor.return_value = mock_crypto_data

    # Act
    result = data_processor.process_data()

    # Assert
    assert result == mock_crypto_data
    data_processor.get_crypto_data.assert_called_once()

def test_process_data_exception(data_processor):
    # Arrange
    mock_data_processor = MagicMock(side_effect=Exception("Test exception"))

    data_processor.get_crypto_data = mock_data_processor

    # Act and Assert
    with pytest.raises(Exception):
        data_processor.process_data()

    data_processor.get_crypto_data.assert_called_once()

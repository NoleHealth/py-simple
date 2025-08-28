"""Tests for the main module."""

from unittest.mock import Mock

from py_simple.main import process_data, setup_logging


def test_setup_logging():
    """Test logging setup."""
    logger = setup_logging("INFO")
    assert logger is not None
    assert logger.name == "py_simple.main"


def test_process_data():
    """Test data processing functionality."""
    # Sample data similar to JSONPlaceholder format
    sample_data = [
        {"userId": 1, "id": 1, "title": "Test post 1", "body": "Body 1"},
        {"userId": 1, "id": 2, "title": "Test post 2", "body": "Body 2"},
        {"userId": 2, "id": 3, "title": "Another post", "body": "Body 3"},
    ]

    mock_logger = Mock()
    result = process_data(sample_data, mock_logger)

    # Verify the structure of processed data
    assert "total_items" in result
    assert "processed_at" in result
    assert "summary" in result
    assert "items" in result

    # Verify the values
    assert result["total_items"] == 3
    assert result["summary"]["unique_users"] == 2
    assert result["summary"]["items_by_user"]["1"] == 2
    assert result["summary"]["items_by_user"]["2"] == 1
    assert result["items"] == sample_data

    # Verify logging was called
    mock_logger.info.assert_called()


def test_process_data_empty():
    """Test data processing with empty data."""
    mock_logger = Mock()
    result = process_data([], mock_logger)

    assert result["total_items"] == 0
    assert result["summary"]["unique_users"] == 0
    assert result["summary"]["average_title_length"] == 0
    assert result["items"] == []

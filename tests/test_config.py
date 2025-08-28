"""Tests for the config module."""

import os
from unittest.mock import patch

from py_simple.config import Config


def test_config_defaults():
    """Test configuration with default values."""
    with patch.dict(os.environ, {}, clear=True):
        config = Config()

        assert config.api_url == "https://jsonplaceholder.typicode.com/posts"
        assert config.api_timeout == 30
        assert config.data_folder == "data"
        assert config.output_prefix == "processed_"
        assert config.log_level == "INFO"


def test_config_custom_values():
    """Test configuration with custom environment variables."""
    custom_env = {
        "API_URL": "https://api.example.com/data",
        "API_TIMEOUT": "60",
        "DATA_FOLDER": "custom_data",
        "OUTPUT_PREFIX": "custom_",
        "LOG_LEVEL": "DEBUG",
    }

    with patch.dict(os.environ, custom_env, clear=True):
        config = Config()

        assert config.api_url == "https://api.example.com/data"
        assert config.api_timeout == 60
        assert config.data_folder == "custom_data"
        assert config.output_prefix == "custom_"
        assert config.log_level == "DEBUG"


def test_config_partial_override():
    """Test configuration with partial environment variable override."""
    partial_env = {"API_URL": "https://custom.api.com/endpoint", "LOG_LEVEL": "WARNING"}

    with patch.dict(os.environ, partial_env, clear=True):
        config = Config()

        assert config.api_url == "https://custom.api.com/endpoint"
        assert config.api_timeout == 30  # default
        assert config.data_folder == "data"  # default
        assert config.output_prefix == "processed_"  # default
        assert config.log_level == "WARNING"

"""Configuration management using environment variables."""

import os
from typing import Optional

from dotenv import load_dotenv


class Config:
    """Configuration class that loads settings from environment variables."""

    def __init__(self, env_file: Optional[str] = None, api_url: Optional[str] = None, data_folder: Optional[str] = None):
        """Initialize configuration, loading from .env file if it exists.
        
        Args:
            env_file: Optional path to .env file
            api_url: Optional override for API URL (from CLI arguments)
            data_folder: Optional override for data folder (from CLI arguments)
        """
        if env_file:
            load_dotenv(env_file)
        else:
            load_dotenv()  # Load from .env in current directory if it exists

        # Store CLI overrides
        self._api_url_override = api_url
        self._data_folder_override = data_folder

    @property
    def api_url(self) -> str:
        """Get the API URL from CLI arguments, environment variables, or default."""
        # Priority: CLI override > environment variable > default
        if self._api_url_override:
            return self._api_url_override
        return os.getenv("API_URL", "https://jsonplaceholder.typicode.com/posts")

    @property
    def api_timeout(self) -> int:
        """Get the API timeout in seconds."""
        return int(os.getenv("API_TIMEOUT", "30"))

    @property
    def data_folder(self) -> str:
        """Get the data folder path from CLI arguments, environment variables, or default."""
        # Priority: CLI override > environment variable > default
        if self._data_folder_override:
            return self._data_folder_override
        return os.getenv("DATA_FOLDER", "data")

    @property
    def output_prefix(self) -> str:
        """Get the output file prefix."""
        return os.getenv("OUTPUT_PREFIX", "processed_")

    @property
    def log_level(self) -> str:
        """Get the log level."""
        return os.getenv("LOG_LEVEL", "INFO")

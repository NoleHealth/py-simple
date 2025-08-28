"""Configuration management using environment variables."""

import os
from typing import Optional

from dotenv import load_dotenv


class Config:
    """Configuration class that loads settings from environment variables."""

    def __init__(self, env_file: Optional[str] = None):
        """Initialize configuration, loading from .env file if it exists."""
        if env_file:
            load_dotenv(env_file)
        else:
            load_dotenv()  # Load from .env in current directory if it exists

    @property
    def api_url(self) -> str:
        """Get the API URL from environment variables."""
        return os.getenv("API_URL", "https://jsonplaceholder.typicode.com/posts")

    @property
    def api_timeout(self) -> int:
        """Get the API timeout in seconds."""
        return int(os.getenv("API_TIMEOUT", "30"))

    @property
    def data_folder(self) -> str:
        """Get the data folder path."""
        return os.getenv("DATA_FOLDER", "data")

    @property
    def output_prefix(self) -> str:
        """Get the output file prefix."""
        return os.getenv("OUTPUT_PREFIX", "processed_")

    @property
    def log_level(self) -> str:
        """Get the log level."""
        return os.getenv("LOG_LEVEL", "INFO")

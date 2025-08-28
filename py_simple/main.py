"""Main script for fetching and processing API data."""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import requests

from .config import Config


def setup_logging(log_level: str) -> logging.Logger:
    """Set up logging configuration."""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    return logging.getLogger(__name__)


def ensure_data_folder(data_folder: str) -> Path:
    """Ensure the data folder exists."""
    data_path = Path(data_folder)
    data_path.mkdir(exist_ok=True)
    return data_path


def fetch_api_data(
    url: str, timeout: int, logger: logging.Logger
) -> List[Dict[str, Any]]:
    """Fetch data from the API."""
    try:
        logger.info(f"Fetching data from: {url}")
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()

        data = response.json()
        logger.info(f"Successfully fetched {len(data)} items")
        return data

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch data from API: {e}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON response: {e}")
        raise


def process_data(data: List[Dict[str, Any]], logger: logging.Logger) -> Dict[str, Any]:
    """Process the fetched data."""
    logger.info("Processing fetched data...")

    processed = {
        "total_items": len(data),
        "processed_at": datetime.now().isoformat(),
        "summary": {
            "unique_users": len(set(item.get("userId", 0) for item in data)),
            "average_title_length": sum(len(item.get("title", "")) for item in data)
            / len(data)
            if data
            else 0,
            "items_by_user": {},
        },
        "items": data,
    }

    # Count items by user
    for item in data:
        user_id = str(item.get("userId", "unknown"))
        processed["summary"]["items_by_user"][user_id] = (
            processed["summary"]["items_by_user"].get(user_id, 0) + 1
        )

    logger.info(
        f"Processed {processed['total_items']} items from {processed['summary']['unique_users']} users"
    )
    return processed


def save_data(
    data: Dict[str, Any], data_folder: Path, prefix: str, logger: logging.Logger
) -> None:
    """Save processed data to files."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save raw data
    raw_file = data_folder / f"{prefix}raw_{timestamp}.json"
    with open(raw_file, "w", encoding="utf-8") as f:
        json.dump(data["items"], f, indent=2, ensure_ascii=False)
    logger.info(f"Raw data saved to: {raw_file}")

    # Save processed summary
    summary = {k: v for k, v in data.items() if k != "items"}
    summary_file = data_folder / f"{prefix}summary_{timestamp}.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    logger.info(f"Summary saved to: {summary_file}")


def main() -> None:
    """Main function."""
    try:
        # Load configuration
        config = Config()

        # Set up logging
        logger = setup_logging(config.log_level)

        logger.info("Starting py-simple data processing...")

        # Ensure data folder exists
        data_folder = ensure_data_folder(config.data_folder)

        # Fetch data from API
        raw_data = fetch_api_data(config.api_url, config.api_timeout, logger)

        # Process the data
        processed_data = process_data(raw_data, logger)

        # Save the results
        save_data(processed_data, data_folder, config.output_prefix, logger)

        logger.info("Processing completed successfully!")

    except Exception as e:
        logging.error(f"Application failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

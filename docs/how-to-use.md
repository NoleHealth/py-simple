# How to Use py-simple

This guide explains how to use the py-simple application for fetching and processing API data.

## Overview

The py-simple application:
1. Fetches JSON data from a public API (JSONPlaceholder by default)
2. Processes the data to generate useful statistics
3. Saves both raw and processed data to the `data/` folder

## Quick Start

### Basic Usage
```bash
# Run with default settings
make run

# Or run directly
uv run python -m py_simple.main
```

This will:
- Fetch data from the default API (JSONPlaceholder posts)
- Process the data and generate statistics
- Save files to the `data/` folder with timestamps

### With Custom Configuration
```bash
# Create your own .env file from the example
cp .env.example .env

# Edit .env with your preferred settings
# Then run normally
make run
```

## Configuration

The application uses environment variables for configuration. You can set these in a `.env` file or as environment variables.

### Environment Variables

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `API_URL` | The API endpoint to fetch data from | `https://jsonplaceholder.typicode.com/posts` |
| `API_TIMEOUT` | Request timeout in seconds | `30` |
| `DATA_FOLDER` | Directory to save output files | `data` |
| `OUTPUT_PREFIX` | Prefix for output filenames | `processed_` |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) | `INFO` |

### Example .env Configuration
```env
# Custom API endpoint
API_URL=https://jsonplaceholder.typicode.com/users
API_TIMEOUT=60

# Custom output settings
DATA_FOLDER=my_data
OUTPUT_PREFIX=api_data_

# Detailed logging
LOG_LEVEL=DEBUG
```

## Running Examples

### Example 1: Default JSONPlaceholder Posts
```bash
make run
```
Fetches blog posts and generates user statistics.

### Example 2: JSONPlaceholder Users
```bash
API_URL=https://jsonplaceholder.typicode.com/users make run
```
Fetches user data instead of posts.

### Example 3: Custom API with Environment Variables
```bash
# Set environment variables inline
API_URL=https://api.github.com/users \
API_TIMEOUT=45 \
DATA_FOLDER=github_data \
make run
```

### Example 4: Different Output Location
```bash
# Create custom data directory
mkdir -p custom_output

# Run with custom settings
DATA_FOLDER=custom_output \
OUTPUT_PREFIX=github_users_ \
API_URL=https://api.github.com/users \
make run
```

## Understanding the Output

The application creates two types of files in the data folder:

### Raw Data File
**Filename**: `{prefix}raw_{timestamp}.json`

Contains the original API response data without modifications.

```json
[
  {
    "userId": 1,
    "id": 1,
    "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
    "body": "quia et suscipit..."
  },
  ...
]
```

### Summary File
**Filename**: `{prefix}summary_{timestamp}.json`

Contains processed statistics and metadata:

```json
{
  "total_items": 100,
  "processed_at": "2024-01-15T10:30:45.123456",
  "summary": {
    "unique_users": 10,
    "average_title_length": 58.2,
    "items_by_user": {
      "1": 10,
      "2": 10,
      ...
    }
  }
}
```

## Command Line Options

### Using the Makefile
```bash
make help           # Show available commands
make run            # Run the application
make lint           # Run code linting
make format         # Format code
make test           # Run tests
make clean          # Clean up temporary files
```

### Direct Python Execution
```bash
# Run the module
uv run python -m py_simple.main

# With custom Python path
PYTHONPATH=. python -m py_simple.main

# Using the installed script (after pip install -e .)
py-simple
```

## Logging

The application provides detailed logging to help you understand what's happening:

```bash
# Example output with INFO logging
2024-01-15 10:30:42 - py_simple.main - INFO - Starting py-simple data processing...
2024-01-15 10:30:42 - py_simple.main - INFO - Fetching data from: https://jsonplaceholder.typicode.com/posts
2024-01-15 10:30:43 - py_simple.main - INFO - Successfully fetched 100 items
2024-01-15 10:30:43 - py_simple.main - INFO - Processing fetched data...
2024-01-15 10:30:43 - py_simple.main - INFO - Processed 100 items from 10 users
2024-01-15 10:30:43 - py_simple.main - INFO - Raw data saved to: data/processed_raw_20240115_103043.json
2024-01-15 10:30:43 - py_simple.main - INFO - Summary saved to: data/processed_summary_20240115_103043.json
2024-01-15 10:30:43 - py_simple.main - INFO - Processing completed successfully!
```

### Adjusting Log Level
```bash
# Debug level logging (very detailed)
LOG_LEVEL=DEBUG make run

# Warning level only (minimal output)
LOG_LEVEL=WARNING make run
```

## Working with Different APIs

The application can work with any JSON API. Here are some examples:

### GitHub API
```bash
API_URL=https://api.github.com/users make run
```

### Cat Facts API
```bash
API_URL=https://catfact.ninja/facts make run
```

### Custom REST API
```bash
API_URL=https://your-api.com/endpoint \
API_TIMEOUT=120 \
make run
```

**Note**: Some APIs may require authentication or have different response structures. You may need to modify the code for complex APIs.

## Troubleshooting

### Common Issues

#### No data files generated
- Check that the `data/` folder exists and is writable
- Verify the API URL is accessible
- Check the logs for error messages

#### API request fails
```bash
# Test the API manually first
curl -v "https://jsonplaceholder.typicode.com/posts"

# Run with debug logging
LOG_LEVEL=DEBUG make run
```

#### Permission denied errors
```bash
# Make sure data folder is writable
chmod 755 data/

# Check if data folder exists
ls -la data/
```

#### Import errors
```bash
# Make sure you've installed dependencies
make install-dev

# Check your virtual environment is activated
which python
```

### Getting Help

If you encounter issues:
1. Check the log output for detailed error messages
2. Verify your configuration in `.env`
3. Test the API endpoint manually with `curl` or a web browser
4. Make sure all dependencies are installed correctly

## Next Steps

- **Customization**: Modify `py_simple/main.py` to add custom data processing logic
- **New APIs**: Adapt the code to work with different API response formats
- **Automation**: Set up cron jobs or scheduled tasks to run the application periodically
- **Integration**: Use the processed data in other applications or analysis tools

For development and contribution information, see:
- [Installation Guide](installation.md) - Setup instructions
- [Git Commands](git-commands.md) - Development workflow
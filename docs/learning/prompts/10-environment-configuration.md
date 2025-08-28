# Learning Prompt 10: Environment Configuration and Secrets Management

## Objective
Master configuration management patterns, environment-specific settings, secrets handling, and configuration validation in Python applications.

## Prerequisites
Complete prompts #1-9 to understand the codebase, error handling, and application architecture.

## Your Task
Enhance the configuration system of the py-simple project to handle multiple environments, secure secrets management, and robust configuration validation.

## Prompt to Use with AI Assistant

```
Create a comprehensive configuration management system for the py_simple project. Cover:

1. **Configuration Architecture Design**
   - Analyze the current Config class and identify limitations
   - Design a hierarchical configuration system (defaults < env files < environment variables < CLI args)
   - Implement configuration validation and type checking
   - Create environment-specific configuration profiles
   - Add configuration documentation and schema definition

2. **Multi-Environment Support**
   - Create configurations for development, testing, staging, and production
   - Implement environment detection and automatic profile selection
   - Handle environment-specific overrides and customizations
   - Create configuration templates and examples
   - Implement configuration inheritance and composition

3. **Secrets Management**
   - Implement secure handling of sensitive configuration values
   - Integration with external secret management systems (AWS Secrets Manager, HashiCorp Vault)
   - Local development secrets handling with .env files
   - Environment variable masking and secure logging
   - Configuration encryption and decryption

4. **Configuration Validation**
   - Implement comprehensive input validation using Pydantic or similar
   - Create custom validators for business rules
   - Add configuration consistency checks
   - Implement runtime configuration updates and validation
   - Create configuration testing and verification tools

5. **Advanced Configuration Patterns**
   - Dynamic configuration loading and hot-reloading
   - Configuration templating and variable substitution
   - Feature flags and configuration-driven behavior
   - Configuration versioning and migration
   - Configuration monitoring and change detection

6. **Developer Experience**
   - Create configuration documentation and examples
   - Implement configuration debugging tools
   - Add configuration validation in development
   - Create setup scripts and configuration wizards
   - Design configuration testing utilities

Create your comprehensive configuration guide in:
docs/learning/$(date +%Y%m%d%H%M)-environment-configuration-guide.md

Include:
- Complete configuration system implementation
- Environment-specific configuration files
- Secrets management examples
- Configuration validation schemas
- Developer tooling and utilities
```

## Key Learning Points
After completing this exercise, you should understand:
- Configuration hierarchy and precedence rules
- Environment-specific configuration management
- Secrets management best practices and tools
- Configuration validation and type safety
- Feature flags and configuration-driven development
- Configuration testing and verification strategies
- Security considerations for configuration data

## Configuration Hierarchy Design

### 1. Configuration Sources (Priority Order)
1. **Command Line Arguments** (Highest Priority)
2. **Environment Variables**
3. **Environment-Specific Config Files** (.env.production, .env.development)
4. **General Config File** (.env)
5. **Default Values** (Lowest Priority)

### 2. Environment Profiles
- **development**: Local development with debug features
- **testing**: Test environment with test data and mocks
- **staging**: Production-like environment for pre-deployment testing
- **production**: Live environment with security and performance optimizations

### 3. Configuration Categories
- **Application Settings**: Core application behavior
- **External Services**: API endpoints, timeouts, credentials
- **Infrastructure**: Database connections, caching, queuing
- **Observability**: Logging, monitoring, metrics
- **Security**: Authentication, encryption, rate limiting

## Advanced Configuration Implementation

### 1. Pydantic-Based Configuration
```python
from pydantic import BaseSettings, validator, HttpUrl
from typing import Optional, Literal
import os

class Config(BaseSettings):
    """Application configuration with validation."""
    
    # Environment detection
    environment: Literal['development', 'testing', 'staging', 'production'] = 'development'
    debug: bool = False
    
    # API Configuration
    api_url: HttpUrl = 'https://jsonplaceholder.typicode.com/posts'
    api_timeout: int = 30
    api_retry_attempts: int = 3
    
    # Output Configuration
    data_folder: str = 'data'
    output_prefix: str = 'processed_'
    
    # Logging Configuration
    log_level: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR'] = 'INFO'
    log_format: Literal['json', 'text'] = 'text'
    
    # Security Configuration
    api_key: Optional[str] = None
    
    @validator('api_timeout')
    def validate_timeout(cls, v):
        if v <= 0 or v > 300:
            raise ValueError('API timeout must be between 1 and 300 seconds')
        return v
    
    @validator('environment')
    def validate_environment_settings(cls, v, values):
        if v == 'production' and values.get('debug'):
            raise ValueError('Debug mode cannot be enabled in production')
        return v
    
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = False
```

### 2. Environment-Specific Configuration Loading
```python
import os
from pathlib import Path

def load_config(env: str = None) -> Config:
    """Load configuration for specific environment."""
    if env is None:
        env = os.getenv('ENVIRONMENT', 'development')
    
    # Load base configuration
    base_env_file = Path('.env')
    env_specific_file = Path(f'.env.{env}')
    
    env_files = []
    if base_env_file.exists():
        env_files.append(str(base_env_file))
    if env_specific_file.exists():
        env_files.append(str(env_specific_file))
    
    return Config(
        _env_file=env_files,
        environment=env
    )
```

### 3. Secrets Management Integration
```python
import boto3
from typing import Dict, Any
import json

class SecretsManager:
    """Manage secrets from various sources."""
    
    def __init__(self, environment: str):
        self.environment = environment
        self.secrets_cache = {}
    
    def get_secret(self, secret_name: str) -> str:
        """Get secret value from appropriate source."""
        if secret_name in self.secrets_cache:
            return self.secrets_cache[secret_name]
        
        if self.environment == 'development':
            # Use .env file for development
            value = os.getenv(secret_name)
        else:
            # Use AWS Secrets Manager for production
            value = self._get_from_aws_secrets(secret_name)
        
        if value:
            self.secrets_cache[secret_name] = value
        
        return value
    
    def _get_from_aws_secrets(self, secret_name: str) -> str:
        """Retrieve secret from AWS Secrets Manager."""
        client = boto3.client('secretsmanager')
        try:
            response = client.get_secret_value(SecretId=secret_name)
            return response['SecretString']
        except Exception as e:
            logger.error(f"Failed to retrieve secret {secret_name}: {e}")
            return None
```

### 4. Configuration Schema and Documentation
```python
from typing import Dict, Any
import yaml

CONFIG_SCHEMA = {
    "type": "object",
    "required": ["api_url", "data_folder"],
    "properties": {
        "environment": {
            "type": "string",
            "enum": ["development", "testing", "staging", "production"],
            "description": "Application environment"
        },
        "api_url": {
            "type": "string",
            "format": "uri",
            "description": "API endpoint URL for data fetching"
        },
        "api_timeout": {
            "type": "integer",
            "minimum": 1,
            "maximum": 300,
            "description": "API request timeout in seconds"
        },
        "data_folder": {
            "type": "string",
            "description": "Directory for output files"
        },
        "log_level": {
            "type": "string",
            "enum": ["DEBUG", "INFO", "WARNING", "ERROR"],
            "description": "Logging verbosity level"
        }
    }
}

def generate_config_docs() -> str:
    """Generate configuration documentation."""
    docs = "# Configuration Reference\n\n"
    for key, spec in CONFIG_SCHEMA["properties"].items():
        docs += f"## {key.upper()}\n"
        docs += f"- **Type**: {spec['type']}\n"
        docs += f"- **Description**: {spec.get('description', 'No description')}\n"
        if 'enum' in spec:
            docs += f"- **Valid Values**: {', '.join(spec['enum'])}\n"
        if 'default' in spec:
            docs += f"- **Default**: {spec['default']}\n"
        docs += "\n"
    return docs
```

## Environment Configuration Files

### 1. Base Configuration (.env)
```env
# Base configuration - common to all environments
API_URL=https://jsonplaceholder.typicode.com/posts
API_TIMEOUT=30
DATA_FOLDER=data
OUTPUT_PREFIX=processed_
LOG_LEVEL=INFO
LOG_FORMAT=text
```

### 2. Development Configuration (.env.development)
```env
# Development-specific overrides
DEBUG=true
LOG_LEVEL=DEBUG
API_TIMEOUT=60
# Use local test server if available
API_URL=http://localhost:3000/api/posts
```

### 3. Production Configuration (.env.production)
```env
# Production-specific settings
DEBUG=false
LOG_LEVEL=INFO
LOG_FORMAT=json
API_TIMEOUT=30
# Production API with authentication
API_URL=https://prod-api.company.com/v1/posts
API_KEY=use_secrets_manager
```

### 4. Testing Configuration (.env.testing)
```env
# Testing-specific settings
DEBUG=false
LOG_LEVEL=WARNING
API_URL=https://httpbin.org/json
DATA_FOLDER=tests/tmp
OUTPUT_PREFIX=test_
```

## Configuration Validation and Testing

### 1. Configuration Validation Tests
```python
import pytest
from pydantic import ValidationError

def test_valid_configuration():
    """Test that valid configuration loads successfully."""
    config = Config(
        api_url='https://api.example.com',
        api_timeout=30,
        data_folder='data'
    )
    assert config.api_timeout == 30

def test_invalid_timeout():
    """Test that invalid timeout raises validation error."""
    with pytest.raises(ValidationError) as exc_info:
        Config(api_timeout=-5)
    assert 'API timeout must be between' in str(exc_info.value)

def test_production_debug_validation():
    """Test that debug cannot be enabled in production."""
    with pytest.raises(ValidationError) as exc_info:
        Config(environment='production', debug=True)
    assert 'Debug mode cannot be enabled' in str(exc_info.value)
```

### 2. Configuration Testing Utilities
```python
class ConfigTester:
    """Utilities for testing configuration."""
    
    def __init__(self, config: Config):
        self.config = config
    
    def validate_api_connectivity(self) -> bool:
        """Test if API is reachable with current configuration."""
        try:
            response = requests.get(
                str(self.config.api_url),
                timeout=self.config.api_timeout
            )
            return response.status_code == 200
        except Exception:
            return False
    
    def validate_file_permissions(self) -> bool:
        """Test if output directory is writable."""
        try:
            Path(self.config.data_folder).mkdir(exist_ok=True)
            test_file = Path(self.config.data_folder) / 'test_write.tmp'
            test_file.write_text('test')
            test_file.unlink()
            return True
        except Exception:
            return False
    
    def run_all_validations(self) -> Dict[str, bool]:
        """Run all configuration validations."""
        return {
            'api_connectivity': self.validate_api_connectivity(),
            'file_permissions': self.validate_file_permissions(),
        }
```

## Feature Flags and Dynamic Configuration

### 1. Feature Flag Implementation
```python
class FeatureFlags:
    """Manage feature flags and dynamic configuration."""
    
    def __init__(self, config: Config):
        self.config = config
        self.flags = self._load_feature_flags()
    
    def _load_feature_flags(self) -> Dict[str, bool]:
        """Load feature flags from configuration."""
        return {
            'enable_retry_logic': True,
            'enable_metrics_collection': self.config.environment != 'development',
            'enable_api_caching': self.config.environment == 'production',
            'enable_data_validation': True,
        }
    
    def is_enabled(self, flag_name: str) -> bool:
        """Check if a feature flag is enabled."""
        return self.flags.get(flag_name, False)
    
    def enable_flag(self, flag_name: str):
        """Enable a feature flag at runtime."""
        self.flags[flag_name] = True
    
    def disable_flag(self, flag_name: str):
        """Disable a feature flag at runtime."""
        self.flags[flag_name] = False
```

## Follow-up Questions
1. How would you handle configuration changes that require application restart?
2. What's the best way to validate that all required configuration is present?
3. How would you implement configuration rollback in case of invalid changes?
4. What security measures should be in place for configuration management?
5. How would you handle configuration conflicts between different sources?

## Configuration Anti-Patterns to Avoid
1. **Hardcoded Values**: Configuration values embedded in code
2. **Environment Detection in Code**: Logic that changes based on environment
3. **Insecure Secrets Storage**: Passwords and keys in plain text files
4. **No Validation**: Accepting any configuration values without validation
5. **Global Configuration**: Configuration accessible from anywhere in the codebase

## Next Steps
After mastering environment configuration, you'll explore package management and dependencies in prompt #11.
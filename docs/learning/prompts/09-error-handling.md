# Learning Prompt 9: Advanced Error Handling and Logging

## Objective
Master robust error handling, logging strategies, and resilience patterns in Python applications. Learn to create applications that fail gracefully and provide excellent debugging information.

## Prerequisites
Complete prompts #1-8 to understand the codebase, testing strategies, and application architecture.

## Your Task
Enhance the error handling and logging capabilities of the py-simple project, implementing comprehensive error recovery, structured logging, and monitoring-ready output.

## Prompt to Use with AI Assistant

```
Create a comprehensive error handling and logging strategy for the py_simple project. Cover:

1. **Error Analysis and Classification**
   - Catalog all possible error scenarios in the current code
   - Classify errors by type: recoverable vs non-recoverable, expected vs unexpected
   - Identify missing error handling in the current implementation
   - Analyze the error propagation chain and impact
   - Map errors to appropriate handling strategies

2. **Robust Error Handling Implementation**
   - Implement comprehensive try-catch blocks with specific exception handling
   - Add retry logic with exponential backoff for transient failures
   - Create custom exception classes for domain-specific errors
   - Implement circuit breaker patterns for external service calls
   - Add graceful degradation for non-critical failures

3. **Advanced Logging Strategy**
   - Design structured logging with consistent format and metadata
   - Implement contextual logging with correlation IDs
   - Add performance logging and metrics collection
   - Create different log levels for different audiences
   - Implement log sampling and rate limiting for high-volume scenarios

4. **Monitoring and Observability**
   - Add health check endpoints and status monitoring
   - Implement metrics collection for key business and technical indicators
   - Create alerting strategies for different error types
   - Add distributed tracing capabilities
   - Design dashboards for operational monitoring

5. **Error Recovery and Resilience**
   - Implement automatic recovery mechanisms where appropriate
   - Add manual intervention points for complex failures
   - Create data consistency and integrity checks
   - Implement backup and rollback strategies
   - Design failover and redundancy approaches

6. **User Experience and Communication**
   - Provide helpful error messages for different audiences (users, operators, developers)
   - Implement progressive error disclosure
   - Add error reporting and feedback mechanisms
   - Create troubleshooting guides and runbooks
   - Design error notification and escalation procedures

Create your comprehensive error handling guide in:
docs/learning/$(date +%Y%m%d%H%M)-error-handling-logging-guide.md

Include:
- Complete error handling implementation
- Structured logging configuration
- Monitoring and alerting setup
- Error recovery procedures
- Troubleshooting and debugging guides
```

## Key Learning Points
After completing this exercise, you should understand:
- Different types of errors and appropriate handling strategies
- Retry patterns and backoff strategies
- Structured logging and observability practices
- Circuit breaker and resilience patterns
- Custom exception design and hierarchy
- Monitoring and alerting best practices
- Error communication and user experience

## Error Classification Framework

### 1. Network and External Service Errors
- **Transient Failures**: Temporary network issues, API rate limits
- **Permanent Failures**: Invalid credentials, service unavailable
- **Timeout Errors**: Slow responses, connection timeouts
- **Data Errors**: Invalid response format, missing data

### 2. File System and I/O Errors
- **Permission Errors**: Insufficient privileges, read-only directories
- **Space Errors**: Disk full, quota exceeded
- **Path Errors**: Invalid paths, missing directories
- **Corruption Errors**: Damaged files, incomplete writes

### 3. Configuration and Environment Errors
- **Missing Configuration**: Required environment variables missing
- **Invalid Configuration**: Malformed URLs, invalid timeouts
- **Environment Issues**: Missing dependencies, version conflicts
- **Security Errors**: Certificate issues, authentication failures

### 4. Data Processing Errors
- **Validation Errors**: Invalid data format, missing required fields
- **Transformation Errors**: JSON parsing failures, encoding issues
- **Business Logic Errors**: Invalid business rules, constraint violations
- **Resource Errors**: Memory exhaustion, processing limits

## Advanced Error Handling Patterns

### 1. Retry with Exponential Backoff
```python
import time
import random
from typing import Any, Callable, Type

def retry_with_backoff(
    func: Callable,
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exceptions: tuple[Type[Exception], ...] = (Exception,)
) -> Any:
    """Retry function with exponential backoff and jitter."""
    for attempt in range(max_retries + 1):
        try:
            return func()
        except exceptions as e:
            if attempt == max_retries:
                raise
            
            delay = min(base_delay * (2 ** attempt), max_delay)
            jitter = random.uniform(0, delay * 0.1)
            time.sleep(delay + jitter)
            
            logger.warning(
                f"Attempt {attempt + 1} failed, retrying in {delay:.2f}s: {e}"
            )
```

### 2. Circuit Breaker Pattern
```python
class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN

    def call(self, func: Callable) -> Any:
        if self.state == 'OPEN':
            if time.time() - self.last_failure_time < self.timeout:
                raise CircuitBreakerOpenError("Circuit breaker is OPEN")
            else:
                self.state = 'HALF_OPEN'

        try:
            result = func()
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise
```

### 3. Custom Exception Hierarchy
```python
class PySimpleError(Exception):
    """Base exception for py-simple application."""
    pass

class ConfigurationError(PySimpleError):
    """Configuration-related errors."""
    pass

class APIError(PySimpleError):
    """API-related errors."""
    def __init__(self, message: str, status_code: int = None, response_body: str = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body

class DataProcessingError(PySimpleError):
    """Data processing errors."""
    pass

class FileOperationError(PySimpleError):
    """File system operation errors."""
    pass
```

## Structured Logging Implementation

### 1. JSON Structured Logging
```python
import json
import logging
from datetime import datetime
from typing import Dict, Any

class StructuredFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }
        
        # Add extra fields if present
        if hasattr(record, 'extra_fields'):
            log_entry.update(record.extra_fields)
            
        return json.dumps(log_entry)

def setup_structured_logging(level: str = 'INFO') -> logging.Logger:
    logger = logging.getLogger('py_simple')
    handler = logging.StreamHandler()
    formatter = StructuredFormatter()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(getattr(logging, level.upper()))
    return logger
```

### 2. Contextual Logging with Correlation IDs
```python
import contextvars
import uuid

# Context variable for correlation ID
correlation_id: contextvars.ContextVar[str] = contextvars.ContextVar(
    'correlation_id', default=None
)

class CorrelationIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.correlation_id = correlation_id.get('unknown')
        return True

def with_correlation_id(func: Callable) -> Callable:
    """Decorator to add correlation ID to function execution."""
    def wrapper(*args, **kwargs):
        if not correlation_id.get(None):
            correlation_id.set(str(uuid.uuid4()))
        return func(*args, **kwargs)
    return wrapper
```

### 3. Performance and Metrics Logging
```python
import time
from functools import wraps

def log_performance(func: Callable) -> Callable:
    """Decorator to log function performance metrics."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            success = True
            return result
        except Exception as e:
            success = False
            raise
        finally:
            execution_time = time.time() - start_time
            logger.info(
                f"Function executed",
                extra={
                    'extra_fields': {
                        'function': func.__name__,
                        'execution_time': execution_time,
                        'success': success,
                        'args_count': len(args),
                        'kwargs_count': len(kwargs)
                    }
                }
            )
    return wrapper
```

## Monitoring and Alerting Strategy

### 1. Health Checks
```python
def health_check() -> Dict[str, Any]:
    """Comprehensive application health check."""
    health = {
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'checks': {}
    }
    
    # API connectivity check
    try:
        response = requests.get(config.api_url, timeout=5)
        health['checks']['api'] = {
            'status': 'healthy' if response.status_code == 200 else 'degraded',
            'response_time': response.elapsed.total_seconds()
        }
    except Exception as e:
        health['checks']['api'] = {
            'status': 'unhealthy',
            'error': str(e)
        }
        health['status'] = 'degraded'
    
    # File system check
    try:
        Path(config.data_folder).mkdir(exist_ok=True)
        health['checks']['filesystem'] = {'status': 'healthy'}
    except Exception as e:
        health['checks']['filesystem'] = {
            'status': 'unhealthy',
            'error': str(e)
        }
        health['status'] = 'degraded'
    
    return health
```

### 2. Metrics Collection
```python
class MetricsCollector:
    def __init__(self):
        self.metrics = {}
    
    def increment_counter(self, name: str, value: int = 1, tags: Dict[str, str] = None):
        """Increment a counter metric."""
        key = f"{name}:{tags or {}}"
        self.metrics[key] = self.metrics.get(key, 0) + value
    
    def record_timing(self, name: str, value: float, tags: Dict[str, str] = None):
        """Record a timing metric."""
        key = f"{name}_timing:{tags or {}}"
        if key not in self.metrics:
            self.metrics[key] = []
        self.metrics[key].append(value)
    
    def export_metrics(self) -> Dict[str, Any]:
        """Export all collected metrics."""
        return {
            'timestamp': datetime.utcnow().isoformat(),
            'metrics': self.metrics
        }
```

## Error Recovery Strategies

### 1. Partial Failure Handling
```python
def process_data_with_recovery(data: List[Dict], logger: logging.Logger) -> Dict:
    """Process data with partial failure recovery."""
    successful_items = []
    failed_items = []
    
    for item in data:
        try:
            processed_item = process_single_item(item)
            successful_items.append(processed_item)
        except Exception as e:
            logger.warning(f"Failed to process item {item.get('id')}: {e}")
            failed_items.append({
                'item': item,
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            })
    
    return {
        'successful_items': successful_items,
        'failed_items': failed_items,
        'success_rate': len(successful_items) / len(data) if data else 1.0
    }
```

### 2. Graceful Degradation
```python
def fetch_data_with_fallback(config: Config, logger: logging.Logger) -> List[Dict]:
    """Fetch data with fallback to cached version."""
    try:
        return fetch_api_data(config.api_url, config.api_timeout, logger)
    except Exception as e:
        logger.warning(f"Primary data source failed: {e}")
        
        # Try fallback data source
        try:
            return load_cached_data(config.data_folder)
        except Exception as fallback_error:
            logger.error(f"Fallback also failed: {fallback_error}")
            # Return minimal viable data to keep system running
            return []
```

## Follow-up Questions
1. When should you retry an operation vs fail fast?
2. How would you handle partial failures in data processing?
3. What information should be included in error logs for debugging?
4. How would you implement rate limiting for error notifications?
5. What's the difference between logging and monitoring?

## Error Handling Anti-Patterns to Avoid
1. **Silent Failures**: Catching exceptions without logging or handling
2. **Generic Exception Handling**: Catching `Exception` instead of specific types
3. **Error Swallowing**: Catching errors but not propagating or handling appropriately
4. **Insufficient Context**: Error messages without enough debugging information
5. **Retry Without Limits**: Infinite retry loops without backoff or circuit breakers

## Next Steps
After mastering error handling and logging, you'll explore environment configuration management in prompt #10.
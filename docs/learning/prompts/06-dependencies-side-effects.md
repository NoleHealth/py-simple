# Learning Prompt 6: Understanding Dependencies and Side Effects

## Objective
Learn to identify, manage, and document dependencies and side effects in Python applications. Understand how they impact testing, deployment, and maintenance.

## Prerequisites
Complete prompts #1-5 to understand the codebase, CLI implementation, and automation concepts.

## Your Task
Analyze the py-simple project to identify all dependencies and side effects, understand their implications, and learn strategies for managing them effectively.

## Prompt to Use with AI Assistant

```
Conduct a comprehensive dependency and side effects analysis of the py_simple project. Create a detailed report covering:

1. **Dependency Analysis**
   - Map all direct and transitive dependencies from pyproject.toml
   - Analyze what each dependency provides and why it's needed
   - Identify potential security vulnerabilities in dependencies
   - Evaluate license compatibility of all dependencies
   - Assess the maintenance status and update frequency of dependencies

2. **Side Effects Identification**
   - Catalog all side effects the application produces
   - Network operations: API calls, DNS lookups, timeouts
   - File system operations: file creation, directory creation, permissions
   - Environment interactions: reading env vars, system resources
   - External service dependencies: internet connectivity, API availability
   - System resource usage: memory, CPU, disk space, file handles

3. **Dependency Management Best Practices**
   - Version pinning strategies (exact, compatible, latest)
   - Virtual environment management and isolation
   - Dependency vulnerability scanning and updates
   - Creating reproducible builds with lock files
   - Managing development vs production dependencies

4. **Side Effect Management**
   - Making side effects explicit and testable
   - Implementing dependency injection for external dependencies
   - Creating mock-able interfaces for testing
   - Graceful degradation when dependencies are unavailable
   - Rollback strategies when side effects fail

5. **Testing Implications**
   - How to test code with external dependencies
   - Mocking strategies for network calls and file operations
   - Integration testing vs unit testing considerations
   - Test environment setup and teardown
   - Handling flaky tests due to external dependencies

6. **Deployment and Operations Impact**
   - How dependencies affect deployment size and time
   - Runtime dependency availability in different environments
   - Monitoring and alerting for dependency failures
   - Backup and recovery strategies for side effects
   - Performance impact of dependencies and side effects

Create your analysis in:
docs/learning/$(date +%Y%m%d%H%M)-dependencies-side-effects-analysis.md

Include:
- Complete dependency tree visualization
- Side effects documentation with impact analysis
- Risk assessment and mitigation strategies
- Refactoring recommendations for better testability
- Monitoring and alerting recommendations
```

## Key Learning Points
After completing this exercise, you should understand:
- How to analyze and document all project dependencies
- The difference between direct and transitive dependencies
- Various types of side effects and their implications
- Strategies for managing and testing code with side effects
- Dependency injection patterns and benefits
- Security and maintenance considerations for dependencies

## Types of Dependencies to Analyze

### 1. Runtime Dependencies
- **requests**: HTTP client library
- **python-dotenv**: Environment variable loader
- **Standard library**: json, logging, pathlib, datetime, os

### 2. Development Dependencies
- **ruff**: Linting and formatting
- **pytest**: Testing framework
- **pytest-cov**: Coverage reporting
- **black**: Code formatting (redundant with ruff)

### 3. System Dependencies
- **Operating system**: File system, networking, process management
- **Python interpreter**: Version compatibility requirements
- **Network connectivity**: Internet access for API calls
- **File system**: Write permissions, disk space

## Types of Side Effects to Document

### 1. Network Side Effects
- **API Calls**: HTTP requests to external services
- **DNS Resolution**: Domain name lookups
- **Connection Pooling**: Network resource management
- **Timeout Handling**: Network failure scenarios

### 2. File System Side Effects
- **File Creation**: Output JSON files with timestamps
- **Directory Creation**: Ensuring data directory exists
- **File Permissions**: Read/write access requirements
- **Disk Space Usage**: Storage requirements for output

### 3. System Resource Side Effects
- **Memory Usage**: Data processing and storage
- **CPU Usage**: JSON processing and HTTP operations
- **File Handles**: Open file and network connections
- **Process Lifetime**: Script execution duration

## Dependency Management Strategies

### 1. Version Pinning
- **Exact Pinning**: `requests==2.31.0` (reproducible but inflexible)
- **Compatible Release**: `requests~=2.31.0` (patch updates allowed)
- **Minimum Version**: `requests>=2.31.0` (flexible but potentially breaking)

### 2. Security Management
- **Vulnerability Scanning**: Use tools like `safety` or `pip-audit`
- **Regular Updates**: Scheduled dependency updates
- **Security Monitoring**: Alerts for new vulnerabilities
- **Dependency Review**: Manual review of dependency changes

### 3. Environment Isolation
- **Virtual Environments**: Isolate project dependencies
- **Container Images**: Reproducible runtime environments
- **Lock Files**: Exact dependency resolution (uv.lock)
- **Multi-stage Builds**: Separate build and runtime dependencies

## Side Effect Testing Strategies

### 1. Mocking External Dependencies
```python
# Mock HTTP requests
@patch('requests.get')
def test_fetch_api_data(mock_get):
    mock_get.return_value.json.return_value = [{"id": 1}]
    # Test logic here
```

### 2. Dependency Injection
```python
def fetch_data(http_client=requests):
    # Use injected client instead of direct import
    return http_client.get(url)
```

### 3. Test Isolation
- **Temporary Directories**: Use `tempfile` for file operations
- **Environment Variables**: Isolate test configuration
- **Network Isolation**: Mock or use local test servers
- **State Cleanup**: Ensure tests don't affect each other

## Follow-up Questions
1. What would happen if the `requests` library had a security vulnerability?
2. How would you test the file writing functionality without creating actual files?
3. What dependencies are only needed for development vs production?
4. How would you handle the script running out of disk space?
5. What external services does the application depend on to function?

## Next Steps
After understanding dependencies and side effects, you'll explore linting and formatting tools in detail in prompt #7.
# Learning Prompt 11: Package Management and Dependency Strategy

## Objective
Master modern Python package management using uv, understand dependency resolution, packaging, and distribution strategies for Python applications.

## Prerequisites
Complete prompts #1-10 to understand the codebase, configuration, and development workflows.

## Your Task
Deep dive into the package management aspects of the py-simple project, exploring uv, pyproject.toml configuration, dependency management, and packaging strategies.

## Prompt to Use with AI Assistant

```
Create a comprehensive package management guide for the py_simple project. Cover:

1. **UV Package Manager Deep Dive**
   - Analyze the current uv.lock file and understand its structure
   - Compare uv vs pip vs poetry for different use cases
   - Understand uv's dependency resolution algorithm and conflict handling
   - Explore uv's performance benefits and limitations
   - Learn uv's integration with virtual environments and project isolation

2. **Pyproject.toml Configuration Mastery**
   - Deep analysis of the current pyproject.toml configuration
   - Understand each section: [build-system], [project], [tool.*]
   - Learn about project metadata, dependencies, and optional dependencies
   - Explore tool-specific configurations (ruff, pytest, etc.)
   - Implement advanced configuration patterns and best practices

3. **Dependency Management Strategy**
   - Analyze direct vs transitive dependencies
   - Implement semantic versioning strategies for dependencies
   - Handle dependency conflicts and resolution
   - Create dependency groups for different use cases
   - Implement security scanning and vulnerability management

4. **Build and Distribution**
   - Create distributable packages (wheels and sdist)
   - Implement version management and tagging strategies
   - Set up package publishing to PyPI (test and production)
   - Create installation scripts and requirements files
   - Handle platform-specific dependencies and compatibility

5. **Advanced Dependency Patterns**
   - Optional dependencies and extras
   - Development vs production dependency separation
   - Plugin architectures and namespace packages
   - Monorepo and multi-package dependency management
   - Dependency injection and loose coupling patterns

6. **Package Security and Maintenance**
   - Implement automated dependency updates
   - Set up security scanning and vulnerability alerts
   - Create license compliance checking
   - Monitor dependency health and maintenance status
   - Implement dependency pinning and update strategies

Create your comprehensive package management guide in:
docs/learning/$(date +%Y%m%d%H%M)-package-management-guide.md

Include:
- Complete pyproject.toml analysis and improvements
- UV workflow documentation and best practices
- Dependency management strategies and tools
- Build and distribution pipeline setup
- Security and maintenance procedures
```

## Key Learning Points
After completing this exercise, you should understand:
- Modern Python package management with uv
- pyproject.toml configuration and standards
- Dependency resolution and conflict handling
- Package building and distribution processes
- Security considerations in dependency management
- Version management and semantic versioning
- Virtual environment and project isolation strategies

## UV Package Manager Analysis

### 1. UV vs Other Package Managers
| Feature | uv | pip | poetry | pipenv |
|---------|----|----|--------|--------|
| Speed | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Dependency Resolution | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Lock Files | ⭐⭐⭐⭐⭐ | ❌ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Virtual Env Management | ⭐⭐⭐⭐⭐ | ❌ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Build System | ⭐⭐⭐ | ❌ | ⭐⭐⭐⭐⭐ | ❌ |
| Maturity | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |

### 2. UV Lock File Structure
```toml
# uv.lock file structure analysis
version = 1
requires-python = ">=3.8"

[options]
exclude-newer = "2024-01-01T00:00:00Z"

[[package]]
name = "requests"
version = "2.31.0"
source = { registry = "https://pypi.org/simple" }
dependencies = [
    "certifi>=2017.4.17",
    "charset-normalizer>=2,<4",
    "idna>=2.5,<4",
    "urllib3>=1.21.1,<3",
]
wheels = [
    { url = "https://files.pythonhosted.org/packages/.../requests-2.31.0-py3-none-any.whl", hash = "sha256:..." },
]
```

### 3. UV Command Reference
```bash
# Virtual environment management
uv venv .venv                    # Create virtual environment
uv venv --python 3.11 .venv     # Create with specific Python version

# Package installation
uv pip install requests          # Install package
uv pip install -e .             # Install current project in editable mode
uv pip install -r requirements.txt  # Install from requirements file

# Dependency management
uv pip freeze > requirements.txt # Export installed packages
uv pip compile pyproject.toml   # Generate requirements from pyproject.toml
uv pip sync requirements.txt    # Sync environment to match requirements

# Advanced usage
uv pip install --resolution=lowest-direct  # Install lowest compatible versions
uv pip install --no-deps package_name      # Install without dependencies
```

## Pyproject.toml Deep Dive

### 1. Complete Configuration Template
```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "py-simple"
version = "0.1.0"
description = "A simple Python template for API data processing"
readme = "README.md"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "your.email@example.com"},
]
maintainers = [
    {name = "Maintainer Name", email = "maintainer@example.com"},
]
keywords = ["api", "data-processing", "template", "python"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Software Development :: Libraries :: Python Modules",
]
requires-python = ">=3.8"
dependencies = [
    "requests>=2.31.0,<3.0.0",
    "python-dotenv>=1.0.0,<2.0.0",
]

[project.optional-dependencies]
dev = [
    "ruff>=0.1.0",
    "black>=23.0.0",    # Note: Redundant with ruff format
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "pytest-mock>=3.10.0",
    "mypy>=1.0.0",
]
test = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "pytest-mock>=3.10.0",
    "httpx>=0.24.0",    # For async testing
]
docs = [
    "mkdocs>=1.4.0",
    "mkdocs-material>=9.0.0",
    "mkdocstrings[python]>=0.20.0",
]
security = [
    "safety>=2.3.0",
    "bandit>=1.7.0",
]

[project.urls]
Homepage = "https://github.com/yourusername/py-simple"
Repository = "https://github.com/yourusername/py-simple.git"
Issues = "https://github.com/yourusername/py-simple/issues"
Documentation = "https://py-simple.readthedocs.io"
Changelog = "https://github.com/yourusername/py-simple/blob/main/CHANGELOG.md"

[project.scripts]
py-simple = "py_simple.main:main"

[project.entry-points."py_simple.plugins"]
default_processor = "py_simple.processors:DefaultProcessor"

[tool.setuptools.packages.find]
include = ["py_simple*"]
exclude = ["tests*"]

[tool.setuptools.package-data]
py_simple = ["py.typed", "*.pyi"]
```

### 2. Advanced Dependency Specifications
```toml
dependencies = [
    # Version constraints
    "requests>=2.31.0,<3.0.0",        # Compatible release
    "python-dotenv~=1.0.0",           # Approximately equal (1.0.x)
    "pydantic>=2.0.0",                # Minimum version
    "httpx==0.24.1",                  # Exact version (use sparingly)
    
    # Conditional dependencies
    "pywin32>=300; platform_system=='Windows'",
    "uvloop>=0.17.0; platform_system!='Windows'",
    
    # URL dependencies (use carefully)
    "mypackage @ git+https://github.com/user/repo.git@v1.0.0",
    
    # Local dependencies
    "shared-utils @ file:///path/to/local/package",
]
```

## Dependency Management Strategies

### 1. Semantic Versioning Strategy
```python
# Version constraint strategies
VERSION_STRATEGIES = {
    "stable_libraries": ">=X.Y.Z,<X+1.0.0",  # Major version compatibility
    "actively_developed": ">=X.Y.Z,<X.Y+1.0",  # Minor version compatibility
    "critical_security": ">=X.Y.Z",             # Minimum version only
    "internal_tools": "==X.Y.Z",               # Pin exactly for reproducibility
}

# Example implementation
def get_version_constraint(package: str, current_version: str, strategy: str) -> str:
    """Generate version constraint based on strategy."""
    major, minor, patch = map(int, current_version.split('.'))
    
    if strategy == "stable":
        return f">={current_version},<{major + 1}.0.0"
    elif strategy == "conservative":
        return f">={current_version},<{major}.{minor + 1}.0"
    elif strategy == "exact":
        return f"=={current_version}"
    else:
        return f">={current_version}"
```

### 2. Dependency Groups and Extras
```toml
[project.optional-dependencies]
# Core development tools
dev = [
    "ruff>=0.1.0",
    "pytest>=7.0.0",
    "mypy>=1.0.0",
]

# Testing-specific dependencies
test = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "pytest-mock>=3.10.0",
    "pytest-asyncio>=0.21.0",
]

# Performance profiling
perf = [
    "py-spy>=0.3.0",
    "memory-profiler>=0.60.0",
    "line-profiler>=4.0.0",
]

# Database integrations
db = [
    "sqlalchemy>=2.0.0",
    "alembic>=1.11.0",
]
db-postgres = [
    "py-simple[db]",
    "psycopg2-binary>=2.9.0",
]
db-sqlite = [
    "py-simple[db]",
]

# All extras combined
all = [
    "py-simple[dev,test,perf,db]",
]
```

### 3. Dependency Security Management
```bash
# Security scanning workflow
uv pip install safety bandit pip-audit

# Check for known vulnerabilities
safety check                           # PyUp.io vulnerability database
pip-audit                             # OSV vulnerability database
bandit -r py_simple/                  # Static security analysis

# Generate security report
safety check --json > security-report.json
pip-audit --format=json --output=audit-report.json
```

## Build and Distribution Pipeline

### 1. Build Configuration
```toml
[build-system]
requires = ["setuptools>=61.0", "wheel", "setuptools-scm>=6.2"]
build-backend = "setuptools.build_meta"

[tool.setuptools]
zip-safe = false
platforms = ["any"]

[tool.setuptools.packages.find]
where = ["."]
include = ["py_simple*"]
exclude = ["tests*", "docs*", "scripts*"]

[tool.setuptools.package-data]
py_simple = [
    "py.typed",
    "*.pyi",
    "data/*.json",
    "templates/*.jinja2",
]

[tool.setuptools-scm]
write_to = "py_simple/_version.py"
version_scheme = "post-release"
local_scheme = "dirty-tag"
```

### 2. Build and Distribution Scripts
```python
#!/usr/bin/env python3
"""Build and distribution script."""

import subprocess
import sys
from pathlib import Path

def build_package():
    """Build wheel and source distribution."""
    print("Building package...")
    subprocess.run([sys.executable, "-m", "build"], check=True)
    
    # Verify built packages
    dist_dir = Path("dist")
    wheels = list(dist_dir.glob("*.whl"))
    tarballs = list(dist_dir.glob("*.tar.gz"))
    
    print(f"Built {len(wheels)} wheel(s) and {len(tarballs)} source distribution(s)")
    for wheel in wheels:
        print(f"  - {wheel.name}")
    for tarball in tarballs:
        print(f"  - {tarball.name}")

def test_package():
    """Test the built package."""
    print("Testing package installation...")
    # Create temporary virtual environment
    subprocess.run(["uv", "venv", ".test-env"], check=True)
    
    # Install from wheel
    wheels = list(Path("dist").glob("*.whl"))
    if wheels:
        subprocess.run([
            "uv", "pip", "install", str(wheels[0])
        ], check=True)
        
        # Test basic import
        subprocess.run([
            ".test-env/bin/python", "-c", "import py_simple; print('Import successful')"
        ], check=True)

def publish_package(repository: str = "testpypi"):
    """Publish package to PyPI."""
    print(f"Publishing to {repository}...")
    if repository == "testpypi":
        subprocess.run([
            "twine", "upload", "--repository", "testpypi", "dist/*"
        ], check=True)
    else:
        subprocess.run(["twine", "upload", "dist/*"], check=True)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "publish":
        build_package()
        test_package()
        publish_package()
    else:
        build_package()
        test_package()
```

### 3. Version Management
```python
# _version.py - Generated by setuptools-scm
__version__ = "0.1.0"

# main.py - Version reporting
def get_version() -> str:
    """Get the application version."""
    try:
        from ._version import __version__
        return __version__
    except ImportError:
        return "unknown"

# CLI integration
if __name__ == "__main__":
    if "--version" in sys.argv:
        print(f"py-simple {get_version()}")
        sys.exit(0)
```

## Advanced Package Management Patterns

### 1. Plugin Architecture
```python
# Plugin system using entry points
import pkg_resources

class PluginManager:
    """Manage plugins via entry points."""
    
    def __init__(self, group_name: str):
        self.group_name = group_name
        self.plugins = {}
        self._discover_plugins()
    
    def _discover_plugins(self):
        """Discover plugins via entry points."""
        for entry_point in pkg_resources.iter_entry_points(self.group_name):
            try:
                plugin_class = entry_point.load()
                self.plugins[entry_point.name] = plugin_class
            except Exception as e:
                logger.warning(f"Failed to load plugin {entry_point.name}: {e}")
    
    def get_plugin(self, name: str):
        """Get plugin by name."""
        return self.plugins.get(name)
    
    def list_plugins(self) -> list:
        """List available plugins."""
        return list(self.plugins.keys())

# Usage
plugin_manager = PluginManager("py_simple.processors")
processor = plugin_manager.get_plugin("default")
```

### 2. Dependency Injection Container
```python
from typing import Dict, Any, Type, TypeVar
import inspect

T = TypeVar('T')

class DIContainer:
    """Simple dependency injection container."""
    
    def __init__(self):
        self._services: Dict[Type, Any] = {}
        self._singletons: Dict[Type, Any] = {}
    
    def register(self, interface: Type[T], implementation: Type[T], singleton: bool = False):
        """Register a service implementation."""
        self._services[interface] = implementation
        if singleton:
            self._singletons[interface] = None
    
    def resolve(self, interface: Type[T]) -> T:
        """Resolve a service instance."""
        if interface in self._singletons:
            if self._singletons[interface] is None:
                self._singletons[interface] = self._create_instance(interface)
            return self._singletons[interface]
        
        return self._create_instance(interface)
    
    def _create_instance(self, interface: Type[T]) -> T:
        """Create service instance with dependency injection."""
        implementation = self._services.get(interface, interface)
        
        # Get constructor parameters
        sig = inspect.signature(implementation.__init__)
        kwargs = {}
        
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
            
            if param.annotation in self._services:
                kwargs[param_name] = self.resolve(param.annotation)
        
        return implementation(**kwargs)
```

## Follow-up Questions
1. What are the trade-offs between pinning exact versions vs allowing ranges?
2. How would you handle dependency conflicts in a large project?
3. What's the difference between wheels and source distributions?
4. How would you set up automated dependency updates safely?
5. What security considerations are important for package management?

## Package Management Best Practices
1. **Use Lock Files**: Always commit lock files for reproducible builds
2. **Regular Updates**: Keep dependencies updated for security and features
3. **Security Scanning**: Regularly scan for vulnerable dependencies
4. **Minimal Dependencies**: Only include necessary dependencies
5. **Version Constraints**: Use appropriate version constraint strategies
6. **Documentation**: Document dependency choices and constraints

## Next Steps
After mastering package management, you'll explore CI/CD pipelines and automation in prompt #12.
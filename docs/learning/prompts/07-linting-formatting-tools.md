# Learning Prompt 7: Linting, Formatting, and Build Tools Deep Dive

## Objective
Master the use of linting, formatting, and build tools in Python development. Understand their configuration, integration, and impact on code quality and team collaboration.

## Prerequisites
Complete prompts #1-6 to understand the codebase, automation, and dependency concepts.

## Your Task
Explore the linting and formatting tools used in the py-simple project, understand their configuration, and learn how to customize them for different project needs.

## Prompt to Use with AI Assistant

```
Create a comprehensive analysis and guide for the linting, formatting, and build tools used in the py_simple project. Cover:

1. **Tool Analysis and Configuration**
   - Deep dive into Ruff configuration in pyproject.toml
   - Understand each linting rule and why it's enabled/disabled
   - Analyze Black configuration (note: redundant with Ruff formatting)
   - Examine pytest configuration and coverage settings
   - Review Makefile commands and their purposes

2. **Ruff Deep Dive**
   - Explore all available Ruff rule categories (E, W, F, I, B, C4, UP, etc.)
   - Understand the difference between linting and formatting in Ruff
   - Learn how to customize rules for specific project needs
   - Practice fixing different types of linting violations
   - Set up per-file rule overrides and ignores

3. **Integration and Automation**
   - Set up pre-commit hooks for automatic linting/formatting
   - Configure VS Code settings for seamless development
   - Integrate tools into CI/CD pipelines
   - Compare different integration strategies (hooks vs CI vs IDE)
   - Handle merge conflicts in formatted code

4. **Code Quality Metrics**
   - Understand different types of code quality metrics
   - Set up and interpret test coverage reports
   - Analyze code complexity metrics
   - Monitor technical debt and code smells
   - Create quality gates and standards

5. **Team Collaboration**
   - Establish team coding standards and style guides
   - Handle disagreements about code style
   - Onboard new team members with consistent tooling
   - Balance automation vs manual review
   - Documentation and knowledge sharing

6. **Advanced Topics**
   - Custom linting rules and plugins
   - Performance optimization of linting tools
   - Handling large codebases and monorepos
   - Integration with other quality tools (mypy, bandit, etc.)
   - Gradual adoption in existing projects

Create your comprehensive guide in:
docs/learning/$(date +%Y%m%d%H%M)-linting-formatting-tools-guide.md

Include:
- Step-by-step configuration examples
- Common issues and troubleshooting
- Best practices for team adoption
- Performance optimization tips
- Integration examples for different environments
```

## Key Learning Points
After completing this exercise, you should understand:
- How modern Python linting and formatting tools work
- The difference between linting (code quality) and formatting (code style)
- How to configure tools for specific project needs
- Integration strategies for teams and CI/CD
- Code quality metrics and how to improve them
- The evolution of Python tooling (flake8 → Ruff, etc.)

## Tools Deep Dive

### 1. Ruff - The All-in-One Tool
- **Linting**: Replaces flake8, isort, pyupgrade, and more
- **Formatting**: Replaces Black with compatible output
- **Speed**: Written in Rust, extremely fast
- **Configuration**: Extensive rule system with granular control
- **Integration**: Native support in most editors and CI systems

### 2. Pytest - Testing Framework
- **Test Discovery**: Automatic test file and function discovery
- **Fixtures**: Reusable test setup and teardown
- **Plugins**: Extensive ecosystem (pytest-cov, pytest-mock, etc.)
- **Configuration**: Flexible configuration in pyproject.toml
- **Reporting**: Coverage, HTML reports, JUnit XML

### 3. Make - Build Automation
- **Task Definition**: Simple command shortcuts
- **Dependency Management**: Target dependencies and ordering
- **Cross-platform**: Works on Unix-like systems
- **Documentation**: Self-documenting help system
- **Integration**: Easy CI/CD integration

## Linting Rule Categories in Detail

### Error Prevention (E, W, F)
- **E**: PEP 8 style errors (indentation, whitespace, line length)
- **W**: PEP 8 style warnings (blank lines, imports, naming)
- **F**: Pyflakes errors (undefined variables, unused imports)

### Code Quality (B, C4, UP)
- **B**: Flake8-bugbear (common bugs and design problems)
- **C4**: Flake8-comprehensions (list/dict comprehension improvements)
- **UP**: Pyupgrade (syntax modernization for newer Python versions)

### Import Organization (I)
- **I**: Isort rules for import sorting and organization
- **Categories**: Standard library, third-party, local imports
- **Formatting**: Line length, trailing commas, grouping

## Configuration Best Practices

### 1. Start Conservative
```toml
[tool.ruff.lint]
select = ["E", "W", "F"]  # Start with basics
ignore = ["E501"]         # Ignore line length initially
```

### 2. Add Rules Gradually
```toml
select = ["E", "W", "F", "I", "B"]  # Add import sorting and bug detection
```

### 3. Project-Specific Customization
```toml
[tool.ruff.lint.per-file-ignores]
"tests/*" = ["B011"]      # Allow assert statements in tests
"__init__.py" = ["F401"]  # Allow unused imports in init files
```

## Integration Strategies

### 1. Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

### 2. VS Code Integration
```json
{
    "python.linting.enabled": true,
    "python.linting.ruffEnabled": true,
    "python.formatting.provider": "ruff",
    "editor.formatOnSave": true
}
```

### 3. CI/CD Integration
```yaml
# GitHub Actions example
- name: Lint with Ruff
  run: |
    ruff check .
    ruff format --check .
```

## Common Issues and Solutions

### 1. Rule Conflicts
- **Problem**: Different tools enforcing conflicting rules
- **Solution**: Use Ruff for everything to ensure consistency

### 2. Large Legacy Codebases
- **Problem**: Too many violations to fix at once
- **Solution**: Gradual adoption with baseline files and ignore lists

### 3. Team Disagreements
- **Problem**: Developers have different style preferences
- **Solution**: Establish team standards and automate enforcement

### 4. CI Performance
- **Problem**: Linting slows down CI pipelines
- **Solution**: Use Ruff for speed, run in parallel, cache results

## Follow-up Questions
1. What's the difference between `ruff check` and `ruff format`?
2. How would you add a custom rule to catch project-specific issues?
3. What happens when Ruff conflicts with existing Black formatting?
4. How would you gradually adopt stricter linting rules in a large project?
5. What's the best way to handle linting violations in third-party code?

## Practical Exercises
1. **Rule Exploration**: Enable different rule categories and fix violations
2. **Custom Configuration**: Create project-specific rule overrides
3. **Pre-commit Setup**: Install and configure pre-commit hooks
4. **CI Integration**: Add linting to a CI/CD pipeline
5. **Team Standards**: Create a style guide and enforcement strategy

## Next Steps
After mastering linting and formatting tools, you'll explore testing strategies in depth in prompt #8.
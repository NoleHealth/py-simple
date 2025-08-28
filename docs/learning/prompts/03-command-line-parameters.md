# Learning Prompt 3: Adding Command Line Parameters

## Objective
Learn how to add command-line interface capabilities to the Python application, understand their effects on application design, and explore different CLI libraries.

## Prerequisites
Complete prompts #1 and #2 to understand the current codebase and refactoring principles.

## Your Task
Enhance the py-simple application by adding command-line parameter support. Learn how CLI parameters affect application architecture and user experience.

## Prompt to Use with AI Assistant

```
Add command-line parameter support to the py_simple application. Create a comprehensive implementation and analysis that covers:

1. **CLI Design & Implementation**
   - Add support for all configuration options as CLI parameters
   - Include help text and parameter validation
   - Support both short (-u) and long (--url) parameter formats
   - Provide sensible defaults that match current .env behavior

2. **CLI Library Comparison**
   - Compare different Python CLI libraries (argparse, click, typer)
   - Recommend the best choice for this project with justification
   - Show implementation examples for your chosen library

3. **Parameter Priority & Configuration**
   - Establish precedence: CLI args > Environment vars > Defaults
   - Handle configuration conflicts gracefully
   - Add a --config option to specify custom .env files

4. **User Experience Improvements**
   - Add verbose/quiet modes for different log levels
   - Include --dry-run option to preview actions without execution
   - Add --version flag to display application version
   - Include comprehensive --help documentation

5. **Architecture Impact Analysis**
   - How do CLI parameters affect the Config class design?
   - What changes are needed in main() function?
   - How does this impact testing and maintainability?
   - What new error cases need to be handled?

Create your implementation and analysis in:
docs/learning/$(date +%Y%m%d%H%M)-cli-parameters-implementation.md

Include:
- Complete working code examples
- Command-line usage examples
- Before/after architecture comparison
- Testing strategy for CLI functionality
- Discussion of design trade-offs made
```

## Key Learning Points
After completing this exercise, you should understand:
- Python CLI development patterns and libraries
- Configuration precedence and merging strategies
- User experience design for command-line tools
- How CLI additions affect application architecture
- Testing strategies for CLI applications
- Argument parsing and validation techniques

## Essential CLI Features to Implement
1. **Core Parameters**
   - `--url` / `-u`: API endpoint URL
   - `--timeout` / `-t`: Request timeout
   - `--output` / `-o`: Output directory
   - `--prefix` / `-p`: File name prefix

2. **Control Parameters**
   - `--verbose` / `-v`: Increase verbosity
   - `--quiet` / `-q`: Decrease verbosity  
   - `--dry-run`: Preview actions without executing
   - `--config` / `-c`: Specify config file path

3. **Utility Parameters**
   - `--help` / `-h`: Show help message
   - `--version` / `-V`: Show application version

## Architecture Considerations
1. **Configuration Layer** - How will CLI args integrate with existing Config class?
2. **Error Handling** - What new error cases are introduced?
3. **Testing** - How will you test CLI functionality?
4. **Backward Compatibility** - Will existing usage still work?
5. **Documentation** - How will help text stay synchronized with functionality?

## Follow-up Questions
1. What's the difference between argparse, click, and typer?
2. How should configuration priority be handled (CLI vs ENV vs defaults)?
3. What happens when invalid parameters are provided?
4. How would you implement subcommands for different operations?
5. What's the best way to test CLI applications?

## Next Steps
After implementing CLI parameters, you'll explore local automation techniques in prompt #4.
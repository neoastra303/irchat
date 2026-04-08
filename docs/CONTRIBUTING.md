# Contributing to IRC Chat Client

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## Getting Started

### Prerequisites

- Python 3.8+
- git

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/neoastra303/irchat.git
   cd irchat
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

4. **Run tests**
   ```bash
   python test_irc.py -v
   ```

## Development Workflow

### Branch Naming

Use descriptive branch names:
- `feature/add-xyz` - New feature
- `fix/issue-xyz` - Bug fix
- `docs/update-xyz` - Documentation
- `refactor/improve-xyz` - Code improvements

### Coding Standards

- **Python Version**: 3.8+
- **Style**: PEP 8 compliant
- **Type Hints**: Required for new functions
- **Docstrings**: Required for public functions
- **Comments**: Explain "why", not "what"

### Making Changes

1. **Create a feature branch**
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make your changes**
   - Keep commits atomic and well-documented
   - Reference issue numbers in commits: `Fix #123`

3. **Run tests and checks**
   ```bash
   python test_irc.py -v          # Unit tests
   python -m pylint *.py           # Linting
   python -m mypy *.py             # Type checking
   ```

4. **Update documentation**
   - Update README.md if needed
   - Update CHANGELOG.md
   - Add docstrings to new code

5. **Commit and push**
   ```bash
   git add .
   git commit -m "feat: add new feature" -m "Detailed description"
   git push origin feature/my-feature
   ```

6. **Create a Pull Request**
   - Use the PR template
   - Link related issues
   - Provide clear description
   - Include test results

## Pull Request Guidelines

### PR Requirements

- ✓ All tests pass
- ✓ Code is linted
- ✓ Type hints are present
- ✓ Documentation is updated
- ✓ Commit messages are clear
- ✓ No merge conflicts

### PR Review

- At least one approval required
- Comments should be constructive
- Be respectful and collaborative
- All feedback should be addressed

## Testing

### Running Tests

```bash
# Run all tests
python test_irc.py -v

# Run specific test class
python test_irc.py TestIRCProtocol -v

# Run with coverage
coverage run -m unittest test_irc.py
coverage report
```

### Writing Tests

When adding new features:

1. Write tests first (TDD)
2. Tests should be in `test_irc.py`
3. Use descriptive test names
4. Test both success and failure cases
5. Aim for >80% code coverage

Example:
```python
def test_feature_name(self):
    """Test description of what feature does"""
    # Arrange
    input_data = ...
    
    # Act
    result = function_under_test(input_data)
    
    # Assert
    self.assertEqual(result, expected_output)
```

## Commit Message Guidelines

Use conventional commits:

```
<type>: <subject>
<blank line>
<body>
<blank line>
<footer>
```

Types:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `style:` - Formatting
- `refactor:` - Code restructuring
- `test:` - Test additions
- `chore:` - Maintenance

Example:
```
feat: add SSL/TLS support

Add support for encrypted IRC connections using SSL/TLS.
Implements RFC 6697 for IRCs protocol.

Fixes #123
```

## Documentation

### README Updates

If your change affects usage:
- Update README.md
- Include examples
- Update the table of contents

### Code Documentation

- Public functions need docstrings
- Complex logic needs comments
- Type hints on all parameters
- Example usage for public APIs

Format:
```python
def connect(self, retry_attempts: int = 3) -> bool:
    """
    Connect to IRC server with automatic retry logic.
    
    Args:
        retry_attempts: Number of connection attempts (default: 3)
    
    Returns:
        True if connection successful, False otherwise
    
    Raises:
        ConnectionError: If all retries fail
    
    Example:
        >>> client = IRCClient("irc.libera.chat", 6667)
        >>> if client.connect():
        ...     print("Connected!")
    """
```

## Issues

### Reporting Issues

When reporting bugs:

1. **Use a clear title** - Describe the problem briefly
2. **Include environment** - Python version, OS, etc.
3. **Describe the bug** - What happened vs. what was expected
4. **Provide steps to reproduce** - Clear steps
5. **Include logs** - Error messages, stack traces
6. **Suggest a fix** - If you have ideas (optional)

### Feature Requests

When requesting features:

1. **Use a clear title** - "Add X feature"
2. **Explain the use case** - Why is this needed?
3. **Provide examples** - How would it be used?
4. **Suggest implementation** - If you have ideas (optional)

## Code Review Process

### What We Look For

- ✓ Code quality and readability
- ✓ Test coverage
- ✓ Documentation
- ✓ Performance impact
- ✓ Security implications
- ✓ Backward compatibility

### Review Checklist

Before submitting, check:
- [ ] Code passes all tests
- [ ] No linting errors
- [ ] Type hints are complete
- [ ] Documentation is updated
- [ ] Changelog is updated
- [ ] Commit messages are clear

## Licensing

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

- Check existing issues and PRs
- Review the documentation
- Open a discussion in the repository

## Recognition

Contributors are recognized in:
- CHANGELOG.md (major contributions)
- GitHub contributors page
- Release notes

Thank you for contributing! 🎉

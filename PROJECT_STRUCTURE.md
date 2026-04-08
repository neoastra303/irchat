# IRChat Project Structure

A professional, well-organized Python project layout following industry best practices.

```
irchat/
├── src/                          # Source code (main application)
│   └── irchat/                   # Package directory
│       ├── __init__.py           # Package initialization & exports
│       ├── __main__.py           # Entry point for `python -m irchat`
│       ├── irc_client.py         # Core IRC protocol client
│       ├── irc_chat.py           # CLI chat interface & user interaction
│       ├── irc_modern.py         # Modern colored terminal UI
│       ├── irc_rich.py           # Rich library UI (advanced)
│       ├── logger.py             # Logging configuration (JSON Lines format)
│       ├── history.py            # Command history management
│       ├── config.py             # Configuration file management
│       └── sanitize.py           # Input validation & security
│
├── tests/                        # Unit & integration tests
│   ├── __init__.py              # Test package marker
│   ├── test_client.py           # IRC client tests
│   ├── test_history.txt         # Test history log
│   └── test_logs/               # Test output logs
│
├── docs/                         # Documentation (markdown & guides)
│   ├── ARCHITECTURE.md          # Technical design & architecture
│   ├── CODE_OF_CONDUCT.md       # Community standards
│   ├── CONTRIBUTING.md          # Development guidelines
│   ├── SECURITY.md              # Security policy & best practices
│   ├── CHANGELOG.md             # Version history & release notes
│   ├── PRESENTATION.md          # Project showcase & vision
│   ├── DOCUMENTATION_INDEX.md   # Navigation guide for all docs
│   └── status/                  # Deployment & project status
│       ├── AUTOMATION_COMPLETE.txt
│       ├── DEPLOYMENT_CHECKLIST.md
│       ├── GIT_SETUP_COMPLETE.txt
│       ├── GITHUB_SETUP.md
│       ├── REDESIGN_COMPLETE.txt
│       └── GITHUB_PUSH_GUIDE.md
│
├── config/                       # Configuration files
│   └── config.example.json      # Example configuration (template)
│
├── examples/                     # Code examples & templates
│   └── bot_template.py          # Example bot implementation
│
├── scripts/                      # Utility scripts & tools
│   └── (automation scripts here)
│
├── .github/                      # GitHub-specific files
│   ├── workflows/               # CI/CD pipelines
│   │   ├── tests.yml           # Unit tests & code quality
│   │   ├── code-quality.yml    # Linting & formatting
│   │   ├── codeql.yml          # Security scanning
│   │   ├── docker-build.yml    # Docker image build
│   │   ├── publish-pypi.yml    # Package publishing
│   │   └── dependabot.yml      # Dependency automation
│   ├── ISSUE_TEMPLATE/         # GitHub issue templates
│   ├── CODEOWNERS              # Repository ownership rules
│   └── pull_request_template.md # PR guidelines
│
├── .gitignore                    # Git ignore rules
├── Dockerfile                    # Container configuration
├── LICENSE                       # MIT License
├── README.md                     # Main project README (public-facing)
├── setup.py                      # Package configuration for pip install
├── requirements.txt              # Production dependencies
├── requirements-dev.txt          # Development dependencies
└── PROJECT_STRUCTURE.md          # This file

```

## Directory Purposes

### `src/irchat/`
Contains all production Python code. This is the actual package that gets installed.
- **Package design**: Uses `src/irchat/` layout (industry standard)
- **Isolation**: Keeps source code separate from tests and docs
- **Imports**: Other projects import this via `from irchat import ...`

### `tests/`
Unit tests and integration tests with pytest/unittest.
- All test files here with `test_*.py` naming
- Automatically discovered by test runners
- Import module under test from `src/irchat/`

### `docs/`
All markdown documentation, guides, and specifications.
- User-facing: README, ARCHITECTURE, CONTRIBUTING
- Development: SECURITY, CODE_OF_CONDUCT, CHANGELOG
- Status: Deployment & project status files
- Public on GitHub automatically

### `config/`
Configuration templates and examples.
- `config.example.json`: Template for users to copy and customize
- Actual configs (`.gitignore` prevents committing real configs)

### `examples/`
Example code, bot templates, and usage demonstrations.
- Shows how to use the library
- Helps developers understand API

### `.github/`
GitHub-specific automation and configuration.
- CI/CD workflows (GitHub Actions)
- Issue & PR templates
- Security settings (CODEOWNERS)

## Installation & Usage

### For Development
```bash
# Clone repository
git clone https://github.com/neoastra303/irchat.git
cd irchat

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Run tests
python -m pytest tests/

# Run linting
flake8 src/ tests/
mypy src/
pylint src/

# Run application
python -m irchat basic irc.libera.chat 6667 mynick #general
```

### For End Users
```bash
# Install from PyPI
pip install irchat

# Run application
irchat basic irc.libera.chat 6667 mynick #general
```

## Key Improvements

✅ **Clarity**: Clear separation of source, tests, docs, and configs
✅ **Standard**: Follows Python packaging best practices (PEP 420)
✅ **Discoverability**: Easy to find what you're looking for
✅ **Maintainability**: Organized for team development
✅ **Professionalism**: Industry-standard structure
✅ **Scalability**: Ready for growth and additional modules

## Module Overview

| Module | Purpose |
|--------|---------|
| `irc_client.py` | Core RFC 2812 IRC protocol implementation (thread-safe) |
| `irc_chat.py` | CLI interface & user interaction loop |
| `irc_modern.py` | Modern colored terminal UI |
| `irc_rich.py` | Advanced Rich library UI with panels |
| `logger.py` | JSON Lines logging system |
| `history.py` | Command history management |
| `config.py` | Configuration file handling |
| `sanitize.py` | Input validation & security layer |

## Testing

All tests in `tests/` directory:
- Import from `src/irchat/` package
- Run with: `python -m pytest tests/`
- Coverage reports available
- CI/CD runs on every push via `.github/workflows/`

# src/irchat - Application Source Code

This directory contains all production Python code for the IRChat IRC client.

## Package Structure

```
irchat/
├── __init__.py          # Package initialization & public API
├── __main__.py          # CLI entry point (python -m irchat)
├── irc_client.py        # Core IRC protocol client
├── irc_chat.py          # CLI chat interface
├── irc_modern.py        # Modern colored terminal UI
├── irc_rich.py          # Rich library UI
├── logger.py            # JSON Lines logging
├── history.py           # Command history
├── config.py            # Configuration management
└── sanitize.py          # Input validation & security
```

## Module Details

### `__init__.py`
**Package initialization and public API**
- Exports main classes: IRCClient, IRCChatBot, etc.
- Version information
- Makes the package importable

### `__main__.py`
**Entry point for `python -m irchat` or `irchat` console command**
- Argument parsing for CLI
- UI selection (basic, modern, rich)
- Server, port, nickname, channel configuration
- Routes to appropriate UI implementation

### `irc_client.py`
**Core IRC protocol implementation (RFC 2812 compliant)**
- Socket management & connection handling
- Thread-safe message buffer (with lock)
- Channel and user management
- PRIVMSG, JOIN, PART, NICK commands
- Ping/Pong for keep-alive
- Non-blocking I/O with select.select()

Key Features:
- Thread-safe access to shared data structures
- Event-based registration (prevents busy-wait)
- Proper CRLF line endings
- Comprehensive error handling

### `irc_chat.py`
**CLI user interface and interaction loop**
- Command processing (/join, /part, /nick, /msg, etc.)
- Message display with formatting
- User input validation
- Integration with logger, history, config, sanitize modules
- Status display with latency calculation
- Clean separation of UI from protocol

### `irc_modern.py`
**Modern colored terminal UI**
- Color-coded output for different message types
- Better visual formatting than basic CLI
- Requires terminal color support
- Alternative to basic interface

### `irc_rich.py`
**Advanced UI using the Rich library**
- Panels, tables, and formatted output
- Professional appearance
- Rich dependency required (optional install)
- Best for modern terminals

### `logger.py`
**JSON Lines logging system**
- Structured logging format (one JSON object per line)
- Easy parsing for analysis
- Logs to file for debugging
- Separate from console output

### `history.py`
**Command history management**
- Stores user commands in `.irc_history`
- Allows browsing previous commands
- Persistent across sessions
- Plain text format (one command per line)

### `config.py`
**Configuration file management**
- Loads config from `config.json`
- Example template in `config/config.example.json`
- Externalizes settings from code
- Supports custom server, port, nickname defaults

### `sanitize.py`
**Input validation and security layer**
- IRC protocol constraints enforcement
- Nickname: max 30 characters, no spaces/control chars
- Channel: max 50 characters
- Message: max 400 characters
- Strips control characters
- Prevents injection attacks

## Importing from This Package

### In User Code
```python
from irchat import IRCClient, IRCChatBot, setup_logging
from irchat.config import load_config
from irchat.sanitize import InputValidator
```

### In Tests
```python
from irchat.irc_client import IRCClient
from irchat.irc_chat import IRCChatBot
from irchat.logger import setup_logging
```

## Running the Application

### As a package (development)
```bash
cd <project_root>
python -m irchat basic irc.libera.chat 6667 mynick #general
```

### As an installed command (production)
```bash
irchat basic irc.libera.chat 6667 mynick #general
```

## Code Style

All code in this package follows:
- **PEP 8**: Python style guide
- **Type hints**: Where applicable
- **Docstrings**: For classes and public functions
- **Tested**: Unit tests in `/tests/`

## Dependencies

**Core Requirements** (from `requirements.txt`):
- Python 3.8+
- Standard library only (no external dependencies)

**Development** (from `requirements-dev.txt`):
- pytest - Unit testing
- coverage - Code coverage
- pylint, flake8, mypy - Code quality
- black, isort - Code formatting
- bandit, safety - Security scanning

## Thread Safety

The package uses thread-safe patterns:
- **Lock-based**: threading.Lock for critical sections
- **Events**: threading.Event for registration (no busy-wait)
- **Message buffer**: Protected dictionary access
- **Channels dict**: Protected with locks
- **Users dict**: Protected with locks

## Performance

- **Non-blocking I/O**: select.select() prevents UI freezing
- **Event-driven**: No busy-wait loops
- **Efficient parsing**: Regex patterns for IRC messages
- **Buffer management**: Stores 100 messages in memory, displays 50

## Testing

All code is tested:
```bash
pytest tests/  # Run all tests
pytest tests/test_client.py  # Run specific test
coverage run -m pytest tests/  # With coverage
```

## Contributing

When adding new modules:
1. Place in this directory (`src/irchat/`)
2. Follow existing code style
3. Add unit tests in `/tests/`
4. Update `__init__.py` if exporting public API
5. Document in docstrings
6. Update this README if appropriate

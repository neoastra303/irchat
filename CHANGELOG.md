# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-04-08

### Added
- Thread safety with locks on shared state
- Input validation and error handling improvements
- Message logging system (JSONL format)
- Command history with persistent storage
- Configuration file support with server presets
- Connection latency monitoring (ping/pong)
- Auto-reconnection with exponential backoff
- Message logging with configurable enable/disable
- 14 comprehensive unit tests
- GitHub Actions CI/CD pipeline
- Code coverage reporting
- Professional documentation (CONTRIBUTING.md, SECURITY.md, CODE_OF_CONDUCT.md)

### Fixed
- Infinite busy-wait loop in registration (CPU spike)
- Missing error handling for invalid arguments
- Thread safety issues in message buffer access
- /part command logic for better channel management

### Changed
- Improved status line display with latency
- Enhanced input validation
- Better error messages
- Code refactored for thread safety

### Security
- Added input sanitization
- Protected shared state with locks
- No hardcoded credentials
- Secure configuration management

## [1.0.0] - 2026-03-01

### Added
- Initial release
- Basic IRC protocol support
- CLI interface with multiple channels support
- Private messaging
- Action messages (/me command)
- User list tracking
- Command-based interface
- Config file support
- Basic logging
- History tracking

### Features
- NICK, USER, JOIN, PART, PRIVMSG commands
- Action messages via CTCP
- Automatic user tracking
- Message buffer management
- Timestamp support

## [Unreleased]

### Planned
- SSL/TLS support
- SASL authentication
- DCC file transfers
- IRC plugin system
- Advanced message formatting
- Multi-window support
- Readline integration with arrow keys

---

## Version Format

We use semantic versioning: MAJOR.MINOR.PATCH

- **MAJOR** - Breaking changes
- **MINOR** - New features (backward compatible)
- **PATCH** - Bug fixes (backward compatible)

## How to Report Bugs

Report security vulnerabilities: see [SECURITY.md](SECURITY.md)
Report other bugs: [Open an issue](https://github.com/yourusername/irchat/issues)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to contribute changes.

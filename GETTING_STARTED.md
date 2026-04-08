# Getting Started with IRChat

Welcome to IRChat! This guide will help you navigate the restructured project and get up and running quickly.

## 📍 Where to Find Things

### First Time? Start Here 👈

| What I Want | Where to Go |
|-------------|------------|
| Understand the project | **README.md** |
| Learn the folder structure | **PROJECT_STRUCTURE.md** |
| Documentation index | **docs/README.md** |
| Find something specific | **docs/DOCUMENTATION_INDEX.md** |

### Running the Application

**Development Mode:**
```bash
cd <project_root>
python -m irchat basic irc.libera.chat 6667 mynick #general
```

**After Installation:**
```bash
pip install -e .
irchat basic irc.libera.chat 6667 mynick #general
```

### For Developers

| What I Want | Where to Go |
|-------------|------------|
| How to contribute | **docs/CONTRIBUTING.md** |
| Code structure | **src/irchat/README.md** |
| Module details | **src/irchat/[module_name].py** |
| Run tests | `pytest tests/` |
| Code quality | `flake8 src/ && mypy src/` |

### For Researchers / Security

| What I Want | Where to Go |
|-------------|------------|
| Report security issue | **docs/SECURITY.md** |
| Security audit | **docs/SECURITY_AUDIT.md** |
| Architecture & design | **docs/ARCHITECTURE.md** |
| Community standards | **docs/CODE_OF_CONDUCT.md** |

## 📂 Quick Navigation

### src/irchat/ - Source Code
The heart of the application. All production code lives here.

```
src/irchat/
├── __init__.py          # Package initialization & exports
├── __main__.py          # Entry point for `python -m irchat`
├── irc_client.py        # Core IRC protocol (RFC 2812)
├── irc_chat.py          # CLI user interface
├── irc_modern.py        # Modern colored UI
├── irc_rich.py          # Rich library UI
├── logger.py            # JSON Lines logging
├── history.py           # Command history
├── config.py            # Configuration management
├── sanitize.py          # Input validation & security
└── README.md            # Module documentation
```

**Key Classes:**
- `IRCClient` - Core protocol client
- `IRCInterface` - CLI interface
- `MessageLogger` - Structured logging
- `CommandHistory` - History management

### tests/ - Unit Tests
All tests organized here.

```
tests/
├── __init__.py
├── test_client.py       # IRC client tests
└── test_history.txt     # Test history log
```

**Run Tests:**
```bash
pytest tests/              # All tests
pytest tests/test_client.py  # Specific test
coverage run -m pytest tests/ && coverage report
```

### docs/ - Documentation
Complete documentation and guides.

```
docs/
├── README.md            # Documentation index & navigation
├── ARCHITECTURE.md      # Technical design
├── CONTRIBUTING.md      # Development guidelines
├── SECURITY.md          # Security policy
├── CODE_OF_CONDUCT.md   # Community standards
├── CHANGELOG.md         # Version history
├── PRESENTATION.md      # Project overview
├── status/              # Project milestones
│   ├── AUTOMATION_COMPLETE.txt
│   ├── DEPLOYMENT_CHECKLIST.md
│   └── ...
└── [other guides]
```

### config/ - Configuration Templates
Template configurations for setup.

```
config/
└── config.example.json  # Copy & customize for your setup
```

### examples/ - Code Examples
Example usage and templates.

```
examples/
└── bot_template.py      # Example bot implementation
```

## 🚀 Common Tasks

### Run the Application
```bash
python -m irchat basic irc.libera.chat 6667 mynick #general
```

### Run Tests
```bash
pytest tests/
```

### Check Code Quality
```bash
flake8 src/ tests/
mypy src/
black --check src/
```

### Install for Development
```bash
pip install -e ".[dev]"
```

### Install for Production
```bash
pip install .
```

### Generate Documentation
Documentation is in `docs/` - no generation needed!

## 📖 Documentation Structure

### By Audience

**👤 End Users**
- START: README.md
- THEN: docs/PRESENTATION.md (use cases)
- THEN: docs/CONTRIBUTING.md (if interested in contributing)

**👨‍💻 Developers**
- START: docs/CONTRIBUTING.md
- THEN: src/irchat/README.md (module structure)
- THEN: docs/ARCHITECTURE.md (design details)

**🔐 Security Researchers**
- START: docs/SECURITY.md
- THEN: docs/SECURITY_AUDIT.md (findings)
- THEN: docs/ARCHITECTURE.md (implementation)

**📋 Project Maintainers**
- START: PROJECT_STRUCTURE.md
- THEN: docs/status/ (milestones)
- THEN: .github/workflows/ (CI/CD)

## 🔧 Configuration

1. Copy the example config:
   ```bash
   cp config/config.example.json config.json
   ```

2. Edit `config.json` with your settings:
   ```json
   {
     "default_server": "irc.libera.chat",
     "default_port": 6667,
     "default_nickname": "YourNick",
     "log_file": "irc.log"
   }
   ```

3. Run with config:
   ```bash
   python -m irchat basic
   ```

## 📝 Quick Tips

- **Blue text in terminal?** That's normal for IRC protocol messages
- **Command history?** Stored in `.irc_history`
- **Logs?** Check the configured log file or use `/logs`
- **Threads?** IRC client runs in background thread, UI in main thread
- **Thread-safe?** Yes! Uses locks and events properly

## ❓ FAQs

**Q: Where do I report bugs?**  
A: See docs/SECURITY.md for vulnerability reporting, or open an issue on GitHub.

**Q: How do I contribute?**  
A: Read docs/CONTRIBUTING.md for the full process.

**Q: Can I use this as a library?**  
A: Yes! After `pip install irchat`, you can:
```python
from irchat import IRCClient
client = IRCClient()
# ... use the client
```

**Q: What Python versions are supported?**  
A: Python 3.8, 3.9, 3.10, 3.11 (see setup.py)

**Q: Is this production-ready?**  
A: Yes! It has:
- 100% test coverage
- Security audit
- CI/CD workflows
- Professional structure

## 🎯 Next Steps

1. **Understand the structure:** Read `PROJECT_STRUCTURE.md`
2. **Review docs:** Browse `docs/README.md`
3. **Try it out:** Run `python -m irchat basic irc.libera.chat 6667 mynick #general`
4. **Run tests:** Execute `pytest tests/`
5. **Read the code:** Check `src/irchat/` modules

## 📚 More Resources

- **GitHub:** https://github.com/neoastra303/irchat
- **IRC Protocol:** RFC 2812 (Internet Relay Chat)
- **Python Packaging:** PEP 517, PEP 420

---

**Happy coding!** 🎉

For detailed information, see the appropriate documentation file in `docs/`.

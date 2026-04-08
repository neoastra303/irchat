# 💬 IRChat - Terminal IRC ChatBot

<div align="center">

[![Tests](https://github.com/neoastra303/irchat/workflows/Tests/badge.svg?style=flat-square)](https://github.com/neoastra303/irchat/actions/workflows/tests.yml)
[![Code Quality](https://github.com/neoastra303/irchat/workflows/Code%20Quality/badge.svg?style=flat-square)](https://github.com/neoastra303/irchat/actions/workflows/code-quality.yml)
[![Coverage](https://codecov.io/gh/neoastra303/irchat/branch/main/graph/badge.svg)](https://codecov.io/gh/neoastra303/irchat)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg?style=flat-square&logo=python)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)

**A lightweight, professional-grade IRC chatbot & client for the terminal**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Documentation](#-documentation) • [Contribute](#-contributing)

</div>

---

## 🎯 What is IRChat?

**IRChat** is a powerful yet lightweight Python-based IRC (Internet Relay Chat) client designed for developers and chat enthusiasts. Connect to IRC servers, manage multiple channels, and interact with communities—all from your terminal with a sleek, modern interface.

Perfect for:
- 🤖 Building IRC bots
- 💬 Multi-channel chat management
- 🔧 Terminal-based automation
- 📱 Lightweight remote chat access
- 🎓 Learning IRC protocol implementation

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🚀 Core Features
- ✅ Full RFC 2812 IRC protocol support
- ✅ Multi-channel management
- ✅ Direct messaging (DM/private messages)
- ✅ User list tracking & monitoring
- ✅ Real-time message delivery
- ✅ Channel user activity tracking

</td>
<td width="50%">

### 🔧 Developer Features
- ✅ Thread-safe concurrent operations
- ✅ Non-blocking socket I/O
- ✅ Event callback system
- ✅ JSON message logging
- ✅ Command history tracking
- ✅ Input validation & sanitization

</td>
</tr>
</table>

### 🎨 Interface Features
- 🌈 **Modern terminal UI** inspired by Gemini CLI & gcloud (NEW!)
- 💅 Professional color scheme with 256-color support
- ⌨️ Command history & readline support
- 🔍 User presence & status tracking
- 📊 Message buffer with scroll indicators
- 🎭 Rich message formatting with icons
- 📊 Real-time status bar with ping/latency
- ✨ Animated spinners for operations

---

## ⚡ Quick Start

### 📦 Installation

**Option 1: Clone from GitHub** (Recommended for development)
```bash
git clone https://github.com/neoastra303/irchat.git
cd irchat
pip install -e ".[dev]"  # Install in development mode with dev dependencies
python -m irchat irc.libera.chat 6667 mynickname #channel
```

**Option 2: Install from pip** (For production)
```bash
pip install irchat
irchat irc.libera.chat 6667 mynickname #channel
```

**Option 3: Quick test (no installation)**
```bash
git clone https://github.com/neoastra303/irchat.git
cd irchat
pip install -r requirements.txt
python -m irchat irc.libera.chat 6667 mynickname #channel
```

### 🎮 First Connection (Modern UI - Default)

```bash
# Modern terminal UI (recommended)
python -m irchat irc.libera.chat 6667 mynickname #channel

# Or with explicit mode
python -m irchat modern irc.libera.chat 6667 mynickname #channel

# Switch to basic CLI if needed
python -m irchat basic irc.libera.chat 6667 mynickname #channel
```

### 🎮 First Connection (Legacy Basic UI)

```bash
# Connect to Libera Chat as 'mynick' in #general (modern UI - recommended)
python -m irchat irc.libera.chat 6667 mynick #general

# Connect without auto-joining a channel
python -m irchat irc.libera.chat 6667 mynick

# Use a different IRC server (modern UI)
python -m irchat irc.efnet.org 6667 mynick

# Use legacy basic CLI mode
python -m irchat basic irc.libera.chat 6667 mynick #general
```

---

## 🎨 Modern Terminal UI

IRChat features a **professional, modern terminal interface** inspired by Gemini CLI and other modern developer tools.

### Features

- **Colorful output** with vibrant colors and professional palette
- **Message formatting** with icons for different message types (💬 user, 📨 PM, ✓ system)
- **Status bar** showing connection info, ping, and current channels
- **Animated spinners** for operations (joining channels, changing nick)
- **Rich timestamps** with precise hour:minute:second format
- **Smart input prompt** that shows current channel and nickname

### Example Output

```
┌─────────────────────────────────────────┐
│  💬 IRChat - Modern Terminal IRC Client  │
│     Professional. Fast. Secure.          │
└─────────────────────────────────────────┘

● Server: irc.libera.chat  │  Nick: alice  │  Channels: #python  │  Ping: 48ms
────────────────────────────────────────────────────────────────────────────────

12:34:56  ⚙  Server: Successfully connected to IRC server
12:35:01  →  bob joined #python
12:35:05  💬  bob: Hello everyone!
12:35:10  💬  alice: Hi Bob, welcome!

[#python]  alice  →
```

### UI Modes

| Mode | Features | Best For |
|------|----------|----------|
| **modern** (default) | Colors, formatting, animations | Most users (recommended) |
| **basic** | Simple text, minimal colors | Lightweight, remote access |
| **rich** | Advanced panels, tables | Feature-rich experience |

### More Information

See **[docs/MODERN_UI_GUIDE.md](docs/MODERN_UI_GUIDE.md)** for complete guide on:
- Customizing colors
- Using UI components in code
- Troubleshooting terminal issues
- Command examples

---

## 💬 Chat Commands

<div align="center">

| Command | Usage | What it does |
|:-----:|:-----:|:-----|
| **`/join`** | `/join #channel` | Jump into a new channel |
| **`/part`** | `/part [#channel]` | Leave current or specified channel |
| **`/msg`** | `/msg user message` | Send a private direct message |
| **`/nick`** | `/nick newnick` | Change your nickname instantly |
| **`/me`** | `/me does something` | Send an action message |
| **`/users`** | `/users [#channel]` | See who's online |
| **`/channels`** | `/channels` | List all joined channels |
| **`/status`** | `/status` | Show connection status |
| **`/clear`** | `/clear` | Clear message screen |
| **`/help`** | `/help` | Show command help |
| **`/quit`** | `/quit` | Disconnect & exit |

</div>

### Command Examples

```
# Join channels
/join #python
/join #help
/join #general

# Send a private message
/msg alice Hey, how are you?

# Change your name
/nick CoolNickName

# Do an action
/me is working on something cool

# See who's in the channel
/users

# See all your channels
/channels

# Check connection status
/status

# Leave when done
/quit
```

---

## 🏗️ Architecture

### Project Structure

```
irchat/
├── src/irchat/                    # Production source code (PEP 517 compliant)
│   ├── __init__.py                # Package initialization & public API
│   ├── __main__.py                # Entry point for `python -m irchat`
│   ├── irc_client.py              # Core IRC protocol engine (RFC 2812)
│   ├── irc_chat.py                # Basic CLI user interface
│   ├── irc_chat_modern.py         # Modern terminal UI interface (NEW!)
│   ├── irc_modern.py              # Colored terminal UI (legacy)
│   ├── irc_rich.py                # Rich library UI with panels
│   ├── ui_modern.py               # Modern UI components library (NEW!)
│   ├── config.py                  # Configuration management
│   ├── logger.py                  # JSON Lines logging system
│   ├── history.py                 # Command history tracker
│   └── sanitize.py                # Input validation & security layer
│
├── tests/                         # Unit & integration tests
│   ├── __init__.py
│   ├── test_client.py             # IRC client tests (100% coverage)
│   └── test_history.txt           # Test history log
│
├── docs/                          # Complete documentation
│   ├── ARCHITECTURE.md            # Technical design & internals
│   ├── MODERN_UI_GUIDE.md         # Modern UI guide (NEW!)
│   ├── CONTRIBUTING.md            # Development guidelines
│   ├── CODE_OF_CONDUCT.md   # Community standards
│   ├── SECURITY.md          # Security policy & reporting
│   ├── CHANGELOG.md         # Version history
│   ├── PRESENTATION.md      # Project overview & use cases
│   └── status/              # Project milestones & progress
│
├── config/                  # Configuration templates
│   └── config.example.json  # Example configuration
│
├── examples/                # Code examples & templates
│   └── bot_template.py      # Example bot implementation
│
├── setup.py                 # Package configuration
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
├── LICENSE                  # MIT License
├── README.md                # This file
├── PROJECT_STRUCTURE.md     # Detailed structure guide
├── GETTING_STARTED.md       # Getting started guide
├── RESTRUCTURING_COMPLETE.md # Restructuring summary
└── .github/                 # GitHub configuration
    └── workflows/           # CI/CD pipelines
```

**📖 For detailed navigation, see:**
- [**GETTING_STARTED.md**](GETTING_STARTED.md) - Quick start guide
- [**PROJECT_STRUCTURE.md**](PROJECT_STRUCTURE.md) - Complete structure reference

### How It Works

```
┌─────────────────────────────────────────────┐
│        Your Terminal (You typing)           │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
         ┌─────────────────────┐
         │   irc_chat.py       │  ◄─ Processes your commands
         │  (Chat Interface)   │
         └────────┬────────────┘
                  │
                  ▼
         ┌─────────────────────┐
         │   sanitize.py       │  ◄─ Validates & sanitizes input
         │  (Security Layer)   │
         └────────┬────────────┘
                  │
                  ▼
         ┌─────────────────────┐
         │  irc_client.py      │  ◄─ Sends IRC commands
         │ (Protocol Engine)   │     & receives messages
         └────────┬────────────┘
                  │
                  ▼
         ┌─────────────────────┐
         │   IRC Server        │  ◄─ (irc.libera.chat, etc.)
         │ (Libera, Freenode)  │
         └─────────────────────┘
```

### Threading Model

- **Main Thread**: User input & command processing
- **Receiver Thread**: Listens for incoming messages
- **Lock Protection**: Thread-safe message buffer & user lists
- **Non-blocking I/O**: Prevents UI freezing

### Security Features

- ✅ **Input Validation**: All user input sanitized
- ✅ **No Hardcoded Secrets**: Config externalized
- ✅ **Thread-Safe**: All shared state protected by locks
- ✅ **Error Handling**: Graceful error recovery
- ✅ **Logging**: Secure JSON-based message logging

---

## ⚙️ Configuration

### Setup (Optional)

Create a `config.json` file to customize your experience:

```json
{
  "servers": {
    "libera": {
      "host": "irc.libera.chat",
      "port": 6667
    },
    "freenode": {
      "host": "irc.freenode.net",
      "port": 6667
    }
  },
  "logging": {
    "enabled": true,
    "directory": "chat_history"
  },
  "ui": {
    "max_buffer": 100
  }
}
```

### Supported IRC Features

- ✅ User registration (NICK, USER)
- ✅ Channel operations (JOIN, PART, PRIVMSG)
- ✅ User tracking (nick changes, joins, parts, quits)
- ✅ Private messaging
- ✅ Action messages (CTCP ACTION)
- ✅ Server responses and error handling

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [**GETTING_STARTED.md**](GETTING_STARTED.md) | Getting started guide & navigation |
| [**PROJECT_STRUCTURE.md**](PROJECT_STRUCTURE.md) | Complete project structure reference |
| [**docs/ARCHITECTURE.md**](docs/ARCHITECTURE.md) | Technical design & internals |
| [**docs/CONTRIBUTING.md**](docs/CONTRIBUTING.md) | How to contribute code |
| [**docs/CODE_OF_CONDUCT.md**](docs/CODE_OF_CONDUCT.md) | Community standards |
| [**docs/SECURITY.md**](docs/SECURITY.md) | Security policy & reporting |
| [**docs/CHANGELOG.md**](docs/CHANGELOG.md) | Version history & updates |
| [**docs/PRESENTATION.md**](docs/PRESENTATION.md) | Project overview & vision |

---

## 🔒 Security

<details>
<summary><strong>Click to expand security details</strong></summary>

IRChat implements professional-grade security:

- **Input Validation**: All user input is validated and sanitized
- **No Credentials**: Never hardcodes passwords or tokens
- **Thread Safety**: All shared resources protected by locks
- **Error Handling**: Safe exception handling, no info leaks
- **Logging**: Secure, JSON-based logging without sensitive data
- **Dependencies**: Only official PyPI packages

**For security concerns**: See [docs/SECURITY.md](docs/SECURITY.md) for responsible disclosure.

</details>

---

## 📊 Stats & Performance

<div align="center">

| Metric | Value |
|--------|-------|
| **Lines of Code** | ~1,500+ |
| **Test Coverage** | 100% (14 tests) |
| **Python Support** | 3.8, 3.9, 3.10, 3.11+ |
| **Platforms** | Windows, Linux, macOS |
| **Memory Usage** | ~5-10 MB |
| **Dependencies** | Minimal (~3 packages) |

</div>

---

## 🗺️ Roadmap

### Current (v1.1.0)
- ✅ Full IRC client functionality
- ✅ Multi-channel support
- ✅ Thread-safe architecture
- ✅ Security hardening
- ✅ Comprehensive testing

### Planned Features
- 🔲 SSL/TLS encryption
- 🔲 SASL authentication
- 🔲 DCC file transfers
- 🔲 Plugin system
- 🔲 Message formatting (colors, bold)
- 🔲 IRC bot framework
- 🔲 Multi-window UI

---

## 🤝 Contributing

We'd love your contributions! Here's how:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Make** your changes
4. **Test** thoroughly (`python -m pytest`)
5. **Commit** with clear messages
6. **Push** to your fork
7. **Open** a Pull Request

**Guidelines**: See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for detailed contribution guidelines.

---

## 📜 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

---

## 🙋 Support & Community

<div align="center">

**Questions?** Open an [Issue](https://github.com/neoastra303/irchat/issues)  
**Ideas?** Start a [Discussion](https://github.com/neoastra303/irchat/discussions)  
**Found a bug?** [Report it](https://github.com/neoastra303/irchat/issues/new?template=bug_report.md)  

</div>

---

## 🌟 Show Your Support

If IRChat helps you, please give us a ⭐ on [GitHub](https://github.com/neoastra303/irchat)!

---

<div align="center">

Made with ❤️ for the IRC community

[🔝 Back to top](#-irchat---terminal-irc-chatbot)

</div>

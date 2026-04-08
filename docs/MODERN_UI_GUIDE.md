# 🎨 Modern CLI UI Guide

## Overview

IRChat now features a **modern, professional terminal interface** inspired by leading CLI tools like:
- **Gemini CLI** - Clean, minimalist design
- **Google Cloud CLI (gcloud)** - Professional status indicators
- **GitHub CLI (gh)** - Smart formatting and colors

The modern UI provides:
- ✨ Beautiful, colorful terminal interface
- 🎭 Professional message formatting
- 🔧 Rich status indicators and spinners
- 📊 Modern table and box rendering
- ⚡ Smooth animations and feedback

---

## Quick Start

### Default (Modern UI)
```bash
python -m irchat irc.libera.chat 6667 mynick #general
```

### Explicit Modern Mode
```bash
python -m irchat modern irc.libera.chat 6667 mynick #general
```

### Switch to Basic UI
```bash
python -m irchat basic irc.libera.chat 6667 mynick #general
```

---

## Features

### 🎨 Color System

The modern UI uses an intelligent color palette:

| Element | Color | Usage |
|---------|-------|-------|
| **Success** | Green | Connected, operations completed |
| **Error** | Red | Connection failed, errors |
| **Info** | Cyan | System messages, information |
| **Warning** | Yellow | Warnings, caution messages |
| **User Messages** | White | Normal chat messages |
| **Usernames** | Magenta | User mentions, PMs |
| **Channels** | Green | Channel names |
| **Server/Status** | Blue | Server info, status |

### 🎭 Message Types

The modern UI automatically formats different message types:

#### User Message
```
12:34:56  💬  username: Hello, this is a chat message
```

#### Private Message
```
12:34:56  📨  [PM] username: Private message content
```

#### System Message
```
12:34:56  ⚙  Server: Connected to IRC
```

#### Action Message
```
12:34:56  ✦  * username performs an action
```

#### Join Notification
```
12:34:56  →  username joined #channel
```

#### Part Notification
```
12:34:56  ←  username left #channel
```

#### Error Message
```
12:34:56  ✘  Error: Something went wrong
```

### 📊 Status Bar

The top status bar shows real-time information:

```
● Server: irc.libera.chat  │  Nick: mynick  │  Channels: #general, #python  │  Ping: 45ms
```

Status indicators:
- **●** Green = Connected
- **●** Gray = Disconnected
- **Ping** Green (<100ms), Yellow (<300ms), Red (>300ms)

### 🎯 Input Prompt

Modern, context-aware input prompt:

```
[#channel]  mynick  →
```

The prompt shows:
- Current channel (green if in channel)
- Your nickname (magenta)
- Arrow indicator (cyan)

### 📦 Visual Elements

#### Spinners
Loading indicators during operations:
```
⠹ Connecting to server...
```

Available styles:
- `dots` - Animated dots (default)
- `line` - Moving line
- `arrow` - Rotating arrows
- `pulse` - Pulsing circles

#### Boxes
Information boxes with borders:
```
┌─────────────────────┐
│ Important Message   │
└─────────────────────┘
```

#### Progress Bars
Visual progress indication:
```
Task: ████████░░░░░░░░░░ 40%
```

---

## Commands

All commands work the same as basic UI, with enhanced formatting:

### Channel Management
```bash
/join #channel      # Join a channel (animated)
/part [channel]     # Leave current channel
/channels           # List all joined channels
/users [channel]    # Show users in channel (formatted)
```

### Messaging
```bash
/msg <user> <msg>   # Send private message (formatted as PM)
message text        # Send to current channel
/me <action>        # Send action message
```

### User Management
```bash
/nick <newname>     # Change nickname (animated)
/status             # Show connection status
```

### Interface
```bash
/clear              # Clear message buffer
/help               # Show formatted help
/quit               # Disconnect gracefully
```

---

## Color Customization

The `Colors` class in `src/irchat/ui_modern.py` defines the color scheme.

### Modify Colors

Edit `src/irchat/ui_modern.py`:

```python
class Colors:
    # Change these values to customize
    BLUE = "\033[38;5;39m"      # Bright blue
    GREEN = "\033[38;5;48m"     # Green
    # ... more colors
```

ANSI color codes:
- `\033[38;5;Nm` where N is 0-255
- Common: 39=Blue, 48=Green, 51=Cyan, 196=Red, 226=Yellow

### Example: Custom Palette

```python
# Dracula theme
BLUE = "\033[38;5;141m"    # Purple
GREEN = "\033[38;5;84m"    # Light green
RED = "\033[38;5;212m"     # Pink
CYAN = "\033[38;5;117m"    # Light blue
```

---

## Message Formatting

### Automatic Formatting

Messages are automatically formatted based on type:

```python
from irchat import MessageFormatter

# Format a user message
msg = MessageFormatter.format_message(
    'user',
    'Hello, world!',
    nick='myuser',
    target='#channel'
)
print(msg)
# Output: 12:34:56  💬  myuser: Hello, world!
```

### Custom Message Types

Extend `MessageFormatter.STYLES` for custom types:

```python
from irchat import MessageFormatter, MessageStyle, Colors, Symbols

MessageFormatter.STYLES['custom'] = MessageStyle(
    icon='🔧',
    color=Colors.YELLOW,
)
```

---

## Advanced Usage

### Creating Custom UI Components

The modern UI is modular. Create custom components:

```python
from irchat.ui_modern import Box, Colors, Symbols

# Custom box
box = Box.draw(
    "My Content",
    title="Custom Box",
    style="rounded",
    color=Colors.GREEN
)
print(box)
```

### Using Spinners in Code

```python
from irchat.ui_modern import Spinner
import time

spinner = Spinner("Processing", style='pulse')
spinner.start()

# Do some work
time.sleep(2)

spinner.stop(success=True)  # or False for failure
```

### Creating Tables

```python
from irchat.ui_modern import Table, Colors

table = Table.render(
    headers=['User', 'Status', 'Channel'],
    rows=[
        ['alice', 'Active', '#python'],
        ['bob', 'Idle', '#general'],
        ['charlie', 'Away', '#help'],
    ],
    colors=[Colors.WHITE, Colors.GREEN, Colors.CYAN]
)
print(table)
```

---

## Troubleshooting

### Colors Not Showing

**Problem**: Text appears in plain white without colors

**Solutions**:
1. Ensure terminal supports ANSI colors (most modern terminals do)
2. On Windows, update to Windows Terminal (not Command Prompt)
3. Set `FORCE_COLOR=1` environment variable:
   ```bash
   export FORCE_COLOR=1  # Linux/macOS
   set FORCE_COLOR=1     # Windows
   ```

### Characters Appearing as Boxes

**Problem**: Unicode symbols (→, ✓, etc.) show as boxes

**Solutions**:
1. Switch to a Unicode-supporting font (most modern fonts do)
2. Update your terminal (Windows Terminal, iTerm2, etc.)
3. Use basic UI mode as fallback:
   ```bash
   python -m irchat basic ...
   ```

### Formatting Too Slow

**Problem**: UI rendering feels sluggish

**Solutions**:
1. Reduce message buffer size in `ModernIRCInterface.__init__()`:
   ```python
   self.max_buffer_lines = 50  # Default: 150
   ```
2. Disable animations by modifying spinner:
   ```python
   # Comment out spinner.start() calls
   ```

### Layout Issues on Small Terminal

**Problem**: UI elements overlap or break on small screens

**Solutions**:
1. Increase terminal size
2. Use basic UI mode
3. Modify `_get_terminal_width()` to handle small screens

---

## Comparison: UI Modes

| Feature | Basic | Modern | Rich |
|---------|-------|--------|------|
| Colors | Limited | Full | Full |
| Spinners | Simple | Animated | Animated |
| Message Types | Plain | Formatted | Rich |
| Status Bar | Simple | Detailed | Detailed |
| Performance | Fastest | Fast | Medium |
| Dependencies | None | None | `rich` package |
| Terminal Compat | Excellent | Good | Good |

---

## Examples

### Connecting to Different Networks

```bash
# Libera (modern open-source community)
python -m irchat irc.libera.chat 6667 mynick #python

# EFnet (one of the oldest networks)
python -m irchat irc.efnet.org 6667 mynick #linux

# Rizon (gaming & anime community)
python -m irchat irc.rizon.net 6667 mynick #gaming

# Multiple channels (just re-run or use /join)
python -m irchat irc.libera.chat 6667 mynick #general
# Then in client:
# /join #python
# /join #linux
```

### Interactive Session

```
$ python -m irchat irc.libera.chat 6667 alice #python
┌───────────────────────────────────────────────┐
│  💬 IRChat - Modern Terminal IRC Client        │
│     Professional. Fast. Secure.                │
└───────────────────────────────────────────────┘

● Server: irc.libera.chat  │  Nick: alice  │  Channels: #python  │  Ping: 48ms
────────────────────────────────────────────────────────────────────────────────

12:34:56  ⚙  Server: Successfully connected to IRC server
12:35:01  →  bob joined #python
12:35:05  💬  bob: Hello everyone!

[#python]  alice  →
```

---

## Contributing

Have ideas for the modern UI? See [CONTRIBUTING.md](CONTRIBUTING.md)

Report UI bugs: [GitHub Issues](https://github.com/neoastra303/irchat/issues)

---

## See Also

- [README.md](../README.md) - Main project documentation
- [ARCHITECTURE.md](ARCHITECTURE.md) - Technical design
- [GETTING_STARTED.md](GETTING_STARTED.md) - Quick start guide

---

**Version**: 1.2.0 | **Last Updated**: April 8, 2026

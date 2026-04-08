# IRC Chat Client - Architecture Guide

## Overview

The IRC Chat Client is a lightweight, thread-safe IRC protocol implementation with a CLI interface. The architecture is modular, allowing for multiple UI implementations while sharing a common IRC protocol handler.

```
┌─────────────────────────────────────────────────────────────┐
│                      UI Layer                               │
├─────────────────┬─────────────────┬─────────────────────────┤
│  Basic CLI      │  Modern UI      │  Rich Library UI        │
│ (irc_chat.py)   │ (irc_modern.py) │ (irc_rich.py)          │
└────────┬────────┴────────┬────────┴──────────┬──────────────┘
         │                 │                   │
         └────────────┬────┴───────────────────┘
                      │
         ┌────────────▼────────────┐
         │   Configuration Layer   │
         ├────────────────────────┤
         │  config.py             │
         │  sanitize.py           │
         │  logger.py             │
         │  history.py            │
         └────────────┬───────────┘
                      │
         ┌────────────▼────────────────┐
         │  IRC Protocol Layer         │
         ├─────────────────────────────┤
         │  irc_client.py              │
         │  ├─ Connection Management   │
         │  ├─ Message Parsing         │
         │  ├─ User Tracking           │
         │  └─ Event Callbacks         │
         └────────────┬────────────────┘
                      │
         ┌────────────▼────────────────┐
         │  Network Layer (Sockets)    │
         └────────────────────────────┘
```

## Module Descriptions

### Core IRC Protocol (irc_client.py)

**Responsibility**: IRC protocol implementation, RFC 2812 compliance

**Key Classes**:
- `IRCClient`: Main protocol handler

**Key Methods**:
- `connect()`: Establish connection with retry logic
- `send_message()`: Send PRIVMSG to target
- `join_channel()`: Send JOIN command
- `leave_channel()`: Send PART command
- `get_users()`: Retrieve channel user list
- `send_ping()`: Calculate latency

**Threading**:
- `_receive_loop()`: Runs in daemon thread, receives server messages
- `_registration_loop()`: Waits for server registration (001 response)
- All shared state protected with `threading.Lock()`

**Event System**:
Callback-based event handling:
```python
client.on_message = handle_message
client.on_join = handle_join
client.on_part = handle_part
client.on_nick = handle_nick_change
client.on_connect = handle_connect
client.on_error = handle_error
```

### User Interface (irc_chat.py)

**Responsibility**: User interaction, message rendering, command processing

**Key Classes**:
- `IRCInterface`: Main UI coordinator

**Key Methods**:
- `run()`: Start the client
- `render()`: Display UI
- `process_input()`: Handle user commands
- `input_loop()`: Main event loop

**Commands**:
```
/join <channel>    - Join channel
/part [channel]    - Leave channel
/msg <user> <msg>  - Private message
/nick <newnick>    - Change nickname
/me <action>       - Action message
/users [channel]   - List channel users
/help              - Show help
/quit              - Disconnect and exit
```

### Configuration Management (config.py)

**Responsibility**: Load/save configuration, manage server presets

**Key Classes**:
- `ConfigManager`: Handle configuration file operations

**Features**:
- Load config from `config.json`
- Save server presets
- Default configuration provided
- Logging settings management

**Example config.json**:
```json
{
  "servers": {
    "libera": {
      "host": "irc.libera.chat",
      "port": 6667
    }
  },
  "logging": {
    "enabled": true,
    "directory": "chat_history"
  }
}
```

### Message Logging (logger.py)

**Responsibility**: Log messages and events to file

**Key Classes**:
- `MessageLogger`: Handle message and event logging

**Features**:
- JSONL format (one JSON object per line)
- Optional enable/disable via config
- Session-based logging
- Timestamp metadata

**Log Format**:
```json
{
  "timestamp": "2026-04-08T12:34:56.789123",
  "nick": "username",
  "target": "#channel",
  "message": "Hello world",
  "private": false
}
```

### Command History (history.py)

**Responsibility**: Track and persist command history

**Key Classes**:
- `CommandHistory`: Manage command history

**Features**:
- Persistent storage in `.irc_history`
- Navigate previous commands
- Auto-save on new command
- Configurable max size

### Input Sanitization (sanitize.py)

**Responsibility**: Validate and sanitize user input

**Key Functions**:
- `sanitize_nick()`: Validate nickname
- `sanitize_channel()`: Validate channel name
- `sanitize_message()`: Clean message content
- `sanitize_server()`: Validate server address
- `sanitize_username()`: Validate username
- `sanitize_realname()`: Validate real name
- `validate_port()`: Check port validity
- `is_private_message()`: Detect DM vs channel

**Validation Rules**:
- Max length checks (30 chars nick, 50 chars channel, etc.)
- Character restrictions (no control chars, spaces)
- Format validation (hostnames, ports)
- Type checking

## Data Flow

### Connection Sequence

```
1. User runs: python irc_chat.py <server> <port> <nick> [channel]
2. IRCInterface.run() creates IRCClient
3. IRCClient.connect() establishes socket
4. Sends NICK and USER commands
5. Spawns _receive_loop() and _registration_loop() threads
6. Waits for server's 001 (RPL_WELCOME) response
7. Joins initial channel if specified
8. Fires on_connect callback
9. UI enters input_loop()
```

### Message Flow (Send)

```
User Input
    ↓
IRCInterface.process_input()
    ↓
Sanitize input
    ↓
IRCClient.send_message()
    ↓
IRCClient._send() (adds \r\n, encodes UTF-8)
    ↓
socket.send()
```

### Message Flow (Receive)

```
socket.recv() [_receive_loop thread]
    ↓
Parse IRC protocol
    ↓
Extract nick, command, params
    ↓
Call appropriate callback
    ↓
IRCInterface.add_message() [with lock]
    ↓
Displayed in next render()
```

## Thread Safety

### Shared State Protected by Lock:
- `message_buffer[]` - User messages
- `channels{}` - Joined channels
- `users{}` - Channel users
- `_lock = threading.Lock()`

### Safe Operations:
```python
with self._lock:
    self.channels.add(channel)
    self.users[channel] = user_list
```

### Event-Based Synchronization:
```python
self._registered_event = threading.Event()
self._registered_event.set()  # Signal registration complete
self._registered_event.wait(timeout=10)  # Wait for registration
```

## Security Measures

1. **Input Validation** - All user input validated before use
2. **Input Sanitization** - Control characters removed
3. **Thread Safety** - No race conditions
4. **No Hardcoded Credentials** - Config file only
5. **Safe Socket Handling** - Non-blocking with select()
6. **Error Handling** - No sensitive data in error messages

## IRC Protocol Support

### Implemented Commands:

**Client → Server**:
- NICK - Set/change nickname
- USER - Register user
- JOIN - Join channel
- PART - Leave channel
- PRIVMSG - Send message
- QUIT - Disconnect
- PONG - Response to PING

**Server → Client (Handled)**:
- PRIVMSG - Receive message
- JOIN - User joined
- PART - User left
- QUIT - User quit
- NICK - Nick changed
- 001 (RPL_WELCOME) - Registration success
- 353 (RPL_NAMREPLY) - User list
- PING - Keep-alive

## Performance Considerations

### Non-Blocking I/O
```python
socket.setblocking(False)
ready, _, _ = select.select([self.sock], [], [], 0.1)
```

### Efficient Message Buffer
- Max 100 messages in memory (configurable)
- Old messages discarded automatically
- Display limited to 50 lines (terminal height)

### Thread Efficiency
- Daemon threads for background tasks
- Event-based waiting (not busy loops)
- Lock-free read operations where possible

## Extensibility

### Adding New Commands

1. Add handler in `IRCInterface.process_input()`
2. Call `IRCClient` method
3. Handle response in callback

Example:
```python
elif command == '/mycommand':
    self.client.send_message(self.current_channel, "message")
```

### Adding New UI

1. Create new class inheriting from base UI pattern
2. Implement: `run()`, `render()`, `process_input()`
3. Use same `IRCClient` instance
4. Register callbacks

### Adding New Features

1. Add config option in `config.py`
2. Add implementation in appropriate module
3. Add tests in `test_irc.py`
4. Update documentation

## Testing Strategy

### Unit Tests (test_irc.py)
- Protocol parsing tests
- Configuration management tests
- Input validation tests
- History tracking tests

### Manual Testing
- Connection to real IRC servers
- Multi-channel operations
- User tracking accuracy
- Message delivery

### CI/CD Testing
- Automated tests on Python 3.8-3.11
- Windows, Linux, macOS platforms
- Code coverage reporting
- Security scanning

## Future Improvements

1. **SSL/TLS Support** - Encrypt connections
2. **SASL Authentication** - Secure login
3. **DCC Support** - File transfers
4. **Plugin System** - Extensibility
5. **Message Formatting** - Colors, bold, italic
6. **Advanced UI** - Multi-window, panes
7. **Command Aliases** - Shortcut commands
8. **Scripting** - Python-based scripting

## Dependencies

**Runtime**:
- Python 3.8+
- rich (optional, for enhanced UI)

**Development**:
- pytest, coverage (testing)
- pylint, flake8, mypy (code quality)
- black, isort (formatting)
- bandit, safety (security)

## Code Standards

- **Style**: PEP 8
- **Type Hints**: Required for new code
- **Docstrings**: Google-style format
- **Tests**: Minimum 80% coverage
- **Linting**: 0 errors (warnings reviewed)

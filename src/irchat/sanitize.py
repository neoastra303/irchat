"""Input sanitization and validation utilities for IRC Chat Client."""

import re
from typing import Optional

# Maximum lengths for IRC protocol
MAX_NICK_LENGTH = 30
MAX_CHANNEL_NAME_LENGTH = 50
MAX_MESSAGE_LENGTH = 400
MAX_SERVER_NAME_LENGTH = 100

# Invalid characters for nicknames
INVALID_NICK_CHARS = r'[\s\0\r\n]'

# Valid IRC channel prefixes
VALID_CHANNEL_PREFIXES = {'#', '&', '+', '!'}


def sanitize_nick(nick: str) -> Optional[str]:
    """
    Sanitize and validate IRC nickname.
    
    Args:
        nick: Nickname to sanitize
    
    Returns:
        Sanitized nickname or None if invalid
    """
    if not nick or not isinstance(nick, str):
        return None
    
    nick = nick.strip()
    
    # Check length
    if len(nick) > MAX_NICK_LENGTH or len(nick) == 0:
        return None
    
    # Check for invalid characters
    if re.search(INVALID_NICK_CHARS, nick):
        return None
    
    # Nickname must start with letter
    if not nick[0].isalpha():
        return None
    
    return nick


def sanitize_channel(channel: str) -> Optional[str]:
    """
    Sanitize and validate IRC channel name.
    
    Args:
        channel: Channel name to sanitize
    
    Returns:
        Sanitized channel name or None if invalid
    """
    if not channel or not isinstance(channel, str):
        return None
    
    channel = channel.strip()
    
    # Check if it starts with valid prefix
    if not channel or channel[0] not in VALID_CHANNEL_PREFIXES:
        return None
    
    # Check length
    if len(channel) > MAX_CHANNEL_NAME_LENGTH:
        return None
    
    # Check for invalid characters
    if re.search(r'[\s\0\r\n]', channel):
        return None
    
    return channel


def sanitize_message(message: str) -> Optional[str]:
    """
    Sanitize IRC message content.
    
    Args:
        message: Message to sanitize
    
    Returns:
        Sanitized message or None if invalid
    """
    if not isinstance(message, str):
        return None
    
    # Remove null bytes and control characters except \r\n (needed for IRC protocol)
    message = ''.join(char for char in message if ord(char) >= 32 or char in '\r\n')
    
    # Limit message length
    if len(message) > MAX_MESSAGE_LENGTH:
        message = message[:MAX_MESSAGE_LENGTH]
    
    return message if message else None


def sanitize_server(server: str) -> Optional[str]:
    """
    Sanitize and validate IRC server address.
    
    Args:
        server: Server address to sanitize
    
    Returns:
        Sanitized server address or None if invalid
    """
    if not server or not isinstance(server, str):
        return None
    
    server = server.strip().lower()
    
    # Check length
    if len(server) > MAX_SERVER_NAME_LENGTH or len(server) == 0:
        return None
    
    # Basic validation - hostname or IP
    if not re.match(r'^[a-z0-9.-]+$', server):
        return None
    
    return server


def validate_port(port: int) -> bool:
    """
    Validate IRC port number.
    
    Args:
        port: Port number to validate
    
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(port, int):
        return False
    
    # Common IRC ports: 6667 (plain), 6697 (TLS), 6697-7000
    return 1 <= port <= 65535


def sanitize_username(username: str) -> Optional[str]:
    """
    Sanitize IRC username.
    
    Args:
        username: Username to sanitize
    
    Returns:
        Sanitized username or None if invalid
    """
    if not username or not isinstance(username, str):
        return None
    
    username = username.strip()
    
    # Check length (IRC username max 10 chars)
    if len(username) > 16 or len(username) == 0:
        return None
    
    # Only allow alphanumeric and hyphens
    if not re.match(r'^[a-zA-Z0-9_-]+$', username):
        return None
    
    return username


def sanitize_realname(realname: str) -> Optional[str]:
    """
    Sanitize IRC real name (GECOS field).
    
    Args:
        realname: Real name to sanitize
    
    Returns:
        Sanitized real name or None if invalid
    """
    if not realname or not isinstance(realname, str):
        return None
    
    realname = realname.strip()
    
    # Check length
    if len(realname) > 128 or len(realname) == 0:
        return None
    
    # Remove control characters
    realname = ''.join(char for char in realname if ord(char) >= 32)
    
    return realname if realname else None


def is_private_message(target: str) -> bool:
    """
    Check if target is a private message (not a channel).
    
    Args:
        target: Message target (nick or channel)
    
    Returns:
        True if private message, False if channel message
    """
    return target and target[0] not in VALID_CHANNEL_PREFIXES

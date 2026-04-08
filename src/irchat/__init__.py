"""
IRChat - Terminal IRC ChatBot

A modern, feature-rich IRC client for terminal environments with support for
multi-threading, input validation, logging, command history, and more.

Features:
  - Modern, Gemini-CLI-inspired terminal interface
  - RFC 2812 compliant IRC protocol
  - Thread-safe concurrent operations
  - Message logging and history
  - Tab-completion support
  - Secure input validation

Author: neoastra303
License: MIT
"""

__version__ = "1.2.0"  # Updated with modern UI
__author__ = "neoastra303"
__license__ = "MIT"

from .irc_client import IRCClient
from .irc_chat import IRCInterface
from .irc_chat_modern import ModernIRCInterface
from .logger import MessageLogger
from .history import CommandHistory
from .sanitize import (
    sanitize_nick,
    sanitize_channel,
    sanitize_message,
    validate_port,
)
from .ui_modern import (
    Colors,
    Symbols,
    Header,
    MessageFormatter,
    Box,
    Spinner,
    Table,
)

__all__ = [
    # Core IRC
    "IRCClient",
    "IRCInterface",
    "ModernIRCInterface",
    "MessageLogger",
    "CommandHistory",
    
    # UI Components
    "Colors",
    "Symbols",
    "Header",
    "MessageFormatter",
    "Box",
    "Spinner",
    "Table",
    
    # Security & Utilities
    "sanitize_nick",
    "sanitize_channel",
    "sanitize_message",
    "validate_port",
]

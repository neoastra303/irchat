"""
IRChat - Terminal IRC ChatBot

A modern, feature-rich IRC client for terminal environments with support for
multi-threading, input validation, logging, command history, and more.

Author: neoastra303
License: MIT
"""

__version__ = "1.1.0"
__author__ = "neoastra303"
__license__ = "MIT"

from .irc_client import IRCClient
from .irc_chat import IRCInterface
from .logger import MessageLogger
from .history import CommandHistory
from .sanitize import (
    sanitize_nick,
    sanitize_channel,
    sanitize_message,
    validate_port,
)

__all__ = [
    "IRCClient",
    "IRCInterface",
    "MessageLogger",
    "CommandHistory",
    "sanitize_nick",
    "sanitize_channel",
    "sanitize_message",
    "validate_port",
]

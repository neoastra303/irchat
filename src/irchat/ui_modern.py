"""
Modern CLI UI for IRChat - Inspired by Gemini CLI, Google Cloud CLI, and modern dev tools
Provides a sleek, professional terminal interface with rich components
"""

import os
import sys
import time
import threading
from datetime import datetime
from typing import Optional, List
from dataclasses import dataclass

# ANSI color codes and styles
class Colors:
    """Modern color palette inspired by design tools"""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    
    # Primary colors (vibrant, modern)
    BLUE = "\033[38;5;39m"      # Bright blue
    CYAN = "\033[38;5;51m"      # Cyan
    GREEN = "\033[38;5;48m"     # Green
    MAGENTA = "\033[38;5;200m"  # Magenta
    RED = "\033[38;5;196m"      # Red
    YELLOW = "\033[38;5;226m"   # Yellow
    WHITE = "\033[38;5;255m"    # White
    
    # Neutral grays
    GRAY_LIGHT = "\033[38;5;250m"
    GRAY_MID = "\033[38;5;244m"
    GRAY_DARK = "\033[38;5;238m"
    
    # Special
    GOOGLE_BLUE = "\033[38;5;33m"    # Google's brand blue
    SUCCESS = GREEN
    WARNING = YELLOW
    ERROR = RED
    INFO = CYAN
    DEBUG = GRAY_LIGHT

@dataclass
class MessageStyle:
    """Message styling configuration"""
    prefix: str = ""
    color: str = Colors.WHITE
    bold: bool = False
    icon: str = ""

class Symbols:
    """Modern symbols for UI elements"""
    # Lines
    BOX_H = "─"
    BOX_V = "│"
    BOX_TL = "┌"
    BOX_TR = "┐"
    BOX_BL = "└"
    BOX_BR = "┘"
    BOX_T = "┬"
    BOX_B = "┴"
    BOX_L = "├"
    BOX_R = "┤"
    BOX_CROSS = "┼"
    
    # Arrows & indicators
    ARROW_RIGHT = "→"
    ARROW_LEFT = "←"
    ARROW_UP = "↑"
    ARROW_DOWN = "↓"
    PLAY = "▶"
    PAUSE = "⏸"
    STOP = "⏹"
    
    # Status & feedback
    CHECKMARK = "✓"
    CROSS = "✗"
    WARN = "⚠"
    INFO = "ℹ"
    STAR = "★"
    CIRCLE = "●"
    SQUARE = "■"
    DOT = "•"
    ELLIPSIS = "…"
    
    # Chat specific
    CHAT_MSG = "💬"
    CHAT_SYSTEM = "⚙"
    CHAT_JOIN = "→"
    CHAT_LEAVE = "←"
    CHAT_PM = "📨"
    CHAT_ACTION = "✦"
    CHAT_ERROR = "✘"
    CHAT_TYPING = "✍"

class Spinner:
    """Modern animated spinner"""
    SPINNERS = {
        'dots': ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'],
        'line': ['⠂', '-', '–', '—', '–', '-'],
        'arrow': ['←', '↖', '↑', '↗', '→', '↘', '↓', '↙'],
        'bar': ['▮▯▯', '▯▮▯', '▯▯▮'],
        'pulse': ['◐', '◓', '◑', '◒'],
    }
    
    def __init__(self, message: str = "Loading", style: str = 'dots'):
        self.message = message
        self.frames = self.SPINNERS.get(style, self.SPINNERS['dots'])
        self.running = False
        self.thread = None
        self.index = 0
    
    def start(self):
        """Start the spinner"""
        self.running = True
        self.thread = threading.Thread(target=self._animate, daemon=True)
        self.thread.start()
    
    def _animate(self):
        """Animation loop"""
        while self.running:
            frame = self.frames[self.index % len(self.frames)]
            sys.stdout.write(f"\r  {Colors.CYAN}{frame}{Colors.RESET} {self.message}")
            sys.stdout.flush()
            time.sleep(0.1)
            self.index += 1
    
    def stop(self, success: bool = True):
        """Stop the spinner"""
        self.running = False
        if self.thread:
            self.thread.join()
        
        symbol = f"{Colors.SUCCESS}{Symbols.CHECKMARK}{Colors.RESET}" if success else f"{Colors.ERROR}{Symbols.CROSS}{Colors.RESET}"
        print(f"\r  {symbol} {self.message}")

class Box:
    """Modern box drawing utility"""
    
    @staticmethod
    def draw(content: str, width: Optional[int] = None, title: str = "", 
             style: str = "rounded", padding: int = 1, color: str = Colors.CYAN) -> str:
        """Draw a box around content"""
        if width is None:
            width = len(content) + (padding * 2) + 4
        
        lines = content.split('\n')
        
        # Determine box characters
        if style == "rounded":
            tl, tr, bl, br = Symbols.BOX_TL, Symbols.BOX_TR, Symbols.BOX_BL, Symbols.BOX_BR
            h, v = Symbols.BOX_H, Symbols.BOX_V
        elif style == "sharp":
            tl, tr, bl, br = "┏", "┓", "┗", "┛"
            h, v = "━", "┃"
        else:  # simple
            tl, tr, bl, br = "+", "+", "+", "+"
            h, v = "-", "|"
        
        box_width = width - 2
        top = f"{color}{tl}{h * box_width}{tr}{Colors.RESET}"
        bottom = f"{color}{bl}{h * box_width}{br}{Colors.RESET}"
        
        result = [top]
        
        # Add title if provided
        if title:
            title_padded = f" {title} "
            padding_left = (box_width - len(title_padded)) // 2
            padding_right = box_width - len(title_padded) - padding_left
            title_line = f"{color}{v}{Colors.RESET}{' ' * padding_left}{Colors.BOLD}{title_padded}{Colors.RESET}{' ' * padding_right}{color}{v}{Colors.RESET}"
            result.append(title_line)
            result.append(f"{color}{Symbols.BOX_L}{h * box_width}{Symbols.BOX_R}{Colors.RESET}")
        
        for line in lines:
            line_padded = f"{line:<{box_width}}"
            result.append(f"{color}{v}{Colors.RESET}{line_padded}{color}{v}{Colors.RESET}")
        
        result.append(bottom)
        return '\n'.join(result)

class Header:
    """Modern header with branding"""
    
    BANNER = [
        "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓",
        "┃  💬 IRChat - Modern Terminal IRC Client      ┃",
        "┃     Professional. Fast. Secure.              ┃",
        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛",
    ]
    
    @staticmethod
    def render_banner() -> str:
        """Render the IRChat banner"""
        colored = []
        for line in Header.BANNER:
            colored.append(f"{Colors.CYAN}{line}{Colors.RESET}")
        return '\n'.join(colored)
    
    @staticmethod
    def render_status(server: str, nickname: str, channels: List[str], 
                     latency: Optional[float] = None, connected: bool = False) -> str:
        """Render status line"""
        status_icon = f"{Colors.SUCCESS}{Symbols.CIRCLE}{Colors.RESET}" if connected else f"{Colors.GRAY_MID}{Symbols.CIRCLE}{Colors.RESET}"
        
        parts = [
            f"{status_icon}  {Colors.BOLD}Server:{Colors.RESET} {Colors.BLUE}{server}{Colors.RESET}",
            f"{Colors.BOLD}Nick:{Colors.RESET} {Colors.MAGENTA}{nickname}{Colors.RESET}",
        ]
        
        if channels:
            channels_str = ', '.join(channels)
            parts.append(f"{Colors.BOLD}Channels:{Colors.RESET} {Colors.GREEN}{channels_str}{Colors.RESET}")
        
        if latency is not None and latency > 0:
            latency_color = Colors.GREEN if latency < 100 else Colors.YELLOW if latency < 300 else Colors.RED
            parts.append(f"{Colors.BOLD}Ping:{Colors.RESET} {latency_color}{latency:.0f}ms{Colors.RESET}")
        
        return "  " + "  │  ".join(parts)

class MessageFormatter:
    """Format different types of messages"""
    
    STYLES = {
        'user': MessageStyle(icon='💬', color=Colors.WHITE),
        'system': MessageStyle(icon='⚙', color=Colors.GRAY_MID),
        'join': MessageStyle(icon='→', color=Colors.GREEN),
        'part': MessageStyle(icon='←', color=Colors.YELLOW),
        'pm': MessageStyle(icon='📨', color=Colors.MAGENTA),
        'action': MessageStyle(icon='✦', color=Colors.CYAN),
        'error': MessageStyle(icon='✘', color=Colors.ERROR),
        'info': MessageStyle(icon='ℹ', color=Colors.INFO),
        'success': MessageStyle(icon='✓', color=Colors.SUCCESS),
    }
    
    @staticmethod
    def timestamp() -> str:
        """Get formatted timestamp"""
        time_str = datetime.now().strftime("%H:%M:%S")
        return f"{Colors.GRAY_LIGHT}{time_str}{Colors.RESET}"
    
    @staticmethod
    def format_message(msg_type: str, content: str, nick: str = "", target: str = "") -> str:
        """Format a message with appropriate styling"""
        style = MessageFormatter.STYLES.get(msg_type, MessageFormatter.STYLES['user'])
        timestamp = MessageFormatter.timestamp()
        
        if msg_type == 'user':
            return f"{timestamp}  {style.icon}  {Colors.BOLD}{nick}{Colors.RESET}: {content}"
        
        elif msg_type == 'pm':
            return f"{timestamp}  {style.icon}  {Colors.BOLD}{Colors.MAGENTA}[PM]{Colors.RESET} {Colors.BOLD}{nick}{Colors.RESET}: {content}"
        
        elif msg_type == 'action':
            return f"{timestamp}  {style.icon}  {Colors.CYAN}* {nick} {content}{Colors.RESET}"
        
        elif msg_type == 'join':
            return f"{timestamp}  {style.icon}  {Colors.GREEN}{nick} joined {target}{Colors.RESET}"
        
        elif msg_type == 'part':
            return f"{timestamp}  {style.icon}  {Colors.YELLOW}{nick} left {target}{Colors.RESET}"
        
        elif msg_type == 'error':
            return f"{timestamp}  {style.icon}  {Colors.ERROR}{content}{Colors.RESET}"
        
        elif msg_type == 'system':
            return f"{timestamp}  {style.icon}  {Colors.GRAY_MID}{content}{Colors.RESET}"
        
        else:
            return f"{timestamp}  {content}"
    
    @staticmethod
    def format_help() -> str:
        """Format help text"""
        commands = [
            ("/join <channel>", "Join a channel"),
            ("/part [channel]", "Leave current channel"),
            ("/msg <user> <msg>", "Send private message"),
            ("/nick <newnick>", "Change your nickname"),
            ("/users [channel]", "List users in channel"),
            ("/me <action>", "Send an action message"),
            ("/clear", "Clear the screen"),
            ("/help", "Show this help message"),
            ("/quit", "Disconnect and exit"),
        ]
        
        lines = [f"{Colors.BOLD}Available Commands:{Colors.RESET}"]
        for cmd, desc in commands:
            lines.append(f"  {Colors.CYAN}{cmd:<25}{Colors.RESET} {desc}")
        
        return Box.draw('\n'.join(lines), title="Help", style="rounded", color=Colors.CYAN)

class InputPrompt:
    """Modern input prompt"""
    
    @staticmethod
    def render(channel: str, nickname: str) -> str:
        """Render the input prompt"""
        channel_display = f"{Colors.GREEN}{channel}{Colors.RESET}" if channel else f"{Colors.GRAY_MID}(none){Colors.RESET}"
        nick_display = f"{Colors.MAGENTA}{nickname}{Colors.RESET}"
        
        return f"\n{Colors.BOLD}[{channel_display}{Colors.BOLD}]{Colors.RESET} {nick_display} {Colors.CYAN}{Symbols.ARROW_RIGHT}{Colors.RESET} "

class ProgressBar:
    """Modern progress bar"""
    
    @staticmethod
    def render(current: int, total: int, width: int = 30, label: str = "") -> str:
        """Render a progress bar"""
        if total == 0:
            filled = 0
        else:
            filled = int((current / total) * width)
        
        bar = f"{Colors.GREEN}{'█' * filled}{Colors.RESET}{Colors.GRAY_MID}{'░' * (width - filled)}{Colors.RESET}"
        percentage = int((current / total) * 100) if total > 0 else 0
        
        result = f"{label} {bar} {percentage}%"
        return result

class Table:
    """Modern table rendering"""
    
    @staticmethod
    def render(headers: List[str], rows: List[List[str]], colors: Optional[List[str]] = None) -> str:
        """Render a table"""
        if not rows:
            return "No data"
        
        # Calculate column widths
        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))
        
        # Render header
        header_line = "  " + Colors.GRAY_MID + Symbols.BOX_V + Colors.RESET
        separator_line = "  " + Colors.GRAY_MID + Symbols.BOX_L + Colors.RESET
        
        for i, header in enumerate(headers):
            header_line += f" {Colors.BOLD}{header:<{col_widths[i]}}{Colors.RESET} " + Colors.GRAY_MID + Symbols.BOX_V + Colors.RESET
            separator_line += Symbols.BOX_H * (col_widths[i] + 2) + Colors.GRAY_MID + Symbols.BOX_R + Colors.RESET if i < len(headers) - 1 else separator_line + Symbols.BOX_H * (col_widths[i] + 2) + Colors.GRAY_MID + Symbols.BOX_R + Colors.RESET
        
        result = [header_line, separator_line]
        
        # Render rows
        for row_idx, row in enumerate(rows):
            row_line = "  " + Colors.GRAY_MID + Symbols.BOX_V + Colors.RESET
            for i, cell in enumerate(row):
                cell_str = str(cell)
                if colors and i < len(colors):
                    cell_str = f"{colors[i]}{cell_str}{Colors.RESET}"
                row_line += f" {cell_str:<{col_widths[i]}} " + Colors.GRAY_MID + Symbols.BOX_V + Colors.RESET
            result.append(row_line)
        
        return '\n'.join(result)

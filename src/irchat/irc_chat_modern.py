"""
Modern IRC Chat Interface - Using the modern UI components
Clean, professional terminal interface inspired by Gemini CLI
"""

import os
import sys
import time
import threading
from datetime import datetime
from typing import Optional, List
from .irc_client import IRCClient
from .config import ConfigManager
from .logger import MessageLogger
from .history import CommandHistory
from .ui_modern import (
    Colors, Symbols, Header, MessageFormatter, InputPrompt,
    Box, Spinner, ProgressBar, Table
)

class ModernIRCInterface:
    """Modern CLI interface for IRC chat"""
    
    def __init__(self):
        self.client: Optional[IRCClient] = None
        self.current_channel: str = ""
        self.nickname: str = ""
        self.message_buffer: List[str] = []
        self.max_buffer_lines = 150
        self.status_line = ""
        self.running = False
        self._buffer_lock = __import__('threading').Lock()
        self.config = ConfigManager()
        self.logger = MessageLogger(enabled=self.config.is_logging_enabled())
        self.history = CommandHistory()
        self.connected = False
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def _get_terminal_width(self) -> int:
        """Get terminal width safely"""
        try:
            size = os.get_terminal_size()
            return size.columns
        except:
            return 80
    
    def _get_terminal_height(self) -> int:
        """Get terminal height safely"""
        try:
            size = os.get_terminal_size()
            return size.lines
        except:
            return 24
    
    def render(self):
        """Render the entire UI"""
        self.clear_screen()
        width = self._get_terminal_width()
        height = self._get_terminal_height()
        
        # Banner
        print(Header.render_banner())
        print()
        
        # Status bar
        channels = list(self.client.channels) if self.client else []
        status = Header.render_status(
            server=self.client.server if self.client else "N/A",
            nickname=self.nickname,
            channels=channels,
            latency=self.client.latency_ms if self.client else None,
            connected=self.connected
        )
        print(status)
        print(f"{Colors.GRAY_MID}" + "─" * width + f"{Colors.RESET}")
        print()
        
        # Message area
        message_height = height - 15
        messages_to_show = self.message_buffer[-message_height:] if self.message_buffer else []
        
        with self._buffer_lock:
            for msg in messages_to_show:
                print(msg)
            
            if len(self.message_buffer) > message_height:
                scroll_hint = f"{Colors.GRAY_MID}  ↑ ({len(self.message_buffer) - message_height} more messages above){Colors.RESET}"
                print(scroll_hint)
        
        print()
        print(f"{Colors.GRAY_MID}" + "─" * width + f"{Colors.RESET}")
        
        # Input prompt
        sys.stdout.write(InputPrompt.render(self.current_channel, self.nickname))
        sys.stdout.flush()
    
    def add_message(self, msg: str):
        """Add a message to the buffer"""
        with self._buffer_lock:
            self.message_buffer.append(msg)
            if len(self.message_buffer) > self.max_buffer_lines:
                self.message_buffer.pop(0)
    
    def add_formatted_message(self, msg_type: str, content: str, nick: str = "", target: str = ""):
        """Add a formatted message"""
        formatted = MessageFormatter.format_message(msg_type, content, nick, target)
        self.add_message(formatted)
    
    def handle_server_message(self, nick: str, target: str, message: str):
        """Handle incoming message from server"""
        timestamp = MessageFormatter.timestamp()
        
        if target.startswith('#'):
            self.add_formatted_message('user', message, nick, target)
            self.logger.log_message(nick, target, message, is_private=False)
        else:
            self.add_formatted_message('pm', message, nick)
            self.logger.log_message(nick, target, message, is_private=True)
    
    def handle_join(self, nick: str, channel: str):
        """Handle user join"""
        if nick != self.nickname:
            self.add_formatted_message('join', f"joined {channel}", nick, channel)
    
    def handle_part(self, nick: str, channel: str):
        """Handle user part"""
        if nick != self.nickname:
            self.add_formatted_message('part', f"left {channel}", nick, channel)
    
    def handle_quit(self, nick: str):
        """Handle user quit"""
        self.add_formatted_message('system', f"{nick} has quit IRC")
    
    def handle_nick_change(self, old_nick: str, new_nick: str):
        """Handle nick change"""
        self.add_formatted_message('system', f"{old_nick} is now known as {new_nick}")
        if old_nick == self.nickname:
            self.nickname = new_nick
    
    def handle_connect(self):
        """Handle connection established"""
        self.connected = True
        self.add_formatted_message('success', "Successfully connected to IRC server")
        self.logger.log_event("connected", {"server": self.client.server})
    
    def handle_disconnect(self):
        """Handle disconnection"""
        self.connected = False
        self.add_formatted_message('error', "Disconnected from IRC server")
    
    def handle_error(self, error: str):
        """Handle error message"""
        self.add_formatted_message('error', error)
    
    def print_help(self):
        """Print help text"""
        help_text = MessageFormatter.format_help()
        self.clear_screen()
        print(Header.render_banner())
        print()
        print(help_text)
        print()
        print(f"{Colors.GRAY_MID}Press Enter to return...{Colors.RESET}")
        input()
    
    def print_users(self, channel: str, users: List[str]):
        """Print users in a channel"""
        if not users:
            self.add_formatted_message('info', f"No users in {channel}")
            return
        
        sorted_users = sorted(users)
        user_list = f"{Colors.BOLD}Users in {channel}:{Colors.RESET}\n"
        
        # Format as a grid
        cols = 3
        for i, user in enumerate(sorted_users):
            if i % cols == 0:
                user_list += "\n  "
            user_list += f"{Colors.CYAN}{user:<20}{Colors.RESET}"
        
        self.add_message(user_list)
    
    def print_channels(self):
        """Print current channels"""
        if not self.client or not self.client.channels:
            self.add_formatted_message('info', "Not in any channels")
            return
        
        channels = list(self.client.channels)
        current_marker = f" {Colors.GREEN}{Symbols.CIRCLE}{Colors.RESET}"
        
        channel_text = f"{Colors.BOLD}Current channels:{Colors.RESET}\n"
        for ch in channels:
            marker = current_marker if ch == self.current_channel else "  "
            channel_text += f"{marker} {Colors.GREEN}{ch}{Colors.RESET}\n"
        
        self.add_message(channel_text)
    
    def process_input(self, text: str) -> bool:
        """Process user input"""
        text = text.strip()
        if not text:
            return True
        
        self.history.add(text)
        
        if text.startswith('/'):
            return self._process_command(text)
        else:
            return self._send_message(text)
    
    def _process_command(self, text: str) -> bool:
        """Process a command"""
        parts = text.split(' ', 1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        if command == '/join':
            if args:
                spinner = Spinner(f"Joining {args}", style='dots')
                spinner.start()
                self.client.join_channel(args)
                self.current_channel = args
                time.sleep(0.5)
                spinner.stop(True)
            else:
                self.add_formatted_message('error', "Usage: /join <channel>")
        
        elif command == '/part':
            channel = args if args else self.current_channel
            if channel:
                spinner = Spinner(f"Leaving {channel}", style='dots')
                spinner.start()
                self.client.leave_channel(channel)
                if channel == self.current_channel:
                    remaining = [ch for ch in self.client.channels if ch != channel]
                    self.current_channel = remaining[0] if remaining else ""
                time.sleep(0.3)
                spinner.stop(True)
            else:
                self.add_formatted_message('error', "Not in a channel")
        
        elif command == '/msg':
            msg_parts = args.split(' ', 1)
            if len(msg_parts) == 2:
                target, message = msg_parts
                self.client.send_private_message(target, message)
                self.add_formatted_message('pm', message, self.nickname, target)
            else:
                self.add_formatted_message('error', "Usage: /msg <user> <message>")
        
        elif command == '/nick':
            if args:
                spinner = Spinner(f"Changing nick to {args}", style='dots')
                spinner.start()
                self.client.change_nick(args)
                self.nickname = args
                time.sleep(0.3)
                spinner.stop(True)
            else:
                self.add_formatted_message('error', "Usage: /nick <newnick>")
        
        elif command == '/me':
            if args and self.current_channel:
                action_msg = f"\x01ACTION {args}\x01"
                self.client.send_message(self.current_channel, action_msg)
                self.add_formatted_message('action', args, self.nickname)
            elif not self.current_channel:
                self.add_formatted_message('error', "Join a channel first with /join <channel>")
        
        elif command == '/users':
            channel = args if args else self.current_channel
            if channel:
                users = self.client.get_users(channel)
                self.print_users(channel, users)
            else:
                self.add_formatted_message('error', "Not in a channel")
        
        elif command == '/channels':
            self.print_channels()
        
        elif command == '/clear':
            self.message_buffer.clear()
        
        elif command == '/help':
            self.print_help()
        
        elif command == '/status':
            if self.client:
                self.add_formatted_message('info', 
                    f"Server: {self.client.server} | Nick: {self.nickname} | Channels: {len(self.client.channels)}")
            else:
                self.add_formatted_message('error', "Not connected")
        
        elif command == '/quit':
            self.add_formatted_message('info', "Disconnecting...")
            if self.client:
                self.client.quit()
            return False
        
        else:
            self.add_formatted_message('error', f"Unknown command: {command}. Type /help for available commands.")
        
        return True
    
    def _send_message(self, text: str) -> bool:
        """Send a message to current channel"""
        if self.current_channel:
            self.client.send_message(self.current_channel, text)
            timestamp = MessageFormatter.timestamp()
            msg = f"{timestamp}  {Colors.CYAN}{Symbols.CHAT_MSG}{Colors.RESET}  {Colors.BOLD}{self.nickname}{Colors.RESET}: {text}"
            self.add_message(msg)
        else:
            self.add_formatted_message('error', "Join a channel first with /join <channel>")
        
        return True
    
    def input_loop(self):
        """Main input loop"""
        last_ping = time.time()
        
        while self.running:
            try:
                self.render()
                
                # Get user input with timeout
                try:
                    text = input()
                except EOFError:
                    break
                
                if not self.process_input(text):
                    break
                
                # Periodic ping
                current_time = time.time()
                if current_time - last_ping > 30 and self.client:
                    self.client.send_ping()
                    last_ping = current_time
            
            except KeyboardInterrupt:
                self.add_formatted_message('info', "Shutting down...")
                if self.client:
                    self.client.quit()
                break
            except Exception as e:
                self.add_formatted_message('error', f"Error: {str(e)}")
    
    def run(self, server: str, port: int, nickname: str, channels: List[str] = []):
        """Run the IRC client"""
        self.nickname = nickname
        self.running = True
        
        # Show connection banner
        self.clear_screen()
        print(Header.render_banner())
        print()
        
        spinner = Spinner(f"Connecting to {server}:{port}", style='dots')
        spinner.start()
        
        try:
            self.client = IRCClient(server, port)
            self.client.on_message = self.handle_server_message
            self.client.on_join = self.handle_join
            self.client.on_part = self.handle_part
            self.client.on_quit = self.handle_quit
            self.client.on_nick = self.handle_nick_change
            self.client.on_connect = self.handle_connect
            self.client.on_error = self.handle_error
            
            if not self.client.connect():
                spinner.stop(False)
                self.add_formatted_message('error', f"Failed to connect to {server}")
                return
            
            self.client.register(nickname)
            
            time.sleep(0.5)
            spinner.stop(True)
            
            # Join channels
            for channel in channels:
                self.client.join_channel(channel)
                self.current_channel = channel
                time.sleep(0.3)
            
            # Start receive thread
            recv_thread = threading.Thread(target=self.client._receive_loop, daemon=True)
            recv_thread.start()
            
            # Main input loop
            self.input_loop()
        
        except Exception as e:
            spinner.stop(False)
            self.add_formatted_message('error', f"Connection error: {str(e)}")
        
        finally:
            self.running = False
            if self.client:
                self.client.quit()

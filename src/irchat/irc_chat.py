import os
import sys
import time
from datetime import datetime
from .irc_client import IRCClient
from .config import ConfigManager
from .logger import MessageLogger
from .history import CommandHistory
from typing import Optional

class IRCInterface:
    def __init__(self):
        self.client: Optional[IRCClient] = None
        self.current_channel: str = ""
        self.nickname: str = ""
        self.message_buffer: list[str] = []
        self.max_buffer_lines = 100
        self.status_line = ""
        self.running = False
        self._buffer_lock = __import__('threading').Lock()
        self.config = ConfigManager()
        self.logger = MessageLogger(enabled=self.config.is_logging_enabled())
        self.history = CommandHistory()

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def render(self):
        self.clear_screen()
        width = self._get_terminal_width()
        
        header = f" IRC Chat - Connected to {self.client.server if self.client else 'N/A'}"
        separator = "=" * width
        
        print(separator)
        print(header.center(width))
        print(separator)
        
        with self._buffer_lock:
            for msg in self.message_buffer[-50:]:
                print(msg)
            
            if len(self.message_buffer) > 50:
                print(f"  ... ({len(self.message_buffer) - 50} more messages) ...")
        
        print(separator)
        print(self.status_line)
        print(f"\n[{self.current_channel}] {self.nickname}> ", end="", flush=True)

    def _get_terminal_width(self) -> int:
        try:
            size = os.get_terminal_size()
            return size.columns
        except:
            return 80

    def add_message(self, msg: str):
        with self._buffer_lock:
            self.message_buffer.append(msg)
            if len(self.message_buffer) > self.max_buffer_lines:
                self.message_buffer.pop(0)

    def handle_server_message(self, nick: str, target: str, message: str):
        timestamp = datetime.now().strftime("%H:%M")
        if target.startswith('#'):
            self.add_message(f"[{timestamp}] <{nick}> {message}")
            self.logger.log_message(nick, target, message, is_private=False)
        else:
            self.add_message(f"[{timestamp}] [PM] <{nick}> {message}")
            self.logger.log_message(nick, target, message, is_private=True)

    def handle_join(self, nick: str, channel: str):
        if nick != self.nickname:
            self.add_message(f"*** {nick} has joined {channel}")

    def handle_part(self, nick: str, channel: str):
        if nick != self.nickname:
            self.add_message(f"*** {nick} has left {channel}")

    def handle_quit(self, nick: str):
        self.add_message(f"*** {nick} has quit")

    def handle_nick_change(self, old_nick: str, new_nick: str):
        self.add_message(f"*** {old_nick} is now known as {new_nick}")
        if old_nick == self.nickname:
            self.nickname = new_nick

    def handle_connect(self):
        self.add_message("*** Connected to server")
        self.logger.log_event("connected", {"server": self.client.server})

    def handle_error(self, error: str):
        self.add_message(f"*** ERROR: {error}")

    def print_help(self):
        self.add_message("Commands:")
        self.add_message("  /join <channel>    - Join a channel")
        self.add_message("  /part [channel]    - Leave current channel")
        self.add_message("  /msg <user> <msg>  - Send private message")
        self.add_message("  /nick <newnick>    - Change your nickname")
        self.add_message("  /users [channel]   - List users in channel")
        self.add_message("  /me <action>       - Send an action")
        self.add_message("  /clear            - Clear screen")
        self.add_message("  /help             - Show this help")
        self.add_message("  /quit             - Disconnect and exit")

    def process_input(self, text: str) -> bool:
        text = text.strip()
        if not text:
            return True

        if text.startswith('/'):
            parts = text.split(' ', 1)
            command = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""

            if command == '/join':
                if args:
                    self.client.join_channel(args)
                    self.current_channel = args
                else:
                    self.add_message("Usage: /join <channel>")

            elif command == '/part':
                channel = args if args else self.current_channel
                if channel:
                    self.client.leave_channel(channel)
                    if channel == self.current_channel:
                        remaining = [ch for ch in self.client.channels if ch != channel]
                        self.current_channel = remaining[0] if remaining else ""
                else:
                    self.add_message("Not in a channel")

            elif command == '/msg':
                msg_parts = args.split(' ', 1)
                if len(msg_parts) == 2:
                    target, message = msg_parts
                    self.client.send_private_message(target, message)
                    self.add_message(f"[PM] -> {target}: {message}")
                else:
                    self.add_message("Usage: /msg <user> <message>")

            elif command == '/nick':
                if args:
                    self.client.change_nick(args)
                else:
                    self.add_message("Usage: /nick <newnick>")

            elif command == '/me':
                if args and self.current_channel:
                    action_msg = f"\x01ACTION {args}\x01"
                    self.client.send_message(self.current_channel, action_msg)
                    self.add_message(f"* {self.nickname} {args}")
                elif not self.current_channel:
                    self.add_message("Not currently in a channel")

            elif command == '/users':
                channel = args if args else self.current_channel
                if channel:
                    users = self.client.get_users(channel)
                    self.add_message(f"Users in {channel}: {', '.join(sorted(users))}")
                else:
                    self.add_message("Not in a channel")

            elif command == '/clear':
                self.message_buffer.clear()

            elif command == '/help':
                self.print_help()

            elif command == '/quit':
                self.client.quit()
                return False

            else:
                self.add_message(f"Unknown command: {command}")
        else:
            if self.current_channel:
                self.client.send_message(self.current_channel, text)
                self.add_message(f"[{datetime.now().strftime('%H:%M')}] <{self.nickname}> {text}")
            else:
                self.add_message("Join a channel first with /join <channel>")

        return True

    def input_loop(self):
        last_ping = time.time()
        while self.running:
            try:
                self.render()
                channels_str = ', '.join(self.client.channels) if self.client else 'None'
                latency_str = f" (Ping: {self.client.latency_ms:.0f}ms)" if self.client and self.client.latency_ms > 0 else ""
                self.status_line = f"Channels: {channels_str}{latency_str}"
                
                # Periodic ping every 30 seconds
                current_time = time.time()
                if current_time - last_ping > 30 and self.client:
                    self.client.send_ping()
                    last_ping = current_time
                
                text = input()
                if text:
                    self.history.add_command(text)
                if not self.process_input(text):
                    break
            except KeyboardInterrupt:
                print("\nUse /quit to exit")
                continue
            except EOFError:
                break
            except Exception as e:
                self.add_message(f"Error: {e}")

    def run(self, server: str, port: int, nick: str, channel: str = ""):
        self.nickname = nick
        self.current_channel = channel

        self.client = IRCClient(
            server=server,
            port=port,
            nick=nick,
            username=nick,
            realname=nick,
            channel=channel
        )
        
        # Start logging session
        self.logger.start_session(server, nick)

        self.client.on_message = self.handle_server_message
        self.client.on_join = self.handle_join
        self.client.on_part = self.handle_part
        self.client.on_quit = self.handle_quit
        self.client.on_nick = self.handle_nick_change
        self.client.on_connect = self.handle_connect
        self.client.on_error = self.handle_error

        if self.client.connect():
            self.running = True
            self.add_message(f"Connecting to {server}:{port}...")
            self.add_message(f"Nickname: {nick}")
            if channel:
                self.add_message(f"Joining: {channel}")
            self.input_loop()
        else:
            print("Failed to connect to server")

        print("Disconnected. Goodbye!")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='IRC CLI Chat Client')
    parser.add_argument('server', help='IRC server address')
    parser.add_argument('port', type=int, help='IRC server port (usually 6667)')
    parser.add_argument('nickname', help='Your nickname')
    parser.add_argument('channel', nargs='?', help='Channel to join (optional, with # prefix)')
    
    args = parser.parse_args()
    
    if not args.server or not args.port or not args.nickname:
        parser.print_help()
        print("\nError: server, port, and nickname are required")
        sys.exit(1)
    
    channel = args.channel
    if channel and not channel.startswith('#'):
        channel = '#' + channel
    
    interface = IRCInterface()
    interface.run(args.server, args.port, args.nickname, channel)

if __name__ == "__main__":
    main()

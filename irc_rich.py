import os
import sys
import io

os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import time
import random
import socket
import ssl
import threading
import select
import re
from datetime import datetime
from typing import Optional
from rich.console import Console

if sys.platform == "win32":
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except:
        pass
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.layout import Layout
from rich.live import Live
from rich.align import Align
from rich.text import Text
from rich.tree import Tree
from rich.columns import Columns
from rich.prompt import Prompt, Confirm
from rich.style import Style
from rich import box

console = Console()

POPULAR_SERVERS = [
    {"id": 1, "name": "Libera.Chat", "server": "irc.libera.chat", "port": 6697, "channels": ["#libera", "#python", "#linux", "#gamedev", "#robotics"], "desc": "Popular open source network", "active": True},
    {"id": 2, "name": "EFnet", "server": "irc.efnet.org", "port": 6697, "channels": ["#efnet", "#linux", "#programming", "#java"], "desc": "One of the oldest networks", "active": True},
    {"id": 3, "name": "Rizon", "server": "irc.rizon.net", "port": 6697, "channels": ["#anime", "#gaming", "#chat", "#music"], "desc": "Gaming & anime community", "active": True},
    {"id": 4, "name": "OFTC", "server": "irc.oftc.net", "port": 6697, "channels": ["#debian", "#gentoo", "#freebsd"], "desc": "Open source focused", "active": True},
    {"id": 5, "name": "Freenode", "server": "irc.libera.chat", "port": 6697, "channels": ["##linux", "##programming", "#archlinux", "#emacs"], "desc": "Open source dev community", "active": False},
    {"id": 6, "name": "DALnet", "server": "irc.dal.net", "port": 6697, "channels": ["#chat", "#music", "#sports"], "desc": "Global chat network", "active": False},
    {"id": 7, "name": "Undernet", "server": "irc.undernet.org", "port": 6697, "channels": ["#chat", "#help", "#irc"], "desc": "User-friendly network", "active": False},
    {"id": 8, "name": "Custom Server", "server": "", "port": 6667, "channels": [], "desc": "Enter your own server", "active": True},
]


class IRCClient:
    def __init__(self, server: str, port: int, nick: str, channel: str):
        self.server = server
        self.port = port
        self.nick = nick
        self.username = nick
        self.realname = nick
        self.channel = channel
        self.sock = None
        self.running = False
        self.channels = set()
        self.users = {}
        self.on_message = None
        self.on_join = None
        self.on_part = None
        self.on_quit = None
        self.on_nick = None
        self.on_connect = None
        self.on_error = None
        self._registered = False

    def connect(self) -> bool:
        try:
            context = ssl.create_default_context()
            raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock = context.wrap_socket(raw_sock, server_hostname=self.server)
            self.sock.connect((self.server, self.port))
            self.sock.setblocking(False)
            
            self._send(f"NICK {self.nick}")
            self._send(f"USER {self.username} 0 * :{self.realname}")
            
            self.running = True
            threading.Thread(target=self._receive_loop, daemon=True).start()
            threading.Thread(target=self._registration_loop, daemon=True).start()
            
            return True
        except Exception as e:
            if self.on_error:
                self.on_error(f"Connection failed: {e}")
            return False

    def _registration_loop(self):
        while not self._registered and self.running:
            time.sleep(0.1)
        
        if self._registered and self.channel:
            self.join_channel(self.channel)
        
        if self.on_connect:
            self.on_connect()

    def _receive_loop(self):
        buffer = ""
        while self.running:
            try:
                ready, _, _ = select.select([self.sock], [], [], 0.1)
                if ready:
                    data = self.sock.recv(4096).decode('utf-8', errors='ignore')
                    if not data:
                        break
                    buffer += data
                    
                    while '\n' in buffer:
                        line, buffer = buffer.split('\n', 1)
                        line = line.strip()
                        if line:
                            self._handle_message(line)
            except:
                if not self.running:
                    break
                continue

    def _handle_message(self, raw: str):
        if raw.startswith('PING'):
            self._send(raw.replace('PING', 'PONG'))
            return

        match = re.match(r':([^!]+)!([^@]+)@([^\s]+)\s(\w+)\s(.+)', raw)
        if match:
            nick = match.group(1)
            command = match.group(4)
            params = match.group(5)
            
            if command == 'PRIVMSG':
                target, message = params.split(' ', 1) if ' ' in params else (params, '')
                message = message.lstrip(':')
                if self.on_message:
                    self.on_message(nick, target, message)
            elif command == 'JOIN':
                channel = params.lstrip(':')
                self.channels.add(channel)
                if channel not in self.users:
                    self.users[channel] = []
                if nick not in self.users[channel]:
                    self.users[channel].append(nick)
                if self.on_join:
                    self.on_join(nick, channel)
            elif command == 'PART':
                channel = params.split()[0] if params else ''
                if channel in self.users and nick in self.users[channel]:
                    self.users[channel].remove(nick)
                if self.on_part:
                    self.on_part(nick, channel)
            elif command == 'QUIT':
                if self.on_quit:
                    self.on_quit(nick)
            elif command == 'NICK':
                new_nick = params.lstrip(':')
                if self.on_nick:
                    self.on_nick(nick, new_nick)
        else:
            if ' 001 ' in raw:
                self._registered = True
            elif raw.startswith(':') and ' 353 ' in raw:
                names_match = re.search(r'353 [^:]+:(.*)', raw)
                if names_match:
                    channel_match = re.search(r'353 [^:]+ (#\S+)', raw)
                    if channel_match:
                        channel = channel_match.group(1)
                        names = names_match.group(1).split()
                        self.users[channel] = [n.lstrip('@%+~') for n in names]
            elif raw.startswith('ERROR'):
                if self.on_error:
                    self.on_error(raw)

    def _send(self, message: str):
        if self.sock:
            try:
                self.sock.send(f"{message}\r\n".encode('utf-8'))
            except Exception as e:
                if self.on_error:
                    self.on_error(f"Send error: {e}")

    def join_channel(self, channel: str):
        self._send(f"JOIN {channel}")
        self.channels.add(channel)

    def leave_channel(self, channel: str):
        self._send(f"PART {channel}")
        self.channels.discard(channel)
        if channel in self.users:
            del self.users[channel]

    def send_message(self, target: str, message: str):
        self._send(f"PRIVMSG {target} :{message}")

    def send_private_message(self, nick: str, message: str):
        self.send_message(nick, message)

    def change_nick(self, new_nick: str):
        self._send(f"NICK {new_nick}")
        self.nick = new_nick

    def quit(self, message: str = "Goodbye!"):
        self._send(f"QUIT :{message}")
        self.running = False
        if self.sock:
            self.sock.close()

    def get_users(self, channel: str) -> list:
        return self.users.get(channel, [])


class ModernIRCGUI:
    def __init__(self):
        self.client: Optional[IRCClient] = None
        self.current_channel = ""
        self.nickname = ""
        self.server_info = {}
        self.messages = []
        self.max_messages = 500
        self.running = False
        self.console = Console()
        
    def clear(self):
        self.console.clear()

    def print_banner(self):
        self.clear()
        
        title = Text("IRC Chat Client", style="bold cyan", justify="center")
        subtitle = Text("The Future of Real-Time Communication", style="dim", justify="center")
        
        panel = Panel(
            Align.center(Text.from_markup(
                "[bold cyan]  ____   ____   ___  __  __  ___  _  _  ____   ___  ____  [/]\n"
                "[bold cyan] (  _ \\ (  _ \\ / __)(  )(  )/ __)( \\/ )(  _ \\ / __)(  _ \\[/]\n"
                "[bold cyan]  )(_) | )   /( (__  )(  )( ( (_ \\)  (  )   /( (__  )   /[/]\n"
                "[bold cyan] (____/ (__\\_) \\___)(__)(__)\\___)(_/\\_)(___/  \\___)(___)\\_\\[/]\n\n"
                "[yellow]>>> Welcome to the modern IRC experience! <<<[/]"
            )),
            title="[bold white]IRC CLI[/]",
            border_style="cyan",
            box=box.DOUBLE
        )
        self.console.print(panel)
        
        date_text = datetime.now().strftime("%A, %B %d %Y • %H:%M")
        self.console.print(Align.center(Text(date_text, style="dim")))
        self.console.print()

    def print_server_selection(self):
        self.console.print()
        
        table = Table(title="[bold cyan]Select Server[/]", box=box.ROUNDED, show_header=True, header_style="bold magenta")
        table.add_column("#", style="cyan", width=3)
        table.add_column("Server", style="bold white", width=15)
        table.add_column("Status", width=8)
        table.add_column("Description", style="dim")
        table.add_column("Popular Channels", style="green")
        
        for server in POPULAR_SERVERS:
            status = "[green]* Online[/]" if server["active"] else "[red]- Offline[/]"
            channels = ", ".join(server["channels"][:3]) if server['channels'] else "-"
            table.add_row(
                str(server["id"]),
                f"[bold]{server['name']}[/]",
                status,
                server["desc"],
                channels
            )
        
        self.console.print(table)
        self.console.print()

    def get_user_input(self, prompt_text: str, default: str = "") -> str:
        if default:
            prompt_text = f"{prompt_text} [{default}]"
        return Prompt.ask(f"[cyan]>[/] {prompt_text}") or default

    def select_server_interactive(self) -> dict:
        while True:
            self.print_banner()
            self.print_server_selection()
            
            choice = self.get_user_input("Select server [1-8]", "1")
            
            if choice.isdigit() and 1 <= int(choice) <= 8:
                server = POPULAR_SERVERS[int(choice) - 1]
                
                if server["id"] == 8:
                    return self.get_custom_server()
                
                return {
                    "name": server["name"],
                    "server": server["server"],
                    "port": server["port"],
                    "channels": server["channels"]
                }
            
            self.console.print("[red]X Invalid selection. Enter 1-8[/]")
            time.sleep(1)

    def get_custom_server(self) -> dict:
        self.console.print(Panel("[bold]Custom Server Configuration[/]", border_style="yellow"))
        
        server = self.get_user_input("Server address", "irc.example.com")
        port = self.get_user_input("Port", "6697")
        
        try:
            port = int(port)
        except ValueError:
            port = 6697
        
        return {
            "name": f"Custom ({server})",
            "server": server,
            "port": port,
            "channels": []
        }

    def select_nickname(self) -> str:
        suggestions = [f"Guest{random.randint(100,999)}", f"User{random.randint(1000,9999)}", 
                       f"Chat{random.randint(10,99)}", f"IRCr{random.randint(100,999)}"]
        
        self.console.print()
        self.console.print(Panel(
            f"[dim]Choose your nickname (visible to others)[/]\n"
            f"Suggestions: [green]{', '.join(suggestions)}[/]",
            title="[bold]Nickname Setup[/]",
            border_style="cyan"
        ))
        
        nickname = self.get_user_input("Nickname", suggestions[0])
        return nickname[:20]

    def select_channel(self, server_info: dict) -> str:
        self.console.print()
        
        table = Table(title=f"[bold]Channels on {server_info['name']}[/]", box=box.SIMPLE, show_header=True)
        table.add_column("#", style="cyan", width=3)
        table.add_column("Channel", style="bold green")
        table.add_column("Description", style="dim")
        
        channels = server_info.get('channels', [])
        if channels:
            desc_map = {
                "#libera": "Main Libera.Chat channel",
                "#python": "Python programming",
                "#linux": "Linux discussions",
                "#gamedev": "Game development",
                "#robotics": "Robotics & AI",
                "#efnet": "EFnet main channel",
                "#programming": "General programming",
                "#java": "Java discussions",
                "#anime": "Anime community",
                "#gaming": "Gaming chat",
                "#chat": "General chat",
                "#music": "Music lovers",
                "#debian": "Debian Linux",
                "#gentoo": "Gentoo Linux",
                "#freebsd": "FreeBSD OS",
                "##linux": "Linux meta channel",
                "##programming": "Programming discussions",
                "#archlinux": "Arch Linux",
                "#emacs": "Emacs editor",
                "#chat": "Chat room",
                "#help": "Help channel",
                "#irc": "IRC discussions",
                "#sports": "Sports talk"
            }
            
            for i, ch in enumerate(channels, 1):
                desc = desc_map.get(ch, "Chat channel")
                table.add_row(str(i), ch, desc)
            
            self.console.print(table)
            choice = self.get_user_input("\nSelect channel number or type name", channels[0])
            
            if choice.isdigit() and 1 <= int(choice) <= len(channels):
                choice = channels[int(choice) - 1]
        else:
            choice = self.get_user_input("Channel name", "#general")
        
        if not choice.startswith('#'):
            choice = '#' + choice
        
        return choice

    def show_connection_progress(self, server: dict, nickname: str, channel: str):
        self.clear()
        
        table = Table(box=box.DOUBLE, show_header=False, title="[bold]Connection Summary[/]")
        table.add_column("Field", style="cyan", width=15)
        table.add_column("Value", style="white")
        
        table.add_row("[bold]Server[/]", f"[cyan]{server['name']}[/] ({server['server']}:{server['port']})")
        table.add_row("[bold]Nickname[/]", f"[green]{nickname}[/]")
        table.add_row("[bold]Channel[/]", f"[yellow]{channel}[/]")
        
        self.console.print(Panel(table, border_style="cyan"))
        self.console.print()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=self.console,
            transient=True
        ) as progress:
            task = progress.add_task("[cyan]Connecting...", total=100)
            for i in range(101):
                progress.update(task, completed=i)
                time.sleep(0.02)

    def show_help(self):
        self.console.print()
        
        table = Table(box=box.ROUNDED, title="[bold cyan]Available Commands[/]", show_header=False)
        table.add_column("Command", style="bold green", width=22)
        table.add_column("Description", style="white")
        
        commands = [
            ("/join <channel>", "Join a new channel"),
            ("/part [channel]", "Leave current channel"),
            ("/msg <user> <msg>", "Send private message"),
            ("/nick <newnick>", "Change your nickname"),
            ("/me <action>", "Send an action/emote"),
            ("/users [channel]", "List users in channel"),
            ("/list", "List joined channels"),
            ("/clear", "Clear the screen"),
            ("/quit", "Disconnect and exit"),
        ]
        
        for cmd, desc in commands:
            table.add_row(cmd, desc)
        
        self.console.print(table)
        self.console.print()
        self.get_user_input("Press Enter to continue")

    def render_chat(self):
        self.clear()
        
        width = self.console.width
        
        header = Panel(
            f"[bold cyan]IRC Chat[/] | {self.server_info.get('name', 'N/A')} | "
            f"[bold green]{self.nickname}[/] | [bold yellow]{self.current_channel or 'No channel'}[/]",
            border_style="cyan",
            box=box.DOUBLE
        )
        self.console.print(header)
        
        help_bar = Text.from_markup("[dim]Commands:[/] [cyan]/join[/] [cyan]/part[/] [cyan]/msg[/] [cyan]/nick[/] [cyan]/me[/] [cyan]/users[/] [cyan]/clear[/] [cyan]/help[/] [cyan]/quit[/]", style="white")
        self.console.print(help_bar)
        self.console.print()
        
        messages_table = Table(box=box.SIMPLE, show_header=False, show_lines=False, padding=(0, 1))
        messages_table.add_column(width=width - 4)
        
        for msg in self.messages[-50:]:
            if msg.startswith("***"):
                messages_table.add_row(Text(msg, style="dim"))
            elif "[PM]" in msg:
                messages_table.add_row(Text(msg, style="magenta"))
            elif "* " in msg and msg.startswith("[") and "]" in msg[:15]:
                messages_table.add_row(Text(msg, style="yellow"))
            else:
                messages_table.add_row(msg)
        
        self.console.print(messages_table)
        
        channels = list(self.client.channels) if self.client and self.client.channels else []
        if channels:
            channels_text = Text.from_markup(f"[dim]Channels:[/] [cyan]{', '.join(channels)}[/]")
            self.console.print(channels_text)

    def add_message(self, msg: str):
        timestamp = datetime.now().strftime("%H:%M")
        self.messages.append(f"[{timestamp}] {msg}")
        if len(self.messages) > self.max_messages:
            self.messages.pop(0)

    def handle_message(self, nick: str, target: str, message: str):
        if message.startswith("\x01ACTION") and message.endswith("\x01"):
            action = message[7:-1]
            self.add_message(f"* {nick} {action}")
        elif target.startswith('#') or target == self.nickname:
            self.add_message(f"<{nick}> {message}")
        else:
            self.add_message(f"[PM] <{nick}> {message}")

    def handle_join(self, nick: str, channel: str):
        self.add_message(f"*** {nick} joined {channel}")

    def handle_part(self, nick: str, channel: str):
        self.add_message(f"*** {nick} left {channel}")

    def handle_quit(self, nick: str):
        self.add_message(f"*** {nick} quit")

    def handle_nick(self, old: str, new: str):
        self.add_message(f"*** {old} is now known as {new}")
        if old == self.nickname:
            self.nickname = new

    def handle_connect(self):
        self.add_message(f"*** Connected to {self.server_info.get('name', 'server')}!")
        if self.current_channel:
            self.add_message(f"*** Joined {self.current_channel}")

    def handle_error(self, error: str):
        self.add_message(f"*** Error: {error}")

    def process_input(self, text: str) -> bool:
        text = text.strip()
        if not text:
            return True

        if text.startswith('/'):
            parts = text.split(' ', 1)
            cmd = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""

            if cmd == '/join':
                if args:
                    ch = args if args.startswith('#') else '#' + args
                    self.client.join_channel(ch)
                    self.current_channel = ch
                    self.add_message(f"*** Joining {ch}...")
                else:
                    self.add_message("Usage: /join <channel>")

            elif cmd == '/part':
                ch = args if args else self.current_channel
                if ch:
                    self.client.leave_channel(ch)
                    self.add_message(f"*** Left {ch}")
                    if ch == self.current_channel:
                        self.current_channel = list(self.client.channels)[0] if self.client.channels else ""

            elif cmd == '/msg':
                parts = args.split(' ', 1)
                if len(parts) == 2:
                    self.client.send_private_message(parts[0], parts[1])
                    self.add_message(f"[PM] -> {parts[0]}: {parts[1]}")

            elif cmd == '/nick':
                if args:
                    self.client.change_nick(args)
                    self.nickname = args

            elif cmd == '/me':
                if args and self.current_channel:
                    self.client.send_message(self.current_channel, f"\x01ACTION {args}\x01")
                    self.add_message(f"* {self.nickname} {args}")

            elif cmd == '/users':
                ch = args if args else self.current_channel
                if ch and self.client:
                    users = self.client.get_users(ch)
                    self.add_message(f"Users in {ch}: {', '.join(sorted(users))}")

            elif cmd == '/list':
                channels = list(self.client.channels) if self.client.channels else []
                self.add_message(f"Channels: {', '.join(channels) if channels else 'None'}")

            elif cmd == '/clear':
                self.messages.clear()

            elif cmd == '/help':
                self.show_help()

            elif cmd == '/quit':
                self.client.quit()
                return False

            else:
                self.add_message(f"Unknown: {cmd}. Type /help")

        else:
            if self.current_channel:
                self.client.send_message(self.current_channel, text)
                self.add_message(f"<{self.nickname}> {text}")
            else:
                self.add_message("Join a channel: /join <channel>")

        return True

    def run(self, server_info: dict, nickname: str, channel: str):
        self.nickname = nickname
        self.current_channel = channel
        self.server_info = server_info

        self.client = IRCClient(server_info['server'], server_info['port'], nickname, channel)
        
        self.client.on_message = self.handle_message
        self.client.on_join = self.handle_join
        self.client.on_part = self.handle_part
        self.client.on_quit = self.handle_quit
        self.client.on_nick = self.handle_nick
        self.client.on_connect = self.handle_connect
        self.client.on_error = self.handle_error

        if self.client.connect():
            self.running = True
            self.show_help()
            self.input_loop()
        else:
            self.console.print("[red]X Failed to connect[/]")
            return

        self.console.print("\n[cyan]Disconnected. Goodbye![/]")

    def input_loop(self):
        while self.running:
            try:
                self.render_chat()
                text = Prompt.ask("[cyan]>[/]")
                if not self.process_input(text):
                    break
            except KeyboardInterrupt:
                self.add_message("*** Use /quit to exit properly")
            except EOFError:
                break
            except Exception as e:
                self.add_message(f"*** Error: {e}")


def main():
    gui = ModernIRCGUI()
    
    gui.print_banner()
    gui.get_user_input("Press Enter to continue")
    
    server_info = gui.select_server_interactive()
    nickname = gui.select_nickname()
    channel = gui.select_channel(server_info)
    
    gui.show_connection_progress(server_info, nickname, channel)
    gui.console.print("[green]OK[/] Connected successfully!")
    time.sleep(0.5)
    
    gui.run(server_info, nickname, channel)


if __name__ == "__main__":
    main()

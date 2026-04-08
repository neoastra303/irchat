import os
import sys
import time
import random
import socket
import ssl
import threading
import select
import re
from datetime import datetime

if sys.platform == "win32":
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

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

BANNER_LINES = [
    "  ____   ____   ___  __  __  ___  _  _  ____   ___  ____",
    " (  _ \\ (  _ \\ / __)(  )(  )/ __)( \\/ )(  _ \\ / __)(  _ \\",
    "  )(_) | )   /( (__  )(  )( ( (_ \\)  (  )   /( (__  )   /",
    " (____/ (__\\_) \\___)(__)(__)\\___)(_/\\_)(___/  \\___)(___)\\_\\",
    "       ___  ____   _  _  ____  ____  ____   ___  ___  ____",
    "      / __)(_  _) ( \\/ )(  __)(  _ \\(  _ \\ / __)/ __)(  __)",
    "     ( (__  _)(_   )  (  ) _)  )(_) ))   /( (_ \\( (__  ) _)",
    "      \\___)(____) (_/\\_)(____)(____/(__) \\)___/ \\___)(____)",
]

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"

def c(color: str, text: str) -> str:
    return f"{color}{text}{RESET}"

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def sleep(seconds: float = 0.5):
    time.sleep(seconds)

class Spinner:
    def __init__(self, message: str = "Loading"):
        self.message = message
        self.frames = ["|", "/", "-", "\\"]
        self.running = False
        self.thread = None
    
    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._spin)
        self.thread.daemon = True
        self.thread.start()
    
    def _spin(self):
        i = 0
        while self.running:
            sys.stdout.write(f"\r  {CYAN}{self.frames[i % 4]}{RESET} {self.message}... ")
            sys.stdout.flush()
            time.sleep(0.12)
            i += 1
    
    def stop(self, success: bool = True, message: str = ""):
        self.running = False
        time.sleep(0.1)
        if success:
            sys.stdout.write(f"\r  {GREEN}[OK]{RESET} {message or self.message} done!\n")
        else:
            sys.stdout.write(f"\r  {RED}[X]{RESET} {message or self.message} failed!\n")
        sys.stdout.flush()

def print_header(text: str, width: int = 70):
    print()
    print(c(CYAN, f"  +{'-' * (width - 4)}+"))
    print(c(CYAN, "  |") + f" {text} ".center(width - 4) + c(CYAN, "|"))
    print(c(CYAN, f"  +{'-' * (width - 4)}+"))
    print()

def print_banner():
    clear()
    print()
    for line in BANNER_LINES:
        print(c(CYAN, line))
    print()
    print(c(YELLOW, "    +--------------------------------------------------+"))
    print(c(YELLOW, "    |") + c(BOLD + WHITE, "    ***  The Future of IRC Chat  ***    ").center(47) + c(YELLOW, "|"))
    print(c(YELLOW, "    +--------------------------------------------------+"))
    print()
    print(c(WHITE, "  Welcome back!").center(60))
    print(c(DIM, f"  {datetime.now().strftime('%A, %B %d %Y  |  %H:%M')}").center(60))
    print()

def print_servers():
    clear()
    print()
    print(c(BOLD, f"  +{'-' * 68}+"))
    print(c(BOLD, "  |" + " SELECT SERVER ".center(68) + "|"))
    print(c(BOLD, f"  +{'=' * 68}+"))
    
    for server in POPULAR_SERVERS:
        status = f"{GREEN}[*]{RESET}" if server["active"] else f"{RED}[ ]{RESET}"
        name = f"{BOLD}{server['name']}{RESET}"
        desc = f"{DIM}{server['desc']}{RESET}"
        
        ch_list = f"{CYAN}{', '.join(server['channels'][:3])}{RESET}" if server['channels'] else ""
        
        line = f"  | {status} [{server['id']}] {name:<18} {desc:<35} |"
        print(line)
        
        if server['channels']:
            ch_line = f"  |      {DIM}Channels: {ch_list}{' ' * max(0, 45 - len(', '.join(server['channels'][:3])))}{RESET} |"
            print(ch_line)
    
    print(c(BOLD, f"  +{'-' * 68}+"))
    print()

def get_input(prompt: str, default: str = "", color: str = CYAN) -> str:
    prompt_text = f"  {c(color, '>')} {prompt}"
    if default:
        prompt_text += f" {c(DIM, f'[{default}]')}"
    prompt_text += ": "
    
    value = input(prompt_text).strip()
    return value if value else default

def select_server_interactive() -> dict:
    while True:
        print_servers()
        
        choice = input(c(CYAN, "  > Select server [1-8]: ")).strip()
        
        if not choice:
            choice = "1"
        
        if choice.isdigit() and 1 <= int(choice) <= 8:
            server = POPULAR_SERVERS[int(choice) - 1]
            
            if server["id"] == 8:
                return get_custom_server()
            
            return {
                "name": server["name"],
                "server": server["server"],
                "port": server["port"],
                "channels": server["channels"]
            }
        
        print(c(RED, "  ! Invalid selection. Enter 1-8"))
        sleep(1)

def get_custom_server() -> dict:
    print_header("CUSTOM SERVER")
    
    server = get_input("Server address", "irc.example.com")
    port = get_input("Port", "6697")
    
    try:
        port = int(port)
    except ValueError:
        port = 6697
    
    ssl_choice = get_input("Use SSL? (y/n)", "y").lower().startswith('y')
    if ssl_choice and port == 6667:
        port = 6697
    
    return {
        "name": f"Custom ({server})",
        "server": server,
        "port": port,
        "channels": []
    }

def select_nickname() -> str:
    print_header("NICKNAME SETUP")
    
    suggestions = [f"Guest{random.randint(100,999)}", f"User{random.randint(1000,9999)}", 
                   f"Chat{random.randint(10,99)}", f"IRCr{random.randint(100,999)}"]
    
    print(f"  {c(DIM, 'Choose your nickname (visible to others)')}")
    print(f"  {c(DIM, 'Suggestions:')} {c(GREEN, ', '.join(suggestions))}")
    print()
    
    nickname = get_input("Nickname", suggestions[0])
    
    while len(nickname) > 20 or not all(c.isalnum() or c in '_-|[]{}' for c in nickname):
        print(c(RED, "  ! Nickname must be alphanumeric (max 20 chars)"))
        nickname = get_input("Nickname", suggestions[0])
    
    return nickname[:20]

def select_channel(server_info: dict) -> str:
    print_header("JOIN A CHANNEL")
    
    print(f"  {c(DIM, f'Channels on {server_info['name']}:')}")
    print()
    
    channels = server_info.get('channels', [])
    if channels:
        for i, channel in enumerate(channels, 1):
            icon = c(GREEN, "[*]") if i == 1 else c(DIM, "[ ]")
            print(f"    {icon} {c(CYAN, channel)}")
        print()
        print(c(DIM, "  Or type any channel name"))
        print()
        
        choice = input(c(CYAN, "  > Channel: ")).strip()
        
        if not choice:
            choice = channels[0]
        
        if choice.isdigit() and 1 <= int(choice) <= len(channels):
            choice = channels[int(choice) - 1]
    else:
        choice = input(c(CYAN, "  > Channel name: ")).strip()
        if not choice:
            choice = "#general"
    
    if not choice.startswith('#'):
        choice = '#' + choice
    
    return choice

def show_connection_summary(server: dict, nickname: str, channel: str):
    clear()
    print()
    print(c(BOLD, f"  +{'-' * 68}+"))
    print(c(BOLD, "  |" + " CONNECTION SUMMARY ".center(68) + "|"))
    print(c(BOLD, f"  +{'=' * 68}+"))
    
    rows = [
        ("Server", f"{CYAN}{server['name']}{RESET} ({server['server']}:{server['port']})"),
        ("Nickname", f"{GREEN}{nickname}{RESET}"),
        ("Channel", f"{YELLOW}{channel}{RESET}"),
    ]
    
    for label, value in rows:
        print(f"  |  {c(DIM, label + ':'):<12} {value:<52} |")
    
    print(c(BOLD, f"  +{'-' * 68}+"))
    print()
    
    spinner = Spinner("Connecting")
    spinner.start()
    sleep(0.5)
    spinner.stop(success=True, message="Connection established")
    print()

def show_commands_help():
    print_header("AVAILABLE COMMANDS")
    
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
        print(f"    {c(CYAN, cmd):<20} {c(DIM, desc)}")
    
    print()
    print(c(DIM, "  Tip: Just type to send messages, /command for actions"))
    print()
    input(f"  {c(DIM, 'Press Enter to start chatting...')}")


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


class ModernIRCInterface:
    def __init__(self):
        self.client = None
        self.current_channel = ""
        self.nickname = ""
        self.server_info = {}
        self.message_buffer = []
        self.max_buffer = 300
        self.running = False

    def render(self):
        clear()
        width = 75
        
        print(c(BLUE, f"  +{'=' * (width - 4)}+"))
        print(c(BLUE, "  |" + " IRC Chat ".center(width - 4, '-') + "|"))
        print(c(BLUE, "  +" + '-' * (width - 4) + "+"))
        info = f" {self.server_info.get('name', 'N/A')} | {self.nickname} | {self.current_channel or 'No channel'}"
        print(c(BLUE, "  |") + info.ljust(width - 4) + c(BLUE, "|"))
        print(c(BLUE, "  +" + '-' * (width - 4) + "+"))
        
        header = c(CYAN, "  Commands: ") + c(DIM, "/join /part /msg /nick /me /users /list /clear /help /quit")
        print(header.ljust(width - 2))
        print(c(BLUE, f"  +{'-' * (width - 4)}+"))
        
        messages = self.message_buffer[-45:]
        for msg in messages:
            if msg.startswith("***"):
                print(c(DIM, f"  | {msg}").ljust(width - 2) + c(BLUE, "|"))
            elif "[PM]" in msg:
                print(c(MAGENTA, f"  | {msg}").ljust(width - 2) + c(BLUE, "|"))
            elif "* " in msg and msg.index("*") == 10:
                print(c(YELLOW, f"  | {msg}").ljust(width - 2) + c(BLUE, "|"))
            else:
                print(c(WHITE, f"  | {msg}").ljust(width - 2) + c(BLUE, "|"))
        
        if len(self.message_buffer) > 45:
            print(c(DIM, f"  | ... {len(self.message_buffer) - 45} more messages ...").ljust(width - 2) + c(BLUE, "|"))
        
        print(c(BLUE, f"  +{'-' * (width - 4)}+"))
        
        channels = list(self.client.channels) if self.client and self.client.channels else []
        ch_text = f"Channels: {', '.join(channels) if channels else 'None'}"
        print(c(DIM, f"  | {ch_text}").ljust(width - 2) + c(BLUE, "|"))
        print(c(BLUE, f"  +{'=' * (width - 4)}+"))
        print()

    def add_message(self, msg: str):
        timestamp = datetime.now().strftime("%H:%M")
        self.message_buffer.append(f"[{timestamp}] {msg}")
        if len(self.message_buffer) > self.max_buffer:
            self.message_buffer.pop(0)

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
                self.message_buffer.clear()

            elif cmd == '/help':
                self.add_message("*** /join /part /msg /nick /me /users /list /clear /help /quit")

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
            show_commands_help()
            self.input_loop()
        else:
            print(c(RED, "\n  [X] Failed to connect\n"))
            return

        print(c(CYAN, "\n  Disconnected. Goodbye!\n"))

    def input_loop(self):
        while self.running:
            try:
                self.render()
                text = input(f"  {c(CYAN, '>')} ").strip()
                if not self.process_input(text):
                    break
            except KeyboardInterrupt:
                self.add_message("*** Use /quit to exit properly")
            except EOFError:
                break
            except Exception as e:
                self.add_message(f"*** Error: {e}")

def main():
    print_banner()
    input(c(DIM, "  Press Enter to continue..."))
    
    server_info = select_server_interactive()
    nickname = select_nickname()
    channel = select_channel(server_info)
    
    show_connection_summary(server_info, nickname, channel)
    
    interface = ModernIRCInterface()
    interface.run(server_info, nickname, channel)

if __name__ == "__main__":
    main()

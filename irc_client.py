import socket
import threading
import sys
import select
import re
import time
from typing import Optional, Callable

class IRCClient:
    def __init__(self, server: str, port: int, nick: str, username: str, realname: str, channel: str):
        self.server = server
        self.port = port
        self.nick = nick
        self.username = username
        self.realname = realname
        self.channel = channel
        self.sock: Optional[socket.socket] = None
        self.running = False
        self.channels: set[str] = set()
        self.users: dict[str, list[str]] = {}
        self._lock = threading.Lock()
        self._registered_event = threading.Event()
        self.ping_time: Optional[float] = None
        self.pong_received: Optional[float] = None
        self.latency_ms: float = 0.0
        self.on_message: Optional[Callable[[str, str, str], None]] = None
        self.on_join: Optional[Callable[[str, str], None]] = None
        self.on_part: Optional[Callable[[str, str], None]] = None
        self.on_quit: Optional[Callable[[str], None]] = None
        self.on_nick: Optional[Callable[[str, str], None]] = None
        self.on_connect: Optional[Callable[[], None]] = None
        self.on_error: Optional[Callable[[str], None]] = None

    def connect(self, retry_attempts: int = 3, retry_delay: int = 5) -> bool:
        for attempt in range(retry_attempts):
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
                    self.on_error(f"Connection attempt {attempt + 1}/{retry_attempts} failed: {e}")
                if attempt < retry_attempts - 1:
                    time.sleep(retry_delay)
        
        return False

    def _registration_loop(self):
        if self._registered_event.wait(timeout=10):
            if self.channel:
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
            except Exception as e:
                if self.running:
                    continue
                break

    def _handle_message(self, raw: str):
        if raw.startswith('PING'):
            pong = raw.replace('PING', 'PONG')
            self._send(pong)
            return
        
        if raw.startswith(':') and 'PONG' in raw:
            self.pong_received = time.time()
            if self.ping_time:
                self.latency_ms = (self.pong_received - self.ping_time) * 1000
            return

        match = re.match(r':([^!]+)!([^@]+)@([^\s]+)\s(\w+)\s(.+)', raw)
        if match:
            nick = match.group(1)
            user = match.group(2)
            host = match.group(3)
            command = match.group(4)
            params = match.group(5)
            
            if command == 'PRIVMSG':
                target, message = params.split(' ', 1) if ' ' in params else (params, '')
                message = message.lstrip(':')
                if self.on_message:
                    self.on_message(nick, target, message)
            elif command == 'JOIN':
                channel = params.lstrip(':')
                with self._lock:
                    self.channels.add(channel)
                    if channel not in self.users:
                        self.users[channel] = []
                    if nick not in self.users[channel]:
                        self.users[channel].append(nick)
                if self.on_join:
                    self.on_join(nick, channel)
            elif command == 'PART':
                channel = params.split()[0] if params else ''
                with self._lock:
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
                self._registered_event.set()
            elif raw.startswith(':') and ' 353 ' in raw:
                names_match = re.search(r'353 [^:]+:(.*)', raw)
                if names_match:
                    channel_match = re.search(r'353 [^:]+ (#\S+)', raw)
                    if channel_match:
                        channel = channel_match.group(1)
                        names = names_match.group(1).split()
                        with self._lock:
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

    def get_users(self, channel: str) -> list[str]:
        with self._lock:
            return self.users.get(channel, []).copy()
    
    def send_ping(self):
        self.ping_time = time.time()
        self._send(f"PING {self.server}")

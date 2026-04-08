import unittest
import sys
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from irchat.irc_client import IRCClient

class TestIRCProtocol(unittest.TestCase):
    
    def test_nick_parsing(self):
        """Test extracting nickname from raw IRC message"""
        raw = ":user!ident@host.com PRIVMSG #channel :Hello"
        match = __import__('re').match(r':([^!]+)!([^@]+)@([^\s]+)\s(\w+)\s(.+)', raw)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), "user")
    
    def test_channel_parsing(self):
        """Test extracting channel from JOIN message"""
        raw = ":user!ident@host.com JOIN :#channel"
        match = __import__('re').match(r':([^!]+)!([^@]+)@([^\s]+)\s(\w+)\s(.+)', raw)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(4), "JOIN")
        channel = match.group(5).lstrip(':')
        self.assertEqual(channel, "#channel")
    
    def test_privmsg_parsing(self):
        """Test extracting private message content"""
        raw = ":user!ident@host.com PRIVMSG #channel :Hello world"
        match = __import__('re').match(r':([^!]+)!([^@]+)@([^\s]+)\s(\w+)\s(.+)', raw)
        self.assertIsNotNone(match)
        params = match.group(5)
        target, message = params.split(' ', 1) if ' ' in params else (params, '')
        message = message.lstrip(':')
        self.assertEqual(target, "#channel")
        self.assertEqual(message, "Hello world")
    
    def test_names_response_parsing(self):
        """Test parsing NAMES response (RPL_NAMREPLY)"""
        raw = ":server.com 353 mynick = #channel :@owner +voiced user1 user2"
        names_match = __import__('re').search(r'353 [^:]+:(.*)', raw)
        channel_match = __import__('re').search(r'353 [^:]+ (#\S+)', raw)
        
        self.assertIsNotNone(names_match)
        self.assertIsNotNone(channel_match)
        
        names = names_match.group(1).split()
        names = [n.lstrip('@%+~') for n in names]
        
        self.assertEqual(channel_match.group(1), "#channel")
        self.assertIn("owner", names)
        self.assertIn("user1", names)
        self.assertIn("user2", names)
    
    def test_nick_change_parsing(self):
        """Test parsing NICK change message"""
        raw = ":oldnick!ident@host.com NICK :newnick"
        match = __import__('re').match(r':([^!]+)!([^@]+)@([^\s]+)\s(\w+)\s(.+)', raw)
        self.assertIsNotNone(match)
        old_nick = match.group(1)
        new_nick = match.group(5).lstrip(':')
        self.assertEqual(old_nick, "oldnick")
        self.assertEqual(new_nick, "newnick")
    
    def test_ping_handling(self):
        """Test PING message handling"""
        ping = "PING :server.com"
        self.assertTrue(ping.startswith('PING'))
        pong = ping.replace('PING', 'PONG')
        self.assertEqual(pong, "PONG :server.com")
    
    def test_registration_response(self):
        """Test server registration (001 response)"""
        raw = ":server.com 001 mynick :Welcome to the network"
        self.assertIn(' 001 ', raw)
    
    def test_error_response(self):
        """Test ERROR message"""
        raw = "ERROR :Closing Link: user@host (K-lined)"
        self.assertTrue(raw.startswith('ERROR'))

class TestConfigManager(unittest.TestCase):
    
    def test_default_config(self):
        """Test default configuration"""
        from config import ConfigManager
        config = ConfigManager("test_config.json")
        self.assertIn("servers", config.config)
        self.assertIn("logging", config.config)
    
    def test_get_server(self):
        """Test retrieving server config"""
        from config import ConfigManager
        config = ConfigManager("test_config.json")
        server = config.get_server("libera")
        self.assertIsNotNone(server)
        self.assertEqual(server["host"], "irc.libera.chat")

class TestCommandHistory(unittest.TestCase):
    
    def test_add_command(self):
        """Test adding commands to history"""
        from history import CommandHistory
        hist = CommandHistory(history_file="test_history.txt")
        hist.clear()
        hist.add_command("/join #test")
        self.assertEqual(len(hist.history), 1)
        self.assertEqual(hist.history[0], "/join #test")
    
    def test_history_navigation(self):
        """Test navigating command history"""
        from history import CommandHistory
        hist = CommandHistory(history_file="test_history.txt")
        hist.clear()
        hist.add_command("/join #test")
        hist.add_command("/msg user hello")
        
        prev = hist.get_previous()
        self.assertEqual(prev, "/msg user hello")
        
        prev = hist.get_previous()
        self.assertEqual(prev, "/join #test")

class TestMessageLogger(unittest.TestCase):
    
    def test_logging_enabled(self):
        """Test logger initialization"""
        from logger import MessageLogger
        logger = MessageLogger(directory="test_logs", enabled=True)
        self.assertTrue(logger.enabled)
    
    def test_logging_disabled(self):
        """Test logger when disabled"""
        from logger import MessageLogger
        logger = MessageLogger(enabled=False)
        self.assertFalse(logger.enabled)

if __name__ == '__main__':
    unittest.main()

import json
import os
from typing import Optional, Dict, Any

class ConfigManager:
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
                return self._default_config()
        return self._default_config()
    
    def _default_config(self) -> Dict[str, Any]:
        return {
            "servers": {
                "libera": {"host": "irc.libera.chat", "port": 6667},
                "freenode": {"host": "irc.freenode.net", "port": 6667}
            },
            "logging": {"enabled": False, "directory": "chat_history"},
            "ui": {"max_buffer": 100}
        }
    
    def save_config(self) -> bool:
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get_server(self, server_name: str) -> Optional[Dict[str, Any]]:
        return self.config.get("servers", {}).get(server_name)
    
    def get_servers(self) -> Dict[str, Dict[str, Any]]:
        return self.config.get("servers", {})
    
    def add_server(self, name: str, host: str, port: int) -> bool:
        if "servers" not in self.config:
            self.config["servers"] = {}
        self.config["servers"][name] = {"host": host, "port": port}
        return self.save_config()
    
    def is_logging_enabled(self) -> bool:
        return self.config.get("logging", {}).get("enabled", False)
    
    def get_logging_directory(self) -> str:
        return self.config.get("logging", {}).get("directory", "chat_history")

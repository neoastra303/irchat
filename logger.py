import os
import json
from datetime import datetime
from typing import Optional

class MessageLogger:
    def __init__(self, directory: str = "chat_history", enabled: bool = False):
        self.directory = directory
        self.enabled = enabled
        self.current_session_file: Optional[str] = None
        self.current_channel: Optional[str] = None
        
        if self.enabled and not os.path.exists(directory):
            os.makedirs(directory)
    
    def start_session(self, server: str, nick: str) -> bool:
        if not self.enabled:
            return False
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{server}_{nick}_{timestamp}.jsonl"
            self.current_session_file = os.path.join(self.directory, filename)
            return True
        except Exception as e:
            print(f"Error starting logging session: {e}")
            return False
    
    def log_message(self, nick: str, target: str, message: str, is_private: bool = False):
        if not self.enabled or not self.current_session_file:
            return
        
        try:
            entry = {
                "timestamp": datetime.now().isoformat(),
                "nick": nick,
                "target": target,
                "message": message,
                "private": is_private
            }
            
            with open(self.current_session_file, 'a') as f:
                f.write(json.dumps(entry) + '\n')
        except Exception as e:
            print(f"Error logging message: {e}")
    
    def log_event(self, event_type: str, details: dict):
        if not self.enabled or not self.current_session_file:
            return
        
        try:
            entry = {
                "timestamp": datetime.now().isoformat(),
                "event": event_type,
                "details": details
            }
            
            with open(self.current_session_file, 'a') as f:
                f.write(json.dumps(entry) + '\n')
        except Exception as e:
            print(f"Error logging event: {e}")

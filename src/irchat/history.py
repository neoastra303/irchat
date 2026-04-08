import os
from typing import List

class CommandHistory:
    def __init__(self, max_size: int = 100, history_file: str = ".irc_history"):
        self.max_size = max_size
        self.history_file = history_file
        self.history: List[str] = []
        self.current_index = -1
        self._load_history()
    
    def _load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    self.history = [line.strip() for line in f.readlines() if line.strip()]
            except Exception:
                self.history = []
    
    def add_command(self, command: str):
        if command and command.strip():
            self.history.append(command)
            if len(self.history) > self.max_size:
                self.history.pop(0)
            self.current_index = -1
            self._save_history()
    
    def get_previous(self) -> str:
        if not self.history:
            return ""
        if self.current_index < 0:
            self.current_index = len(self.history) - 1
        else:
            self.current_index = max(0, self.current_index - 1)
        return self.history[self.current_index]
    
    def get_next(self) -> str:
        if not self.history:
            return ""
        self.current_index = min(len(self.history) - 1, self.current_index + 1)
        if self.current_index >= len(self.history):
            self.current_index = -1
            return ""
        return self.history[self.current_index]
    
    def reset_position(self):
        self.current_index = -1
    
    def _save_history(self):
        try:
            with open(self.history_file, 'w') as f:
                for cmd in self.history:
                    f.write(cmd + '\n')
        except Exception:
            pass
    
    def clear(self):
        self.history.clear()
        self.current_index = -1
        self._save_history()

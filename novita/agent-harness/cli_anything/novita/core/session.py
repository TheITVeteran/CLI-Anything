"""Lightweight session for chat history management."""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path


class ChatSession:
    """Lightweight session for chat history management."""

    def __init__(self, session_file: str = None):
        self.session_file = session_file or str(
            Path.home() / ".cli-anything-novita" / "session.json"
        )
        self.messages = []
        self.history = []
        self.max_history = 50
        self.modified = False
        if os.path.exists(self.session_file):
            try:
                with open(self.session_file, "r") as f:
                    data = json.load(f)
                    self.messages = data.get("messages", [])
            except (json.JSONDecodeError, IOError):
                self.messages = []

    def add_user_message(self, content: str):
        self.messages.append({"role": "user", "content": content})
        self.modified = True
        self._save()

    def add_assistant_message(self, content: str):
        self.messages.append({"role": "assistant", "content": content})
        self.modified = True
        self._save()

    def get_messages(self):
        return self.messages.copy()

    def clear(self):
        self.messages = []
        self.modified = True
        self._save()

    def status(self):
        return {
            "message_count": len(self.messages),
            "modified": self.modified,
            "session_file": self.session_file,
        }

    def _save(self):
        os.makedirs(os.path.dirname(self.session_file), exist_ok=True)
        with open(self.session_file, "w") as f:
            json.dump({"messages": self.messages}, f, indent=2)

    def save_history(self, command: str, result: dict):
        self.history.append(
            {"command": command, "result": result, "timestamp": str(datetime.now())}
        )
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history :]

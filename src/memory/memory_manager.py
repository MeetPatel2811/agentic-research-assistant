# This module implements a JSON-based memory manager
# which stores past conversations and extracted facts for contextual awareness.

import json
import os
from typing import Any, Dict, List, Optional

from utils.logger import log_error, log_info


MEMORY_FILE_DEFAULT = "memory_store.json"


class MemoryManager:
    # This class manages loading, saving, and updating the agentic system's memory.
    def __init__(self, filename: str = MEMORY_FILE_DEFAULT, max_entries: int = 50) -> None:
        self.filename = filename
        self.max_entries = max_entries
        self.state: Dict[str, Any] = {
            "conversations": [],  # list of {query, response}
            "facts": []           # list of extracted facts from sources
        }
        self._load()

    def _load(self) -> None:
        # This private method loads memory from disk if the file exists.
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    self.state = json.load(f)
                log_info(f"Memory loaded from {self.filename}")
            except Exception as e:
                log_error(f"Failed to load memory: {e}. Initializing fresh memory.")
                self.state = {"conversations": [], "facts": []}

    def _save(self) -> None:
        # This private method persists memory state to disk as JSON.
        try:
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(self.state, f, indent=2, ensure_ascii=False)
        except Exception as e:
            log_error(f"Failed to save memory: {e}")

    def add_conversation(self, query: str, response: str) -> None:
        # This method stores a new query-response pair in memory.
        self.state["conversations"].append({"query": query, "response": response})
        # This keeps memory bounded by trimming older entries if necessary.
        if len(self.state["conversations"]) > self.max_entries:
            self.state["conversations"] = self.state["conversations"][-self.max_entries :]
        self._save()

    def add_fact(self, fact: str, source: Optional[str] = None) -> None:
        # This method stores an extracted fact, optionally with its source.
        self.state["facts"].append({"fact": fact, "source": source})
        if len(self.state["facts"]) > self.max_entries:
            self.state["facts"] = self.state["facts"][-self.max_entries :]
        self._save()

    def get_recent_context(self, limit: int = 5) -> Dict[str, List[Dict[str, str]]]:
        # This method returns the most recent conversations and facts
        # to give agents a basic contextual awareness.
        conversations = self.state["conversations"][-limit:]
        facts = self.state["facts"][-limit:]
        return {"conversations": conversations, "facts": facts}

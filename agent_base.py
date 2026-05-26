"""
lib/agents/agent.py — minimal Agent base class.

Mirrors the typical course pattern:
  * Subclasses implement _handle_turn(query, session) and return a string.
  * The base class owns session_id routing, persistence, and history.

Sessions are stored as one JSON file per session_id under ./agent_sessions/,
so:
  * Two callers using different session_ids never see each other's history.
  * A session can be resumed after a kernel restart.
  * Wiping a session is one delete; inspecting one is `cat`.
"""

from __future__ import annotations

import json
import os
import re
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Turn:
    """One user/agent exchange. Subclasses can extend via `extra`."""
    query: str
    rewritten_query: str
    answer: str
    source: str
    topic: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)


class Session:
    """In-memory view of one session's history. Persistence is the store's job."""

    def __init__(self, session_id: str, turns: Optional[List[Turn]] = None) -> None:
        self.session_id = session_id
        self.turns: List[Turn] = turns or []

    def append(self, turn: Turn) -> None:
        self.turns.append(turn)

    @property
    def last(self) -> Optional[Turn]:
        return self.turns[-1] if self.turns else None

    def __len__(self) -> int:
        return len(self.turns)


class SessionStore(ABC):
    """Pluggable persistence backend."""

    @abstractmethod
    def load(self, session_id: str) -> Session: ...
    @abstractmethod
    def save(self, session: Session) -> None: ...
    @abstractmethod
    def list_sessions(self) -> List[str]: ...
    @abstractmethod
    def delete(self, session_id: str) -> None: ...


class InMemoryStore(SessionStore):
    """Useful for tests; lost on restart."""

    def __init__(self) -> None:
        self._data: Dict[str, List[Turn]] = {}

    def load(self, session_id: str) -> Session:
        return Session(session_id, list(self._data.get(session_id, [])))

    def save(self, session: Session) -> None:
        self._data[session.session_id] = list(session.turns)

    def list_sessions(self) -> List[str]:
        return sorted(self._data.keys())

    def delete(self, session_id: str) -> None:
        self._data.pop(session_id, None)


class JsonFileStore(SessionStore):
    """One JSON file per session under base_dir. Survives kernel restart."""

    _SAFE = re.compile(r"[^A-Za-z0-9._-]")

    def __init__(self, base_dir: str = "./agent_sessions") -> None:
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def _path(self, session_id: str) -> str:
        # Sanitize so a session_id can't escape base_dir or collide with files.
        safe = self._SAFE.sub("_", session_id) or "default"
        return os.path.join(self.base_dir, f"{safe}.json")

    def load(self, session_id: str) -> Session:
        path = self._path(session_id)
        if not os.path.exists(path):
            return Session(session_id, [])
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        turns = [Turn(**t) for t in raw.get("turns", [])]
        return Session(session_id, turns)

    def save(self, session: Session) -> None:
        path = self._path(session.session_id)
        payload = {
            "session_id": session.session_id,
            "turns": [asdict(t) for t in session.turns],
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

    def list_sessions(self) -> List[str]:
        if not os.path.isdir(self.base_dir):
            return []
        return sorted(
            os.path.splitext(f)[0]
            for f in os.listdir(self.base_dir)
            if f.endswith(".json")
        )

    def delete(self, session_id: str) -> None:
        path = self._path(session_id)
        if os.path.exists(path):
            os.remove(path)


class Agent(ABC):
    """Base class for any agent that needs isolated, resumable sessions."""

    DEFAULT_SESSION = "default"

    def __init__(self, store: Optional[SessionStore] = None) -> None:
        self.store: SessionStore = store or JsonFileStore()

    # ---- public API --------------------------------------------------------
    def run(self, query: str, session_id: Optional[str] = None) -> str:
        sid = session_id or self.DEFAULT_SESSION
        session = self.store.load(sid)
        answer = self._handle_turn(query, session)
        self.store.save(session)
        return answer

    def history(self, session_id: Optional[str] = None) -> List[Turn]:
        sid = session_id or self.DEFAULT_SESSION
        return self.store.load(sid).turns

    def list_sessions(self) -> List[str]:
        return self.store.list_sessions()

    def clear_session(self, session_id: Optional[str] = None) -> None:
        self.store.delete(session_id or self.DEFAULT_SESSION)

    # ---- subclass contract -------------------------------------------------
    @abstractmethod
    def _handle_turn(self, query: str, session: Session) -> str:
        """Process one turn. Must append a Turn to `session` and return the answer."""

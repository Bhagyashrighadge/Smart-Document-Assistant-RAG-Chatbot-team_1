"""
Session Store - In-memory storage for document context and chat history
"""
from typing import Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class ChatMessage:
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class SessionData:
    session_id: str
    document_name: str = ""
    document_text: str = ""
    vector_store: Any = None  # ChromaDB vector store
    chat_history: List[ChatMessage] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    language: str = "en"  # Current selected language
    

class SessionStore:
    """In-memory session storage"""
    
    def __init__(self):
        self.sessions: Dict[str, SessionData] = {}
    
    def create_session(self) -> str:
        """Create a new session and return session ID"""
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = SessionData(session_id=session_id)
        return session_id
    
    def get_session(self, session_id: str) -> SessionData:
        """Get session by ID"""
        return self.sessions.get(session_id)
    
    def update_session(self, session_id: str, **kwargs) -> SessionData:
        """Update session data"""
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.sessions[session_id]
        for key, value in kwargs.items():
            if hasattr(session, key):
                setattr(session, key, value)
        
        return session
    
    def add_message(self, session_id: str, role: str, content: str) -> ChatMessage:
        """Add a message to chat history"""
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
        
        message = ChatMessage(role=role, content=content)
        self.sessions[session_id].chat_history.append(message)
        return message
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False
    
    def list_sessions(self) -> List[str]:
        """List all active session IDs"""
        return list(self.sessions.keys())


# Global session store instance
session_store = SessionStore()

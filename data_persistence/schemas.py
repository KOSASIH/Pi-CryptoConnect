from typing import List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
import json

@dataclass
class StateChangeSchema:
    """A class representing the schema for a state change."""
    
    entity_id: str
    entity_type: str
    state: Dict[str, Any]
    user: str
    timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Post-initialization validation."""
        if not self.entity_id or not self.entity_type:
            raise ValueError("Entity ID and Entity Type cannot be empty.")
        if not isinstance(self.state, dict):
            raise ValueError("State must be a valid dictionary.")
        if not isinstance(self.timestamp, datetime):
            raise ValueError("Timestamp must be a datetime object.")

    def to_dict(self) -> Dict[str, Any]:
        """Convert the state change schema to a dictionary."""
        return {
            "entity_id": self.entity_id,
            "entity_type": self.entity_type,
            "state": self.state,
            "user": self.user,
            "timestamp": self.timestamp.isoformat()  # Convert to ISO format for JSON serialization
        }

    def to_json(self) -> str:
        """Convert the state change schema to a JSON string."""
        return json.dumps(self.to_dict())

@dataclass
class StateHistorySchema:
    """A class representing the schema for a state history."""
    
    state_changes: List[StateChangeSchema]

    def __post_init__(self):
        """Post-initialization validation."""
        if not isinstance(self.state_changes, list):
            raise ValueError("State changes must be a list.")
        for change in self.state_changes:
            if not isinstance(change, StateChangeSchema):
                raise ValueError("Each state change must be an instance of StateChangeSchema.")

    def to_dict(self) -> Dict[str, Any]:
        """Convert the state history schema to a dictionary."""
        return {
            "state_changes": [change.to_dict() for change in self.state_changes]
        }

    def to_json(self) -> str:
        """Convert the state history schema to a JSON string."""
        return json.dumps(self.to_dict())

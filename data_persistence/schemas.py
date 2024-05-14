from typing import List, Dict, Any

class StateChangeSchema:
    """A class representing the schema for a state change."""

    def__init__(self, entity_id: str, entity_type: str, state: Dict[str, Any], user: str, timestamp: str):
        """Initialize the state change schema.

        Args:
            entity_id (str): The ID of the entity that was changed.
            entity_type (str): The type of the entity that was changed.
            state (Dict[str, Any]): The new state of the entity.
            user (str): The username of the user who made the state change.
            timestamp (str): The date and time the state change was made.
        """
        self.entity_id = entity_id
        self.entity_type = entity_type
        self.state = state
        self.user = user
        self.timestamp = timestamp

class StateHistorySchema:
    """A class representing the schema for a state history."""

    def __init__(self, state_changes: List[Dict[str, Any]]):
        """Initialize the state history schema.

        Args:
            state_changes (List[Dict[str, Any]]): A list of state changes.
        """
        self.state_changes = state_changes

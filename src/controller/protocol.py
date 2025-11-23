# This module defines simple data structures (protocol)
# for messages passed between the controller and agents.

from dataclasses import dataclass
from typing import Dict, List, Any


@dataclass
class AgentMessage:
    # This dataclass represents a generic message between controller and agents.
    sender: str
    receiver: str
    task_type: str
    payload: Dict[str, Any]


@dataclass
class ControllerDecision:
    # This dataclass captures a controller decision about which agent to call next.
    next_agent: str
    reason: str
    metadata: Dict[str, Any]

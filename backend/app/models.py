"""In-memory domain models for the Spider Safety Network MVP."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class NodeStatus(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    MAINTENANCE = "maintenance"


class NodeCapability(str, Enum):
    FIRST_AID_KIT = "first_aid_kit"
    AED = "aed"
    DRONE = "drone"
    COMMUNICATION_RELAY = "communication_relay"
    AMBULANCE_COORDINATION = "ambulance_coordination"


class IncidentStatus(str, Enum):
    OPEN = "open"
    ACKNOWLEDGED = "acknowledged"
    DRONE_DISPATCHED = "drone_dispatched"
    KIT_DELIVERED = "kit_delivered"
    ESCALATED = "escalated"
    RESOLVED = "resolved"


class IncidentType(str, Enum):
    MEDICAL = "medical"
    SAFETY = "safety"
    HARASSMENT = "harassment"
    ACCIDENT = "accident"
    FIRE = "fire"
    OTHER = "other"


class PlanType(str, Enum):
    FREE = "free"
    TRAVEL_PASS = "travel_pass"
    NODE_PASS = "node_pass"
    FIELD_WORKER = "field_worker"
    ENTERPRISE = "enterprise"


class EmergencyContact(BaseModel):
    name: str
    phone: str
    relationship: str = "family"


class User(BaseModel):
    id: str
    name: str
    phone: str
    emergency_contacts: List[EmergencyContact] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)


class SpiderNode(BaseModel):
    id: str
    name: str
    node_type: str
    latitude: float
    longitude: float
    coverage_radius_km: float
    capabilities: List[NodeCapability]
    status: NodeStatus = NodeStatus.ONLINE


class TravelPass(BaseModel):
    id: str
    user_id: str
    area_name: str
    start_latitude: float
    start_longitude: float
    end_latitude: float
    end_longitude: float
    valid_from: datetime
    valid_to: datetime
    plan: PlanType
    status: str = "active"
    created_at: datetime = Field(default_factory=utc_now)


class TimelineEvent(BaseModel):
    status: str
    note: str
    timestamp: datetime = Field(default_factory=utc_now)


class Incident(BaseModel):
    id: str
    user_id: str
    travel_pass_id: Optional[str] = None
    incident_type: IncidentType
    latitude: float
    longitude: float
    description: str = ""
    assigned_node_id: Optional[str] = None
    estimated_response_minutes: int = 15
    status: IncidentStatus = IncidentStatus.OPEN
    trusted_contacts_notified: int = 0
    insurance_flag: bool = False
    timeline: List[TimelineEvent] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)


class Subscription(BaseModel):
    id: str
    user_id: str
    plan: PlanType
    status: str = "active"
    started_at: datetime = Field(default_factory=utc_now)
    expires_at: Optional[datetime] = None


class InMemoryStore:
    """Simple demo store. Replace with PostgreSQL in production."""

    def __init__(self) -> None:
        self.users: Dict[str, User] = {}
        self.nodes: Dict[str, SpiderNode] = {}
        self.travel_passes: Dict[str, TravelPass] = {}
        self.incidents: Dict[str, Incident] = {}
        self.subscriptions: Dict[str, Subscription] = {}

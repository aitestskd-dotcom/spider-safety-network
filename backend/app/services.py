"""Business services for node selection, SOS handling, and incident workflow."""

from __future__ import annotations

import math
import uuid
from typing import List, Optional, Tuple

from .models import (
    InMemoryStore,
    Incident,
    IncidentStatus,
    IncidentType,
    NodeStatus,
    SpiderNode,
    TimelineEvent,
    TravelPass,
    User,
)


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    radius = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = (
        math.sin(delta_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    )
    return 2 * radius * math.asin(math.sqrt(a))


class NetworkService:
    def __init__(self, store: InMemoryStore) -> None:
        self.store = store

    def create_user(self, name: str, phone: str, emergency_contacts=None) -> User:
        user_id = f"usr_{uuid.uuid4().hex[:10]}"
        user = User(
            id=user_id,
            name=name,
            phone=phone,
            emergency_contacts=emergency_contacts or [],
        )
        self.store.users[user_id] = user
        return user

    def create_travel_pass(
        self,
        user_id: str,
        area_name: str,
        start_latitude: float,
        start_longitude: float,
        end_latitude: float,
        end_longitude: float,
        valid_from,
        valid_to,
        plan,
    ) -> TravelPass:
        if user_id not in self.store.users:
            raise ValueError("User not found")
        if valid_to <= valid_from:
            raise ValueError("Travel pass end time must be after start time")

        pass_id = f"pass_{uuid.uuid4().hex[:10]}"
        travel_pass = TravelPass(
            id=pass_id,
            user_id=user_id,
            area_name=area_name,
            start_latitude=start_latitude,
            start_longitude=start_longitude,
            end_latitude=end_latitude,
            end_longitude=end_longitude,
            valid_from=valid_from,
            valid_to=valid_to,
            plan=plan,
        )
        self.store.travel_passes[pass_id] = travel_pass
        return travel_pass

    def find_nearest_node(
        self,
        latitude: float,
        longitude: float,
        required_capabilities: Optional[List[str]] = None,
    ) -> Tuple[Optional[SpiderNode], int]:
        candidates = [
            node
            for node in self.store.nodes.values()
            if node.status == NodeStatus.ONLINE
        ]
        if required_capabilities:
            candidates = [
                node
                for node in candidates
                if all(capability in node.capabilities for capability in required_capabilities)
            ]

        if not candidates:
            return None, 30

        nearest = min(
            candidates,
            key=lambda node: haversine_km(latitude, longitude, node.latitude, node.longitude),
        )
        distance_km = haversine_km(latitude, longitude, nearest.latitude, nearest.longitude)
        estimated_minutes = max(5, int(distance_km * 2))
        return nearest, estimated_minutes

    def trigger_sos(
        self,
        user_id: str,
        incident_type: IncidentType,
        latitude: float,
        longitude: float,
        description: str,
        travel_pass_id: Optional[str] = None,
    ) -> Incident:
        if user_id not in self.store.users:
            raise ValueError("User not found")

        user = self.store.users[user_id]
        nearest_node, eta = self.find_nearest_node(latitude, longitude)

        incident_id = f"inc_{uuid.uuid4().hex[:10]}"
        incident = Incident(
            id=incident_id,
            user_id=user_id,
            travel_pass_id=travel_pass_id,
            incident_type=incident_type,
            latitude=latitude,
            longitude=longitude,
            description=description,
            assigned_node_id=nearest_node.id if nearest_node else None,
            estimated_response_minutes=eta,
            trusted_contacts_notified=len(user.emergency_contacts),
            insurance_flag=True,
            timeline=[
                TimelineEvent(status="open", note="SOS received and incident created"),
                TimelineEvent(
                    status="escalation_recorded",
                    note="Escalation pathway to 112 ERSS and local responders recorded",
                ),
            ],
        )

        if nearest_node:
            incident.timeline.append(
                TimelineEvent(
                    status="node_assigned",
                    note=f"Nearest node {nearest_node.name} assigned; ETA {eta} minutes",
                )
            )
        else:
            incident.timeline.append(
                TimelineEvent(
                    status="no_node_available",
                    note="No online node available; direct emergency escalation required",
                )
            )

        self.store.incidents[incident_id] = incident
        return incident

    def update_status(self, incident_id: str, status: IncidentStatus, note: str) -> Incident:
        if incident_id not in self.store.incidents:
            raise ValueError("Incident not found")

        incident = self.store.incidents[incident_id]
        incident.status = status
        incident.timeline.append(TimelineEvent(status=status.value, note=note))
        return incident
